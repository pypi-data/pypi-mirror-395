"""
Command Line Interface for WindTerm-like MCP Server
"""

import asyncio
import json
import logging
import argparse
import sys
import os
from pathlib import Path

from .mcp_server_v2 import WindTermMCPServer
from .terminal_session_manager import ServerConfig
from .config_manager import ConfigManager
from .config_validator import ConfigValidator

logger = logging.getLogger(__name__)


async def start_server():
    """Start the MCP server"""
    import sys
    import signal

    # Check if MCP server is being started correctly
    # For MCP mode, we need to check if stdin is available and not closed
    try:
        # Test if stdin is available for reading
        sys.stdin.peek(1)
        is_interactive = sys.stdin.isatty()
    except (ValueError, OSError, AttributeError):
        # stdin is closed or not available - this is MCP mode
        is_interactive = False

    if is_interactive:
        # Interactive mode - provide helpful guidance
        print("=" * 60)
        print("Linux SSH MCP Server v2.0.0")
        print("=" * 60)
        print()
        print("[OK] Server ready for MCP connections")
        print()
        print("[INFO] Usage Tips:")
        print("   * This server is designed for Claude Code or MCP clients")
        print("   * For manual SSH testing: linux-ssh-mcp test <host> <user>")
        print("   * To check your config: linux-ssh-mcp check")
        print("   * Press Ctrl+C to stop the server gracefully")
        print()
        print("[WAIT] Waiting for MCP client connection...")
        print("   (In a real scenario, Claude Code would connect automatically)")
        print("-" * 60)
        print()

    # Set up graceful shutdown
    shutdown_event = asyncio.Event()

    def signal_handler(signum, frame):
        try:
            print("\n\n[STOP] Shutdown signal received. Closing server gracefully...")
        except (ValueError, OSError):
            # Handle case where stdout is already closed
            pass
        shutdown_event.set()

    if is_interactive:
        signal.signal(signal.SIGINT, signal_handler)
        # Windows doesn't have SIGTERM
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)

    try:
        server = WindTermMCPServer()

        # Start server with timeout or shutdown event
        if is_interactive:
            # In interactive mode, run with graceful shutdown handling
            server_task = asyncio.create_task(server.run())
            shutdown_task = asyncio.create_task(shutdown_event.wait())

            done, pending = await asyncio.wait(
                [server_task, shutdown_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            if shutdown_event.is_set():
                try:
                    print("[OK] Server stopped gracefully")
                except (ValueError, OSError):
                    pass  # stdout might be closed
            else:
                # In non-interactive mode (MCP client), run normally
                await server.run()

    except asyncio.CancelledError:
        if is_interactive:
            try:
                print("\n[OK] Server cancelled and stopped")
            except (ValueError, OSError):
                pass
    except KeyboardInterrupt:
        if is_interactive:
            try:
                print("\n[OK] Server stopped by user")
            except (ValueError, OSError):
                pass
    except Exception as e:
        if is_interactive:
            try:
                print(f"\n[ERROR] Server error: {e}")
            except (ValueError, OSError):
                pass
        raise


async def create_sample_config():
    """Create sample configuration file"""
    config_dir = Path.home() / ".ssh-mcp"
    config_dir.mkdir(parents=True, exist_ok=True)

    servers_file = config_dir / "servers.json"

    sample_config = {
        "version": "2.0",
        "servers": {
            "localhost": {
                "id": "localhost",
                "host": "localhost",
                "port": 22,
                "username": "user",
                "password": "",
                "description": "Local development server"
            },
            "web-server": {
                "id": "web-server",
                "host": "192.168.1.100",
                "port": 22,
                "username": "admin",
                "password": "",
                "description": "Web server"
            }
        },
        "settings": {
            "default_terminal_size": {
                "cols": 80,
                "rows": 24
            },
            "auto_save_interval": 300,
            "max_history": 1000
        }
    }

    with open(servers_file, 'w') as f:
        json.dump(sample_config, f, indent=2)

    print(f"Sample configuration created at: {servers_file}")
    print("Please edit the file with your actual server details and passwords.")


async def test_terminal(host: str, username: str, password: str = "", port: int = 22):
    """Test terminal connection to a server"""
    from .terminal_session_manager import TerminalSessionManager

    manager = TerminalSessionManager()

    try:
        # Create server config
        server_config = ServerConfig(
            id="test",
            host=host,
            port=port,
            username=username,
            password=password
        )

        # Create and start session
        tab = await manager.create_tab(server_config, "Test Terminal")

        print(f"[OK] Terminal session created: {tab.tab_id}")
        print(f"[OK] Connected to {host}:{port}")
        print(f"[INFO] Terminal size: {tab.state.terminal_size.cols}x{tab.state.terminal_size.rows}")

        # Send a test command
        await tab.send_input("echo 'Hello from WindTerm-like MCP!'\n")

        # Wait a moment for output
        await asyncio.sleep(1)

        # Get output
        output_lines = await tab.get_output_since_last()
        if output_lines:
            print("[OK] Received output:")
            for line in output_lines[-5:]:  # Last 5 lines
                print(f"  {line.strip()}")

        # Close session
        await tab.close()
        print("[OK] Test completed successfully")

    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

    finally:
        await manager.shutdown()

    return True


def check_config():
    """Check configuration and show available servers"""
    import json
    from pathlib import Path

    config_paths = [
        Path.home() / ".ssh-mcp" / "servers.json",
        Path(os.environ.get('APPDATA', '')) / "ssh-mcp" / "servers.json" if os.name == 'nt' else Path.home() / ".config" / "ssh-mcp" / "servers.json",
        Path.cwd() / "servers.json",
        Path(__file__).parent / "servers.json"
    ]

    config_file = None
    for path in config_paths:
        if path.exists():
            config_file = path
            break

    if config_file:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)

            servers = config.get('servers', {})
            print(f"Configuration file: {config_file}")
            print(f"Found {len(servers)} configured server(s):")

            for server_id, server_info in servers.items():
                host = server_info.get('host', 'N/A')
                port = server_info.get('port', 22)
                username = server_info.get('username', 'N/A')
                has_password = bool(server_info.get('password', ''))

                print(f"  - {server_id}: {username}@{host}:{port} {'(password set)' if has_password else '(no password)'}")

                # Show test command
                print(f"    Test: linux-ssh-mcp test {host} {username}" + (f" --password [password]" if has_password else ""))

            return len(servers) > 0

        except Exception as e:
            print(f"Error reading configuration file: {e}")

    print("No configuration file found.")
    print("Run 'linux-ssh-mcp init' to create one.")
    return False


async def check_configuration_status(test_connections: bool = False):
    """Enhanced configuration status check"""
    try:
        config_manager = ConfigManager()
        config_status = await config_manager.get_config_status(test_connections)

        if not config_status.config_found:
            print("[ERROR] No configuration file found")
            print()
            print("[MEMO] Suggestions:")
            for suggestion in config_status.suggestions:
                print(f"   - {suggestion}")
            print()
            print("[INFO] Quick start:")
            print("   linux-ssh-mcp init --interactive")
            return False

        print(f"[OK] Configuration file found: {config_status.config_file}")
        print(f"[SCORE] Health Score: {config_status.health_score}/100")
        print()

        # Show servers
        if config_status.servers:
            print(f"[TOOLS]  Configured Servers ({config_status.servers_count}):")
            for server in config_status.servers:
                status_icon = "[OK]" if server.connection_status == "reachable" else "[ERROR]" if server.connection_status == "unreachable" else "[UNKNOWN]"
                auth_method = "[KEY]" if server.has_key_file else "[PWD]" if server.has_password else "[UNKNOWN]"
                print(f"   {status_icon} {auth_method} {server.id}: {server.username}@{server.host}:{server.port}")
                if server.description:
                    print(f"      [MEMO] {server.description}")
                if test_connections and server.connection_status != "unknown":
                    print(f"      [STATUS] Connection: {server.connection_status}")
                if server.last_connected:
                    print(f"      [TIME] Last connected: {server.last_connected[:19]}")
        else:
            print("[ERROR] No servers configured")
            print("   Add servers with: linux-ssh-mcp config add-server")

        # Show configuration summary
        print(f"\n[INFO] Configuration Summary:")
        print(f"   - Server Groups: {config_status.groups_count}")
        print(f"   - Scripts: {config_status.scripts_count}")
        print(f"   - Workspaces: {config_status.workspaces_count}")

        # Show suggestions
        if config_status.suggestions:
            print(f"\n[INFO] Suggestions:")
            for suggestion in config_status.suggestions:
                print(f"   - {suggestion}")

        # Show validation errors
        if config_status.validation_errors:
            print(f"\n[WARNING]  Validation Issues:")
            for error in config_status.validation_errors:
                print(f"   - {error}")

        return True

    except Exception as e:
        print(f"[ERROR] Error checking configuration: {e}")
        return False


async def interactive_init():
    """Interactive configuration setup"""
    try:
        config_manager = ConfigManager()

        # Check if config already exists
        existing_config = config_manager.find_config_file()
        if existing_config:
            print(f"[WARNING]  Configuration already exists at: {existing_config}")
            response = input("Do you want to overwrite it? (y/N): ").strip().lower()
            if response != 'y':
                print("[OK] Keeping existing configuration")
                return

        print("\n📋 Let's configure your SSH servers step by step")
        print("=" * 50)

        servers = {}
        server_count = 0

        while True:
            server_count += 1
            print(f"\n[TOOLS]  Server #{server_count}")
            print("-" * 30)

            # Server details
            server_id = input(f"Server name (server-{server_count}): ").strip() or f"server-{server_count}"

            host = input("Hostname or IP address: ").strip()
            if not host:
                print("[ERROR] Hostname is required")
                server_count -= 1
                continue

            username = input("SSH username: ").strip()
            if not username:
                print("[ERROR] Username is required")
                server_count -= 1
                continue

            port = input("SSH port (22): ").strip() or "22"
            try:
                port = int(port)
                if port < 1 or port > 65535:
                    print("[ERROR] Invalid port number")
                    server_count -= 1
                    continue
            except ValueError:
                print("[ERROR] Port must be a number")
                server_count -= 1
                continue

            description = input("Description (optional): ").strip()

            # Authentication method
            print("\n🔐 Authentication method:")
            print("1) Password authentication")
            print("2) SSH key authentication")

            auth_choice = input("Choose (1 or 2) [1]: ").strip() or "1"

            password = ""
            key_file = ""

            if auth_choice == "1":
                password = input("Password: ").strip()
            else:
                key_file = input("SSH key file path [~/.ssh/id_rsa]: ").strip() or "~/.ssh/id_rsa"

            # Store server config
            servers[server_id] = {
                "id": server_id,
                "host": host,
                "port": port,
                "username": username,
                "description": description,
                "timeout": 30
            }

            if password:
                servers[server_id]["password"] = password
            if key_file:
                servers[server_id]["key_file"] = key_file

            # Continue adding servers?
            another = input("\nAdd another server? (y/N): ").strip().lower()
            if another != 'y':
                break

        # Create configuration
        config = {
            "version": "2.0",
            "description": "Linux SSH MCP Configuration",
            "created": "linux-ssh-mcp init --interactive",
            "servers": servers,
            "groups": {},
            "scripts": {
                "system-info": {
                    "description": "Get system information",
                    "commands": ["uname -a", "df -h", "free -m", "uptime"]
                }
            },
            "settings": {
                "connection_pool_size": 10,
                "default_timeout": 30,
                "keep_alive_interval": 60
            }
        }

        # Save configuration
        config_dir = Path.home() / ".ssh-mcp"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "servers.json"

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print(f"\n[OK] Configuration saved to: {config_file}")
        print(f"[TOOLS]  Configured {len(servers)} server(s)")

        # Test connections if requested
        test_connections = input("\n🧪 Test connections to servers? (y/N): ").strip().lower()
        if test_connections == 'y':
            print("\n🔄 Testing connections...")
            await check_configuration_status(test_connections=True)

        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Test a specific server: linux-ssh-mcp test <host> <username>")
        print("2. Start MCP server: linux-ssh-mcp server")
        print("3. Use with Claude Code")

    except KeyboardInterrupt:
        print("\n\n[STOP] Setup cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] Error during setup: {e}")


async def import_ssh_config():
    """Import from existing SSH configuration"""
    try:
        known_hosts_file = Path.home() / ".ssh" / "known_hosts"
        config_file = Path.home() / ".ssh" / "config"

        servers = {}

        # Read known_hosts
        if known_hosts_file.exists():
            print(f"📖 Reading from {known_hosts_file}")
            with open(known_hosts_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse known_hosts line
                        try:
                            # Split hostname and key
                            parts = line.split()
                            if len(parts) >= 2:
                                hostname = parts[0]
                                # Remove brackets for IPv6 addresses
                                hostname = hostname.strip('[]')
                                servers[f"imported-{hostname}"] = {
                                    "id": f"imported-{hostname}",
                                    "host": hostname,
                                    "port": 22,
                                    "username": "user",  # Default username
                                    "description": f"Imported from known_hosts (line {line_num})",
                                    "timeout": 30
                                }
                        except Exception as e:
                            logger.debug(f"Failed to parse known_hosts line {line_num}: {e}")

        # Read SSH config for more details
        if config_file.exists():
            print(f"📖 Reading from {config_file}")
            with open(config_file, 'r') as f:
                current_host = None
                for line in f:
                    line = line.strip()
                    if line.startswith('Host '):
                        # Extract hostname
                        host_name = line[5:].strip()
                        current_host = host_name

                        # Check if we have this host in servers
                        server_id = f"imported-{host_name}"
                        if server_id not in servers:
                            servers[server_id] = {
                                "id": server_id,
                                "host": host_name,
                                "port": 22,
                                "username": "user",
                                "description": f"Imported from SSH config",
                                "timeout": 30
                            }
                        else:
                            servers[server_id]["description"] = f"Imported from SSH config"

                    elif current_host and line.startswith('    '):
                        # Parse host configuration
                        line = line.strip()
                        if line.startswith('User '):
                            username = line[5:].strip()
                            server_id = f"imported-{current_host}"
                            if server_id in servers:
                                servers[server_id]["username"] = username
                        elif line.startswith('Port '):
                            port = line[5:].strip()
                            try:
                                port = int(port)
                                server_id = f"imported-{current_host}"
                                if server_id in servers:
                                    servers[server_id]["port"] = port
                            except ValueError:
                                pass
                        elif line.startswith('HostName '):
                            hostname = line[9:].strip()
                            server_id = f"imported-{current_host}"
                            if server_id in servers:
                                servers[server_id]["host"] = hostname

        if not servers:
            print("[ERROR] No SSH configuration found to import")
            return

        # Create configuration
        config = {
            "version": "2.0",
            "description": "Linux SSH MCP Configuration - Imported from SSH",
            "created": "linux-ssh-mcp init --import-ssh",
            "servers": servers,
            "groups": {},
            "scripts": {
                "system-info": {
                    "description": "Get system information",
                    "commands": ["uname -a", "df -h", "free -m", "uptime"]
                }
            },
            "settings": {
                "connection_pool_size": 10,
                "default_timeout": 30,
                "keep_alive_interval": 60
            }
        }

        # Save configuration
        config_dir = Path.home() / ".ssh-mcp"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "servers.json"

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print(f"[OK] Imported {len(servers)} server(s) to configuration")
        print(f"💾 Configuration saved to: {config_file}")
        print("\n[WARNING]  Note: You may need to update usernames and add authentication details")
        print("   Edit the configuration file to add passwords or SSH key paths")

    except Exception as e:
        print(f"[ERROR] Error importing SSH configuration: {e}")


async def handle_config_command(args):
    """Handle config subcommand"""
    try:
        config_manager = ConfigManager()

        if args.list:
            await list_servers(args.group, args.test_connections)
        elif args.add_server:
            await add_server_interactive()
        elif args.validate:
            await validate_config_file()
        else:
            print("🔧 Configuration Management")
            print("=" * 40)
            print("Available options:")
            print("  --list             List configured servers")
            print("  --add-server       Add new server configuration")
            print("  --validate         Validate configuration file")
            print("  --test-connections  Test server connections")
            print("  --group <name>      Filter servers by group")
            print()
            print("Examples:")
            print("  linux-ssh-mcp config --list")
            print("  linux-ssh-mcp config --list --group production")
            print("  linux-ssh-mcp config --validate --test-connections")
            print("  linux-ssh-mcp config --add-server")

    except Exception as e:
        print(f"[ERROR] Error handling config command: {e}")


async def list_servers(group_filter: Optional[str] = None, test_connections: bool = False):
    """List configured servers"""
    try:
        config_manager = ConfigManager()
        servers = await config_manager.discover_servers(group_filter)

        if not servers:
            print("[ERROR] No configured servers found")
            print("   Add servers with: linux-ssh-mcp config add-server")
            return

        print(f"[TOOLS]  Configured Servers")
        if group_filter:
            print(f"   Group: {group_filter}")
        print("=" * 40)

        for server in servers:
            status_icon = "[OK]" if server.connection_status == "reachable" else "[ERROR]" if server.connection_status == "unreachable" else "[UNKNOWN]"
            auth_method = "[KEY]" if server.has_key_file else "[PWD]" if server.has_password else "[UNKNOWN]"

            print(f"{status_icon} {auth_method} {server.id}")
            print(f"   [HOST] {server.username}@{server.host}:{server.port}")

            if server.description:
                print(f"   [MEMO] {server.description}")

            if server.tags:
                print(f"   [TAGS] {', '.join(server.tags)}")

            if test_connections and server.connection_status != "unknown":
                print(f"   [STATUS] Connection: {server.connection_status}")

            print()

    except Exception as e:
        print(f"[ERROR] Error listing servers: {e}")


async def add_server_interactive():
    """Interactive server addition"""
    try:
        print("➕ Add New Server Configuration")
        print("=" * 35)

        # Server details
        server_id = input("Server ID: ").strip()
        if not server_id:
            print("[ERROR] Server ID is required")
            return

        host = input("Hostname or IP address: ").strip()
        if not host:
            print("[ERROR] Hostname is required")
            return

        username = input("SSH username: ").strip()
        if not username:
            print("[ERROR] Username is required")
            return

        port = input("SSH port (22): ").strip() or "22"
        try:
            port = int(port)
            if port < 1 or port > 65535:
                print("[ERROR] Invalid port number")
                return
        except ValueError:
            print("[ERROR] Port must be a number")
            return

        description = input("Description (optional): ").strip()

        # Authentication
        print("\n🔐 Authentication method:")
        print("1) Password")
        print("2) SSH key")

        auth_choice = input("Choose (1 or 2) [2]: ").strip() or "2"

        password = ""
        key_file = ""

        if auth_choice == "1":
            password = input("Password: ").strip()
        else:
            key_file = input("SSH key file path [~/.ssh/id_rsa]: ").strip() or "~/.ssh/id_rsa"

        # Load existing config
        config_manager = ConfigManager()
        config = await config_manager.load_configuration()

        if not config:
            print("[ERROR] No existing configuration found")
            print("   Run 'linux-ssh-mcp init' first")
            return

        # Add server to config
        if "servers" not in config:
            config["servers"] = {}

        config["servers"][server_id] = {
            "id": server_id,
            "host": host,
            "port": port,
            "username": username,
            "description": description,
            "timeout": 30
        }

        if password:
            config["servers"][server_id]["password"] = password
        if key_file:
            config["servers"][server_id]["key_file"] = key_file

        # Save configuration
        config_file = config_manager.find_config_file()
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print(f"\n[OK] Server '{server_id}' added successfully")
        print(f"   Host: {host}:{port}")
        print(f"   User: {username}")

    except KeyboardInterrupt:
        print("\n[STOP] Server addition cancelled")
    except Exception as e:
        print(f"\n[ERROR] Error adding server: {e}")


async def validate_config_file():
    """Validate configuration file"""
    try:
        config_manager = ConfigManager()
        config = await config_manager.load_configuration()

        if not config:
            print("[ERROR] No configuration file found")
            return

        config_validator = ConfigValidator()
        validation_result = await config_validator.validate_configuration(config)

        print("🔍 Configuration Validation")
        print("=" * 35)

        if validation_result.valid:
            print("[OK] Configuration is valid")
        else:
            print("[ERROR] Configuration has issues")

        print(f"\n[INFO] Scores:")
        print(f"   Security: {validation_result.security_score}/100")
        print(f"   Best Practices: {validation_result.best_practices_score}/100")

        if validation_result.issues:
            print(f"\n[WARNING]  Issues ({len(validation_result.issues)}):")
            for issue in validation_result.issues:
                icon = "[ERROR]" if issue.severity == "error" else "[WARNING]" if issue.severity == "warning" else "[INFO]"
                print(f"   {icon} {issue.field}: {issue.message}")
                if issue.suggestion:
                    print(f"      [INFO] {issue.suggestion}")

        if validation_result.suggestions:
            print(f"\n[INFO] Suggestions:")
            for suggestion in validation_result.suggestions:
                print(f"   - {suggestion}")

    except Exception as e:
        print(f"[ERROR] Error validating configuration: {e}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="WindTerm-like Linux SSH MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s server                    # Start MCP server (for Claude Code)
  %(prog)s check                     # Check configuration and show available servers
  %(prog)s init                      # Create sample configuration
  %(prog)s test localhost user       # Test terminal connection
  %(prog)s test 192.168.1.100 admin --password secret

Common Usage:
  1. Run '%(prog)s init' to create configuration
  2. Edit the configuration file with your server details
  3. Run '%(prog)s check' to verify your setup
  4. Use with Claude Code or run '%(prog)s server' for manual testing
        """
    )

    parser.add_argument(
        "command",
        choices=["server", "init", "test", "check", "config"],
        help="Command to execute"
    )

    parser.add_argument(
        "host",
        nargs="?",
        help="Server hostname for test command"
    )

    parser.add_argument(
        "username",
        nargs="?",
        help="Username for test command"
    )

    parser.add_argument(
        "--password",
        help="Password for test command"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=22,
        help="SSH port for test command (default: 22)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    # Configuration subcommand arguments
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive configuration setup (for init command)"
    )

    parser.add_argument(
        "--import-ssh",
        action="store_true",
        help="Import from existing SSH configuration (for init command)"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration file"
    )

    parser.add_argument(
        "--test-connections",
        action="store_true",
        help="Test server connections"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List configured servers (for config command)"
    )

    parser.add_argument(
        "--add-server",
        action="store_true",
        help="Add new server configuration (for config command)"
    )

    parser.add_argument(
        "--group",
        help="Filter servers by group (for config --list)"
    )

    args = parser.parse_args()

    # Setup logging - reduce noise in interactive mode
    if args.command == "server" and sys.stdin.isatty():
        # In interactive server mode, suppress almost all logs
        log_level = logging.CRITICAL if not args.debug else logging.DEBUG
        # Also suppress mcp.server logs specifically
        logging.getLogger('mcp.server').setLevel(logging.CRITICAL)
        logging.getLogger('mcp.server.lowlevel.server').setLevel(logging.CRITICAL)
    else:
        # Normal logging for other commands
        log_level = logging.DEBUG if args.debug else logging.INFO

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Execute command
    if args.command == "server":
        asyncio.run(start_server())

    elif args.command == "init":
        if args.interactive:
            print("🔍 Interactive Configuration Setup")
            print("=" * 50)
            asyncio.run(interactive_init())
        elif args.import_ssh:
            print("📥 Importing from SSH configuration...")
            asyncio.run(import_ssh_config())
        else:
            print("Creating sample configuration...")
            asyncio.run(create_sample_config())

    elif args.command == "check":
        print("Checking SSH MCP configuration...")
        print()
        asyncio.run(check_configuration_status(args.test_connections))

    elif args.command == "test":
        if not args.host or not args.username:
            parser.error("test command requires host and username arguments")

        print(f"Testing terminal connection to {args.host}:{args.port}...")
        success = asyncio.run(test_terminal(
            host=args.host,
            username=args.username,
            password=args.password or "",
            port=args.port
        ))

        if not success:
            sys.exit(1)

    elif args.command == "config":
        asyncio.run(handle_config_command(args))

    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()