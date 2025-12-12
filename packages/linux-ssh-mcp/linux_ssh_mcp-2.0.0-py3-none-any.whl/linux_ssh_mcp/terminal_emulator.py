"""
Terminal Emulation Core
Provides PTY management, terminal protocol handling, and real-time streaming
for WindTerm-like terminal experience.
"""

import asyncio
import os
import platform
from typing import Optional, AsyncIterator, Tuple, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import logging
import selectors
import threading
from io import BytesIO

# Platform-specific imports
IS_WINDOWS = platform.system() == 'Windows'

if not IS_WINDOWS:
    import pty
    import tty
    import termios
    import fcntl
    import struct
    import signal
else:
    # Windows doesn't have pty/tty/termios, we'll use alternative approaches
    import subprocess
    import win32con
    import win32console
    import win32api
    import win32pipe
    import win32file


logger = logging.getLogger(__name__)


class TerminalState(Enum):
    """Terminal session states"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PAUSED = "paused"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class TerminalSize:
    """Terminal size configuration"""
    cols: int = 80
    rows: int = 24

    def to_tuple(self) -> Tuple[int, int]:
        return (self.rows, self.cols)


@dataclass
class PTYSession:
    """PTY session data"""
    session_id: str
    master_fd: int
    slave_fd: int
    pid: int
    size: TerminalSize
    state: TerminalState
    created_at: float
    buffer: BytesIO

    def __post_init__(self):
        if self.buffer is None:
            self.buffer = BytesIO()


class PTYManager:
    """Manages pseudo-terminal creation and lifecycle"""

    def __init__(self):
        self.active_sessions: Dict[str, PTYSession] = {}
        self._loop = asyncio.get_event_loop()

    async def create_pty(self, session_id: str, size: TerminalSize = None) -> PTYSession:
        """Create a new pseudo-terminal session"""
        if size is None:
            size = TerminalSize()

        logger.info(f"Creating PTY session {session_id} with size {size.cols}x{size.rows}")

        if IS_WINDOWS:
            return await self._create_windows_pty(session_id, size)
        else:
            return await self._create_unix_pty(session_id, size)

    async def _create_unix_pty(self, session_id: str, size: TerminalSize) -> PTYSession:
        """Create PTY on Unix-like systems"""
        try:
            # Create pseudoterminal
            master_fd, slave_fd = pty.openpty()

            # Set terminal size
            self._set_terminal_size(master_fd, size)

            # Set raw mode on slave
            tty.setraw(slave_fd)

            # Create session object
            session = PTYSession(
                session_id=session_id,
                master_fd=master_fd,
                slave_fd=slave_fd,
                pid=os.getpid(),
                size=size,
                state=TerminalState.INITIALIZING,
                created_at=asyncio.get_event_loop().time(),
                buffer=BytesIO()
            )

            # Add to active sessions
            self.active_sessions[session_id] = session
            session.state = TerminalState.ACTIVE

            logger.info(f"Unix PTY session {session_id} created successfully")
            return session

        except Exception as e:
            logger.error(f"Failed to create Unix PTY session {session_id}: {e}")
            # Cleanup on failure
            if 'master_fd' in locals():
                os.close(master_fd)
            if 'slave_fd' in locals():
                os.close(slave_fd)
            raise

    async def _create_windows_pty(self, session_id: str, size: TerminalSize) -> PTYSession:
        """Create PTY-like session on Windows"""
        try:
            # On Windows, we simulate PTY using subprocess with pseudo-console
            # This is a simplified implementation

            # Create a subprocess that will act as our terminal
            process = subprocess.Popen(
                ['cmd.exe'],  # Or could use powershell.exe
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=False,
                bufsize=0,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            # Create session object with Windows-specific file descriptors
            session = PTYSession(
                session_id=session_id,
                master_fd=process.stdin.fileno(),
                slave_fd=process.stdout.fileno(),
                pid=process.pid,
                size=size,
                state=TerminalState.INITIALIZING,
                created_at=asyncio.get_event_loop().time(),
                buffer=BytesIO()
            )

            # Store the process for Windows-specific operations
            session._windows_process = process

            # Add to active sessions
            self.active_sessions[session_id] = session
            session.state = TerminalState.ACTIVE

            logger.info(f"Windows PTY session {session_id} created successfully")
            return session

        except Exception as e:
            logger.error(f"Failed to create Windows PTY session {session_id}: {e}")
            raise

    async def resize_pty(self, session_id: str, size: TerminalSize) -> bool:
        """Resize PTY session"""
        session = self.active_sessions.get(session_id)
        if not session:
            logger.warning(f"PTY session {session_id} not found for resizing")
            return False

        try:
            self._set_terminal_size(session.master_fd, size)
            session.size = size

            # Send SIGWINCH to process group if process is running
            if session.pid != os.getpid():
                os.killpg(os.getpgid(session.pid), signal.SIGWINCH)

            logger.info(f"PTY session {session_id} resized to {size.cols}x{size.rows}")
            return True

        except Exception as e:
            logger.error(f"Failed to resize PTY session {session_id}: {e}")
            return False

    async def close_pty(self, session_id: str) -> bool:
        """Close PTY session"""
        session = self.active_sessions.get(session_id)
        if not session:
            logger.warning(f"PTY session {session_id} not found for closing")
            return False

        try:
            session.state = TerminalState.DISCONNECTED

            # Close file descriptors
            if session.master_fd >= 0:
                os.close(session.master_fd)
                session.master_fd = -1

            if session.slave_fd >= 0:
                os.close(session.slave_fd)
                session.slave_fd = -1

            # Remove from active sessions
            del self.active_sessions[session_id]

            logger.info(f"PTY session {session_id} closed successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to close PTY session {session_id}: {e}")
            return False

    def _set_terminal_size(self, fd: int, size: TerminalSize):
        """Set terminal size using TIOCSWINSZ"""
        if IS_WINDOWS:
            # Windows doesn't use TIOCSWINSZ, size is handled differently
            return
        try:
            # Create winsize structure: rows, cols, xpixels, ypixels
            winsize = struct.pack("HHHH", size.rows, size.cols, 0, 0)
            fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)
        except Exception as e:
            logger.error(f"Failed to set terminal size: {e}")
            raise

    async def read_stream(self, session_id: str) -> AsyncIterator[str]:
        """Read output stream from PTY session"""
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"PTY session {session_id} not found")

        if IS_WINDOWS and hasattr(session, '_windows_process'):
            async for output in self._read_windows_stream(session):
                yield output
        else:
            async for output in self._read_unix_stream(session):
                yield output

    async def _read_unix_stream(self, session: PTYSession) -> AsyncIterator[str]:
        """Read stream on Unix systems"""
        selector = selectors.DefaultSelector()
        selector.register(session.slave_fd, selectors.EVENT_READ)

        try:
            while session.state == TerminalState.ACTIVE:
                # Wait for data with timeout
                events = selector.select(timeout=0.1)

                if not events:
                    # No data, continue loop
                    continue

                for key, mask in events:
                    try:
                        data = os.read(key.fileobj, 4096)
                        if data:
                            yield data.decode('utf-8', errors='replace')
                        else:
                            # EOF reached
                            session.state = TerminalState.DISCONNECTED
                            break

                    except OSError as e:
                        if e.errno == 5:  # Input/output error
                            session.state = TerminalState.DISCONNECTED
                            break
                        logger.warning(f"Read error on PTY {session.session_id}: {e}")

                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.01)

        finally:
            selector.close()

    async def _read_windows_stream(self, session: PTYSession) -> AsyncIterator[str]:
        """Read stream on Windows systems"""
        process = session._windows_process
        try:
            while session.state == TerminalState.ACTIVE and process.poll() is None:
                try:
                    # Read from stdout with timeout
                    line = process.stdout.readline()
                    if line:
                        yield line.decode('utf-8', errors='replace')
                    else:
                        # No data, small delay
                        await asyncio.sleep(0.01)

                except Exception as e:
                    logger.warning(f"Read error on Windows PTY {session.session_id}: {e}")
                    break

        except Exception as e:
            logger.error(f"Error in Windows stream reader: {e}")

    async def write_stream(self, session_id: str, data: str) -> bool:
        """Write data to PTY session"""
        session = self.active_sessions.get(session_id)
        if not session:
            logger.warning(f"PTY session {session_id} not found for writing")
            return False

        if session.state != TerminalState.ACTIVE:
            logger.warning(f"PTY session {session_id} not active for writing")
            return False

        try:
            if IS_WINDOWS and hasattr(session, '_windows_process'):
                # Windows: write to process stdin
                process = session._windows_process
                data_bytes = data.encode('utf-8')
                process.stdin.write(data_bytes)
                process.stdin.flush()
            else:
                # Unix: write to master file descriptor
                data_bytes = data.encode('utf-8')
                os.write(session.master_fd, data_bytes)

            return True

        except Exception as e:
            logger.error(f"Failed to write to PTY session {session_id}: {e}")
            session.state = TerminalState.ERROR
            return False


class TerminalProtocolHandler:
    """Handles terminal protocols (ANSI, VT100, xterm-256color)"""

    def __init__(self):
        self.reset_sequences = {
            '\x1b[H': 'cursor_home',      # Move cursor to home
            '\x1b[2J': 'clear_screen',    # Clear screen
            '\x1b[0m': 'reset_format',    # Reset all formatting
        }

    def process_output(self, data: str) -> Dict[str, Any]:
        """Process terminal output and extract state information"""
        # Remove carriage returns
        cleaned_data = data.replace('\r\n', '\n').replace('\r', '\n')

        # Extract terminal state information
        state = {
            'raw_data': data,
            'cleaned_data': cleaned_data,
            'cursor_position': self._extract_cursor_position(data),
            'screen_clear': '\x1b[2J' in data,
            'format_changes': self._extract_format_changes(data)
        }

        return state

    def format_input(self, text: str) -> str:
        """Format input for terminal consumption"""
        # Handle special characters
        formatted = text.replace('\n', '\r\n')  # Convert LF to CRLF for terminals
        return formatted

    def handle_terminal_commands(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Process terminal control commands"""
        results = []

        for command in commands:
            if command in self.reset_sequences:
                results.append({
                    'command': command,
                    'action': self.reset_sequences[command],
                    'type': 'control'
                })
            elif command.startswith('\x1b['):
                # ANSI escape sequence
                results.append({
                    'command': command,
                    'action': 'ansi_sequence',
                    'parameters': self._parse_ansi_sequence(command),
                    'type': 'ansi'
                })

        return results

    def _extract_cursor_position(self, data: str) -> Optional[Tuple[int, int]]:
        """Extract cursor position from terminal output"""
        # Look for cursor position reports: ESC[<row>;<col>R
        import re
        match = re.search(r'\x1b\[(\d+);(\d+)R', data)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return None

    def _extract_format_changes(self, data: str) -> List[str]:
        """Extract text formatting changes"""
        import re
        # Find SGR (Select Graphic Rendition) sequences
        matches = re.findall(r'\x1b\[(?:\d+;)*\d+m', data)
        return matches

    def _parse_ansi_sequence(self, sequence: str) -> Dict[str, Any]:
        """Parse ANSI escape sequence"""
        # Remove ESC[ prefix and final character
        content = sequence[2:-1]
        parts = content.split(';')

        return {
            'command': sequence[-1],  # Final character
            'parameters': [int(p) if p.isdigit() else p for p in parts]
        }


