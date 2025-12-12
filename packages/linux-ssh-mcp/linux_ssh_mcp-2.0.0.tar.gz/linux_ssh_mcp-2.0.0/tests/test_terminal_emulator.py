"""
PTI测试 - 基本功能测试
测试PTY管理和终端会话功能
"""

import pytest
import asyncio
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from linux_ssh_mcp.terminal_emulator import PTYManager, TerminalSize, TerminalState


class TestPTYManager:
    """测试PTY管理器"""

    @pytest.fixture
    async def pty_manager(self):
        """创建PTY管理器实例"""
        manager = PTYManager()
        yield manager
        # 清理资源
        await manager.cleanup()

    @pytest.mark.asyncio
    async def test_create_pty(self, pty_manager):
        """测试创建PTY会话"""
        session = await pty_manager.create_pty("test-session", TerminalSize(80, 24))

        assert session is not None
        assert session.session_id == "test-session"
        assert session.state == TerminalState.ACTIVE
        assert session.size.cols == 80
        assert session.size.rows == 24

    @pytest.mark.asyncio
    async def test_resize_pty(self, pty_manager):
        """测试调整PTY大小"""
        session = await pty_manager.create_pty("resize-test", TerminalSize(80, 24))

        new_size = TerminalSize(120, 40)
        success = await pty_manager.resize_pty("resize-test", new_size)

        assert success is True
        # 验证大小已更改
        updated_session = await pty_manager.get_session("resize-test")
        assert updated_session.size.cols == 120
        assert updated_session.size.rows == 40

    @pytest.mark.asyncio
    async def test_close_pty(self, pty_manager):
        """测试关闭PTY会话"""
        session = await pty_manager.create_pty("close-test", TerminalSize(80, 24))

        success = await pty_manager.close_pty("close-test")
        assert success is True

        # 验证会话已关闭
        with pytest.raises(Exception):
            await pty_manager.get_session("close-test")


@pytest.mark.asyncio
async def test_terminal_size():
    """测试终端大小数据类"""
    size = TerminalSize(80, 24)

    assert size.cols == 80
    assert size.rows == 24
    assert str(size) == "80x24"


@pytest.mark.asyncio
async def test_terminal_state():
    """测试终端状态枚举"""
    assert TerminalState.INITIALIZING.value == "initializing"
    assert TerminalState.ACTIVE.value == "active"
    assert TerminalState.PAUSED.value == "paused"
    assert TerminalState.DISCONNECTED.value == "disconnected"
    assert TerminalState.ERROR.value == "error"