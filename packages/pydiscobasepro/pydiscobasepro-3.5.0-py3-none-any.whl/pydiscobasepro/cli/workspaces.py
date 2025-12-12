"""
CLI Workspace Manager

Manages multiple project workspaces and configurations.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.table import Table

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class WorkspaceManager:
    """Multi-workspace management system."""

    def __init__(self, config):
        self.config = config
        self.workspaces_dir = Path.home() / ".pydiscobasepro" / "workspaces"
        self.workspaces_dir.mkdir(exist_ok=True)
        self.workspaces_file = self.workspaces_dir / "workspaces.json"
        self.workspaces: Dict[str, Dict[str, Any]] = {}

        self.load_workspaces()

    def load_workspaces(self):
        """Load workspaces configuration."""
        if self.workspaces_file.exists():
            try:
                with open(self.workspaces_file, 'r') as f:
                    self.workspaces = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load workspaces: {e}")
                self.workspaces = {}

    def save_workspaces(self):
        """Save workspaces configuration."""
        try:
            with open(self.workspaces_file, 'w') as f:
                json.dump(self.workspaces, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save workspaces: {e}")

    def create_workspace(self, name: str, path: Optional[str] = None):
        """Create a new workspace."""
        if name in self.workspaces:
            console.print(f"[red]Workspace '{name}' already exists.[/red]")
            return

        workspace_path = Path(path) if path else Path.cwd() / name
        workspace_path.mkdir(parents=True, exist_ok=True)

        self.workspaces[name] = {
            "path": str(workspace_path),
            "created": str(Path.cwd()),
            "description": f"Workspace {name}",
            "active": False
        }

        self.save_workspaces()
        console.print(f"[green]Workspace '{name}' created at {workspace_path}[/green]")

    def switch_workspace(self, name: str):
        """Switch to a different workspace."""
        if name not in self.workspaces:
            console.print(f"[red]Workspace '{name}' does not exist.[/red]")
            return

        # Deactivate current workspace
        for ws_name, ws_data in self.workspaces.items():
            ws_data["active"] = False

        # Activate new workspace
        self.workspaces[name]["active"] = True
        self.save_workspaces()

        workspace_path = Path(self.workspaces[name]["path"])
        console.print(f"[green]Switched to workspace '{name}' at {workspace_path}[/green]")

        # Change directory (in real implementation, this would affect the shell)
        try:
            import os
            os.chdir(workspace_path)
        except Exception as e:
            logger.warning(f"Could not change directory: {e}")

    def list_workspaces(self):
        """List all workspaces."""
        if not self.workspaces:
            console.print("[yellow]No workspaces defined.[/yellow]")
            return

        table = Table(title="Workspaces")
        table.add_column("Name", style="cyan")
        table.add_column("Path", style="green")
        table.add_column("Active", style="magenta")
        table.add_column("Description", style="yellow")

        for name, workspace in self.workspaces.items():
            active = "✓" if workspace.get("active", False) else ""
            table.add_row(
                name,
                workspace["path"],
                active,
                workspace.get("description", "")
            )

        console.print(table)

    def delete_workspace(self, name: str):
        """Delete a workspace."""
        if name not in self.workspaces:
            console.print(f"[red]Workspace '{name}' does not exist.[/red]")
            return

        # Don't delete the actual directory, just the workspace entry
        del self.workspaces[name]
        self.save_workspaces()
        console.print(f"[green]Workspace '{name}' removed from list.[/green]")

    def get_active_workspace(self) -> Optional[str]:
        """Get the currently active workspace."""
        for name, workspace in self.workspaces.items():
            if workspace.get("active", False):
                return name
        return None

    def get_workspace_path(self, name: str) -> Optional[Path]:
        """Get the path of a workspace."""
        workspace = self.workspaces.get(name)
        return Path(workspace["path"]) if workspace else None