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

        print(f"[+] Terminal session created: {tab.tab_id}")
        print(f"[+] Connected to {host}:{port}")
        print(f"[+] Terminal size: {tab.state.terminal_size.cols}x{tab.state.terminal_size.rows}")

        # Send a test command
        await tab.send_input("echo 'Hello from WindTerm-like MCP!'\n")

        # Wait a moment for output
        await asyncio.sleep(1)

        # Get output
        output_lines = await tab.get_output_since_last()
        if output_lines:
            print("[+] Received output:")
            for line in output_lines[-5:]:  # Last 5 lines
                print(f"  {line.strip()}")

        # Close session
        await tab.close()
        print("[+] Test completed successfully")

    except Exception as e:
        print(f"[-] Test failed: {e}")
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
        choices=["server", "init", "test", "check"],
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
        print("Creating sample configuration...")
        asyncio.run(create_sample_config())

    elif args.command == "check":
        print("Checking SSH MCP configuration...")
        print()
        has_config = check_config()
        if has_config:
            print()
            print("Configuration looks good! You can:")
            print("1. Test a connection: linux-ssh-mcp test <host> <username>")
            print("2. Start MCP server: linux-ssh-mcp server")
            print("3. Use with Claude Code (automatic)")
        else:
            print()
            print("Please run 'linux-ssh-mcp init' to create a configuration file first.")

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

    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()