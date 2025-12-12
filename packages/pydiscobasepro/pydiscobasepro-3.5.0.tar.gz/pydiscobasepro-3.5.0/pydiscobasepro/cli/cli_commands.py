"""
CLI Commands Module

Core CLI command implementations for project management, running, and testing.
"""

import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class CLICommands:
    """CLI command implementations."""

    def __init__(self, config):
        self.config = config

    async def create_project(self, project_name: Optional[str] = None):
        """Create a new PyDiscoBasePro project."""
        if not project_name:
            from rich.prompt import Prompt
            project_name = Prompt.ask("Enter project name")

        if not project_name:
            console.print("[red]Project name is required.[/red]")
            return

        target_dir = Path.cwd() / project_name
        if target_dir.exists():
            console.print(f"[red]Directory {project_name} already exists![/red]")
            return

        # Get template directory
        template_dir = Path(__file__).parent.parent.parent / "pydiscobasepro" / "template"

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Creating project '{project_name}'...", total=5)

            # Copy template
            progress.update(task, advance=1, description="Copying template files...")
            import shutil
            shutil.copytree(template_dir, target_dir, ignore=shutil.ignore_patterns('__pycache__', '.git'))

            # Replace placeholders
            progress.update(task, advance=1, description="Configuring project...")
            await self._replace_placeholders(target_dir, project_name)

            # Install dependencies
            progress.update(task, advance=1, description="Installing dependencies...")
            requirements_file = target_dir / "requirements.txt"
            if requirements_file.exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                             capture_output=True, cwd=target_dir)

            # Initialize git
            progress.update(task, advance=1, description="Initializing git repository...")
            subprocess.run(["git", "init"], capture_output=True, cwd=target_dir)
            subprocess.run(["git", "add", "."], capture_output=True, cwd=target_dir)

            progress.update(task, advance=1, description="Project created successfully!")

        console.print(f"[green]Project '{project_name}' created successfully![/green]")
        console.print(f"[cyan]Navigate to {project_name} and run: python bot.py[/cyan]")

    async def run_bot(self):
        """Run the Discord bot."""
        bot_file = Path.cwd() / "bot.py"
        if not bot_file.exists():
            console.print("[red]bot.py not found in current directory.[/red]")
            console.print("[yellow]Make sure you're in a PyDiscoBasePro project directory.[/yellow]")
            return

        console.print("[green]Starting PyDiscoBasePro bot...[/green]")

        try:
            # Import and run bot
            sys.path.insert(0, str(Path.cwd()))
            import bot
            # The bot.run() is already called in bot.py
        except KeyboardInterrupt:
            console.print("[yellow]Bot stopped by user.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error running bot: {e}[/red]")
            logger.exception("Bot runtime error")

    async def run_tests(self):
        """Run the test suite."""
        test_dir = Path.cwd() / "tests"
        if not test_dir.exists():
            console.print("[yellow]No tests directory found. Creating basic test structure...[/yellow]")
            await self._create_test_structure(test_dir)

        console.print("[green]Running tests...[/green]")

        try:
            import pytest
            result = pytest.main([
                str(test_dir),
                "-v",
                "--tb=short",
                "--color=yes",
                f"--cov={'pydiscobasepro' if Path('pydiscobasepro').exists() else ''}",
                "--cov-report=term-missing"
            ])

            if result == 0:
                console.print("[green]All tests passed![/green]")
            else:
                console.print(f"[red]Tests failed with exit code: {result}[/red]")

        except ImportError:
            console.print("[red]pytest not installed. Install with: pip install pytest pytest-cov[/red]")
        except Exception as e:
            console.print(f"[red]Error running tests: {e}[/red]")

    async def _replace_placeholders(self, directory: Path, project_name: str):
        """Replace placeholders in template files."""
        files_to_replace = [
            'README.md',
            'bot.py',
            'config/config.json',
            'requirements.txt'
        ]

        for file_path in files_to_replace:
            full_path = directory / file_path
            if full_path.exists():
                content = full_path.read_text()
                content = content.replace('PyDiscoBasePro', project_name)
                content = content.replace('pydiscobasepro', project_name.lower())
                full_path.write_text(content)

    async def _create_test_structure(self, test_dir: Path):
        """Create basic test structure."""
        test_dir.mkdir(exist_ok=True)

        # Create __init__.py
        (test_dir / "__init__.py").write_text('"""Test package."""\n')

        # Create conftest.py
        conftest_content = '''"""Pytest configuration."""
import pytest
import asyncio
from unittest.mock import AsyncMock

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mock_bot():
    """Mock Discord bot for testing."""
    bot = AsyncMock()
    bot.user = AsyncMock()
    bot.user.id = 123456789
    bot.user.name = "TestBot"
    return bot
'''
        (test_dir / "conftest.py").write_text(conftest_content)

        # Create basic test file
        test_content = '''"""Basic functionality tests."""
import pytest

class TestBasic:
    """Basic test cases."""

    def test_import(self):
        """Test that the package can be imported."""
        try:
            import pydiscobasepro
            assert pydiscobasepro.__version__ == "3.0.0"
        except ImportError:
            pytest.skip("Package not installed")

    @pytest.mark.asyncio
    async def test_mock_bot(self, mock_bot):
        """Test with mock bot."""
        assert mock_bot.user.id == 123456789
        assert mock_bot.user.name == "TestBot"
'''
        (test_dir / "test_basic.py").write_text(test_content)

        console.print("[green]Created basic test structure.[/green]")