class StreamHandler:
    """Manages real-time streaming of terminal I/O"""

    def __init__(self, pty_manager: PTYManager, protocol_handler: TerminalProtocolHandler):
        self.pty_manager = pty_manager
        self.protocol_handler = protocol_handler
        self.output_buffers: Dict[str, List[str]] = {}
        self.stream_tasks: Dict[str, asyncio.Task] = {}

    async def start_streaming(self, session_id: str, callback=None) -> None:
        """Start streaming output from PTY session"""
        if session_id in self.stream_tasks:
            logger.warning(f"Streaming already active for session {session_id}")
            return

        # Initialize buffer
        self.output_buffers[session_id] = []

        # Start streaming task
        task = asyncio.create_task(self._stream_worker(session_id, callback))
        self.stream_tasks[session_id] = task

        logger.info(f"Started streaming for PTY session {session_id}")

    async def stop_streaming(self, session_id: str) -> None:
        """Stop streaming output from PTY session"""
        if session_id not in self.stream_tasks:
            logger.warning(f"No active streaming for session {session_id}")
            return

        # Cancel task
        task = self.stream_tasks[session_id]
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

        # Clean up
        del self.stream_tasks[session_id]
        if session_id in self.output_buffers:
            del self.output_buffers[session_id]

        logger.info(f"Stopped streaming for PTY session {session_id}")

    async def get_output_since_last(self, session_id: str, last_seen: int = 0) -> List[str]:
        """Get output lines since last seen index"""
        if session_id not in self.output_buffers:
            return []

        buffer = self.output_buffers[session_id]
        return buffer[last_seen:] if last_seen < len(buffer) else []

    async def _stream_worker(self, session_id: str, callback=None) -> None:
        """Worker task for streaming terminal output"""
        try:
            async for output in self.pty_manager.read_stream(session_id):
                # Process through protocol handler
                state = self.protocol_handler.process_output(output)

                # Add to buffer
                if session_id not in self.output_buffers:
                    self.output_buffers[session_id] = []
                self.output_buffers[session_id].append(state['cleaned_data'])

                # Limit buffer size
                max_buffer_size = 1000
                if len(self.output_buffers[session_id]) > max_buffer_size:
                    self.output_buffers[session_id] = self.output_buffers[session_id][-max_buffer_size:]

                # Call callback if provided
                if callback:
                    try:
                        await callback(session_id, state)
                    except Exception as e:
                        logger.error(f"Error in stream callback for {session_id}: {e}")

        except asyncio.CancelledError:
            logger.info(f"Streaming worker for {session_id} cancelled")
        except Exception as e:
            logger.error(f"Error in streaming worker for {session_id}: {e}")

    async def get_buffer_stats(self, session_id: str) -> Dict[str, int]:
        """Get buffer statistics for session"""
        if session_id not in self.output_buffers:
            return {'size': 0, 'lines': 0}

        buffer = self.output_buffers[session_id]
        total_chars = sum(len(line) for line in buffer)

        return {
            'size': len(buffer),
            'lines': len(buffer),
            'total_chars': total_chars
        }