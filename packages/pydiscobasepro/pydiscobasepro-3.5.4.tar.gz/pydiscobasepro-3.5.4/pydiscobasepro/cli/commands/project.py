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
    template: str = typer.Option("basic", help="Project template: basic, advanced, enterprise"),
    dashboard: bool = typer.Option(True, help="Include web dashboard"),
    database: str = typer.Option("mongodb", help="Database type: mongodb, sqlite, postgres"),
    testing: bool = typer.Option(True, help="Include testing framework"),
    ci_cd: bool = typer.Option(False, help="Include CI/CD configuration"),
    docker: bool = typer.Option(False, help="Include Docker configuration"),
    interactive: bool = typer.Option(True, help="Use interactive mode"),
    force: bool = typer.Option(False, help="Overwrite existing directory")
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
        if force:
            import shutil
            shutil.rmtree(project_path)
        elif not questionary.confirm(f"Directory {name} already exists. Continue?").ask():
            return

    console.print(f"[green]Creating project: {name} (template: {template})[/green]")

    # Create project structure
    project_path.mkdir(exist_ok=True)
    (project_path / "commands").mkdir(exist_ok=True)
    (project_path / "events").mkdir(exist_ok=True)
    (project_path / "components").mkdir(exist_ok=True)
    (project_path / "handlers").mkdir(exist_ok=True)
    (project_path / "utils").mkdir(exist_ok=True)

    if dashboard:
        (project_path / "static").mkdir(exist_ok=True)
        (project_path / "templates").mkdir(exist_ok=True)

    if testing:
        (project_path / "tests").mkdir(exist_ok=True)

    if ci_cd:
        (project_path / ".github").mkdir(exist_ok=True)
        (project_path / ".github" / "workflows").mkdir(exist_ok=True)

    # Create basic files
    create_basic_files(project_path, name, dashboard, database, testing, ci_cd, docker, template)

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


