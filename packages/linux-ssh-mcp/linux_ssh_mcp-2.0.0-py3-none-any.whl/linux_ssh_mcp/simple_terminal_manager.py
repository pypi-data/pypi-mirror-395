"""
简化的终端会话管理器 - 直接SSH实现
"""
import asyncio
import logging
import asyncssh
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class TabStatus(Enum):
    """终端标签页状态"""
    CONNECTING = "connecting"
    ACTIVE = "active"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class ServerConfig:
    """服务器配置"""
    id: str
    host: str
    port: int
    username: str
    password: str
    timeout: int = 30


@dataclass
class TabMetadata:
    """标签页元数据"""
    tab_id: str
    title: str
    server_config: ServerConfig
    status: TabStatus = TabStatus.CONNECTING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    has_unread_output: bool = False


class SimpleTabSession:
    """简化的标签页会话"""

    def __init__(self, tab_id: str, server_config: ServerConfig, title: Optional[str] = None):
        self.tab_id = tab_id
        self.server_config = server_config
        self.metadata = TabMetadata(
            tab_id=tab_id,
            title=title or f"{server_config.username}@{server_config.host}",
            server_config=server_config
        )
        self.ssh_connection: Optional[asyncssh.SSHClientConnection] = None
        self.output_buffer: List[str] = []
        self.max_history = 1000
        self._output_callbacks = []

    def add_output_callback(self, callback):
        """添加输出回调"""
        self._output_callbacks.append(callback)

    def remove_output_callback(self, callback):
        """移除输出回调"""
        if callback in self._output_callbacks:
            self._output_callbacks.remove(callback)

    async def start(self) -> bool:
        """启动SSH连接"""
        try:
            self.metadata.status = TabStatus.CONNECTING

            logger.info(f"Connecting to SSH server {self.server_config.host}:{self.server_config.port}")

            # 创建SSH连接
            self.ssh_connection = await asyncssh.connect(
                host=self.server_config.host,
                port=self.server_config.port,
                username=self.server_config.username,
                password=self.server_config.password,
                known_hosts=None,  # 跳过主机密钥检查
                connect_timeout=self.server_config.timeout
            )

            self.metadata.status = TabStatus.ACTIVE

            # 显示连接成功的输出
            connection_output = f"Connected to {self.server_config.host}\n"
            connection_output += f"{self.server_config.username}@{self.server_config.host}:~$ "

            await self._handle_output(connection_output)

            logger.info(f"SSH connection established for session {self.tab_id}")
            return True

        except Exception as e:
            self.metadata.status = TabStatus.ERROR
            error_output = f"Connection failed: {str(e)}\n"
            await self._handle_output(error_output)
            logger.error(f"SSH connection error for session {self.tab_id}: {e}")
            return False

    async def send_input(self, input_text: str) -> bool:
        """发送输入到SSH会话"""
        if not self.ssh_connection or self.metadata.status != TabStatus.ACTIVE:
            return False

        try:
            # 显示输入的命令
            prompt = f"{self.server_config.username}@{self.server_config.host}:~$ "
            await self._handle_output(f"{prompt}{input_text}")

            # 确保命令以换行符结尾
            if not input_text.endswith('\n'):
                input_text += '\n'

            # 执行命令
            result = await self.ssh_connection.run(input_text, check=False)

            # 显示命令输出
            if result.stdout.strip():
                await self._handle_output(result.stdout)

            # 显示错误输出（如果有）
            if result.stderr.strip():
                await self._handle_output(f"ERROR: {result.stderr}")

            # 显示下一个提示符
            await self._handle_output(f"{prompt}")

            return True

        except Exception as e:
            error_msg = f"Command execution error: {str(e)}\n"
            await self._handle_output(error_msg)
            logger.error(f"Command execution error for session {self.tab_id}: {e}")
            return False

    async def _handle_output(self, output: str):
        """处理输出"""
        # 添加到缓冲区
        lines = output.split('\n')
        for line in lines:
            if line:  # 忽略空行
                self.output_buffer.append(line)
                self.metadata.has_unread_output = True

        # 限制缓冲区大小
        if len(self.output_buffer) > self.max_history:
            self.output_buffer = self.output_buffer[-self.max_history:]

        # 通知回调
        output_state = {
            'tab_id': self.tab_id,
            'output': output,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'has_unread': True
        }

        for callback in self._output_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(output_state)
                else:
                    callback(output_state)
            except Exception as e:
                logger.warning(f"Output callback error: {e}")

    def get_output(self, lines: int = 50) -> List[str]:
        """获取输出历史"""
        if lines > 0:
            return self.output_buffer[-lines:]
        return self.output_buffer.copy()

    async def close(self):
        """关闭会话"""
        if self.ssh_connection:
            self.ssh_connection.close()
            self.ssh_connection = None

        self.metadata.status = TabStatus.DISCONNECTED
        await self._handle_output("Connection closed.\n")


class SimpleTerminalSessionManager:
    """简化的终端会话管理器"""

    def __init__(self):
        self.tabs: Dict[str, SimpleTabSession] = {}
        self.active_tab_id: Optional[str] = None

    async def create_tab(self, server_config: ServerConfig, title: Optional[str] = None,
                        auto_start: bool = True) -> SimpleTabSession:
        """创建新的终端标签页"""
        tab_id = f"tab_{server_config.host}_{server_config.port}_{server_config.username}"

        session = SimpleTabSession(tab_id, server_config, title)
        self.tabs[tab_id] = session
        self.active_tab_id = tab_id

        if auto_start:
            success = await session.start()
            if not success:
                # 清理失败的会话
                del self.tabs[tab_id]
                if self.active_tab_id == tab_id:
                    self.active_tab_id = None
                raise Exception(f"Failed to start SSH session for {server_config.host}")

        return session

    async def get_active_tab(self) -> Optional[SimpleTabSession]:
        """获取当前活跃的标签页"""
        if self.active_tab_id:
            return self.tabs.get(self.active_tab_id)
        return None

    async def switch_to_tab(self, tab_id: str) -> bool:
        """切换到指定的标签页"""
        if tab_id in self.tabs:
            self.active_tab_id = tab_id
            return True
        return False

    async def close_tab(self, tab_id: str) -> bool:
        """关闭指定的标签页"""
        session = self.tabs.get(tab_id)
        if session:
            await session.close()
            del self.tabs[tab_id]

            if self.active_tab_id == tab_id:
                self.active_tab_id = None
                # 如果还有其他标签页，切换到第一个
                if self.tabs:
                    self.active_tab_id = next(iter(self.tabs))

            return True
        return False

    async def list_tabs(self) -> List[Dict[str, Any]]:
        """列出所有标签页"""
        tabs_info = []
        for tab_id, session in self.tabs.items():
            tabs_info.append({
                'tab_id': tab_id,
                'title': session.metadata.title,
                'status': session.metadata.status.value,
                'server': session.server_config.host,
                'username': session.server_config.username,
                'is_active': tab_id == self.active_tab_id,
                'has_unread_output': session.metadata.has_unread_output
            })
        return tabs_info

    async def shutdown(self):
        """关闭管理器，清理所有会话"""
        for tab_id in list(self.tabs.keys()):
            await self.close_tab(tab_id)