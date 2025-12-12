"""
PyDiscoBasePro v3.0.0 CLI Application

Modular CLI framework with 30+ advanced features including rich output,
authentication, plugins, security, and more.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

from pydiscobasepro.cli.config import CLIConfig
from pydiscobasepro.cli.auth import CLIAuth
from pydiscobasepro.cli.plugins import CLIPluginManager
from pydiscobasepro.cli.cli_commands import CLICommands
from pydiscobasepro.cli.history import CommandHistory
from pydiscobasepro.cli.macros import MacroManager
from pydiscobasepro.cli.scheduler import CommandScheduler
from pydiscobasepro.cli.snapshots import SnapshotManager
from pydiscobasepro.cli.workspaces import WorkspaceManager
from pydiscobasepro.cli.sandbox import SandboxEnvironment
from pydiscobasepro.cli.benchmark import BenchmarkTools
from pydiscobasepro.cli.health import HealthChecker
from pydiscobasepro.cli.export_import import ExportImportManager
from pydiscobasepro.cli.metrics_viewer import CLIMetricsViewer
from pydiscobasepro.core.logging import get_logger
from pydiscobasepro.core.metrics import MetricsEngine

logger = get_logger(__name__)
console = Console()

class CLIApp:
    """Main CLI application class with all advanced features."""

    def __init__(self):
        self.config = CLIConfig()
        self.auth = CLIAuth(self.config)
        self.plugin_manager = CLIPluginManager(self.config)
        self.commands = CLICommands(self.config)
        self.history = CommandHistory(self.config)
        self.macros = MacroManager(self.config)
        self.scheduler = CommandScheduler(self.config)
        self.snapshots = SnapshotManager(self.config)
        self.workspaces = WorkspaceManager(self.config)
        self.sandbox = SandboxEnvironment(self.config)
        self.benchmark = BenchmarkTools(self.config)
        self.health = HealthChecker(self.config)
        self.export_import = ExportImportManager(self.config)
        self.metrics_viewer = CLIMetricsViewer(self.config)
        self.metrics = MetricsEngine()

        # Interactive mode components
        self.interactive_session = PromptSession(
            history=FileHistory(str(self.config.get_history_file())),
            completer=self._get_completer()
        )

        # CLI state
        self.interactive_mode = False
        self.safe_mode = False
        self.debug_mode = False
        self.dry_run = False

    def _get_completer(self) -> WordCompleter:
        """Get command completer for interactive mode."""
        commands = [
            "create", "run", "test", "benchmark", "health", "metrics",
            "auth", "config", "plugins", "workspace", "snapshot", "export",
            "import", "schedule", "macro", "history", "help", "exit"
        ]
        return WordCompleter(commands, ignore_case=True)

    def show_welcome(self):
        """Show welcome message with system info."""
        table = Table(title="System Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Version", style="yellow")

        table.add_row("PyDiscoBasePro", "v3.0.0", "Ready")
        table.add_row("CLI Framework", "Active", "1.0.0")
        table.add_row("Plugin System", f"{len(self.plugin_manager.plugins)} loaded", "1.0.0")
        table.add_row("Security", "Enabled", "1.0.0")
        table.add_row("Metrics", "Collecting", "1.0.0")

        console.print(table)

    async def run_interactive(self):
        """Run interactive CLI mode."""
        self.interactive_mode = True
        console.print("[green]Entering interactive mode. Type 'help' for commands, 'exit' to quit.[/green]")

        while True:
            try:
                user_input = await self.interactive_session.prompt_async("pydiscobasepro> ")
                if not user_input.strip():
                    continue

                # Add to history
                self.history.add_command(user_input)

                # Parse and execute
                await self._execute_command(user_input.split())

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit interactive mode.[/yellow]")
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                if self.debug_mode:
                    import traceback
                    console.print(traceback.format_exc())

    async def _execute_command(self, args: List[str]):
        """Execute a command from args."""
        if not args:
            return

        command = args[0].lower()

        # Handle built-in commands
        if command == "exit":
            if self.interactive_mode:
                self.interactive_mode = False
                return
            else:
                sys.exit(0)

        elif command == "help":
            self.show_help()

        elif command == "create":
            await self.commands.create_project(args[1] if len(args) > 1 else None)

        elif command == "run":
            await self.commands.run_bot()

        elif command == "test":
            await self.commands.run_tests()

        elif command == "benchmark":
            await self.benchmark.run_benchmarks()

        elif command == "health":
            await self.health.run_checks()

        elif command == "metrics":
            await self.metrics_viewer.show_metrics()

        elif command == "auth":
            await self._handle_auth(args[1:])

        elif command == "config":
            await self._handle_config(args[1:])

        elif command == "plugins":
            await self._handle_plugins(args[1:])

        elif command == "workspace":
            await self._handle_workspace(args[1:])

        elif command == "snapshot":
            await self._handle_snapshot(args[1:])

        elif command == "export":
            await self.export_import.export_data(args[1:])

        elif command == "import":
            await self.export_import.import_data(args[1:])

        elif command == "schedule":
            await self._handle_schedule(args[1:])

        elif command == "macro":
            await self._handle_macro(args[1:])

        elif command == "history":
            self.history.show_history()

        else:
            # Check for plugin commands
            handled = await self.plugin_manager.handle_command(args)
            if not handled:
                console.print(f"[red]Unknown command: {command}[/red]")
                console.print("Type 'help' for available commands.")

    def show_help(self):
        """Show help information."""
        help_text = """
