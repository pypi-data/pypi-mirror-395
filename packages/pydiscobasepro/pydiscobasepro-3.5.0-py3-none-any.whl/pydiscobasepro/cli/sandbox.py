"""
CLI Sandbox Environment

Isolated execution environment for testing commands safely.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Any
import tempfile
import shutil

from rich.console import Console
from rich.panel import Panel

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class SandboxEnvironment:
    """Isolated sandbox environment for safe command execution."""

    def __init__(self, config):
        self.config = config
        self.sandbox_dir = Path.home() / ".pydiscobasepro" / "sandbox"
        self.sandbox_dir.mkdir(exist_ok=True)

    def create_sandbox(self, name: str) -> Path:
        """Create a new sandbox environment."""
        sandbox_path = self.sandbox_dir / name
        if sandbox_path.exists():
            shutil.rmtree(sandbox_path)

        sandbox_path.mkdir(parents=True)

        # Copy minimal required files
        template_dir = Path(__file__).parent.parent.parent / "pydiscobasepro" / "template"
        if template_dir.exists():
            for file_path in ["requirements.txt", "config/config.json"]:
                src = template_dir / file_path
                dst = sandbox_path / file_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.exists():
                    shutil.copy2(src, dst)

        return sandbox_path

    def execute_in_sandbox(self, command: str, sandbox_name: str) -> bool:
        """Execute a command in the sandbox environment."""
        sandbox_path = self.sandbox_dir / sandbox_name
        if not sandbox_path.exists():
            console.print(f"[red]Sandbox '{sandbox_name}' does not exist.[/red]")
            return False

        console.print(f"[cyan]Executing in sandbox '{sandbox_name}': {command}[/cyan]")

        try:
            # Execute command in sandbox directory
            result = subprocess.run(
                command,
                shell=True,
                cwd=sandbox_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.stdout:
                console.print(Panel(result.stdout, title="Output", border_style="green"))
            if result.stderr:
                console.print(Panel(result.stderr, title="Errors", border_style="red"))

            success = result.returncode == 0
            status = "[green]✓ Success[/green]" if success else "[red]✗ Failed[/red]"
            console.print(f"Sandbox execution: {status}")

            return success

        except subprocess.TimeoutExpired:
            console.print("[red]Command timed out.[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Sandbox execution error: {e}[/red]")
            return False

    def list_sandboxes(self):
        """List all sandbox environments."""
        sandboxes = [d.name for d in self.sandbox_dir.iterdir() if d.is_dir()]

        if not sandboxes:
            console.print("[yellow]No sandboxes found.[/yellow]")
            return

        from rich.table import Table

        table = Table(title="Sandbox Environments")
        table.add_column("Name", style="cyan")
        table.add_column("Path", style="green")
        table.add_column("Size", style="yellow")

        for sandbox in sandboxes:
            path = self.sandbox_dir / sandbox
            size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            table.add_row(sandbox, str(path), ".1f")

        console.print(table)

    def delete_sandbox(self, name: str):
        """Delete a sandbox environment."""
        sandbox_path = self.sandbox_dir / name
        if not sandbox_path.exists():
            console.print(f"[red]Sandbox '{name}' does not exist.[/red]")
            return

        shutil.rmtree(sandbox_path)
        console.print(f"[green]Sandbox '{name}' deleted.[/green]")

    def clone_to_sandbox(self, source_path: Path, sandbox_name: str):
        """Clone a project into a sandbox."""
        sandbox_path = self.create_sandbox(sandbox_name)

        console.print(f"[cyan]Cloning to sandbox '{sandbox_name}'...[/cyan]")

        try:
            # Copy project files
            for item in source_path.iterdir():
                if item.name not in ['__pycache__', '.git', 'logs']:
                    dest = sandbox_path / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    else:
                        shutil.copytree(item, dest, ignore=shutil.ignore_patterns('__pycache__', '.git'))

            console.print(f"[green]Project cloned to sandbox '{sandbox_name}'.[/green]")

        except Exception as e:
            console.print(f"[red]Failed to clone to sandbox: {e}[/red]")

    def run_tests_in_sandbox(self, sandbox_name: str):
        """Run tests in a sandbox environment."""
        sandbox_path = self.sandbox_dir / sandbox_name
        if not sandbox_path.exists():
            console.print(f"[red]Sandbox '{sandbox_name}' does not exist.[/red]")
            return

        # Install dependencies
        console.print("[cyan]Installing dependencies in sandbox...[/cyan]")
        self.execute_in_sandbox("pip install -r requirements.txt", sandbox_name)

        # Run tests
        console.print("[cyan]Running tests in sandbox...[/cyan]")
        self.execute_in_sandbox("python -m pytest tests/ -v", sandbox_name)