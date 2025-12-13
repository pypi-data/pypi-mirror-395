"""
Configuration Manager for Linux SSH MCP
Provides configuration discovery, validation, and management capabilities
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ServerInfo:
    """Server information data class"""
    id: str
    host: str
    port: int
    username: str
    description: Optional[str] = None
    has_password: bool = False
    has_key_file: bool = False
    key_file: Optional[str] = None
    timeout: int = 30
    connection_status: str = "unknown"  # unknown, reachable, unreachable, error
    last_connected: Optional[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class ConfigStatus:
    """Configuration status data class"""
    config_found: bool
    config_file: Optional[str] = None
    config_valid: bool = False
    servers_count: int = 0
    servers: List[ServerInfo] = None
    groups_count: int = 0
    scripts_count: int = 0
    workspaces_count: int = 0
    last_validated: Optional[str] = None
    validation_errors: List[str] = None
    health_score: int = 0
    suggestions: List[str] = None

    def __post_init__(self):
        if self.servers is None:
            self.servers = []
        if self.validation_errors is None:
            self.validation_errors = []
        if self.suggestions is None:
            self.suggestions = []


class ConfigManager:
    """Configuration discovery and validation manager"""

    def __init__(self):
        """Initialize configuration manager"""
        self.config_paths = self._get_config_paths()
        self._config_cache = {}
        self._last_check_time = None

    def _get_config_paths(self) -> List[Path]:
        """Get configuration file search paths"""
        paths = [
            # Environment variable override
            Path(os.environ.get('SSH_MCP_CONFIG_PATH', '')) if os.environ.get('SSH_MCP_CONFIG_PATH') else None,

            # User home directory
            Path.home() / ".ssh-mcp" / "servers.json",

            # Platform-specific config directories
            Path(os.environ.get('APPDATA', '')) / "ssh-mcp" / "servers.json" if os.name == 'nt'
            else Path.home() / ".config" / "ssh-mcp" / "servers.json",

            # Current working directory
            Path.cwd() / "servers.json",

            # Project root directory
            Path(__file__).parent.parent.parent / "servers.json"
        ]

        # Filter out None values and ensure paths are absolute
        return [Path(p).resolve() for p in paths if p]

    def find_config_file(self) -> Optional[Path]:
        """Find configuration file in standard locations"""
        for path in self.config_paths:
            if path.exists() and path.is_file():
                logger.debug(f"Found configuration file: {path}")
                return path
        return None

    async def load_configuration(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load and parse configuration file"""
        try:
            if config_path:
                path = Path(config_path)
            else:
                path = self.find_config_file()

            if not path or not path.exists():
                return {}

            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            logger.debug(f"Loaded configuration from {path}")
            return config

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file {path}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading configuration from {path}: {e}")
            return {}

    async def get_config_status(self, validate_connections: bool = False) -> ConfigStatus:
        """Get comprehensive configuration status"""
        try:
            config_file = self.find_config_file()

            if not config_file:
                return ConfigStatus(
                    config_found=False,
                    suggestions=[
                        "Run 'linux-ssh-mcp init' to create a configuration file",
                        "Run 'linux-ssh-mcp init --interactive' for guided setup"
                    ]
                )

            # Load configuration
            config = await self.load_configuration(str(config_file))

            if not config:
                return ConfigStatus(
                    config_found=True,
                    config_file=str(config_file),
                    config_valid=False,
                    validation_errors=["Configuration file is empty or invalid"],
                    suggestions=[
                        "Check configuration file format",
                        "Run 'linux-ssh-mcp validate' to fix issues"
                    ]
                )

            # Extract server information
            servers = []
            servers_config = config.get('servers', {})

            for server_id, server_config in servers_config.items():
                server_info = ServerInfo(
                    id=server_id,
                    host=server_config.get('host', ''),
                    port=server_config.get('port', 22),
                    username=server_config.get('username', ''),
                    description=server_config.get('description'),
                    has_password=bool(server_config.get('password', '')),
                    has_key_file=bool(server_config.get('key_file')),
                    key_file=server_config.get('key_file'),
                    timeout=server_config.get('timeout', 30),
                    tags=server_config.get('tags', [])
                )

                # Test connection if requested
                if validate_connections:
                    server_info.connection_status = await self._test_server_connection(server_info)
                    server_info.last_connected = datetime.now().isoformat()

                servers.append(server_info)

            # Calculate health score
            health_score = self._calculate_health_score(config, servers)

            # Generate suggestions
            suggestions = self._generate_suggestions(config, servers)

            return ConfigStatus(
                config_found=True,
                config_file=str(config_file),
                config_valid=True,
                servers_count=len(servers),
                servers=servers,
                groups_count=len(config.get('groups', {})),
                scripts_count=len(config.get('scripts', {})),
                workspaces_count=len(config.get('workspaces', {})),
                last_validated=datetime.now().isoformat(),
                health_score=health_score,
                suggestions=suggestions
            )

        except Exception as e:
            logger.error(f"Error getting configuration status: {e}")
            return ConfigStatus(
                config_found=False,
                validation_errors=[str(e)],
                suggestions=[
                    "Check system logs for detailed error information",
                    "Verify configuration file permissions"
                ]
            )

    async def discover_servers(self, group_filter: Optional[str] = None) -> List[ServerInfo]:
        """Discover configured servers"""
        config_status = await self.get_config_status()

        if not config_status.config_found or not config_status.servers:
            return []

        servers = config_status.servers

        # Apply group filter if specified
        if group_filter:
            config = await self.load_configuration()
            groups = config.get('groups', {})

            if group_filter in groups:
                group_config = groups[group_filter]
                allowed_server_ids = set(group_config.get('servers', []))
                servers = [s for s in servers if s.id in allowed_server_ids]
            else:
                servers = []

        return servers

    async def validate_configuration(self, detailed_report: bool = False) -> Dict[str, Any]:
        """Validate configuration file integrity"""
        config_status = await self.get_config_status(validate_connections=True)

        validation_result = {
            "valid": config_status.config_valid,
            "config_file": config_status.config_file,
            "servers": {
                "total": config_status.servers_count,
                "reachable": len([s for s in config_status.servers if s.connection_status == "reachable"]),
                "unreachable": len([s for s in config_status.servers if s.connection_status == "unreachable"]),
                "unknown": len([s for s in config_status.servers if s.connection_status == "unknown"])
            },
            "issues": config_status.validation_errors,
            "suggestions": config_status.suggestions,
            "health_score": config_status.health_score
        }

        if detailed_report:
            validation_result["server_details"] = [asdict(server) for server in config_status.servers]
            validation_result["validation_timestamp"] = datetime.now().isoformat()

        return validation_result

    async def _test_server_connection(self, server_info: ServerInfo) -> str:
        """Test connection to a server"""
        try:
            # Import here to avoid circular imports
            from .simple_terminal_manager import SimpleTerminalSessionManager

            # Create a temporary manager for testing
            manager = SimpleTerminalSessionManager()

            # Create server config for testing
            from .simple_terminal_manager import ServerConfig
            server_config = ServerConfig(
                id="test",
                host=server_info.host,
                port=server_info.port,
                username=server_info.username,
                password="",  # We'll test with key if available
                key_file=server_info.key_file
            )

            # Quick connection test
            try:
                # This is a simplified test - in a real implementation,
                # you might want to use a more robust connection testing method
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((server_info.host, server_info.port))
                sock.close()

                if result == 0:
                    return "reachable"
                else:
                    return "unreachable"

            except Exception as e:
                logger.debug(f"Connection test failed for {server_info.host}: {e}")
                return "unreachable"

        except Exception as e:
            logger.error(f"Error testing server connection: {e}")
            return "error"

    def _calculate_health_score(self, config: Dict[str, Any], servers: List[ServerInfo]) -> int:
        """Calculate configuration health score (0-100)"""
        score = 0

        # Base score for having a valid config
        if config:
            score += 20

        # Score for servers
        if servers:
            score += min(30, len(servers) * 5)  # Up to 30 points for servers

            # Score for server connectivity
            reachable_servers = len([s for s in servers if s.connection_status == "reachable"])
            if servers:
                score += int((reachable_servers / len(servers)) * 30)  # Up to 30 points

        # Score for security best practices
        key_auth_servers = len([s for s in servers if s.has_key_file])
        if servers:
            score += int((key_auth_servers / len(servers)) * 20)  # Up to 20 points

        return min(100, score)

    def _generate_suggestions(self, config: Dict[str, Any], servers: List[ServerInfo]) -> List[str]:
        """Generate configuration improvement suggestions"""
        suggestions = []

        if not servers:
            suggestions.append("Add servers to your configuration using 'linux-ssh-mcp config add-server'")
            return suggestions

        # Security suggestions
        password_auth_servers = [s for s in servers if s.has_password and not s.has_key_file]
        if password_auth_servers:
            suggestions.append(f"Consider using SSH key authentication for {len(password_auth_servers)} server(s) using password auth")

        # Connectivity suggestions
        unreachable_servers = [s for s in servers if s.connection_status == "unreachable"]
        if unreachable_servers:
            suggestions.append(f"Check network connectivity for {len(unreachable_servers)} unreachable server(s)")

        # Configuration suggestions
        if not config.get('groups'):
            suggestions.append("Consider organizing servers into groups for easier management")

        if not config.get('scripts'):
            suggestions.append("Add common command scripts to automate repetitive tasks")

        # Description suggestions
        servers_without_desc = [s for s in servers if not s.description]
        if servers_without_desc:
            suggestions.append(f"Add descriptions for {len(servers_without_desc)} server(s) for better organization")

        return suggestions