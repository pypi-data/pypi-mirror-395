"""
CLI Test Runner

Command-line test execution interface.
"""

import asyncio
from rich.console import Console
from rich.table import Table
from typing import Dict, Any, List, Optional

console = Console()

class CLITestRunner:
    """CLI test runner with rich output."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def run_tests(self, test_pattern: Optional[str] = None, verbose: bool = False):
        """Run tests with CLI output."""
        console.print("[cyan]Running PyDiscoBasePro Tests[/cyan]")

        # Discover tests
        from pydiscobasepro.core.automatic_test_discovery import AutomaticTestDiscovery
        discovery = AutomaticTestDiscovery(self.config)
        test_files = discovery.discover_tests()

        if not test_files:
            console.print("[yellow]No test files found.[/yellow]")
            return

        table = Table(title="Test Discovery")
        table.add_column("Test Files Found", style="cyan")

        for test_file in test_files:
            table.add_row(test_file)

        console.print(table)

        # Run tests
        result = discovery.run_discovered_tests()

        # Display results
        if result["return_code"] == 0:
            console.print("[green]✓ All tests passed![/green]")
        else:
            console.print("[red]✗ Some tests failed.[/red]")

        if verbose:
            console.print("\n[bold]Test Output:[/bold]")
            console.print(result["stdout"])

            if result["stderr"]:
                console.print("\n[bold red]Errors:[/bold red]")
                console.print(result["stderr"])