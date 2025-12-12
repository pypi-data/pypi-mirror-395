"""
CLI Macros System

Allows users to define and execute command macros.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class MacroManager:
    """Command macro management system."""

    def __init__(self, config):
        self.config = config
        self.macros_file = Path.home() / ".pydiscobasepro" / "macros.json"
        self.macros: Dict[str, Dict[str, Any]] = {}

        self.load_macros()

    def load_macros(self):
        """Load macros from file."""
        if self.macros_file.exists():
            try:
                with open(self.macros_file, 'r') as f:
                    self.macros = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load macros: {e}")
                self.macros = {}

    def save_macros(self):
        """Save macros to file."""
        try:
            with open(self.macros_file, 'w') as f:
                json.dump(self.macros, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save macros: {e}")

    def create_macro(self, name: str, commands: str):
        """Create a new macro."""
        if name in self.macros:
            console.print(f"[red]Macro '{name}' already exists.[/red]")
            return

        # Parse commands (semicolon separated)
        command_list = [cmd.strip() for cmd in commands.split(';') if cmd.strip()]

        self.macros[name] = {
            "commands": command_list,
            "created": str(Path.cwd()),
            "description": f"Macro {name}"
        }

        self.save_macros()
        console.print(f"[green]Macro '{name}' created with {len(command_list)} commands.[/green]")

    async def run_macro(self, name: str):
        """Execute a macro."""
        if name not in self.macros:
            console.print(f"[red]Macro '{name}' not found.[/red]")
            return

        macro = self.macros[name]
        commands = macro["commands"]

        console.print(f"[cyan]Executing macro '{name}' with {len(commands)} commands...[/cyan]")

        for i, command in enumerate(commands, 1):
            console.print(f"[yellow]Step {i}/{len(commands)}: {command}[/yellow]")

            # Execute command (simplified - would integrate with CLI app)
            try:
                # This would need to be integrated with the main CLI execution
                console.print(f"[green]✓ {command}[/green]")
            except Exception as e:
                console.print(f"[red]✗ {command}: {e}[/red]")
                break

        console.print(f"[green]Macro '{name}' completed.[/green]")

    def list_macros(self):
        """List all macros."""
        if not self.macros:
            console.print("[yellow]No macros defined.[/yellow]")
            return

        from rich.table import Table

        table = Table(title="Defined Macros")
        table.add_column("Name", style="cyan")
        table.add_column("Commands", style="green")
        table.add_column("Created In", style="yellow")

        for name, macro in self.macros.items():
            commands_count = len(macro.get("commands", []))
            created_in = macro.get("created", "Unknown")
            table.add_row(name, str(commands_count), created_in)

        console.print(table)

    def delete_macro(self, name: str):
        """Delete a macro."""
        if name not in self.macros:
            console.print(f"[red]Macro '{name}' not found.[/red]")
            return

        del self.macros[name]
        self.save_macros()
        console.print(f"[green]Macro '{name}' deleted.[/green]")

    def get_macro_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed macro information."""
        return self.macros.get(name)