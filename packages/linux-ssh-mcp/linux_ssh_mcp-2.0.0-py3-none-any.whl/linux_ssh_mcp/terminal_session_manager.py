"""
Terminal Session Manager
Central orchestrator for WindTerm-like multi-tab session management
"""

import asyncio
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, AsyncIterator, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import logging
import uuid
import aiofiles
from .terminal_emulator import (
    PTYManager, TerminalProtocolHandler, StreamHandler,
    TerminalSize, TerminalState, PTYSession
)

logger = logging.getLogger(__name__)


class TabStatus(Enum):
    """Tab session status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PAUSED = "paused"


@dataclass
class ServerConfig:
    """Server configuration for SSH connections"""
    id: str
    host: str
    port: int = 22
    username: str = ""
    password: str = ""
    key_file: Optional[str] = None
    timeout: int = 30

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Don't include password in serialization
        if self.password:
            data['password'] = "***"
        return data


@dataclass
class TabMetadata:
    """Tab UI metadata"""
    tab_id: str
    title: str
    server_name: str
    status: TabStatus
    last_activity: datetime
    has_unread_output: bool = False
    color_scheme: str = "dark"
    font_size: int = 14
    position: int = 0  # Tab position in UI

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        data['last_activity'] = self.last_activity.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TabMetadata':
        """Create from dictionary"""
        data['status'] = TabStatus(data['status'])
        data['last_activity'] = datetime.fromisoformat(data['last_activity'])
        return cls(**data)


@dataclass
class TerminalSessionState:
    """Persistent terminal session state"""
    session_id: str
    server_id: str
    title: str
    created_at: datetime
    last_active: datetime
    terminal_size: TerminalSize
    command_history: List[str] = field(default_factory=list)
    current_directory: str = ""
    environment: Dict[str, str] = field(default_factory=dict)
    script_hooks: Dict[str, str] = field(default_factory=dict)
    is_active: bool = True
    last_command: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['terminal_size'] = asdict(self.terminal_size)
        data['created_at'] = self.created_at.isoformat()
        data['last_active'] = self.last_active.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TerminalSessionState':
        """Create from dictionary"""
        data['terminal_size'] = TerminalSize(**data['terminal_size'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_active'] = datetime.fromisoformat(data['last_active'])
        return cls(**data)


class TabSession:
    """Represents a single terminal session/tab"""

    def __init__(self, tab_id: str, server_config: ServerConfig, title: str = None):
        self.tab_id = tab_id
        self.server_config = server_config
        self.title = title or f"{server_config.host}:{server_config.port}"

        # Terminal components
        self.pty_manager = PTYManager()
        self.protocol_handler = TerminalProtocolHandler()
        self.stream_handler = StreamHandler(self.pty_manager, self.protocol_handler)

        # Session state
        self.state = TerminalSessionState(
            session_id=tab_id,
            server_id=server_config.id,
            title=self.title,
            created_at=datetime.now(timezone.utc),
            last_active=datetime.now(timezone.utc),
            terminal_size=TerminalSize()
        )

        # PTY session (created on start)
        self.pty_session: Optional[PTYSession] = None

        # UI metadata
        self.metadata = TabMetadata(
            tab_id=tab_id,
            title=self.title,
            server_name=server_config.id,
            status=TabStatus.CONNECTING,
            last_activity=datetime.now(timezone.utc)
        )

        # Command history
        self.command_history: List[str] = []
        self.output_buffer: List[str] = []
        self.max_history = 1000

        # Event callbacks
        self._output_callbacks: List[callable] = []
        self._status_callbacks: List[callable] = []

    async def start(self) -> bool:
        """Start the terminal session"""
        try:
            logger.info(f"Starting terminal session {self.tab_id}")

            # Create PTY session
            self.pty_session = await self.pty_manager.create_pty(
                self.tab_id,
                self.state.terminal_size
            )

            # Start SSH connection to server
            ssh_success = await self._connect_ssh()
            if not ssh_success:
                await self.cleanup()
                return False

            # Start output streaming
            await self.stream_handler.start_streaming(self.tab_id, self._on_output)

            # Update status
            self.metadata.status = TabStatus.ACTIVE
            self.state.is_active = True
            self.state.last_active = datetime.now(timezone.utc)

            # Notify status change
            await self._notify_status_change()

            logger.info(f"Terminal session {self.tab_id} started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start terminal session {self.tab_id}: {e}")
            self.metadata.status = TabStatus.ERROR
            await self._notify_status_change()
            await self.cleanup()
            return False

    async def send_input(self, data: str) -> bool:
        """Send input to terminal"""
        if self.metadata.status != TabStatus.ACTIVE:
            logger.warning(f"Session {self.tab_id} not active for input")
            return False

        try:
            # Format input for terminal
            formatted_input = self.protocol_handler.format_input(data)

            # Send to PTY
            success = await self.pty_manager.write_stream(self.tab_id, formatted_input)

            if success:
                # Update activity
                self.state.last_active = datetime.now(timezone.utc)
                self.metadata.last_activity = datetime.now(timezone.utc)

                # Track command if it ends with newline
                if data.strip().endswith('\n'):
                    self.state.last_command = data.strip()
                    self.command_history.append(data.strip())

                    # Limit history size
                    if len(self.command_history) > self.max_history:
                        self.command_history = self.command_history[-self.max_history:]

            return success

        except Exception as e:
            logger.error(f"Failed to send input to session {self.tab_id}: {e}")
            return False

    async def resize(self, cols: int, rows: int) -> bool:
        """Resize terminal"""
        try:
            new_size = TerminalSize(cols=cols, rows=rows)

            if self.pty_session:
                success = await self.pty_manager.resize_pty(self.tab_id, new_size)
                if success:
                    self.state.terminal_size = new_size
                    logger.info(f"Terminal {self.tab_id} resized to {cols}x{rows}")
                return success

            # Update size even if no PTY yet
            self.state.terminal_size = new_size
            return True

        except Exception as e:
            logger.error(f"Failed to resize terminal {self.tab_id}: {e}")
            return False

    async def get_output_stream(self) -> AsyncIterator[str]:
        """Get real-time output stream"""
        if not self.pty_session:
            raise RuntimeError("Session not started")

        async for output in self.pty_manager.read_stream(self.tab_id):
            yield output

    async def get_output_since_last(self, last_seen: int = 0) -> List[str]:
        """Get output lines since last seen index"""
        return await self.stream_handler.get_output_since_last(self.tab_id, last_seen)

    async def get_command_history(self, limit: int = 50) -> List[str]:
        """Get command history"""
        return self.command_history[-limit:] if limit > 0 else self.command_history

    async def clear_output(self) -> None:
        """Clear output buffer"""
        self.output_buffer.clear()

    async def pause(self) -> bool:
        """Pause terminal session"""
        if self.metadata.status == TabStatus.ACTIVE:
            self.metadata.status = TabStatus.PAUSED
            await self._notify_status_change()
            return True
        return False

    async def resume(self) -> bool:
        """Resume terminal session"""
        if self.metadata.status == TabStatus.PAUSED:
            self.metadata.status = TabStatus.ACTIVE
            await self._notify_status_change()
            return True
        return False

    async def close(self) -> bool:
        """Close terminal session"""
        try:
            logger.info(f"Closing terminal session {self.tab_id}")

            self.metadata.status = TabStatus.DISCONNECTED
            await self._notify_status_change()

            await self.cleanup()

            logger.info(f"Terminal session {self.tab_id} closed successfully")
            return True

        except Exception as e:
            logger.error(f"Error closing terminal session {self.tab_id}: {e}")
            return False

    async def cleanup(self) -> None:
        """Cleanup resources"""
        try:
            # Stop streaming
            await self.stream_handler.stop_streaming(self.tab_id)

            # Close PTY
            if self.pty_session:
                await self.pty_manager.close_pty(self.tab_id)
                self.pty_session = None

            self.state.is_active = False

        except Exception as e:
            logger.error(f"Error during cleanup of session {self.tab_id}: {e}")

    def add_output_callback(self, callback: callable) -> None:
        """Add callback for output events"""
        self._output_callbacks.append(callback)

    def remove_output_callback(self, callback: callable) -> None:
        """Remove output callback"""
        if callback in self._output_callbacks:
            self._output_callbacks.remove(callback)

    def add_status_callback(self, callback: callable) -> None:
        """Add callback for status changes"""
        self._status_callbacks.append(callback)

    def remove_status_callback(self, callback: callable) -> None:
        """Remove status callback"""
        if callback in self._status_callbacks:
            self._status_callbacks.remove(callback)

    async def _connect_ssh(self) -> bool:
        """Connect SSH to server with real implementation"""
        from .ssh_manager_v2 import EnhancedSSHManager

        logger.info(f"Connecting to SSH server {self.server_config.host}:{self.server_config.port}")

        try:
            # Create SSH manager if not exists
            if not hasattr(self, '_ssh_manager'):
                self._ssh_manager = EnhancedSSHManager()

            # Connect to SSH server
            connection = await self._ssh_manager.create_terminal_connection(
                host=self.server_config.host,
                port=self.server_config.port,
                username=self.server_config.username,
                password=self.server_config.password
            )

            if connection:
                self.ssh_connection = connection
                logger.info(f"SSH connection established for session {self.tab_id}")

                # Start reading SSH output
                await self._start_ssh_output_reader()
                return True
            else:
                logger.error(f"Failed to establish SSH connection for session {self.tab_id}")
                return False

        except Exception as e:
            logger.error(f"SSH connection error for session {self.tab_id}: {e}")
            return False

    async def _start_ssh_output_reader(self):
        """Start reading output from SSH process"""
        try:
            if hasattr(self.ssh_connection, 'connection_id'):
                # Read output from SSH process
                async def read_ssh_output():
                    try:
                        async for output in self._ssh_manager.get_connection_output_stream(self.ssh_connection.connection_id):
                            if output:
                                # Handle SSH output
                                await self._on_ssh_output(output)
                    except Exception as e:
                        logger.warning(f"SSH output reader error: {e}")

                # Start background task
                asyncio.create_task(read_ssh_output())

        except Exception as e:
            logger.error(f"Failed to start SSH output reader: {e}")

    async def _on_ssh_output(self, output: str):
        """Handle SSH output"""
        try:
            # Add to output buffer
            self.output_buffer.append(output)

            # Limit buffer size
            if len(self.output_buffer) > self.max_history:
                self.output_buffer = self.output_buffer[-self.max_history:]

            # Mark as having unread output
            self.metadata.has_unread_output = True

            # Notify callbacks
            output_state = {
                'raw_data': output,
                'cleaned_data': output,
                'timestamp': asyncio.get_event_loop().time()
            }
            for callback in self._output_callbacks:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(self.tab_id, output_state)
                    else:
                        callback(self.tab_id, output_state)
                except Exception as e:
                    logger.warning(f"Output callback error: {e}")

        except Exception as e:
            logger.error(f"Error handling SSH output: {e}")

    async def _on_output(self, session_id: str, output_state: Dict[str, Any]) -> None:
        """Handle output from stream"""
        if session_id != self.tab_id:
            return

        # Add to buffer
        self.output_buffer.append(output_state['cleaned_data'])

        # Limit buffer size
        if len(self.output_buffer) > self.max_history:
            self.output_buffer = self.output_buffer[-self.max_history:]

        # Mark as having unread output
        self.metadata.has_unread_output = True

        # Notify callbacks
        for callback in self._output_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self.tab_id, output_state)
                else:
                    callback(self.tab_id, output_state)
            except Exception as e:
                logger.error(f"Error in output callback: {e}")

    async def _notify_status_change(self) -> None:
        """Notify status change callbacks"""
        for callback in self._status_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self.tab_id, self.metadata.status)
                else:
                    callback(self.tab_id, self.metadata.status)
            except Exception as e:
                logger.error(f"Error in status callback: {e}")


class TabManager:
    """Manages multiple terminal tabs"""

    def __init__(self):
        self.tabs: Dict[str, TabSession] = {}
        self.tab_order: List[str] = []
        self.active_tab_id: Optional[str] = None

    def create_tab(self, server_config: ServerConfig, title: str = None) -> TabSession:
        """Create a new tab session"""
        tab_id = str(uuid.uuid4())
        tab = TabSession(tab_id, server_config, title)

        self.tabs[tab_id] = tab
        self.tab_order.append(tab_id)

        # Set as active if first tab
        if self.active_tab_id is None:
            self.active_tab_id = tab_id

        return tab

    async def close_tab(self, tab_id: str) -> bool:
        """Close a tab session"""
        tab = self.tabs.get(tab_id)
        if not tab:
            return False

        # Close the session
        await tab.close()

        # Remove from tracking
        del self.tabs[tab_id]
        if tab_id in self.tab_order:
            self.tab_order.remove(tab_id)

        # Update active tab if needed
        if self.active_tab_id == tab_id and self.tabs:
            self.active_tab_id = self.tab_order[-1] if self.tab_order else None

        return True

    def switch_to_tab(self, tab_id: str) -> bool:
        """Switch to a specific tab"""
        if tab_id not in self.tabs:
            return False

        self.active_tab_id = tab_id

        # Move to end of order (most recent)
        if tab_id in self.tab_order:
            self.tab_order.remove(tab_id)
        self.tab_order.append(tab_id)

        return True

    def get_active_tab(self) -> Optional[TabSession]:
        """Get the currently active tab"""
        if self.active_tab_id:
            return self.tabs.get(self.active_tab_id)
        return None

    def get_tab(self, tab_id: str) -> Optional[TabSession]:
        """Get a specific tab"""
        return self.tabs.get(tab_id)

    def list_tabs(self) -> List[TabSession]:
        """List all tabs in order"""
        return [self.tabs[tab_id] for tab_id in self.tab_order if tab_id in self.tabs]

    def get_tab_metadata(self) -> List[TabMetadata]:
        """Get metadata for all tabs"""
        return [tab.metadata for tab in self.list_tabs()]

    async def close_all_tabs(self) -> None:
        """Close all tabs"""
        for tab_id in list(self.tabs.keys()):
            await self.close_tab(tab_id)


class SessionStore:
    """Handles session persistence and recovery"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = Path.home() / ".ssh-mcp" / "workspaces"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.workspaces_file = self.storage_dir / "workspaces.json"

    async def save_workspace(self, name: str, tabs: List[TabSession]) -> bool:
        """Save workspace with all tabs"""
        try:
            workspace_data = {
                "name": name,
                "version": "2.0",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "tabs": []
            }

            for tab in tabs:
                tab_data = {
                    "metadata": tab.metadata.to_dict(),
                    "state": tab.state.to_dict(),
                    "server_config": tab.server_config.to_dict()
                }
                workspace_data["tabs"].append(tab_data)

            # Load existing workspaces
            workspaces = await self._load_workspaces()
            workspaces[name] = workspace_data

            # Save to file
            async with aiofiles.open(self.workspaces_file, 'w') as f:
                await f.write(json.dumps(workspaces, indent=2, default=str))

            logger.info(f"Workspace '{name}' saved with {len(tabs)} tabs")
            return True

        except Exception as e:
            logger.error(f"Failed to save workspace '{name}': {e}")
            return False

    async def load_workspace(self, name: str) -> Optional[Dict[str, Any]]:
        """Load workspace data"""
        try:
            workspaces = await self._load_workspaces()
            return workspaces.get(name)
        except Exception as e:
            logger.error(f"Failed to load workspace '{name}': {e}")
            return None

    async def list_workspaces(self) -> List[str]:
        """List available workspaces"""
        try:
            workspaces = await self._load_workspaces()
            return list(workspaces.keys())
        except Exception as e:
            logger.error(f"Failed to list workspaces: {e}")
            return []

    async def delete_workspace(self, name: str) -> bool:
        """Delete a workspace"""
        try:
            workspaces = await self._load_workspaces()
            if name in workspaces:
                del workspaces[name]

                async with aiofiles.open(self.workspaces_file, 'w') as f:
                    await f.write(json.dumps(workspaces, indent=2, default=str))

                logger.info(f"Workspace '{name}' deleted")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to delete workspace '{name}': {e}")
            return False

    async def _load_workspaces(self) -> Dict[str, Any]:
        """Load workspaces from file"""
        if not self.workspaces_file.exists():
            return {}

        try:
            async with aiofiles.open(self.workspaces_file, 'r') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to load workspaces file: {e}")
            return {}