def create_basic_files(project_path: Path, name: str, dashboard: bool, database: str, testing: bool, ci_cd: bool, docker: bool, template: str):
    """Create basic project files."""

    # bot.py
    if template == "enterprise":
        bot_content = f'''"""
{name} - PyDiscoBasePro Enterprise Bot

Generated PyDiscoBasePro v3.0.0 enterprise project.
"""

import asyncio
import os
from pathlib import Path
from pydiscobasepro import PyDiscoBasePro
from database import Database
from handlers import CommandHandler, EventHandler, ComponentHandler
from utils import setup_logging
from dashboard import Dashboard

async def main():
    """Main enterprise bot function."""
    # Load configuration
    config_path = Path("config/config.json")
    if not config_path.exists():
        print("config/config.json not found. Please create it with your bot token.")
        return

    import json
    with open(config_path, "r") as f:
        config = json.load(f)

    # Setup logging
    setup_logging(config["logging"])

    # Database setup
    db_client = None
    if database == "mongodb":
        from motor.motor_asyncio import AsyncIOMotorClient
        db_client = AsyncIOMotorClient(config["mongodb"]["uri"])
    # Add other database setups

    database_instance = Database(db_client[config["mongodb"]["database"]])

    # Initialize bot
    bot = PyDiscoBasePro(
        token=config["token"],
        prefix=config["prefix"],
        intents=None
    )

    # Handlers
    command_handler = CommandHandler(bot, database_instance)
    event_handler = EventHandler(bot, database_instance)
    component_handler = ComponentHandler(bot, database_instance)

    # Dashboard
    dashboard_instance = Dashboard(bot, database_instance, config["dashboard"]) if dashboard else None

    # Load all components
    await command_handler.load_commands()
    await event_handler.load_events()
    await component_handler.load_components()

    if dashboard_instance:
        await dashboard_instance.run()

    # Start bot
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
'''
    else:
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

    # config.json or config/config.json
    if template == "enterprise":
        (project_path / "config").mkdir(exist_ok=True)
        config_file = project_path / "config" / "config.json"
        config_content = f'''{{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "description": "{name}",
  "version": "1.0.0",
  "mongodb": {{
    "uri": "mongodb://localhost:27017",
    "database": "{name.lower()}"
  }},
  "dashboard": {{
    "enabled": {str(dashboard).lower()},
    "port": 8080,
    "host": "0.0.0.0"
  }},
  "logging": {{
    "level": "INFO",
    "file": "logs/bot.log"
  }}
}}'''
    else:
        config_file = project_path / "config.json"
        config_content = f'''{{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "description": "{name}",
  "version": "1.0.0"
}}'''

    config_file.write_text(config_content)

    # requirements.txt
    req_content = '''pydiscobasepro>=3.0.0
discord.py>=2.3.0'''

    if database == "mongodb":
        req_content += '''
motor>=3.1.0
pymongo>=4.3.0'''
    elif database == "postgres":
        req_content += '''
psycopg2-binary>=2.9.0'''
    elif database == "sqlite":
        req_content += '''
aiosqlite>=0.17.0'''

    if dashboard:
        req_content += '''
fastapi>=0.100.0
uvicorn>=0.23.0'''

    if testing:
        req_content += '''
pytest>=7.0.0
pytest-asyncio>=0.21.0'''

    (project_path / "requirements.txt").write_text(req_content)

    if dashboard:
        # index.html
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{name} Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .status {{ padding: 10px; border-radius: 5px; margin: 10px 0; }}
        .online {{ background-color: #d4edda; color: #155724; }}
        .offline {{ background-color: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <h1>{name} Dashboard</h1>
    <p>PyDiscoBasePro v3.0.0</p>
    <div class="status offline" id="status">Bot Status: Offline</div>
    <div id="stats"></div>
    <script>
        // Basic dashboard JavaScript
        setInterval(() => {{
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {{
                    document.getElementById('status').className = data.online ? 'status online' : 'status offline';
                    document.getElementById('status').textContent = `Bot Status: ${{data.online ? 'Online' : 'Offline'}}`;
                    document.getElementById('stats').innerHTML = `<pre>${{JSON.stringify(data, null, 2)}}</pre>`;
                }})
                .catch(() => {{
                    document.getElementById('status').className = 'status offline';
                    document.getElementById('status').textContent = 'Bot Status: Offline';
                }});
        }}, 5000);
    </script>
</body>
</html>'''

        if template == "enterprise":
            (project_path / "static").mkdir(exist_ok=True)
            (project_path / "static" / "index.html").write_text(html_content)
        else:
            (project_path / "index.html").write_text(html_content)

    if testing:
        # Create basic test file
        test_content = f'''"""Tests for {name} bot."""

import pytest
import asyncio
from unittest.mock import AsyncMock

class Test{name}:
    """Test cases for the bot."""

    @pytest.mark.asyncio
    async def test_bot_initialization(self):
        """Test that the bot can be initialized."""
        # This would test bot initialization
        assert True  # Placeholder

    @pytest.mark.asyncio
    async def test_command_loading(self):
        """Test that commands can be loaded."""
        # This would test command loading
        assert True  # Placeholder
'''
        (project_path / "tests" / "__init__.py").write_text('')
        (project_path / "tests" / f"test_{name.lower()}.py").write_text(test_content)

    if ci_cd:
        # GitHub Actions workflow
        workflow_content = f'''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/ -v --cov={name.lower()} --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: echo "Deploy step would go here"
'''
        (project_path / ".github" / "workflows" / "ci-cd.yml").write_text(workflow_content)

    if docker:
        # Dockerfile
        dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash botuser
USER botuser

# Expose dashboard port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Run the bot
CMD ["python", "bot.py"]
'''
        (project_path / "Dockerfile").write_text(dockerfile_content)

        # docker-compose.yml
        compose_content = f'''version: '3.8'

services:
  {name.lower()}:
    build: .
    ports:
      - "8080:8080"
    environment:
      - BOT_TOKEN=${{BOT_TOKEN}}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

volumes:
  mongodb_data:
'''
        (project_path / "docker-compose.yml").write_text(compose_content)

    # README.md
    readme_content = f'''# {name}

A PyDiscoBasePro v3.0.0 Discord bot.

## Features

- Modern Discord.py bot framework
- Modular command system
- Event handling
- Component interactions
{"- Web dashboard" if dashboard else ""}
{"- Database integration (" + database + ")" if database != "none" else ""}
{"- Testing framework" if testing else ""}
{"- CI/CD pipeline" if ci_cd else ""}
{"- Docker support" if docker else ""}

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your bot:
   - Edit `config.json` and add your bot token
   - Customize settings as needed

3. Run the bot:
   ```bash
   python bot.py
   ```

## Development

{"### Testing\n```bash\npytest tests/\n```" if testing else ""}

{"### Docker\n```bash\ndocker-compose up --build\n```" if docker else ""}

## License

MIT License
'''
    (project_path / "README.md").write_text(readme_content)