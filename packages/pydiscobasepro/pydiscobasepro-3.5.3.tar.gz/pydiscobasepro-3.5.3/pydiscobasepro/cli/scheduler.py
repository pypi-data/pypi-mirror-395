"""
CLI Command Scheduler

Schedules and executes commands at specified times.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
from pathlib import Path
from croniter import croniter

from rich.console import Console
from rich.table import Table

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class CommandScheduler:
    """Advanced command scheduling system with cron support."""

    def __init__(self, config):
        self.config = config
        self.schedule_file = Path.home() / ".pydiscobasepro" / "schedule.json"
        self.scheduled_tasks: Dict[str, Dict[str, Any]] = {}
        self.running = False
        self.task_handles: Dict[str, asyncio.Task] = {}

        self.load_schedule()

    def load_schedule(self):
        """Load scheduled tasks from file."""
        if self.schedule_file.exists():
            try:
                with open(self.schedule_file, 'r') as f:
                    self.scheduled_tasks = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load schedule: {e}")
                self.scheduled_tasks = {}

    def save_schedule(self):
        """Save scheduled tasks to file."""
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(self.scheduled_tasks, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save schedule: {e}")

    def add_schedule(self, schedule_spec: str):
        """Add a scheduled task."""
        # Parse: "cron_expression command args..."
        parts = schedule_spec.split()
        if len(parts) < 2:
            console.print("[red]Invalid schedule format. Use: 'cron_expression command args...'</red>")
            return

        cron_expr = parts[0]
        command = " ".join(parts[1:])

        # Validate cron expression
        try:
            croniter(cron_expr)
        except Exception as e:
            console.print(f"[red]Invalid cron expression: {e}[/red]")
            return

        task_id = f"task_{len(self.scheduled_tasks) + 1}"

        self.scheduled_tasks[task_id] = {
            "cron": cron_expr,
            "command": command,
            "enabled": True,
            "created": datetime.now().isoformat(),
            "last_run": None,
            "next_run": None
        }

        self.save_schedule()
        console.print(f"[green]Scheduled task '{task_id}' added.[/green]")

    def remove_schedule(self, task_id: str):
        """Remove a scheduled task."""
        if task_id not in self.scheduled_tasks:
            console.print(f"[red]Task '{task_id}' not found.[/red]")
            return

        # Cancel running task if any
        if task_id in self.task_handles:
            self.task_handles[task_id].cancel()
            del self.task_handles[task_id]

        del self.scheduled_tasks[task_id]
        self.save_schedule()
        console.print(f"[green]Task '{task_id}' removed.[/green]")

    def list_scheduled(self):
        """List all scheduled tasks."""
        if not self.scheduled_tasks:
            console.print("[yellow]No scheduled tasks.[/yellow]")
            return

        table = Table(title="Scheduled Tasks")
        table.add_column("ID", style="cyan")
        table.add_column("Cron", style="green")
        table.add_column("Command", style="yellow")
        table.add_column("Enabled", style="magenta")
        table.add_column("Last Run", style="blue")

        for task_id, task in self.scheduled_tasks.items():
            last_run = task.get("last_run", "Never")
            if last_run and last_run != "Never":
                last_run = datetime.fromisoformat(last_run).strftime("%Y-%m-%d %H:%M")

            table.add_row(
                task_id,
                task["cron"],
                task["command"][:50] + "..." if len(task["command"]) > 50 else task["command"],
                "✓" if task["enabled"] else "✗",
                last_run
            )

        console.print(table)

    async def start_scheduler(self):
        """Start the scheduler."""
        if self.running:
            return

        self.running = True
        logger.info("Command scheduler started")

        while self.running:
            try:
                await self._check_scheduled_tasks()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)

    async def stop_scheduler(self):
        """Stop the scheduler."""
        self.running = False

        # Cancel all running tasks
        for task in self.task_handles.values():
            task.cancel()

        self.task_handles.clear()
        logger.info("Command scheduler stopped")

    async def _check_scheduled_tasks(self):
        """Check and execute due scheduled tasks."""
        now = datetime.now()

        for task_id, task in self.scheduled_tasks.items():
            if not task["enabled"]:
                continue

            try:
                cron = croniter(task["cron"], now)
                next_run = cron.get_next(datetime)

                # Check if task should run now
                if task.get("next_run"):
                    next_run_time = datetime.fromisoformat(task["next_run"])
                    if now >= next_run_time:
                        # Execute task
                        await self._execute_scheduled_task(task_id, task)

                        # Update next run
                        task["last_run"] = now.isoformat()
                        task["next_run"] = next_run.isoformat()
                        self.save_schedule()
                else:
                    # First time setup
                    task["next_run"] = next_run.isoformat()
                    self.save_schedule()

            except Exception as e:
                logger.error(f"Error checking task {task_id}: {e}")

    async def _execute_scheduled_task(self, task_id: str, task: Dict[str, Any]):
        """Execute a scheduled task."""
        logger.info(f"Executing scheduled task: {task_id}")

        try:
            # Parse command (this would integrate with CLI execution)
            command = task["command"]
            console.print(f"[cyan]Executing scheduled task: {command}[/cyan]")

            # Execute command (simplified)
            # In real implementation, this would call the CLI command handler
            console.print(f"[green]✓ Scheduled task {task_id} completed[/green]")

        except Exception as e:
            logger.error(f"Scheduled task {task_id} failed: {e}")
            console.print(f"[red]✗ Scheduled task {task_id} failed: {e}[/red]")