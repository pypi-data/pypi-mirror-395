"""
CLI History Management

Tracks command history with persistence and search capabilities.
"""

import atexit
from pathlib import Path
from typing import List, Optional
import readline
from datetime import datetime

class CommandHistory:
    """Command history management with persistence."""

    def __init__(self, config):
        self.config = config
        self.history_file = config.get_history_file()
        self.history: List[str] = []
        self.max_history = 1000

        self.load_history()
        self.setup_readline()

    def setup_readline(self):
        """Setup readline for history."""
        if hasattr(readline, 'read_history_file'):
            try:
                readline.read_history_file(str(self.history_file))
            except FileNotFoundError:
                pass

        # Set history file for readline
        readline.set_history_length(self.max_history)

        # Register save on exit
        atexit.register(self.save_history)

    def load_history(self):
        """Load history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    lines = f.readlines()
                    self.history = [line.strip() for line in lines if line.strip()]
            except Exception:
                self.history = []

    def save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, 'w') as f:
                for command in self.history[-self.max_history:]:
                    f.write(f"{command}\n")

            # Also save readline history
            if hasattr(readline, 'write_history_file'):
                readline.write_history_file(str(self.history_file))

        except Exception:
            pass  # Ignore save errors

    def add_command(self, command: str):
        """Add command to history."""
        if command and command != self.history[-1] if self.history else True:
            self.history.append(command)
            if len(self.history) > self.max_history:
                self.history.pop(0)

    def get_history(self, limit: Optional[int] = None) -> List[str]:
        """Get command history."""
        return self.history[-limit:] if limit else self.history

    def search_history(self, query: str) -> List[str]:
        """Search command history."""
        return [cmd for cmd in self.history if query.lower() in cmd.lower()]

    def clear_history(self):
        """Clear command history."""
        self.history.clear()
        if self.history_file.exists():
            self.history_file.unlink()

    def show_history(self, limit: Optional[int] = 20):
        """Display command history."""
        from rich.console import Console
        from rich.table import Table

        console = Console()
        history = self.get_history(limit)

        if not history:
            console.print("[yellow]No command history found.[/yellow]")
            return

        table = Table(title=f"Command History (last {len(history)} commands)")
        table.add_column("Command", style="cyan", no_wrap=True)

        for cmd in history:
            table.add_row(cmd)

        console.print(table)