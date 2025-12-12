"""
简化但功能完整的MCP服务器 - 直接SSH实现，显示命令和输出
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    CallToolResult, ReadResourceResult, ListResourcesResult, ListToolsResult
)

from .simple_terminal_manager import (
    SimpleTerminalSessionManager, ServerConfig, TabStatus
)

logger = logging.getLogger(__name__)


class SimpleWindTermMCPServer:
    """简化但功能完整的MCP服务器 - 专注于SSH终端功能"""

    def __init__(self):
        self.server = Server("linux-ssh-mcp-simple")
        self.session_manager = SimpleTerminalSessionManager()
        self._setup_handlers()
        self._setup_tools()

    def _setup_handlers(self):
        """设置MCP服务器处理器"""

        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """列出可用资源"""
            resources = []

            # 活跃的终端会话
            tabs = await self.session_manager.list_tabs()
            for tab in tabs:
                resources.append(Resource(
                    uri=f"terminal://session/{tab['tab_id']}",
                    name=f"Terminal: {tab['title']}",
                    description=f"SSH session to {tab['server']} as {tab['username']} ({tab['status']})",
                    mimeType="text/plain"
                ))

            return resources

        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """读取资源内容"""
            try:
                if uri.startswith("terminal://session/"):
                    tab_id = uri.split("/")[-1]

                    # 获取会话信息
                    tabs = await self.session_manager.list_tabs()
                    tab_info = next((t for t in tabs if t['tab_id'] == tab_id), None)

                    if tab_info:
                        session = self.session_manager.tabs.get(tab_id)
                        if session:
                            # 获取输出历史
                            output_lines = session.get_output(100)
                            output_text = "\n".join(output_lines)

                            # 添加会话信息头部
                            header = f"=== Terminal Session: {tab_info['title']} ===\n"
                            header += f"Server: {tab_info['server']}\n"
                            header += f"User: {tab_info['username']}\n"
                            header += f"Status: {tab_info['status']}\n"
                            header += f"{'='*50}\n\n"

                            content = header + output_text
                        else:
                            content = f"Session {tab_id} not found"
                    else:
                        content = f"Invalid session ID: {tab_id}"
                else:
                    content = f"Unknown resource: {uri}"

                return ReadResourceResult(
                    contents=[TextContent(type="text", text=content)]
                )

            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                raise

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """列出可用工具"""
            return self._tools

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """执行工具"""
            try:
                handler = self._tool_handlers.get(name)
                if not handler:
                    raise ValueError(f"Unknown tool: {name}")

                result = await handler(arguments)

                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
                )

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Error: {str(e)}"
                    )],
                    isError=True
                )

    def _setup_tools(self):
        """设置可用工具"""
        self._tools = [
            # 核心终端工具
            Tool(
                name="create_terminal_tab",
                description="创建新的SSH终端会话",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "host": {"type": "string", "description": "服务器主机名或IP"},
                        "port": {"type": "integer", "description": "SSH端口 (默认: 22)"},
                        "username": {"type": "string", "description": "SSH用户名"},
                        "password": {"type": "string", "description": "SSH密码"},
                        "title": {"type": "string", "description": "可选的标签页标题"}
                    },
                    "required": ["host", "username", "password"]
                }
            ),

            Tool(
                name="send_terminal_input",
                description="发送命令到活跃的SSH终端",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "标签页ID (可选，使用活跃标签页)"},
                        "input": {"type": "string", "description": "要发送的命令或输入"},
                        "send_enter": {"type": "boolean", "description": "是否添加回车键 (默认: true)"}
                    },
                    "required": ["input"]
                }
            ),

            Tool(
                name="get_terminal_output",
                description="获取SSH终端输出历史",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "标签页ID (可选，使用活跃标签页)"},
                        "lines": {"type": "integer", "description": "返回的最大行数 (默认: 50)"}
                    }
                }
            ),

            Tool(
                name="list_terminal_tabs",
                description="列出所有SSH终端标签页",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),

            Tool(
                name="close_terminal_tab",
                description="关闭指定的SSH终端标签页",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "标签页ID"}
                    },
                    "required": ["tab_id"]
                }
            ),

            Tool(
                name="switch_terminal_tab",
                description="切换到指定的SSH终端标签页",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "标签页ID"}
                    },
                    "required": ["tab_id"]
                }
            )
        ]

        self._tool_handlers = {
            "create_terminal_tab": self._handle_create_tab,
            "send_terminal_input": self._handle_send_input,
            "get_terminal_output": self._handle_get_output,
            "list_terminal_tabs": self._handle_list_tabs,
            "close_terminal_tab": self._handle_close_tab,
            "switch_terminal_tab": self._handle_switch_tab,
        }

    async def _handle_create_tab(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理创建终端标签页工具"""
        try:
            # 创建服务器配置
            server_config = ServerConfig(
                id=args.get("server_id", f"server_{args['host']}_{args.get('port', 22)}"),
                host=args["host"],
                port=args.get("port", 22),
                username=args["username"],
                password=args["password"],
                timeout=30
            )

            # 创建标签页
            tab = await self.session_manager.create_tab(
                server_config=server_config,
                title=args.get("title"),
                auto_start=True
            )

            return {
                "success": True,
                "tab_id": tab.tab_id,
                "title": tab.metadata.title,
                "server": server_config.host,
                "status": tab.metadata.status.value,
                "message": f"已创建到 {server_config.host} 的SSH终端会话"
            }

        except Exception as e:
            logger.error(f"Error creating terminal tab: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_send_input(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理发送终端输入工具"""
        try:
            tab_id = args.get("tab_id")
            input_text = args["input"]
            send_enter = args.get("send_enter", True)

            # 获取标签页
            if tab_id:
                tab = self.session_manager.tabs.get(tab_id)
                if not tab:
                    return {"success": False, "error": f"标签页 {tab_id} 不存在"}
            else:
                tab = await self.session_manager.get_active_tab()
                if not tab:
                    return {"success": False, "error": "没有活跃的标签页"}

            # 发送输入
            success = await tab.send_input(input_text)

            return {
                "success": success,
                "tab_id": tab.tab_id,
                "command": input_text,
                "message": f"已发送命令到 {tab.metadata.title}"
            }

        except Exception as e:
            logger.error(f"Error sending terminal input: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_get_output(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理获取终端输出工具"""
        try:
            tab_id = args.get("tab_id")
            lines = args.get("lines", 50)

            # 获取标签页
            if tab_id:
                tab = self.session_manager.tabs.get(tab_id)
                if not tab:
                    return {"success": False, "error": f"标签页 {tab_id} 不存在"}
            else:
                tab = await self.session_manager.get_active_tab()
                if not tab:
                    return {"success": False, "error": "没有活跃的标签页"}

            # 获取输出
            output_lines = tab.get_output(lines)

            return {
                "success": True,
                "tab_id": tab.tab_id,
                "title": tab.metadata.title,
                "lines": len(output_lines),
                "output": "\n".join(output_lines)
            }

        except Exception as e:
            logger.error(f"Error getting terminal output: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_list_tabs(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理列出标签页工具"""
        try:
            tabs = await self.session_manager.list_tabs()

            return {
                "success": True,
                "tabs": tabs,
                "count": len(tabs)
            }

        except Exception as e:
            logger.error(f"Error listing tabs: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_close_tab(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理关闭标签页工具"""
        try:
            tab_id = args["tab_id"]
            success = await self.session_manager.close_tab(tab_id)

            return {
                "success": success,
                "tab_id": tab_id,
                "message": f"已关闭标签页 {tab_id}" if success else f"关闭标签页 {tab_id} 失败"
            }

        except Exception as e:
            logger.error(f"Error closing tab: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_switch_tab(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理切换标签页工具"""
        try:
            tab_id = args["tab_id"]
            success = await self.session_manager.switch_to_tab(tab_id)

            return {
                "success": success,
                "tab_id": tab_id,
                "message": f"已切换到标签页 {tab_id}" if success else f"切换到标签页 {tab_id} 失败"
            }

        except Exception as e:
            logger.error(f"Error switching tab: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def run(self):
        """运行MCP服务器"""
        logger.info("Starting Simple WindTerm-like MCP Server")

        try:
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="linux-ssh-mcp-simple",
                        server_version="2.0.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        )
                    )
                )
        finally:
            logger.info("Shutting down Simple WindTerm-like MCP Server")
            await self.session_manager.shutdown()


def main():
    """MCP服务器主入口点"""
    import asyncio
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    async def run_server():
        server = SimpleWindTermMCPServer()
        await server.run()

    asyncio.run(run_server())


if __name__ == "__main__":
    main()