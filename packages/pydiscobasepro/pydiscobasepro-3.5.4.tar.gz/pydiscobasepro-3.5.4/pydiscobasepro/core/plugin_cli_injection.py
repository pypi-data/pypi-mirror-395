"""
Plugin CLI Command Injection

Allow plugins to inject CLI commands.
"""

from typing import Dict, Any, List, Optional, Callable, Awaitable

class PluginCLICommandInjection:
    """Plugin CLI command injection system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.injected_commands: Dict[str, Dict[str, Any]] = {}

    def inject_command(self, plugin_name: str, command_name: str, handler: Callable[..., Awaitable[Any]], help_text: str = ""):
        """Inject CLI command from plugin."""
        self.injected_commands[command_name] = {
            "plugin": plugin_name,
            "handler": handler,
            "help": help_text
        }

    def remove_command(self, command_name: str):
        """Remove injected command."""
        self.injected_commands.pop(command_name, None)

    async def execute_command(self, command_name: str, args: List[str]) -> Optional[Any]:
        """Execute injected command."""
        if command_name not in self.injected_commands:
            return None

        command_info = self.injected_commands[command_name]
        try:
            return await command_info["handler"](args)
        except Exception as e:
            logger.error(f"Plugin command {command_name} error: {e}")
            return None

    def list_injected_commands(self) -> Dict[str, str]:
        """List all injected commands."""
        return {name: info["help"] for name, info in self.injected_commands.items()}