[bold cyan]PyDiscoBasePro v3.0.0 CLI Commands:[/bold cyan]

[green]Project Management:[/green]
  create <name>     Create new bot project
  run               Run the bot
  test              Run test suite
  benchmark         Run performance benchmarks
  health            Run system health checks

[green]Monitoring & Metrics:[/green]
  metrics           View system metrics
  export <format>   Export data (json/yaml)
  import <file>     Import data

[green]Configuration:[/green]
  config <action>   Manage configuration
  auth <action>     Authentication commands
  workspace <cmd>   Workspace management
  snapshot <cmd>    Snapshot management

[green]Advanced Features:[/green]
  plugins <cmd>     Plugin management
  schedule <cmd>    Command scheduling
  macro <cmd>       Macro management
  history           Command history

[green]Interactive Mode:[/green]
  help              Show this help
  exit              Exit interactive mode

[yellow]Flags:[/yellow]
  --safe-mode       Run in safe mode
  --debug           Enable debug output
  --dry-run         Show what would be done
  --offline         Run in offline mode
        """
        console.print(Panel(help_text, title="CLI Help", border_style="blue"))

    async def _handle_auth(self, args: List[str]):
        """Handle authentication commands."""
        if not args:
            console.print("[red]Usage: auth <login|logout|status|users>[/red]")
            return

        subcommand = args[0].lower()
        if subcommand == "login":
            await self.auth.login()
        elif subcommand == "logout":
            await self.auth.logout()
        elif subcommand == "status":
            await self.auth.show_status()
        elif subcommand == "users":
            await self.auth.manage_users(args[1:])
        else:
            console.print(f"[red]Unknown auth command: {subcommand}[/red]")

    async def _handle_config(self, args: List[str]):
        """Handle configuration commands."""
        if not args:
            self.config.show_config()
            return

        subcommand = args[0].lower()
        if subcommand == "set":
            if len(args) >= 3:
                self.config.set(args[1], " ".join(args[2:]))
            else:
                console.print("[red]Usage: config set <key> <value>[/red]")
        elif subcommand == "get":
            if len(args) >= 2:
                value = self.config.get(args[1])
                console.print(f"{args[1]}: {value}")
            else:
                console.print("[red]Usage: config get <key>[/red]")
        elif subcommand == "profiles":
            self.config.manage_profiles(args[1:])
        else:
            console.print(f"[red]Unknown config command: {subcommand}[/red]")

    async def _handle_plugins(self, args: List[str]):
        """Handle plugin commands."""
        if not args:
            await self.plugin_manager.list_plugins()
            return

        subcommand = args[0].lower()
        if subcommand == "list":
            await self.plugin_manager.list_plugins()
        elif subcommand == "install":
            if len(args) >= 2:
                await self.plugin_manager.install_plugin(args[1])
            else:
                console.print("[red]Usage: plugins install <name>[/red]")
        elif subcommand == "remove":
            if len(args) >= 2:
                await self.plugin_manager.remove_plugin(args[1])
            else:
                console.print("[red]Usage: plugins remove <name>[/red]")
        elif subcommand == "update":
            await self.plugin_manager.update_plugins()
        else:
            console.print(f"[red]Unknown plugins command: {subcommand}[/red]")

    async def _handle_workspace(self, args: List[str]):
        """Handle workspace commands."""
        if not args:
            self.workspaces.list_workspaces()
            return

        subcommand = args[0].lower()
        if subcommand == "list":
            self.workspaces.list_workspaces()
        elif subcommand == "switch":
            if len(args) >= 2:
                self.workspaces.switch_workspace(args[1])
            else:
                console.print("[red]Usage: workspace switch <name>[/red]")
        elif subcommand == "create":
            if len(args) >= 2:
                self.workspaces.create_workspace(args[1])
            else:
                console.print("[red]Usage: workspace create <name>[/red]")
        else:
            console.print(f"[red]Unknown workspace command: {subcommand}[/red]")

    async def _handle_snapshot(self, args: List[str]):
        """Handle snapshot commands."""
        if not args:
            self.snapshots.list_snapshots()
            return

        subcommand = args[0].lower()
        if subcommand == "list":
            self.snapshots.list_snapshots()
        elif subcommand == "create":
            if len(args) >= 2:
                self.snapshots.create_snapshot(args[1])
            else:
                console.print("[red]Usage: snapshot create <name>[/red]")
        elif subcommand == "restore":
            if len(args) >= 2:
                self.snapshots.restore_snapshot(args[1])
            else:
                console.print("[red]Usage: snapshot restore <name>[/red]")
        else:
            console.print(f"[red]Unknown snapshot command: {subcommand}[/red]")

    async def _handle_schedule(self, args: List[str]):
        """Handle scheduler commands."""
        if not args:
            self.scheduler.list_scheduled()
            return

        subcommand = args[0].lower()
        if subcommand == "list":
            self.scheduler.list_scheduled()
        elif subcommand == "add":
            if len(args) >= 3:
                self.scheduler.add_schedule(" ".join(args[1:]))
            else:
                console.print("[red]Usage: schedule add <cron> <command>[/red]")
        elif subcommand == "remove":
            if len(args) >= 2:
                self.scheduler.remove_schedule(args[1])
            else:
                console.print("[red]Usage: schedule remove <id>[/red]")
        else:
            console.print(f"[red]Unknown schedule command: {subcommand}[/red]")

    async def _handle_macro(self, args: List[str]):
        """Handle macro commands."""
        if not args:
            self.macros.list_macros()
            return

        subcommand = args[0].lower()
        if subcommand == "list":
            self.macros.list_macros()
        elif subcommand == "create":
            if len(args) >= 3:
                self.macros.create_macro(args[1], " ".join(args[2:]))
            else:
                console.print("[red]Usage: macro create <name> <commands>[/red]")
        elif subcommand == "run":
            if len(args) >= 2:
                await self.macros.run_macro(args[1])
            else:
                console.print("[red]Usage: macro run <name>[/red]")
        else:
            console.print(f"[red]Unknown macro command: {subcommand}[/red]")

# Global CLI app instance
cli_app = CLIApp()

def create_cli_app() -> typer.Typer:
    """Create the main Typer CLI app with all commands."""
    app = typer.Typer(
        name="pydiscobasepro",
        help="PyDiscoBasePro v3.0.0 - Enterprise-Grade Discord Bot Framework",
        rich_markup_mode="rich"
    )

    # Global options
    def callback(
        safe_mode: bool = typer.Option(False, "--safe-mode", help="Run in safe mode"),
        debug: bool = typer.Option(False, "--debug", help="Enable debug output"),
        dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done"),
        offline: bool = typer.Option(False, "--offline", help="Run in offline mode"),
        interactive: bool = typer.Option(False, "-i", "--interactive", help="Run in interactive mode")
    ):
        cli_app.safe_mode = safe_mode
        cli_app.debug_mode = debug
        cli_app.dry_run = dry_run
        cli_app.config.set("offline_mode", offline)

        if interactive:
            asyncio.run(cli_app.run_interactive())
            sys.exit(0)

    app.callback()(callback)

    # Include command modules
    from pydiscobasepro.cli.commands.project import project_app
    from pydiscobasepro.cli.commands.auth import auth_app
    from pydiscobasepro.cli.commands.config_cmd import config_app
    from pydiscobasepro.cli.commands.plugins_cmd import plugins_app
    from pydiscobasepro.cli.commands.monitoring import monitoring_app
    from pydiscobasepro.cli.commands.devops import devops_app
    from pydiscobasepro.cli.commands.testing import testing_app

    app.add_typer(project_app, name="project")
    app.add_typer(auth_app, name="auth")
    app.add_typer(config_app, name="config")
    app.add_typer(plugins_app, name="plugins")
    app.add_typer(monitoring_app, name="monitoring")
    app.add_typer(devops_app, name="devops")
    app.add_typer(testing_app, name="testing")

    @app.command()
    def interactive():
        """Enter interactive CLI mode."""
        asyncio.run(cli_app.run_interactive())

    return app