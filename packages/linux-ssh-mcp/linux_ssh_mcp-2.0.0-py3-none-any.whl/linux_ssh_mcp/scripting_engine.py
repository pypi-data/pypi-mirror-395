"""
Scripting Engine for WindTerm-like Automation
Provides Python/Lua scripting capabilities for terminal automation
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ScriptLanguage(Enum):
    """Supported scripting languages"""
    PYTHON = "python"
    LUA = "lua"


@dataclass
class ScriptResult:
    """Result of script execution"""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class ScriptContext:
    """Execution context for scripts"""
    # These would be populated with actual instances in real usage
    session_id: str = ""
    ssh_manager = None
    terminal_state = None

    # Built-in functions for scripts
    async def send_command(self, command: str) -> str:
        """Send command to terminal"""
        # Placeholder implementation
        return f"Command sent: {command}"

    async def wait_for_output(self, pattern: str, timeout: float = 10.0) -> str:
        """Wait for specific output pattern"""
        # Placeholder implementation
        await asyncio.sleep(0.1)
        return f"Pattern '{pattern}' matched"

    async def send_keys(self, keys: str) -> bool:
        """Send keystrokes to terminal"""
        # Placeholder implementation
        return True

    async def get_cursor_position(self) -> tuple[int, int]:
        """Get current cursor position"""
        # Placeholder implementation
        return (1, 1)

    async def save_screenshot(self, path: str) -> bool:
        """Save terminal screenshot"""
        # Placeholder implementation
        return True


class ScriptingEngine:
    """Scripting engine supporting Python and Lua-like syntax"""

    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {}
        self.script_context: Optional[ScriptContext] = None

    async def execute_script(self, script: str, context: ScriptContext = None,
                           language: ScriptLanguage = ScriptLanguage.PYTHON) -> ScriptResult:
        """Execute script in specified language"""
        import time
        start_time = time.time()

        try:
            if language == ScriptLanguage.PYTHON:
                result = await self._execute_python_script(script, context or ScriptContext())
            elif language == ScriptLanguage.LUA:
                result = await self._execute_lua_script(script, context or ScriptContext())
            else:
                raise ValueError(f"Unsupported script language: {language}")

            execution_time = time.time() - start_time
            result.execution_time = execution_time

            logger.info(f"Script executed successfully in {execution_time:.2f}s")
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Script execution failed: {e}")
            return ScriptResult(
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time
            )

    async def _execute_python_script(self, script: str, context: ScriptContext) -> ScriptResult:
        """Execute Python script"""
        try:
            # Create a local namespace with context functions
            namespace = {
                'ctx': context,
                'send_command': context.send_command,
                'wait_for_output': context.wait_for_output,
                'send_keys': context.send_keys,
                'get_cursor_position': context.get_cursor_position,
                'save_screenshot': context.save_screenshot,
                'asyncio': asyncio
            }

            # Execute the script
            exec_locals = {}
            exec(script, namespace, exec_locals)

            # If script returned a value, use it as output
            output = exec_locals.get('result', 'Script executed successfully')

            return ScriptResult(
                success=True,
                output=str(output)
            )

        except Exception as e:
            return ScriptResult(
                success=False,
                output="",
                error=str(e)
            )

    async def _execute_lua_script(self, script: str, context: ScriptContext) -> ScriptResult:
        """Execute Lua-like script (simplified implementation)"""
        # This is a placeholder - real Lua support would require lupa or similar
        logger.warning("Lua script execution not fully implemented, treating as pseudo-code")

        # For now, just return a placeholder result
        return ScriptResult(
            success=True,
            output="Lua script execution (placeholder)"
        )

    async def register_hook(self, event: str, callback: Callable) -> bool:
        """Register event hook for automation"""
        if event not in self.hooks:
            self.hooks[event] = []

        self.hooks[event].append(callback)
        logger.info(f"Registered hook for event: {event}")
        return True

    async def unregister_hook(self, event: str, callback: Callable) -> bool:
        """Unregister event hook"""
        if event in self.hooks and callback in self.hooks[event]:
            self.hooks[event].remove(callback)
            logger.info(f"Unregistered hook for event: {event}")
            return True
        return False

    async def call_hooks(self, event: str, data: Any = None) -> List[Any]:
        """Call all hooks for an event"""
        results = []

        if event in self.hooks:
            for callback in self.hooks[event]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        result = await callback(data)
                    else:
                        result = callback(data)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error in hook callback for {event}: {e}")

        return results

    def list_hooks(self) -> Dict[str, int]:
        """List all registered hooks and their counts"""
        return {event: len(callbacks) for event, callbacks in self.hooks.items()}