"""
Enhanced MCP Server with WindTerm-like Terminal Capabilities
Provides interactive terminal management tools while maintaining backward compatibility
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
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


class WindTermMCPServer:
    """Enhanced MCP Server with WindTerm-like terminal capabilities"""

    def __init__(self):
        self.server = Server("linux-ssh-mcp-windterm")
        self.session_manager = SimpleTerminalSessionManager()
        self._setup_handlers()
        self._setup_tools()

    def _setup_handlers(self):
        """Setup MCP server handlers"""

        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources"""
            resources = []

            # Active terminal sessions
            tabs = await self.session_manager.list_tabs()
            for tab in tabs:
                resources.append(Resource(
                    uri=f"terminal://session/{tab.tab_id}",
                    name=f"Terminal: {tab.title}",
                    description=f"Active terminal session on {tab.server_config.host}",
                    mimeType="text/plain"
                ))

            # Workspaces
            workspaces = await self.session_manager.list_workspaces()
            for workspace in workspaces:
                resources.append(Resource(
                    uri=f"workspace://{workspace}",
                    name=f"Workspace: {workspace}",
                    description=f"Saved terminal workspace",
                    mimeType="application/json"
                ))

            return resources

        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Read resource content"""
            try:
                if uri.startswith("terminal://session/"):
                    tab_id = uri.split("/")[-1]
                    tab = self.session_manager.tab_manager.get_tab(tab_id)

                    if not tab:
                        raise ValueError(f"Terminal session {tab_id} not found")

                    # Get recent output
                    output_lines = await tab.get_output_since_last()
                    content = "\n".join(output_lines[-100:])  # Last 100 lines

                    return ReadResourceResult([
                        TextContent(type="text", text=content)
                    ])

                elif uri.startswith("workspace://"):
                    workspace_name = uri.split("//")[1]
                    workspace_data = await self.session_manager.session_store.load_workspace(workspace_name)

                    if not workspace_data:
                        raise ValueError(f"Workspace {workspace_name} not found")

                    return ReadResourceResult([
                        TextContent(type="text", text=json.dumps(workspace_data, indent=2))
                    ])

                else:
                    raise ValueError(f"Unknown resource URI: {uri}")

            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                raise

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools"""
            return self._tools

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Execute tool"""
            try:
                handler = self._tool_handlers.get(name)
                if not handler:
                    raise ValueError(f"Unknown tool: {name}")

                result = await handler(arguments)

                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2))]
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
        """Setup available tools"""
        self._tools = [
            # Tab Management Tools
            Tool(
                name="create_terminal_tab",
                description="Create a new terminal session tab",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "server_id": {"type": "string", "description": "Server ID from configuration"},
                        "host": {"type": "string", "description": "Server hostname/IP"},
                        "port": {"type": "integer", "description": "SSH port (default: 22)"},
                        "username": {"type": "string", "description": "SSH username"},
                        "password": {"type": "string", "description": "SSH password"},
                        "title": {"type": "string", "description": "Optional tab title"},
                        "cols": {"type": "integer", "description": "Terminal width (default: 80)"},
                        "rows": {"type": "integer", "description": "Terminal height (default: 24)"},
                        "auto_start": {"type": "boolean", "description": "Auto start session (default: true)"}
                    },
                    "required": ["host", "username"]
                }
            ),

            Tool(
                name="switch_terminal_tab",
                description="Switch to an active terminal tab",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID"}
                    },
                    "required": ["tab_id"]
                }
            ),

            Tool(
                name="list_terminal_tabs",
                description="List all active terminal tabs",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "active_only": {"type": "boolean", "description": "Show only active tabs"}
                    }
                }
            ),

            Tool(
                name="close_terminal_tab",
                description="Close a terminal tab",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID"},
                        "force": {"type": "boolean", "description": "Force close if busy"}
                    },
                    "required": ["tab_id"]
                }
            ),

            # Interactive Terminal Tools
            Tool(
                name="send_terminal_input",
                description="Send input to active terminal",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"},
                        "input": {"type": "string", "description": "Text/input to send"},
                        "send_enter": {"type": "boolean", "description": "Add Enter key (default: true)"}
                    },
                    "required": ["input"]
                }
            ),

            Tool(
                name="get_terminal_output",
                description="Get terminal output since last call",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"},
                        "lines": {"type": "integer", "description": "Max lines to return (default: 50)"},
                        "follow": {"type": "boolean", "description": "Continue streaming output"}
                    }
                }
            ),

            Tool(
                name="resize_terminal",
                description="Resize terminal dimensions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"},
                        "cols": {"type": "integer", "description": "New width"},
                        "rows": {"type": "integer", "description": "New height"}
                    },
                    "required": ["cols", "rows"]
                }
            ),

            # Session Management Tools
            Tool(
                name="save_session_workspace",
                description="Save current session workspace",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Workspace name"},
                        "include_history": {"type": "boolean", "description": "Include command history (default: true)"}
                    },
                    "required": ["name"]
                }
            ),

            Tool(
                name="restore_session_workspace",
                description="Restore saved session workspace",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Workspace name"},
                        "auto_connect": {"type": "boolean", "description": "Auto-connect sessions (default: false)"}
                    },
                    "required": ["name"]
                }
            ),

            Tool(
                name="list_workspaces",
                description="List available workspaces",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),

            Tool(
                name="get_session_stats",
                description="Get session manager statistics",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),

            # Command History Tools
            Tool(
                name="get_command_history",
                description="Get command history for a tab",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"},
                        "limit": {"type": "integer", "description": "Maximum number of commands to return (default: 50)"}
                    }
                }
            ),

            # Session Control Tools
            Tool(
                name="pause_terminal",
                description="Pause a terminal session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"}
                    }
                }
            ),

            Tool(
                name="resume_terminal",
                description="Resume a paused terminal session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"}
                    }
                }
            ),

            # File Operation Tools
            Tool(
                name="upload_file",
                description="Upload a file to the remote server via SCP",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"},
                        "local_path": {"type": "string", "description": "Local file path to upload"},
                        "remote_path": {"type": "string", "description": "Remote destination path"},
                        "create_dirs": {"type": "boolean", "description": "Create remote directories if needed (default: true)"}
                    },
                    "required": ["local_path", "remote_path"]
                }
            ),

            Tool(
                name="download_file",
                description="Download a file from the remote server via SCP",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"},
                        "remote_path": {"type": "string", "description": "Remote file path to download"},
                        "local_path": {"type": "string", "description": "Local destination path"},
                        "create_dirs": {"type": "boolean", "description": "Create local directories if needed (default: true)"}
                    },
                    "required": ["remote_path", "local_path"]
                }
            ),

            Tool(
                name="read_remote_file",
                description="Read file contents directly from remote server",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tab_id": {"type": "string", "description": "Tab session ID (optional, uses active if not provided)"},
                        "remote_path": {"type": "string", "description": "Remote file path to read"},
                        "encoding": {"type": "string", "description": "File encoding (default: utf-8)"},
                        "max_lines": {"type": "integer", "description": "Maximum lines to read (default: 1000)"}
                    },
                    "required": ["remote_path"]
                }
            )
        ]

        # Setup tool handlers
        self._tool_handlers = {
            "create_terminal_tab": self._handle_create_tab,
            "switch_terminal_tab": self._handle_switch_tab,
            "list_terminal_tabs": self._handle_list_tabs,
            "close_terminal_tab": self._handle_close_tab,
            "send_terminal_input": self._handle_send_input,
            "get_terminal_output": self._handle_get_output,
            "resize_terminal": self._handle_resize_terminal,
            "save_session_workspace": self._handle_save_workspace,
            "restore_session_workspace": self._handle_restore_workspace,
            "list_workspaces": self._handle_list_workspaces,
            "get_session_stats": self._handle_get_stats,
            "get_command_history": self._handle_get_command_history,
            "pause_terminal": self._handle_pause_terminal,
            "resume_terminal": self._handle_resume_terminal,
            "upload_file": self._handle_upload_file,
            "download_file": self._handle_download_file,
            "read_remote_file": self._handle_read_remote_file,
        }

    async def _handle_create_tab(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_terminal_tab tool - Simplified SSH implementation"""
        try:
            # Create server config
            server_config = ServerConfig(
                id=args.get("server_id", f"server_{args['host']}_{args.get('port', 22)}"),
                host=args["host"],
                port=args.get("port", 22),
                username=args["username"],
                password=args.get("password", ""),
                timeout=30
            )

            # Create tab with auto-start
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

    async def _handle_switch_tab(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle switch_terminal_tab tool"""
        tab_id = args["tab_id"]
        success = await self.session_manager.switch_to_tab(tab_id)

        if success:
            tab = self.session_manager.tab_manager.get_tab(tab_id)
            return {
                "success": True,
                "tab_id": tab_id,
                "title": tab.title if tab else None,
                "status": tab.metadata.status.value if tab else None
            }
        else:
            return {
                "success": False,
                "error": f"Tab {tab_id} not found"
            }

    async def _handle_list_tabs(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_terminal_tabs tool"""
        active_only = args.get("active_only", False)

        tabs = await self.session_manager.list_tabs()
        if active_only:
            tabs = [tab for tab in tabs if tab.metadata.status == TabStatus.ACTIVE]

        tab_info = []
        for tab in tabs:
            tab_info.append({
                "tab_id": tab.tab_id,
                "title": tab.title,
                "server": tab.server_config.host,
                "status": tab.metadata.status.value,
                "last_activity": tab.metadata.last_activity.isoformat(),
                "has_unread_output": tab.metadata.has_unread_output,
                "terminal_size": {
                    "cols": tab.state.terminal_size.cols,
                    "rows": tab.state.terminal_size.rows
                }
            })

        return {
            "tabs": tab_info,
            "active_tab_id": self.session_manager.active_tab_id,
            "total_count": len(tab_info)
        }

    async def _handle_close_tab(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle close_terminal_tab tool - Simplified SSH implementation"""
        tab_id = args["tab_id"]
        force = args.get("force", False)

        # Get tab from SimpleTerminalSessionManager
        tab = self.session_manager.tabs.get(tab_id)
        if not tab:
            return {
                "success": False,
                "error": f"Tab {tab_id} not found"
            }

        # For simplified version, we'll allow closing active tabs
        success = await self.session_manager.close_tab(tab_id)

        return {
            "success": success,
            "tab_id": tab_id,
            "message": f"Tab {tab_id} closed successfully" if success else f"Failed to close tab {tab_id}"
        }

    async def _handle_send_input(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle send_terminal_input tool - Simplified SSH implementation"""
        try:
            tab_id = args.get("tab_id")
            input_text = args["input"]
            send_enter = args.get("send_enter", True)

            # Get tab (use active if not specified)
            if tab_id:
                tab = self.session_manager.tabs.get(tab_id)
                if not tab:
                    return {"success": False, "error": f"标签页 {tab_id} 不存在"}
            else:
                tab = await self.session_manager.get_active_tab()
                if not tab:
                    return {"success": False, "error": "没有活跃的标签页"}

            # Send input to SSH session
            success = await tab.send_input(input_text)

            return {
                "success": success,
                "tab_id": tab.tab_id,
                "command": input_text,
                "message": f"已发送命令到 {tab.metadata.title}" if success else "发送命令失败"
            }

        except Exception as e:
            logger.error(f"Error sending terminal input: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_get_output(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_terminal_output tool - Simplified SSH implementation"""
        try:
            tab_id = args.get("tab_id")
            lines = args.get("lines", 50)

            # Get tab (use active if not specified)
            if tab_id:
                tab = self.session_manager.tabs.get(tab_id)
                if not tab:
                    return {"success": False, "error": f"标签页 {tab_id} 不存在"}
            else:
                tab = await self.session_manager.get_active_tab()
                if not tab:
                    return {"success": False, "error": "没有活跃的标签页"}

            # Get output from buffer
            output_lines = tab.get_output(lines)
            output_text = "\n".join(output_lines)

            return {
                "success": True,
                "tab_id": tab.tab_id,
                "title": tab.metadata.title,
                "lines": len(output_lines),
                "output": output_text
            }

        except Exception as e:
            logger.error(f"Error getting terminal output: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_resize_terminal(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resize_terminal tool"""
        tab_id = args.get("tab_id")
        cols = args["cols"]
        rows = args["rows"]

        # Get tab (use active if not specified)
        if tab_id:
            tab = self.session_manager.tab_manager.get_tab(tab_id)
            if not tab:
                return {"success": False, "error": f"Tab {tab_id} not found"}
        else:
            tab = await self.session_manager.get_active_tab()
            if not tab:
                return {"success": False, "error": "No active tab found"}

        success = await tab.resize(cols, rows)

        return {
            "success": success,
            "tab_id": tab.tab_id,
            "new_size": {"cols": cols, "rows": rows}
        }

    async def _handle_save_workspace(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle save_session_workspace tool"""
        name = args["name"]
        include_history = args.get("include_history", True)

        success = await self.session_manager.save_workspace(name, include_history)

        return {
            "success": success,
            "workspace_name": name,
            "message": f"Workspace '{name}' saved successfully" if success else f"Failed to save workspace '{name}'"
        }

    async def _handle_restore_workspace(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle restore_session_workspace tool"""
        name = args["name"]
        auto_connect = args.get("auto_connect", False)

        tabs = await self.session_manager.restore_workspace(name, auto_connect)

        return {
            "success": True,
            "workspace_name": name,
            "tabs_restored": len(tabs),
            "tab_ids": [tab.tab_id for tab in tabs]
        }

    async def _handle_list_workspaces(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_workspaces tool"""
        workspaces = await self.session_manager.list_workspaces()

        return {
            "workspaces": workspaces,
            "count": len(workspaces)
        }

    async def _handle_get_stats(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_session_stats tool"""
        stats = await self.session_manager.get_stats()

        return stats

    async def _handle_get_command_history(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_command_history tool"""
        tab_id = args.get("tab_id")
        limit = args.get("limit", 50)

        # Get tab (use active if not specified)
        if tab_id:
            tab = self.session_manager.tab_manager.get_tab(tab_id)
            if not tab:
                return {"success": False, "error": f"Tab {tab_id} not found"}
        else:
            tab = await self.session_manager.get_active_tab()
            if not tab:
                return {"success": False, "error": "No active tab found"}

        history = await tab.get_command_history(limit)

        return {
            "success": True,
            "tab_id": tab.tab_id,
            "history": history,
            "count": len(history)
        }

    async def _handle_pause_terminal(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pause_terminal tool"""
        tab_id = args.get("tab_id")

        # Get tab (use active if not specified)
        if tab_id:
            tab = self.session_manager.tab_manager.get_tab(tab_id)
            if not tab:
                return {"success": False, "error": f"Tab {tab_id} not found"}
        else:
            tab = await self.session_manager.get_active_tab()
            if not tab:
                return {"success": False, "error": "No active tab found"}

        success = await tab.pause()

        return {
            "success": success,
            "tab_id": tab.tab_id,
            "status": tab.metadata.status.value
        }

    async def _handle_resume_terminal(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resume_terminal tool"""
        tab_id = args.get("tab_id")

        # Get tab (use active if not specified)
        if tab_id:
            tab = self.session_manager.tab_manager.get_tab(tab_id)
            if not tab:
                return {"success": False, "error": f"Tab {tab_id} not found"}
        else:
            tab = await self.session_manager.get_active_tab()
            if not tab:
                return {"success": False, "error": "No active tab found"}

        success = await tab.resume()

        return {
            "success": success,
            "tab_id": tab.tab_id,
            "status": tab.metadata.status.value
        }

    async def _handle_upload_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle upload_file tool - Upload file via SCP"""
        try:
            import os
            import pathlib

            tab_id = args.get("tab_id")
            local_path = args["local_path"]
            remote_path = args["remote_path"]
            create_dirs = args.get("create_dirs", True)

            # Get active tab if tab_id not provided
            if not tab_id:
                tab = await self.session_manager.get_active_tab()
                if not tab:
                    return {"success": False, "error": "No active tab found"}
            else:
                tab = self.session_manager.tabs.get(tab_id)
                if not tab:
                    return {"success": False, "error": f"Tab {tab_id} not found"}

            # Check local file exists
            if not os.path.exists(local_path):
                return {"success": False, "error": f"Local file not found: {local_path}"}

            # Get SSH connection from session
            if not tab.ssh_connection:
                return {"success": False, "error": "SSH connection not established"}

            try:
                # Create remote directories if needed
                if create_dirs:
                    remote_dir = os.path.dirname(remote_path)
                    if remote_dir:
                        mkdir_cmd = f"mkdir -p {remote_dir}"
                        await tab.ssh_connection.run(mkdir_cmd, check=False)

                # Use asyncssh SCP for file upload
                async with tab.ssh_connection.start_sftp_client() as sftp:
                    await sftp.put(local_path, remote_path)

                # Get file info
                file_stat = os.stat(local_path)

                return {
                    "success": True,
                    "tab_id": tab.tab_id,
                    "local_path": local_path,
                    "remote_path": remote_path,
                    "size_bytes": file_stat.st_size,
                    "message": f"Successfully uploaded {os.path.basename(local_path)} to {remote_path}"
                }

            except Exception as scp_error:
                return {
                    "success": False,
                    "error": f"SCP upload failed: {str(scp_error)}"
                }

        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_download_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle download_file tool - Download file via SCP"""
        try:
            import os
            import pathlib

            tab_id = args.get("tab_id")
            remote_path = args["remote_path"]
            local_path = args["local_path"]
            create_dirs = args.get("create_dirs", True)

            # Get active tab if tab_id not provided
            if not tab_id:
                tab = await self.session_manager.get_active_tab()
                if not tab:
                    return {"success": False, "error": "No active tab found"}
            else:
                tab = self.session_manager.tabs.get(tab_id)
                if not tab:
                    return {"success": False, "error": f"Tab {tab_id} not found"}

            # Get SSH connection from session
            if not tab.ssh_connection:
                return {"success": False, "error": "SSH connection not established"}

            try:
                # Check if remote file exists
                check_result = await tab.ssh_connection.run(f"test -f {remote_path} && echo 'exists' || echo 'not_found'", check=False)
                if "not_found" in check_result.stdout:
                    return {"success": False, "error": f"Remote file not found: {remote_path}"}

                # Create local directories if needed
                if create_dirs:
                    local_dir = os.path.dirname(local_path)
                    if local_dir:
                        os.makedirs(local_dir, exist_ok=True)

                # Use asyncssh SCP for file download
                async with tab.ssh_connection.start_sftp_client() as sftp:
                    await sftp.get(remote_path, local_path)

                # Get file info
                if os.path.exists(local_path):
                    file_stat = os.stat(local_path)
                    return {
                        "success": True,
                        "tab_id": tab.tab_id,
                        "remote_path": remote_path,
                        "local_path": local_path,
                        "size_bytes": file_stat.st_size,
                        "message": f"Successfully downloaded {os.path.basename(remote_path)} to {local_path}"
                    }
                else:
                    return {"success": False, "error": "Download completed but local file not found"}

            except Exception as scp_error:
                return {
                    "success": False,
                    "error": f"SCP download failed: {str(scp_error)}"
                }

        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_read_remote_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle read_remote_file tool - Read file contents directly"""
        try:
            tab_id = args.get("tab_id")
            remote_path = args["remote_path"]
            encoding = args.get("encoding", "utf-8")
            max_lines = args.get("max_lines", 1000)

            # Get active tab if tab_id not provided
            if not tab_id:
                tab = await self.session_manager.get_active_tab()
                if not tab:
                    return {"success": False, "error": "No active tab found"}
            else:
                tab = self.session_manager.tabs.get(tab_id)
                if not tab:
                    return {"success": False, "error": f"Tab {tab_id} not found"}

            # Get SSH connection from session
            if not tab.ssh_connection:
                return {"success": False, "error": "SSH connection not established"}

            try:
                # Check if remote file exists and get file info
                check_result = await tab.ssh_connection.run(f"test -f {remote_path} && echo 'exists' || echo 'not_found'", check=False)
                if "not_found" in check_result.stdout:
                    return {"success": False, "error": f"Remote file not found: {remote_path}"}

                # Read file content with head command for line limiting
                if max_lines > 0:
                    read_cmd = f"head -n {max_lines} '{remote_path}'"
                else:
                    read_cmd = f"cat '{remote_path}'"

                result = await tab.ssh_connection.run(read_cmd, check=False)

                return {
                    "success": True,
                    "tab_id": tab.tab_id,
                    "remote_path": remote_path,
                    "content": result.stdout,
                    "encoding": encoding,
                    "lines_read": len(result.stdout.splitlines()) if result.stdout else 0,
                    "max_lines": max_lines,
                    "exit_status": result.exit_status
                }

            except Exception as read_error:
                return {
                    "success": False,
                    "error": f"Failed to read remote file: {str(read_error)}"
                }

        except Exception as e:
            logger.error(f"Error reading remote file: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def run(self):
        """Run the MCP server"""
        logger.info("Starting WindTerm-like MCP Server")

        try:
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="linux-ssh-mcp-windterm",
                        server_version="2.0.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        )
                    )
                )
        finally:
            logger.info("Shutting down WindTerm-like MCP Server")
            await self.session_manager.shutdown()


def main():
    """Main entry point for MCP server"""
    import asyncio
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    async def run_server():
        server = WindTermMCPServer()
        await server.run()

    asyncio.run(run_server())


if __name__ == "__main__":
    main()