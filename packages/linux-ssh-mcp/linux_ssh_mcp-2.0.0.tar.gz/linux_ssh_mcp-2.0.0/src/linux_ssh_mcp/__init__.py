"""
Linux SSH MCP - WindTerm-like Terminal Emulator
A powerful Linux server management system with WindTerm-like terminal emulation
through Model Context Protocol (MCP).
"""

__version__ = "2.0.0"
__author__ = "xiapan"
__email__ = "1019693995@qq.com"

from .terminal_session_manager import TerminalSessionManager
from .terminal_emulator import PTYManager, TerminalProtocolHandler
from .ssh_manager_v2 import EnhancedSSHManager
from .scripting_engine import ScriptingEngine
from .simple_terminal_manager import SimpleTerminalSessionManager, SimpleTabSession, ServerConfig, TabStatus

__all__ = [
    "TerminalSessionManager",
    "PTYManager",
    "TerminalProtocolHandler",
    "EnhancedSSHManager",
    "ScriptingEngine",
    "SimpleTerminalSessionManager",
    "SimpleTabSession",
    "ServerConfig",
    "TabStatus",
]