"""
CLI Export/Import Manager

Handles data export and import functionality for configurations and data.
"""

import json
import yaml
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class ExportImportManager:
    """Data export and import functionality."""

    def __init__(self, config):
        self.config = config
        self.exports_dir = Path.home() / ".pydiscobasepro" / "exports"
        self.exports_dir.mkdir(exist_ok=True)

    async def export_data(self, args: List[str]):
        """Export data in various formats."""
        if not args:
            console.print("[red]Usage: export <type> [format] [filename][/red]")
            console.print("Types: config, users, plugins, metrics, logs")
            console.print("Formats: json, yaml, csv")
            return

        export_type = args[0].lower()
        format_type = args[1].lower() if len(args) > 1 else "json"
        filename = args[2] if len(args) > 2 else None

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{export_type}_export_{timestamp}.{format_type}"

        export_path = self.exports_dir / filename

        console.print(f"[cyan]Exporting {export_type} data to {export_path}[/cyan]")

        try:
            data = await self._gather_export_data(export_type)

            if format_type == "json":
                with open(export_path, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            elif format_type == "yaml":
                with open(export_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)
            elif format_type == "csv":
                await self._export_csv(data, export_path)
            else:
                console.print(f"[red]Unsupported format: {format_type}[/red]")
                return

            console.print(f"[green]Export completed: {export_path}[/green]")

        except Exception as e:
            console.print(f"[red]Export failed: {e}[/red]")
            logger.exception("Export error")

    async def import_data(self, args: List[str]):
        """Import data from file."""
        if len(args) < 1:
            console.print("[red]Usage: import <filename> [type][/red]")
            return

        filename = args[0]
        import_type = args[1].lower() if len(args) > 1 else None

        import_path = Path(filename)
        if not import_path.exists():
            # Try in exports directory
            import_path = self.exports_dir / filename
            if not import_path.exists():
                console.print(f"[red]File not found: {filename}[/red]")
                return

        console.print(f"[cyan]Importing data from {import_path}[/cyan]")

        try:
            # Detect format from extension
            if import_path.suffix == ".json":
                with open(import_path, 'r') as f:
                    data = json.load(f)
            elif import_path.suffix in [".yaml", ".yml"]:
                with open(import_path, 'r') as f:
                    data = yaml.safe_load(f)
            else:
                console.print(f"[red]Unsupported file format: {import_path.suffix}[/red]")
                return

            # Auto-detect type if not specified
            if not import_type:
                import_type = self._detect_import_type(data)

            await self._process_import_data(import_type, data)
            console.print(f"[green]Import completed successfully.[/green]")

        except Exception as e:
            console.print(f"[red]Import failed: {e}[/red]")
            logger.exception("Import error")

    async def _gather_export_data(self, export_type: str) -> Any:
        """Gather data for export based on type."""
        if export_type == "config":
            from pydiscobasepro.cli.config import CLIConfig
            config = CLIConfig()
            return config._config

        elif export_type == "users":
            from pydiscobasepro.cli.auth import CLIAuth
            auth = CLIAuth(self.config)
            return auth._users

        elif export_type == "plugins":
            from pydiscobasepro.cli.plugins import CLIPluginManager
            plugin_manager = CLIPluginManager(self.config)
            return {
                "plugins": plugin_manager.plugin_metadata,
                "loaded_count": len(plugin_manager.plugins)
            }

        elif export_type == "metrics":
            from pydiscobasepro.core.metrics import MetricsEngine
            metrics = MetricsEngine()
            return await metrics.export_metrics()

        elif export_type == "logs":
            # Export recent logs
            logs_dir = Path("logs")
            if logs_dir.exists():
                log_files = list(logs_dir.glob("*.log"))
                logs_data = {}
                for log_file in log_files:
                    with open(log_file, 'r') as f:
                        logs_data[log_file.name] = f.readlines()[-1000:]  # Last 1000 lines
                return logs_data
            else:
                return {"error": "No logs directory found"}

        else:
            raise ValueError(f"Unknown export type: {export_type}")

    async def _export_csv(self, data: Any, export_path: Path):
        """Export data as CSV."""
        with open(export_path, 'w', newline='') as f:
            writer = csv.writer(f)

            if isinstance(data, dict):
                # Write headers
                writer.writerow(["Key", "Value"])
                for key, value in data.items():
                    writer.writerow([key, str(value)])
            elif isinstance(data, list):
                # Assume list of dicts
                if data and isinstance(data[0], dict):
                    headers = list(data[0].keys())
                    writer.writerow(headers)
                    for item in data:
                        writer.writerow([item.get(h, "") for h in headers])
                else:
                    writer.writerow(["Value"])
                    for item in data:
                        writer.writerow([str(item)])

    def _detect_import_type(self, data: Any) -> str:
        """Auto-detect import type from data structure."""
        if isinstance(data, dict):
            if "version" in data and "logging" in data:
                return "config"
            elif any(isinstance(v, dict) and "password_hash" in v for v in data.values()):
                return "users"
            elif "plugins" in data:
                return "plugins"
        return "unknown"

    async def _process_import_data(self, import_type: str, data: Any):
        """Process imported data based on type."""
        if import_type == "config":
            from pydiscobasepro.cli.config import CLIConfig
            config = CLIConfig()
            config._config.update(data)
            config.save_config()

        elif import_type == "users":
            from pydiscobasepro.cli.auth import CLIAuth
            auth = CLIAuth(self.config)
            auth._users.update(data)
            auth.save_users()

        elif import_type == "plugins":
            # Plugin import would require special handling
            console.print("[yellow]Plugin import not yet implemented.[/yellow]")

        else:
            console.print(f"[yellow]Unknown import type: {import_type}. Data structure preserved.[/yellow]")

    def list_exports(self):
        """List available export files."""
        exports = list(self.exports_dir.glob("*"))

        if not exports:
            console.print("[yellow]No export files found.[/yellow]")
            return

        table = Table(title="Export Files")
        table.add_column("Filename", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Modified", style="yellow")

        for export_file in sorted(exports, key=lambda x: x.stat().st_mtime, reverse=True):
            size = export_file.stat().st_size
            size_str = ".1f" if size < 1024*1024 else ".1f"
            modified = datetime.fromtimestamp(export_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

            table.add_row(export_file.name, size_str, modified)

        console.print(table)

    def delete_export(self, filename: str):
        """Delete an export file."""
        export_path = self.exports_dir / filename
        if export_path.exists():
            export_path.unlink()
            console.print(f"[green]Deleted export file: {filename}[/green]")
        else:
            console.print(f"[red]Export file not found: {filename}[/red]")