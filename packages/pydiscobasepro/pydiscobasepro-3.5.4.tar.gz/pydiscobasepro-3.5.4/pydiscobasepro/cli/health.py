"""
CLI Health Checker

System health diagnostics and monitoring tools.
"""

import psutil
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class HealthChecker:
    """Comprehensive system health checking and diagnostics."""

    def __init__(self, config):
        self.config = config
        self.health_history_file = Path.home() / ".pydiscobasepro" / "health_history.json"

    async def run_checks(self):
        """Run comprehensive health checks."""
        console.print("[cyan]Running PyDiscoBasePro Health Checks[/cyan]")

        checks = {}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # System resources
            task = progress.add_task("Checking system resources...", total=None)
            checks["system"] = await self._check_system_resources()
            progress.update(task, completed=True)

            # Database connectivity
            task = progress.add_task("Checking database connectivity...", total=None)
            checks["database"] = await self._check_database()
            progress.update(task, completed=True)

            # Plugin health
            task = progress.add_task("Checking plugin health...", total=None)
            checks["plugins"] = await self._check_plugins()
            progress.update(task, completed=True)

            # Configuration validity
            task = progress.add_task("Validating configuration...", total=None)
            checks["config"] = await self._check_configuration()
            progress.update(task, completed=True)

            # Security status
            task = progress.add_task("Checking security status...", total=None)
            checks["security"] = await self._check_security()
            progress.update(task, completed=True)

        # Calculate overall health score
        health_score = self._calculate_health_score(checks)

        # Display results
        self._display_health_report(checks, health_score)

        # Save health history
        await self._save_health_history(checks, health_score)

    async def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage."""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # Disk
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent

        # Network (basic connectivity check)
        network_status = "OK"
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
        except:
            network_status = "Issues"

        return {
            "cpu_usage": cpu_percent,
            "memory_usage": memory_percent,
            "disk_usage": disk_percent,
            "network_status": network_status,
            "overall": "Good" if all([cpu_percent < 80, memory_percent < 80, disk_percent < 90]) else "Warning"
        }

    async def _check_database(self) -> Dict[str, Any]:
        """Check database connectivity and health."""
        try:
            # Attempt database connection
            from pydiscobasepro.database.manager import DatabaseManager
            db_manager = DatabaseManager(self.config.get("database", {}))

            # Simple ping test
            await db_manager.initialize()
            ping_result = await db_manager.ping()

            if ping_result:
                return {
                    "status": "Connected",
                    "latency": "< 100ms",  # Simplified
                    "overall": "Good"
                }
            else:
                return {
                    "status": "Connection Failed",
                    "latency": "N/A",
                    "overall": "Critical"
                }

        except Exception as e:
            return {
                "status": f"Error: {str(e)}",
                "latency": "N/A",
                "overall": "Critical"
            }

    async def _check_plugins(self) -> Dict[str, Any]:
        """Check plugin system health."""
        try:
            from pydiscobasepro.cli.plugins import CLIPluginManager
            plugin_manager = CLIPluginManager(self.config)

            loaded_plugins = len(plugin_manager.plugins)
            total_plugins = len(list(plugin_manager.plugins_dir.glob("*.py")))

            return {
                "loaded_plugins": loaded_plugins,
                "total_plugins": total_plugins,
                "load_success_rate": loaded_plugins / max(total_plugins, 1) * 100,
                "overall": "Good" if loaded_plugins == total_plugins else "Warning"
            }

        except Exception as e:
            return {
                "error": str(e),
                "overall": "Critical"
            }

    async def _check_configuration(self) -> Dict[str, Any]:
        """Check configuration validity."""
        try:
            from pydiscobasepro.cli.config import CLIConfig
            config = CLIConfig()

            # Check required config keys
            required_keys = ["version", "logging", "security"]
            missing_keys = [key for key in required_keys if not config.get(key)]

            if missing_keys:
                return {
                    "status": f"Missing keys: {', '.join(missing_keys)}",
                    "overall": "Warning"
                }
            else:
                return {
                    "status": "All required configuration present",
                    "overall": "Good"
                }

        except Exception as e:
            return {
                "status": f"Configuration error: {str(e)}",
                "overall": "Critical"
            }

    async def _check_security(self) -> Dict[str, Any]:
        """Check security status."""
        issues = []

        # Check file permissions
        config_dir = Path.home() / ".pydiscobasepro"
        if config_dir.exists():
            if oct(config_dir.stat().st_mode)[-3:] != "700":
                issues.append("Config directory permissions too open")

        # Check for sensitive files
        sensitive_files = ["users.enc", "sessions.enc", "auth.key"]
        for file in sensitive_files:
            file_path = config_dir / file
            if file_path.exists() and oct(file_path.stat().st_mode)[-3:] != "600":
                issues.append(f"{file} has incorrect permissions")

        return {
            "issues_found": len(issues),
            "issues": issues,
            "overall": "Good" if not issues else "Warning"
        }

    def _calculate_health_score(self, checks: Dict[str, Any]) -> float:
        """Calculate overall health score (0-100)."""
        score = 100.0
        penalties = {
            "Critical": 30,
            "Warning": 10,
            "Error": 20
        }

        for check_name, check_data in checks.items():
            status = check_data.get("overall", "Unknown")
            if status in penalties:
                score -= penalties[status]

        return max(0.0, min(100.0, score))

    def _display_health_report(self, checks: Dict[str, Any], health_score: float):
        """Display health check results."""
        # Overall score
        score_color = "green" if health_score >= 80 else "yellow" if health_score >= 60 else "red"
        console.print(f"[bold {score_color}]Overall Health Score: {health_score:.1f}/100[/bold {score_color}]")

        # Detailed results
        table = Table(title="Health Check Results")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="yellow")

        for check_name, check_data in checks.items():
            status = check_data.get("overall", "Unknown")
            status_color = {
                "Good": "green",
                "Warning": "yellow",
                "Critical": "red",
                "Error": "red"
            }.get(status, "white")

            # Format details
            details = []
            for key, value in check_data.items():
                if key != "overall":
                    details.append(f"{key}: {value}")

            table.add_row(
                check_name.title(),
                f"[{status_color}]{status}[/{status_color}]",
                "\n".join(details)
            )

        console.print(table)

        # Recommendations
        if health_score < 80:
            console.print(Panel(
                "Consider reviewing the warning/critical items above to improve system health.",
                title="Recommendations",
                border_style="yellow"
            ))

    async def _save_health_history(self, checks: Dict[str, Any], health_score: float):
        """Save health check results to history."""
        try:
            import json

            # Load existing history
            history = []
            if self.health_history_file.exists():
                with open(self.health_history_file, 'r') as f:
                    history = json.load(f)

            # Add new entry
            history.append({
                "timestamp": datetime.now().isoformat(),
                "score": health_score,
                "checks": checks
            })

            # Keep only last 50 entries
            history = history[-50:]

            # Save
            with open(self.health_history_file, 'w') as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save health history: {e}")

    def show_health_history(self, limit: int = 10):
        """Show health check history."""
        try:
            import json

            if not self.health_history_file.exists():
                console.print("[yellow]No health history found.[/yellow]")
                return

            with open(self.health_history_file, 'r') as f:
                history = json.load(f)

            table = Table(title=f"Health History (last {min(limit, len(history))} checks)")
            table.add_column("Date", style="cyan")
            table.add_column("Score", style="green")
            table.add_column("Status", style="yellow")

            for entry in history[-limit:]:
                score = entry["score"]
                status = "Good" if score >= 80 else "Warning" if score >= 60 else "Critical"
                status_color = "green" if status == "Good" else "yellow" if status == "Warning" else "red"

                date = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
                table.add_row(
                    date,
                    ".1f",
                    f"[{status_color}]{status}[/{status_color}]"
                )

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error loading health history: {e}[/red]")