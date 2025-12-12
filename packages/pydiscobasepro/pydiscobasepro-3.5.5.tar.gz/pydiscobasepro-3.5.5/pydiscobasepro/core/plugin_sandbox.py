"""
Plugin Sandboxing

Secure execution environment for plugins.
"""

import sys
from typing import Any, Dict, Set
import builtins

class PluginSandbox:
    """Sandbox environment for plugin execution."""

    def __init__(self, allowed_modules: Set[str] = None, allowed_builtins: Set[str] = None):
        self.allowed_modules = allowed_modules or {
            'asyncio', 'logging', 'json', 'datetime', 'time', 'math', 'random'
        }

        self.allowed_builtins = allowed_builtins or {
            'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple',
            'range', 'enumerate', 'zip', 'sorted', 'reversed', 'sum', 'min', 'max',
            'abs', 'round', 'print', 'isinstance', 'hasattr', 'getattr', 'setattr'
        }

    def create_sandbox_globals(self, plugin_name: str, plugin_file: str) -> Dict[str, Any]:
        """Create restricted global environment for plugin."""
        # Restricted builtins
        restricted_builtins = {}
        for name in self.allowed_builtins:
            if hasattr(builtins, name):
                restricted_builtins[name] = getattr(builtins, name)

        # Restricted globals
        sandbox_globals = {
            '__builtins__': restricted_builtins,
            '__name__': f'plugins.{plugin_name}',
            '__file__': plugin_file,
            '__sandbox__': True,
            'logger': self._get_sandbox_logger(plugin_name)
        }

        return sandbox_globals

    def _get_sandbox_logger(self, plugin_name: str):
        """Get logger for sandboxed plugin."""
        from pydiscobasepro.core.logging import get_logger
        return get_logger(f"plugin.{plugin_name}")

    def validate_code(self, code: str) -> bool:
        """Validate plugin code for security."""
        dangerous_patterns = [
            'import os', 'import sys', 'import subprocess',
            'eval(', 'exec(', '__import__(',
            'open(', 'file(', 'input('
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                return False

        return True

    def execute_in_sandbox(self, code: str, globals_dict: Dict[str, Any]) -> Any:
        """Execute code in sandbox environment."""
        try:
            if not self.validate_code(code):
                raise SecurityError("Code contains dangerous patterns")

            # Execute code
            exec(code, globals_dict)

            return True

        except Exception as e:
            raise SecurityError(f"Sandbox execution failed: {e}")

class SecurityError(Exception):
    """Security violation in sandbox."""
    pass