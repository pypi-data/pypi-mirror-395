"""
CLI Metrics Viewer

Interactive metrics display and analysis.
"""

import asyncio
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from typing import Dict, Any

console = Console()

class CLIMetricsViewer:
    """CLI metrics viewer with rich display."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def show_metrics(self):
        """Display current system metrics."""
        console.print("[cyan]PyDiscoBasePro System Metrics[/cyan]")

        # Get metrics (would integrate with metrics engine)
        metrics = await self._get_metrics()

        # Display in sections
        self._display_system_metrics(metrics)
        self._display_performance_metrics(metrics)

    def _display_system_metrics(self, metrics: Dict[str, Any]):
        """Display system resource metrics."""
        table = Table(title="System Resources")
        table.add_column("Resource", style="cyan")
        table.add_column("Current", style="green")
        table.add_column("Status", style="yellow")

        # CPU
        cpu = metrics.get("cpu_percent", 0)
        cpu_status = "Good" if cpu < 70 else "High" if cpu < 90 else "Critical"
        table.add_row("CPU Usage", f"{cpu:.1f}%", cpu_status)

        # Memory
        memory = metrics.get("memory_percent", 0)
        mem_status = "Good" if memory < 70 else "High" if memory < 90 else "Critical"
        table.add_row("Memory Usage", f"{memory:.1f}%", mem_status)

        # Disk
        disk = metrics.get("disk_percent", 0)
        disk_status = "Good" if disk < 80 else "High" if disk < 95 else "Critical"
        table.add_row("Disk Usage", f"{disk:.1f}%", disk_status)

        console.print(table)

    def _display_performance_metrics(self, metrics: Dict[str, Any]):
        """Display performance metrics."""
        table = Table(title="Performance Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        perf_metrics = [
            ("Uptime", f"{metrics.get('uptime_seconds', 0):.0f}s"),
            ("Commands/Min", str(metrics.get("commands_per_minute", 0))),
            ("Active Guilds", str(metrics.get("total_guilds", 0))),
        ]

        for metric, value in perf_metrics:
            table.add_row(metric, value)

        console.print(table)

    async def _get_metrics(self) -> Dict[str, Any]:
        """Get current metrics (placeholder)."""
        # This would integrate with the actual metrics engine
        return {
            "cpu_percent": 45.2,
            "memory_percent": 62.1,
            "disk_percent": 34.5,
            "uptime_seconds": 3600,
            "commands_per_minute": 12,
            "total_guilds": 150
        }