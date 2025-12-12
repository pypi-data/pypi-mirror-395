"""
CLI Plugin Management System

Handles plugin loading, sandboxing, permissions, and marketplace integration.
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
import asyncio

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class CLIPluginManager:
    """Advanced plugin management system with sandboxing and marketplace."""

    def __init__(self, config):
        self.config = config
        self.plugins_dir = Path.home() / ".pydiscobasepro" / "plugins"
        self.plugins_dir.mkdir(exist_ok=True)
        self.marketplace_dir = self.plugins_dir / "marketplace"
        self.marketplace_dir.mkdir(exist_ok=True)

        self.plugins: Dict[str, Any] = {}
        self.plugin_metadata: Dict[str, Dict] = {}
        self.sandbox_enabled = config.get("plugins.sandbox_enabled", True)
        self.max_plugins = config.get("plugins.max_plugins", 50)

        # Plugin execution environment
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def initialize(self):
        """Initialize plugin system."""
        if self.config.get("plugins.auto_load", True):
            await self.load_plugins()

    async def load_plugins(self):
        """Load all available plugins."""
        if len(self.plugins) >= self.max_plugins:
            logger.warning(f"Maximum plugins limit ({self.max_plugins}) reached")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Loading plugins...", total=None)

            for plugin_file in self.plugins_dir.glob("*.py"):
                if plugin_file.name.startswith('_'):
                    continue

                try:
                    plugin_name = plugin_file.stem
                    if plugin_name in self.plugins:
                        continue

                    plugin = await self.load_plugin(plugin_file)
                    if plugin:
                        self.plugins[plugin_name] = plugin
                        self.plugin_metadata[plugin_name] = {
                            "file": str(plugin_file),
                            "loaded_at": asyncio.get_event_loop().time(),
                            "version": getattr(plugin, "__version__", "1.0.0"),
                            "permissions": getattr(plugin, "REQUIRED_PERMISSIONS", [])
                        }
                        logger.info(f"Loaded plugin: {plugin_name}")

                except Exception as e:
                    logger.error(f"Failed to load plugin {plugin_file}: {e}")

            progress.update(task, completed=True)

        console.print(f"[green]Loaded {len(self.plugins)} plugins[/green]")

    async def load_plugin(self, plugin_file: Path) -> Optional[Any]:
        """Load a single plugin with sandboxing."""
        try:
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)

            if self.sandbox_enabled:
                # Execute in sandboxed environment
                await self.execute_in_sandbox(spec.loader, module)
            else:
                spec.loader.exec_module(module)

            # Validate plugin interface
            if not hasattr(module, 'register'):
                logger.warning(f"Plugin {plugin_file.stem} missing register function")
                return None

            return module

        except Exception as e:
            logger.error(f"Error loading plugin {plugin_file}: {e}")
            return None

    async def execute_in_sandbox(self, loader, module):
        """Execute plugin in sandboxed environment."""
        # Create restricted globals
        restricted_globals = {
            '__builtins__': {
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'sorted': sorted,
                'reversed': reversed,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'print': print,
                # Add other safe builtins as needed
            },
            '__name__': module.__name__,
            '__file__': module.__file__,
            'asyncio': asyncio,
            'logger': logger,
        }

        # Execute with restricted environment
        code = loader.get_code(module.__name__)
        exec(code, restricted_globals)

        # Copy safe attributes to module
        for name, value in restricted_globals.items():
            if not name.startswith('_'):
                setattr(module, name, value)

    async def unload_plugin(self, plugin_name: str):
        """Unload a plugin."""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            if hasattr(plugin, 'cleanup'):
                try:
                    await plugin.cleanup()
                except Exception as e:
                    logger.error(f"Error cleaning up plugin {plugin_name}: {e}")

            del self.plugins[plugin_name]
            del self.plugin_metadata[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")

    async def reload_plugin(self, plugin_file: Path):
        """Reload a plugin."""
        plugin_name = plugin_file.stem
        await self.unload_plugin(plugin_name)
        plugin = await self.load_plugin(plugin_file)
        if plugin:
            self.plugins[plugin_name] = plugin
            self.plugin_metadata[plugin_name]["loaded_at"] = asyncio.get_event_loop().time()

    async def list_plugins(self):
        """List all loaded plugins."""
        if not self.plugins:
            console.print("[yellow]No plugins loaded.[/yellow]")
            return

        table = Table(title="Loaded Plugins")
        table.add_column("Name", style="cyan")
        table.add_column("Version", style="green")
        table.add_column("Permissions", style="yellow")
        table.add_column("Status", style="magenta")

        for name, metadata in self.plugin_metadata.items():
            permissions = ", ".join(metadata.get("permissions", []))
            status = "Active" if name in self.plugins else "Inactive"
            table.add_row(
                name,
                metadata.get("version", "1.0.0"),
                permissions or "None",
                status
            )

        console.print(table)

    async def install_plugin(self, plugin_name: str):
        """Install plugin from marketplace."""
        marketplace_file = self.marketplace_dir / f"{plugin_name}.py"
        if not marketplace_file.exists():
            console.print(f"[red]Plugin '{plugin_name}' not found in marketplace.[/red]")
            return

        # Copy to plugins directory
        plugin_file = self.plugins_dir / f"{plugin_name}.py"
        plugin_file.write_bytes(marketplace_file.read_bytes())

        # Load the plugin
        plugin = await self.load_plugin(plugin_file)
        if plugin:
            self.plugins[plugin_name] = plugin
            console.print(f"[green]Plugin '{plugin_name}' installed and loaded.[/green]")
        else:
            console.print(f"[red]Failed to load plugin '{plugin_name}'.[/red]")

    async def remove_plugin(self, plugin_name: str):
        """Remove a plugin."""
        await self.unload_plugin(plugin_name)

        plugin_file = self.plugins_dir / f"{plugin_name}.py"
        if plugin_file.exists():
            plugin_file.unlink()
            console.print(f"[green]Plugin '{plugin_name}' removed.[/green]")
        else:
            console.print(f"[yellow]Plugin '{plugin_name}' not found.[/yellow]")

    async def update_plugins(self):
        """Update all plugins from marketplace."""
        console.print("[cyan]Checking for plugin updates...[/cyan]")

        updated = 0
        for plugin_name in list(self.plugins.keys()):
            marketplace_file = self.marketplace_dir / f"{plugin_name}.py"
            if marketplace_file.exists():
                # Compare versions (simplified)
                local_file = self.plugins_dir / f"{plugin_name}.py"
                if local_file.exists():
                    local_hash = hashlib.md5(local_file.read_bytes()).hexdigest()
                    market_hash = hashlib.md5(marketplace_file.read_bytes()).hexdigest()

                    if local_hash != market_hash:
                        # Update plugin
                        local_file.write_bytes(marketplace_file.read_bytes())
                        await self.reload_plugin(local_file)
                        updated += 1
                        console.print(f"[green]Updated plugin: {plugin_name}[/green]")

        if updated == 0:
            console.print("[yellow]All plugins are up to date.[/yellow]")
        else:
            console.print(f"[green]Updated {updated} plugins.[/green]")

    async def handle_command(self, args: List[str]) -> bool:
        """Handle plugin-injected CLI commands."""
        if not args:
            return False

        command = args[0]
        for plugin_name, plugin in self.plugins.items():
            if hasattr(plugin, 'cli_commands') and command in plugin.cli_commands:
                try:
                    result = await plugin.cli_commands[command](args[1:])
                    return True
                except Exception as e:
                    console.print(f"[red]Plugin command error: {e}[/red]")
                    return True

        return False

    def get_plugin_info(self, plugin_name: str) -> Optional[Dict]:
        """Get detailed information about a plugin."""
        return self.plugin_metadata.get(plugin_name)

    async def validate_permissions(self, plugin_name: str, required_permissions: List[str]) -> bool:
        """Validate plugin permissions."""
        if not self.config.get("plugins.permission_control", True):
            return True

        plugin_info = self.get_plugin_info(plugin_name)
        if not plugin_info:
            return False

        granted_permissions = plugin_info.get("permissions", [])
        return all(perm in granted_permissions for perm in required_permissions)

    async def cleanup(self):
        """Cleanup all plugins."""
        for plugin_name in list(self.plugins.keys()):
            await self.unload_plugin(plugin_name)

        self.executor.shutdown(wait=True)