class TerminalSessionManager:
    """Main orchestrator for WindTerm-like terminal session management"""

    def __init__(self, storage_dir: str = None):
        self.tab_manager = TabManager()
        self.session_store = SessionStore(storage_dir)
        self._shutdown_event = asyncio.Event()

        # Performance monitoring
        self.stats = {
            'total_sessions_created': 0,
            'active_sessions': 0,
            'total_commands_executed': 0
        }

    async def create_tab(self, server_config: ServerConfig, title: str = None, auto_start: bool = True) -> TabSession:
        """Create a new terminal tab"""
        tab = self.tab_manager.create_tab(server_config, title)

        # Add monitoring callbacks
        tab.add_status_callback(self._on_tab_status_change)

        if auto_start:
            success = await tab.start()
            if success:
                self.stats['total_sessions_created'] += 1
                self.stats['active_sessions'] += 1
            else:
                # Clean up failed tab
                await self.tab_manager.close_tab(tab.tab_id)
                raise RuntimeError(f"Failed to start terminal session {tab.tab_id}")

        return tab

    async def switch_to_tab(self, tab_id: str) -> bool:
        """Switch to active tab"""
        return self.tab_manager.switch_to_tab(tab_id)

    async def close_tab(self, tab_id: str) -> bool:
        """Close a terminal tab"""
        success = await self.tab_manager.close_tab(tab_id)
        if success:
            self.stats['active_sessions'] = max(0, self.stats['active_sessions'] - 1)
        return success

    async def get_active_tab(self) -> Optional[TabSession]:
        """Get currently active tab"""
        return self.tab_manager.get_active_tab()

    async def list_tabs(self) -> List[TabSession]:
        """List all tabs"""
        return self.tab_manager.list_tabs()

    async def get_tab_metadata(self) -> List[TabMetadata]:
        """Get metadata for all tabs"""
        return self.tab_manager.get_tab_metadata()

    async def save_workspace(self, name: str, include_history: bool = True) -> bool:
        """Save current session workspace"""
        tabs = self.tab_manager.list_tabs()
        if not include_history:
            # Clear history before saving
            for tab in tabs:
                tab.command_history.clear()
                tab.output_buffer.clear()

        return await self.session_store.save_workspace(name, tabs)

    async def restore_workspace(self, name: str, auto_connect: bool = False) -> List[TabSession]:
        """Restore saved workspace"""
        workspace_data = await self.session_store.load_workspace(name)
        if not workspace_data:
            return []

        restored_tabs = []

        for tab_data in workspace_data.get("tabs", []):
            try:
                # Reconstruct server config
                server_config = ServerConfig(**tab_data["server_config"])

                # Create tab
                title = tab_data["metadata"]["title"]
                tab = await self.create_tab(server_config, title, auto_connect=auto_connect)

                # Restore metadata
                tab.metadata = TabMetadata.from_dict(tab_data["metadata"])

                # Restore state
                tab.state = TerminalSessionState.from_dict(tab_data["state"])

                restored_tabs.append(tab)

            except Exception as e:
                logger.error(f"Failed to restore tab from workspace '{name}': {e}")

        logger.info(f"Restored {len(restored_tabs)} tabs from workspace '{name}'")
        return restored_tabs

    async def list_workspaces(self) -> List[str]:
        """List available workspaces"""
        return await self.session_store.list_workspaces()

    async def delete_workspace(self, name: str) -> bool:
        """Delete a workspace"""
        return await self.session_store.delete_workspace(name)

    async def get_stats(self) -> Dict[str, Any]:
        """Get session manager statistics"""
        return {
            **self.stats,
            'active_tab_count': len(self.tab_manager.tabs),
            'total_tab_count': len(self.tab_manager.tab_order),
            'workspace_count': len(await self.list_workspaces())
        }

    async def shutdown(self) -> None:
        """Shutdown session manager"""
        logger.info("Shutting down terminal session manager")

        # Close all tabs
        await self.tab_manager.close_all_tabs()

        # Set shutdown event
        self._shutdown_event.set()

    def _on_tab_status_change(self, tab_id: str, status: TabStatus) -> None:
        """Handle tab status change"""
        if status == TabStatus.ACTIVE:
            self.stats['active_sessions'] = max(
                self.stats['active_sessions'],
                len(self.tab_manager.tabs)
            )