"""
CLI Snapshot Manager

Manages system snapshots for backup and restore functionality.
"""

import hashlib
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import tarfile
import gzip

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class SnapshotManager:
    """System snapshot management for backup and restore."""

    def __init__(self, config):
        self.config = config
        self.snapshots_dir = Path.home() / ".pydiscobasepro" / "snapshots"
        self.snapshots_dir.mkdir(exist_ok=True)
        self.snapshots_metadata_file = self.snapshots_dir / "metadata.json"
        self.snapshots_metadata: Dict[str, Dict[str, Any]] = {}

        self.load_metadata()

    def load_metadata(self):
        """Load snapshots metadata."""
        if self.snapshots_metadata_file.exists():
            try:
                with open(self.snapshots_metadata_file, 'r') as f:
                    self.snapshots_metadata = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load snapshots metadata: {e}")
                self.snapshots_metadata = {}

    def save_metadata(self):
        """Save snapshots metadata."""
        try:
            with open(self.snapshots_metadata_file, 'w') as f:
                json.dump(self.snapshots_metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save snapshots metadata: {e}")

    def create_snapshot(self, name: str, description: Optional[str] = None):
        """Create a system snapshot."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"{name}_{timestamp}"
        snapshot_file = self.snapshots_dir / f"{snapshot_name}.tar.gz"

        console.print(f"[cyan]Creating snapshot '{snapshot_name}'...[/cyan]")

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Creating snapshot...", total=None)

                # Create tar.gz archive
                with tarfile.open(snapshot_file, "w:gz") as tar:
                    # Add current directory
                    cwd = Path.cwd()
                    for file_path in cwd.rglob("*"):
                        if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                            tar.add(file_path, arcname=file_path.relative_to(cwd.parent))

                # Calculate checksum
                with open(snapshot_file, 'rb') as f:
                    checksum = hashlib.sha256(f.read()).hexdigest()

                # Store metadata
                self.snapshots_metadata[snapshot_name] = {
                    "name": name,
                    "description": description or f"Snapshot created on {datetime.now().isoformat()}",
                    "created": datetime.now().isoformat(),
                    "file": str(snapshot_file),
                    "checksum": checksum,
                    "size": snapshot_file.stat().st_size
                }

                self.save_metadata()
                progress.update(task, completed=True)

            console.print(f"[green]Snapshot '{snapshot_name}' created successfully.[/green]")

        except Exception as e:
            logger.error(f"Failed to create snapshot: {e}")
            console.print(f"[red]Failed to create snapshot: {e}[/red]")

    def restore_snapshot(self, snapshot_name: str):
        """Restore from a snapshot."""
        if snapshot_name not in self.snapshots_metadata:
            console.print(f"[red]Snapshot '{snapshot_name}' not found.[/red]")
            return

        metadata = self.snapshots_metadata[snapshot_name]
        snapshot_file = Path(metadata["file"])

        if not snapshot_file.exists():
            console.print(f"[red]Snapshot file not found: {snapshot_file}[/red]")
            return

        # Verify checksum
        with open(snapshot_file, 'rb') as f:
            current_checksum = hashlib.sha256(f.read()).hexdigest()

        if current_checksum != metadata["checksum"]:
            console.print("[red]Snapshot checksum verification failed. File may be corrupted.[/red]")
            return

        console.print(f"[cyan]Restoring from snapshot '{snapshot_name}'...[/cyan]")

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Restoring snapshot...", total=None)

                # Extract archive
                with tarfile.open(snapshot_file, "r:gz") as tar:
                    tar.extractall(Path.cwd().parent)

                progress.update(task, completed=True)

            console.print(f"[green]Snapshot '{snapshot_name}' restored successfully.[/green]")

        except Exception as e:
            logger.error(f"Failed to restore snapshot: {e}")
            console.print(f"[red]Failed to restore snapshot: {e}[/red]")

    def list_snapshots(self):
        """List all snapshots."""
        if not self.snapshots_metadata:
            console.print("[yellow]No snapshots found.[/yellow]")
            return

        table = Table(title="System Snapshots")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Created", style="yellow")
        table.add_column("Size", style="magenta")

        for name, metadata in sorted(self.snapshots_metadata.items(), 
                                   key=lambda x: x[1]["created"], reverse=True):
            size_mb = metadata["size"] / (1024 * 1024)
            table.add_row(
                name,
                metadata["description"],
                datetime.fromisoformat(metadata["created"]).strftime("%Y-%m-%d %H:%M"),
                ".1f"
            )

        console.print(table)

    def delete_snapshot(self, snapshot_name: str):
        """Delete a snapshot."""
        if snapshot_name not in self.snapshots_metadata:
            console.print(f"[red]Snapshot '{snapshot_name}' not found.[/red]")
            return

        metadata = self.snapshots_metadata[snapshot_name]
        snapshot_file = Path(metadata["file"])

        # Delete file
        if snapshot_file.exists():
            snapshot_file.unlink()

        # Remove metadata
        del self.snapshots_metadata[snapshot_name]
        self.save_metadata()

        console.print(f"[green]Snapshot '{snapshot_name}' deleted.[/green]")

    def get_snapshot_info(self, snapshot_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed snapshot information."""
        return self.snapshots_metadata.get(snapshot_name)