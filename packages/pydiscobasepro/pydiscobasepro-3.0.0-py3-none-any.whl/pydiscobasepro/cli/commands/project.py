"""
CLI Project Commands

Handles project creation, management, and operations.
"""

import asyncio
import typer
from pathlib import Path
from typing import Optional
import questionary
from rich.console import Console
from rich.panel import Panel

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

project_app = typer.Typer(help="Project management commands")


@project_app.command()
def create(
    name: Optional[str] = typer.Argument(None, help="Project name"),
    template: str = typer.Option("basic", help="Project template"),
    dashboard: bool = typer.Option(True, help="Include web dashboard"),
    interactive: bool = typer.Option(True, help="Use interactive mode")
):
    """Create a new PyDiscoBasePro project."""
    if interactive and not name:
        name = questionary.text("Enter project name:").ask()
        if not name:
            console.print("[red]Project name is required[/red]")
            return

    if not name:
        console.print("[red]Project name is required[/red]")
        return

    project_path = Path.cwd() / name

    if project_path.exists():
        if not questionary.confirm(f"Directory {name} already exists. Continue?").ask():
            return

    console.print(f"[green]Creating project: {name}[/green]")

    # Create project structure
    project_path.mkdir(exist_ok=True)
    (project_path / "commands").mkdir(exist_ok=True)
    (project_path / "events").mkdir(exist_ok=True)
    (project_path / "components").mkdir(exist_ok=True)

    if dashboard:
        (project_path / "static").mkdir(exist_ok=True)
        (project_path / "templates").mkdir(exist_ok=True)

    # Create basic files
    create_basic_files(project_path, name, dashboard)

    console.print(Panel(f"✅ Project '{name}' created successfully!\n\nNext steps:\n  cd {name}\n  python bot.py", title="Success"))


@project_app.command()
def run():
    """Run the bot."""
    console.print("[green]Starting PyDiscoBasePro bot...[/green]")
    # Implementation would go here


@project_app.command()
def test():
    """Run project tests."""
    console.print("[green]Running tests...[/green]")
    # Implementation would go here


def create_basic_files(project_path: Path, name: str, dashboard: bool):
    """Create basic project files."""

    # bot.py
    bot_content = f'''"""
{name} - PyDiscoBasePro Bot

Generated PyDiscoBasePro v3.0.0 project.
"""

import asyncio
from pydiscobasepro import PyDiscoBasePro

async def main():
    """Main bot function."""
    bot = PyDiscoBasePro(
        token="YOUR_BOT_TOKEN_HERE",
        prefix="!",
        intents=None
    )

    # Load commands, events, components
    await bot.load_all()

    # Start bot
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
'''

    (project_path / "bot.py").write_text(bot_content)

    # config.json
    config_content = '''{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "description": "''' + name + '''",
  "version": "1.0.0"
}'''

    (project_path / "config.json").write_text(config_content)

    # requirements.txt
    req_content = '''pydiscobasepro>=3.0.0
discord.py>=2.3.0'''

    (project_path / "requirements.txt").write_text(req_content)

    if dashboard:
        # index.html
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{name} Dashboard</title>
</head>
<body>
    <h1>{name} Dashboard</h1>
    <p>PyDiscoBasePro v3.0.0</p>
</body>
</html>'''

        (project_path / "static" / "index.html").write_text(html_content)