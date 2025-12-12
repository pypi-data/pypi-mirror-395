"""
测试终端会话管理器
测试多标签页管理和会话持久化
"""

import pytest
import asyncio
import sys
import os
from datetime import datetime, timezone

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from linux_ssh_mcp.terminal_session_manager import (
    TerminalSessionManager, ServerConfig, TabStatus, TabMetadata
)
from linux_ssh_mcp.terminal_emulator import TerminalSize


class TestTerminalSessionManager:
    """测试终端会话管理器"""

    @pytest.fixture
    async def session_manager(self):
        """创建会话管理器实例"""
        manager = TerminalSessionManager()
        yield manager
        # 清理资源
        await manager.cleanup()

    @pytest.fixture
    def server_config(self):
        """创建测试服务器配置"""
        return ServerConfig(
            id="test-server",
            host="localhost",
            port=22,
            username="testuser",
            password="testpass"
        )

    @pytest.mark.asyncio
    async def test_create_tab(self, session_manager, server_config):
        """测试创建标签页"""
        tab = await session_manager.create_tab(
            server_config=server_config,
            title="Test Terminal",
            size=TerminalSize(80, 24)
        )

        assert tab is not None
        assert tab.tab_id is not None
        assert tab.title == "Test Terminal"
        assert tab.status == TabStatus.CONNECTING

    @pytest.mark.asyncio
    async def test_list_tabs(self, session_manager, server_config):
        """测试列出标签页"""
        # 创建几个标签页
        await session_manager.create_tab(server_config, "Tab 1", TerminalSize(80, 24))
        await session_manager.create_tab(server_config, "Tab 2", TerminalSize(80, 24))

        tabs = await session_manager.list_tabs()
        assert len(tabs) >= 2

        # 验证标签页信息
        tab_titles = [tab.title for tab in tabs]
        assert "Tab 1" in tab_titles
        assert "Tab 2" in tab_titles

    @pytest.mark.asyncio
    async def test_get_tab(self, session_manager, server_config):
        """测试获取指定标签页"""
        created_tab = await session_manager.create_tab(
            server_config, "Test Tab", TerminalSize(80, 24)
        )
        tab_id = created_tab.tab_id

        retrieved_tab = await session_manager.get_tab(tab_id)
        assert retrieved_tab is not None
        assert retrieved_tab.tab_id == tab_id
        assert retrieved_tab.title == "Test Tab"

    @pytest.mark.asyncio
    async def test_close_tab(self, session_manager, server_config):
        """测试关闭标签页"""
        tab = await session_manager.create_tab(server_config, "Close Test", TerminalSize(80, 24))
        tab_id = tab.tab_id

        success = await session_manager.close_tab(tab_id)
        assert success is True

        # 验证标签页已关闭
        with pytest.raises(Exception):
            await session_manager.get_tab(tab_id)

    @pytest.mark.asyncio
    async def test_workspace_save_load(self, session_manager, server_config):
        """测试工作区保存和加载"""
        # 创建一些标签页
        await session_manager.create_tab(server_config, "Workspace Tab 1", TerminalSize(80, 24))
        await session_manager.create_tab(server_config, "Workspace Tab 2", TerminalSize(120, 40))

        # 保存工作区
        workspace_data = await session_manager.save_workspace("test-workspace")
        assert workspace_data is not None
        assert "tabs" in workspace_data

        # 清除现有标签页
        for tab in await session_manager.list_tabs():
            await session_manager.close_tab(tab.tab_id)

        # 加载工作区
        success = await session_manager.load_workspace("test-workspace")
        assert success is True

        # 验证标签页已恢复
        tabs = await session_manager.list_tabs()
        assert len(tabs) >= 2


class TestTabMetadata:
    """测试标签页元数据"""

    def test_tab_metadata_creation(self):
        """测试标签页元数据创建"""
        now = datetime.now(timezone.utc)
        metadata = TabMetadata(
            tab_id="test-tab",
            title="Test Terminal",
            server_name="test-server",
            status=TabStatus.ACTIVE,
            last_activity=now
        )

        assert metadata.tab_id == "test-tab"
        assert metadata.title == "Test Terminal"
        assert metadata.status == TabStatus.ACTIVE

    def test_tab_metadata_serialization(self):
        """测试标签页元数据序列化"""
        now = datetime.now(timezone.utc)
        metadata = TabMetadata(
            tab_id="test-tab",
            title="Test Terminal",
            server_name="test-server",
            status=TabStatus.ACTIVE,
            last_activity=now
        )

        # 转换为字典
        data = metadata.to_dict()
        assert data["tab_id"] == "test-tab"
        assert data["status"] == "active"  # 枚举值
        assert "last_activity" in data

        # 从字典创建
        restored_metadata = TabMetadata.from_dict(data)
        assert restored_metadata.tab_id == metadata.tab_id
        assert restored_metadata.status == metadata.status


class TestServerConfig:
    """测试服务器配置"""

    def test_server_config_creation(self):
        """测试服务器配置创建"""
        config = ServerConfig(
            id="test-server",
            host="192.168.1.100",
            port=22,
            username="admin",
            password="secret"
        )

        assert config.id == "test-server"
        assert config.host == "192.168.1.100"
        assert config.port == 22
        assert config.username == "admin"

    def test_server_config_serialization(self):
        """测试服务器配置序列化"""
        config = ServerConfig(
            id="test-server",
            host="192.168.1.100",
            port=22,
            username="admin",
            password="secret"
        )

        # 转换为字典，密码应被掩码
        data = config.to_dict()
        assert data["id"] == "test-server"
        assert data["password"] == "***"  # 密码被掩码