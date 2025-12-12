"""
Enhanced SSH Manager
Extends SSH management with terminal session support and connection multiplexing
"""

import asyncio
import asyncssh
import logging
from typing import Dict, Optional, List, Any, AsyncIterator
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)


@dataclass
class SSHConnection:
    """SSH connection with terminal support"""
    connection_id: str
    host: str
    port: int
    username: str
    process: Optional[asyncssh.SSHClientProcess] = None
    connection: Optional[asyncssh.SSHClientConnection] = None
    created_at: float = 0
    last_used: float = 0


class EnhancedSSHManager:
    """Enhanced SSH manager with terminal session support"""

    def __init__(self):
        self.connections: Dict[str, SSHConnection] = {}
        self.connection_pools: Dict[str, List[asyncssh.SSHClientConnection]] = {}
        self.max_pool_size = 5
        self.connection_timeout = 30

    async def create_terminal_connection(self, host: str, port: int, username: str,
                                       password: str = "", key_file: str = None,
                                       term_type: str = "xterm-256color",
                                       cols: int = 80, rows: int = 24) -> SSHConnection:
        """Create SSH connection for terminal session"""
        connection_id = f"{host}:{port}:{username}:{int(time.time())}"

        try:
            # Connection options
            connect_kwargs = {
                'host': host,
                'port': port,
                'username': username,
                'connect_timeout': self.connection_timeout,
                'known_hosts': None  # Disable host key checking for development
            }

            if password:
                connect_kwargs['password'] = password
            if key_file:
                connect_kwargs['client_keys'] = [key_file]

            # Establish connection
            connection = await asyncssh.connect(**connect_kwargs)

            # Create terminal process
            process = await connection.create_process(
                term_type=term_type,
                term_size=(rows, cols)
            )

            # Create connection object
            ssh_conn = SSHConnection(
                connection_id=connection_id,
                host=host,
                port=port,
                username=username,
                process=process,
                connection=connection,
                created_at=time.time(),
                last_used=time.time()
            )

            self.connections[connection_id] = ssh_conn
            logger.info(f"Created terminal connection {connection_id} to {host}:{port}")

            return ssh_conn

        except Exception as e:
            logger.error(f"Failed to create terminal connection to {host}:{port}: {e}")
            raise

    async def get_connection_output_stream(self, connection_id: str) -> AsyncIterator[str]:
        """Get output stream from SSH connection"""
        connection = self.connections.get(connection_id)
        if not connection or not connection.process:
            raise ValueError(f"SSH connection {connection_id} not found or no process")

        try:
            # SSHClientProcess needs to be read differently
            # We'll read from stdout in a loop
            while True:
                try:
                    # Read with timeout to avoid blocking
                    data = await asyncio.wait_for(connection.process.stdout.read(1024), timeout=0.1)
                    if data:
                        yield data.decode('utf-8', errors='replace')
                        connection.last_used = time.time()
                    else:
                        # No data, small delay and continue
                        await asyncio.sleep(0.01)

                except asyncio.TimeoutError:
                    # Timeout is expected, continue loop
                    continue
                except Exception:
                    # Connection closed or other error
                    break

        except Exception as e:
            logger.error(f"Error reading from connection {connection_id}: {e}")
            # Don't raise here, just stop yielding

    async def send_connection_input(self, connection_id: str, data: str) -> bool:
        """Send input to SSH connection"""
        connection = self.connections.get(connection_id)
        if not connection or not connection.process:
            return False

        try:
            connection.process.stdin.write(data)
            # SSHWriter doesn't have flush() method, data is sent automatically
            connection.last_used = time.time()
            return True

        except Exception as e:
            logger.error(f"Error sending input to connection {connection_id}: {e}")
            return False

    async def resize_connection_terminal(self, connection_id: str, cols: int, rows: int) -> bool:
        """Resize terminal for SSH connection"""
        connection = self.connections.get(connection_id)
        if not connection or not connection.process:
            return False

        try:
            connection.process.change_term_size(rows, cols)
            return True

        except Exception as e:
            logger.error(f"Error resizing terminal for connection {connection_id}: {e}")
            return False

    async def close_connection(self, connection_id: str) -> bool:
        """Close SSH connection"""
        connection = self.connections.get(connection_id)
        if not connection:
            return False

        try:
            if connection.process:
                connection.process.terminate()
                await connection.process.wait_closed()

            if connection.connection:
                connection.connection.close()
                await connection.connection.wait_closed()

            del self.connections[connection_id]
            logger.info(f"Closed SSH connection {connection_id}")
            return True

        except Exception as e:
            logger.error(f"Error closing connection {connection_id}: {e}")
            return False

    async def get_connection_info(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Get connection information"""
        connection = self.connections.get(connection_id)
        if not connection:
            return None

        return {
            'connection_id': connection_id,
            'host': connection.host,
            'port': connection.port,
            'username': connection.username,
            'created_at': connection.created_at,
            'last_used': connection.last_used,
            'has_process': connection.process is not None,
            'is_active': connection.process and not connection.process.is_closing()
        }

    async def list_connections(self) -> List[Dict[str, Any]]:
        """List all connections"""
        connections = []
        for conn_id in self.connections:
            info = await self.get_connection_info(conn_id)
            if info:
                connections.append(info)
        return connections

    async def cleanup_idle_connections(self, max_idle_time: int = 300) -> int:
        """Clean up idle connections"""
        current_time = time.time()
        closed_count = 0

        for conn_id, connection in list(self.connections.items()):
            if current_time - connection.last_used > max_idle_time:
                await self.close_connection(conn_id)
                closed_count += 1

        if closed_count > 0:
            logger.info(f"Cleaned up {closed_count} idle connections")

        return closed_count

    async def shutdown(self) -> None:
        """Shutdown all connections"""
        logger.info(f"Shutting down {len(self.connections)} SSH connections")

        for conn_id in list(self.connections.keys()):
            await self.close_connection(conn_id)