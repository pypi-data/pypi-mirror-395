"""
CLI Config Commands

Handles configuration management.
"""

import typer
from rich.console import Console

config_app = typer.Typer(help="Configuration management commands")

console = Console()

@config_app.command()
def show(
    format: str = typer.Option("table", help="Output format: table, json, yaml"),
    section: str = typer.Option(None, help="Show only specific section")
):
    """Show current configuration."""
    from pydiscobasepro.cli.config import CLIConfig
    config = CLIConfig()

    if format == "json":
        import json
        console.print(json.dumps(config._config, indent=2))
    elif format == "yaml":
        try:
            import yaml
            console.print(yaml.dump(config._config, default_flow_style=False))
        except ImportError:
            console.print("[red]PyYAML not installed. Install with: pip install PyYAML[/red]")
            return
    else:  # table format
        if section:
            section_data = config.get(section, {})
            if isinstance(section_data, dict):
                from rich.table import Table
                table = Table(title=f"Configuration - {section}")
                table.add_column("Key", style="cyan")
                table.add_column("Value", style="green")
                for k, v in section_data.items():
                    table.add_row(k, str(v))
                console.print(table)
            else:
                console.print(f"{section}: {section_data}")
        else:
            config.show_config()


@config_app.command()
def set(
    key: str = typer.Argument(..., help="Configuration key"),
    value: str = typer.Argument(..., help="Configuration value"),
    type_hint: str = typer.Option("auto", help="Value type: auto, str, int, float, bool")
):
    """Set configuration value."""
    from pydiscobasepro.cli.config import CLIConfig
    config = CLIConfig()

    # Convert value based on type_hint
    if type_hint == "int":
        try:
            value = int(value)
        except ValueError:
            console.print("[red]Invalid integer value[/red]")
            return
    elif type_hint == "float":
        try:
            value = float(value)
        except ValueError:
            console.print("[red]Invalid float value[/red]")
            return
    elif type_hint == "bool":
        value = value.lower() in ("true", "1", "yes", "on")
    # auto or str - keep as string

    config.set(key, value)
    console.print(f"[green]Set {key} = {value}[/green]")


@config_app.command()
def get(
    key: str = typer.Argument(..., help="Configuration key"),
    default: str = typer.Option(None, help="Default value if key not found")
):
    """Get configuration value."""
    from pydiscobasepro.cli.config import CLIConfig
    config = CLIConfig()

    value = config.get(key, default)
    if value is not None:
        console.print(f"{key}: {value}")
    else:
        console.print(f"[yellow]Key '{key}' not found[/yellow]")