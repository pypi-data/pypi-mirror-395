"""
CLI Benchmarking Tools

Performance benchmarking and profiling tools for the CLI.
"""

import time
import psutil
import tracemalloc
from pathlib import Path
from typing import Dict, List, Optional, Any
import cProfile
import pstats
from io import StringIO

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class BenchmarkTools:
    """Performance benchmarking and profiling tools."""

    def __init__(self, config):
        self.config = config
        self.results_dir = Path.home() / ".pydiscobasepro" / "benchmarks"
        self.results_dir.mkdir(exist_ok=True)

    async def run_benchmarks(self):
        """Run comprehensive benchmarking suite."""
        console.print("[cyan]Running PyDiscoBasePro Benchmark Suite[/cyan]")

        results = {}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Memory benchmark
            task = progress.add_task("Memory profiling...", total=None)
            results["memory"] = await self._benchmark_memory()
            progress.update(task, completed=True)

            # CPU benchmark
            task = progress.add_task("CPU profiling...", total=None)
            results["cpu"] = await self._benchmark_cpu()
            progress.update(task, completed=True)

            # Startup time
            task = progress.add_task("Startup time measurement...", total=None)
            results["startup"] = await self._benchmark_startup()
            progress.update(task, completed=True)

            # Command execution
            task = progress.add_task("Command execution benchmark...", total=None)
            results["commands"] = await self._benchmark_commands()
            progress.update(task, completed=True)

        # Display results
        self._display_benchmark_results(results)

        # Save results
        self._save_benchmark_results(results)

    async def _benchmark_memory(self) -> Dict[str, Any]:
        """Benchmark memory usage."""
        tracemalloc.start()

        # Simulate some operations
        import asyncio
        await asyncio.sleep(0.1)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "current_mb": current / 1024 / 1024,
            "peak_mb": peak / 1024 / 1024,
            "efficiency": "Good" if peak < 50 * 1024 * 1024 else "High Usage"
        }

    async def _benchmark_cpu(self) -> Dict[str, Any]:
        """Benchmark CPU usage."""
        process = psutil.Process()
        cpu_start = process.cpu_times()

        # Simulate CPU intensive task
        import asyncio
        await asyncio.sleep(0.1)

        cpu_end = process.cpu_times()
        cpu_usage = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)

        return {
            "cpu_time_seconds": cpu_usage,
            "cpu_percent": process.cpu_percent(),
            "performance": "Good" if cpu_usage < 0.1 else "CPU Intensive"
        }

    async def _benchmark_startup(self) -> Dict[str, Any]:
        """Benchmark application startup time."""
        start_time = time.time()

        # Simulate import
        import sys
        if 'pydiscobasepro' in sys.modules:
            del sys.modules['pydiscobasepro']

        import pydiscobasepro

        startup_time = time.time() - start_time

        return {
            "startup_time_seconds": startup_time,
            "rating": "Fast" if startup_time < 1.0 else "Slow"
        }

    async def _benchmark_commands(self) -> Dict[str, Any]:
        """Benchmark command execution performance."""
        # Profile a sample command execution
        profiler = cProfile.Profile()
        profiler.enable()

        # Simulate command execution
        import asyncio
        await asyncio.sleep(0.01)

        profiler.disable()

        # Get stats
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')

        # Capture output
        output = StringIO()
        stats.print_stats(10, stream=output)
        profile_output = output.getvalue()

        return {
            "profile_data": profile_output,
            "total_calls": stats.total_calls,
            "performance": "Good" if stats.total_calls < 1000 else "Complex"
        }

    def _display_benchmark_results(self, results: Dict[str, Any]):
        """Display benchmark results in a table."""
        table = Table(title="Benchmark Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Assessment", style="yellow")

        # Memory
        mem = results["memory"]
        table.add_row(
            "Memory Usage",
            ".1f",
            mem["efficiency"]
        )

        # CPU
        cpu = results["cpu"]
        table.add_row(
            "CPU Usage",
            ".2f",
            cpu["performance"]
        )

        # Startup
        startup = results["startup"]
        table.add_row(
            "Startup Time",
            ".2f",
            startup["rating"]
        )

        # Commands
        cmd = results["commands"]
        table.add_row(
            "Command Calls",
            str(cmd["total_calls"]),
            cmd["performance"]
        )

        console.print(table)

        # Show detailed profile if available
        if "profile_data" in cmd:
            console.print(Panel(cmd["profile_data"], title="Performance Profile", border_style="blue"))

    def _save_benchmark_results(self, results: Dict[str, Any]):
        """Save benchmark results to file."""
        import json
        from datetime import datetime

        result_file = self.results_dir / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(result_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": results
            }, f, indent=2)

        console.print(f"[green]Benchmark results saved to: {result_file}[/green]")

    def compare_benchmarks(self, file1: str, file2: str):
        """Compare two benchmark results."""
        # Implementation for comparing benchmark files
        console.print("[yellow]Benchmark comparison feature coming soon![/yellow]")

    def list_benchmark_results(self):
        """List saved benchmark results."""
        results = list(self.results_dir.glob("benchmark_*.json"))

        if not results:
            console.print("[yellow]No benchmark results found.[/yellow]")
            return

        table = Table(title="Benchmark History")
        table.add_column("Date", style="cyan")
        table.add_column("File", style="green")

        for result_file in sorted(results, reverse=True):
            date = result_file.stem.replace("benchmark_", "").replace("_", " ")
            table.add_row(date, result_file.name)

        console.print(table)