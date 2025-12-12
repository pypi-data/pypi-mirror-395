"""
CLI Monitoring Commands

Handles monitoring and metrics.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live
import psutil
import time
from pathlib import Path
import json

monitoring_app = typer.Typer(help="Monitoring and metrics commands")

console = Console()

@monitoring_app.command()
def metrics(
    format: str = typer.Option("table", help="Output format: table, json, prometheus"),
    live: bool = typer.Option(False, help="Show live metrics"),
    interval: int = typer.Option(5, help="Update interval in seconds")
):
    """Show system metrics."""
    def get_metrics():
        table = Table(title="System Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Status", style="yellow")

        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_status = "🟢 Good" if cpu_percent < 80 else "🟡 High" if cpu_percent < 90 else "🔴 Critical"
        table.add_row("CPU Usage", f"{cpu_percent:.1f}%", cpu_status)

        # Memory
        memory = psutil.virtual_memory()
        mem_percent = memory.percent
        mem_status = "🟢 Good" if mem_percent < 80 else "🟡 High" if mem_percent < 90 else "🔴 Critical"
        table.add_row("Memory Usage", f"{mem_percent:.1f}% ({memory.used//1024//1024}MB/{memory.total//1024//1024}MB)", mem_status)

        # Disk
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_status = "🟢 Good" if disk_percent < 80 else "🟡 High" if disk_percent < 90 else "🔴 Critical"
        table.add_row("Disk Usage", f"{disk_percent:.1f}% ({disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB)", disk_status)

        # Network
        net = psutil.net_io_counters()
        table.add_row("Network Sent", f"{net.bytes_sent//1024//1024}MB", "ℹ️ Info")
        table.add_row("Network Received", f"{net.bytes_recv//1024//1024}MB", "ℹ️ Info")

        return table

    if format == "json":
        metrics_data = {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_sent_mb": psutil.net_io_counters().bytes_sent//1024//1024,
            "network_recv_mb": psutil.net_io_counters().bytes_recv//1024//1024
        }
        console.print(json.dumps(metrics_data, indent=2))
    elif format == "prometheus":
        console.print("# HELP pydiscobasepro_cpu_usage CPU usage percentage")
        console.print("# TYPE pydiscobasepro_cpu_usage gauge")
        console.print(f"pydiscobasepro_cpu_usage {psutil.cpu_percent()}")
        console.print("# HELP pydiscobasepro_memory_usage Memory usage percentage")
        console.print("# TYPE pydiscobasepro_memory_usage gauge")
        console.print(f"pydiscobasepro_memory_usage {psutil.virtual_memory().percent}")
    else:
        if live:
            with Live(get_metrics(), refresh_per_second=1/interval) as live_display:
                while True:
                    time.sleep(interval)
                    live_display.update(get_metrics())
        else:
            console.print(get_metrics())


@monitoring_app.command()
def logs(
    lines: int = typer.Option(50, help="Number of lines to show"),
    follow: bool = typer.Option(False, help="Follow log file"),
    level: str = typer.Option(None, help="Filter by log level"),
    grep: str = typer.Option(None, help="Filter logs containing text")
):
    """Show application logs."""
    log_file = Path("logs/bot.log")
    if not log_file.exists():
        console.print("[yellow]No log file found at logs/bot.log[/yellow]")
        return

    def print_logs():
        try:
            with open(log_file, 'r') as f:
                all_lines = f.readlines()
                filtered_lines = []

                for line in all_lines[-lines:]:
                    if level and f"[{level.upper()}]" not in line:
                        continue
                    if grep and grep.lower() not in line.lower():
                        continue
                    filtered_lines.append(line.strip())

                for line in filtered_lines:
                    # Color code log levels
                    if "[ERROR]" in line:
                        console.print(f"[red]{line}[/red]")
                    elif "[WARNING]" in line:
                        console.print(f"[yellow]{line}[/yellow]")
                    elif "[INFO]" in line:
                        console.print(f"[blue]{line}[/blue]")
                    elif "[DEBUG]" in line:
                        console.print(f"[gray]{line}[/gray]")
                    else:
                        console.print(line)
        except Exception as e:
            console.print(f"[red]Error reading log file: {e}[/red]")

    print_logs()

    if follow:
        try:
            with open(log_file, 'r') as f:
                f.seek(0, 2)  # Go to end of file
                while True:
                    line = f.readline()
                    if line:
                        line = line.strip()
                        if level and f"[{level.upper()}]" not in line:
                            continue
                        if grep and grep.lower() not in line.lower():
                            continue
                        if "[ERROR]" in line:
                            console.print(f"[red]{line}[/red]")
                        elif "[WARNING]" in line:
                            console.print(f"[yellow]{line}[/yellow]")
                        elif "[INFO]" in line:
                            console.print(f"[blue]{line}[/blue]")
                        elif "[DEBUG]" in line:
                            console.print(f"[gray]{line}[/gray]")
                        else:
                            console.print(line)
                    time.sleep(0.1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped following logs[/yellow]")


@monitoring_app.command()
def health():
    """Check system health."""
    table = Table(title="Health Check Results")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")

    # CPU Health
    cpu_percent = psutil.cpu_percent()
    cpu_status = "✅ Healthy" if cpu_percent < 80 else "⚠️ Warning" if cpu_percent < 90 else "❌ Critical"
    table.add_row("CPU", cpu_status, f"{cpu_percent:.1f}% usage")

    # Memory Health
    memory = psutil.virtual_memory()
    mem_status = "✅ Healthy" if memory.percent < 80 else "⚠️ Warning" if memory.percent < 90 else "❌ Critical"
    table.add_row("Memory", mem_status, f"{memory.percent:.1f}% usage")

    # Disk Health
    disk = psutil.disk_usage('/')
    disk_status = "✅ Healthy" if disk.percent < 80 else "⚠️ Warning" if disk.percent < 90 else "❌ Critical"
    table.add_row("Disk", disk_status, f"{disk.percent:.1f}% usage")

    # Network Health
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        net_status = "✅ Healthy"
        net_details = "Internet connection OK"
    except:
        net_status = "❌ Critical"
        net_details = "No internet connection"
    table.add_row("Network", net_status, net_details)

    # Python Health
    import sys
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_status = "✅ Healthy" if sys.version_info >= (3, 8) else "⚠️ Warning"
    table.add_row("Python", py_status, f"Version {py_version}")

    console.print(table)


@monitoring_app.command()
def alerts(
    active_only: bool = typer.Option(True, help="Show only active alerts"),
    format: str = typer.Option("table", help="Output format: table, json")
):
    """Show active alerts."""
    # This would integrate with a real alerting system
    # For now, we'll show mock alerts based on system status

    alerts = []

    # Check CPU
    cpu_percent = psutil.cpu_percent()
    if cpu_percent > 90:
        alerts.append({
            "id": "cpu_high",
            "level": "critical",
            "message": f"CPU usage is critically high: {cpu_percent:.1f}%",
            "timestamp": "2024-12-04T08:40:00Z",
            "active": True
        })
    elif cpu_percent > 80:
        alerts.append({
            "id": "cpu_warning",
            "level": "warning",
            "message": f"CPU usage is high: {cpu_percent:.1f}%",
            "timestamp": "2024-12-04T08:40:00Z",
            "active": True
        })

    # Check Memory
    memory = psutil.virtual_memory()
    if memory.percent > 90:
        alerts.append({
            "id": "memory_critical",
            "level": "critical",
            "message": f"Memory usage is critically high: {memory.percent:.1f}%",
            "timestamp": "2024-12-04T08:40:00Z",
            "active": True
        })
    elif memory.percent > 80:
        alerts.append({
            "id": "memory_warning",
            "level": "warning",
            "message": f"Memory usage is high: {memory.percent:.1f}%",
            "timestamp": "2024-12-04T08:40:00Z",
            "active": True
        })

    # Check Disk
    disk = psutil.disk_usage('/')
    if disk.percent > 95:
        alerts.append({
            "id": "disk_critical",
            "level": "critical",
            "message": f"Disk usage is critically high: {disk.percent:.1f}%",
            "timestamp": "2024-12-04T08:40:00Z",
            "active": True
        })
    elif disk.percent > 85:
        alerts.append({
            "id": "disk_warning",
            "level": "warning",
            "message": f"Disk usage is high: {disk.percent:.1f}%",
            "timestamp": "2024-12-04T08:40:00Z",
            "active": True
        })

    if not active_only:
        # Add some resolved alerts for demonstration
        alerts.extend([
            {
                "id": "network_down",
                "level": "critical",
                "message": "Network connection lost",
                "timestamp": "2024-12-04T08:30:00Z",
                "active": False,
                "resolved_at": "2024-12-04T08:35:00Z"
            }
        ])

    if format == "json":
        console.print(json.dumps(alerts, indent=2))
    else:
        if not alerts:
            console.print("[green]✅ No active alerts[/green]")
            return

        table = Table(title="System Alerts")
        table.add_column("Level", style="cyan")
        table.add_column("Message", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Time", style="gray")

        for alert in alerts:
            level_style = {
                "critical": "red",
                "warning": "yellow",
                "info": "blue"
            }.get(alert["level"], "white")

            status = "🔔 Active" if alert["active"] else "✅ Resolved"
            time_display = alert.get("resolved_at", alert["timestamp"]) if not alert["active"] else alert["timestamp"]

            table.add_row(
                f"[{level_style}]{alert['level'].upper()}[/{level_style}]",
                alert["message"],
                status,
                time_display
            )

        console.print(table)