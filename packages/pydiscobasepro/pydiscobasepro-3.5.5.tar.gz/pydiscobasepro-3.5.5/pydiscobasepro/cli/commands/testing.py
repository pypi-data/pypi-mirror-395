"""
CLI Testing Commands

Handles testing operations like running tests, coverage, etc.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess
import sys
from pathlib import Path
import json

testing_app = typer.Typer(help="Testing and quality assurance commands")

console = Console()

@testing_app.command()
def run(
    pattern: str = typer.Option("*", help="Test pattern to run"),
    verbose: bool = typer.Option(False, help="Verbose output"),
    coverage: bool = typer.Option(True, help="Run with coverage"),
    parallel: bool = typer.Option(False, help="Run tests in parallel"),
    fail_fast: bool = typer.Option(False, help="Stop on first failure")
):
    """Run all tests."""
    console.print("[green]Running tests...[/green]")

    # Check if we're in a project directory
    if not Path("tests").exists() and not Path("pytest.ini").exists() and not Path("pyproject.toml").exists():
        console.print("[yellow]No test configuration found. Creating basic test structure...[/yellow]")
        # Import and run the test creation from cli_commands
        from pydiscobasepro.cli.cli_commands import CLICommands
        cli_commands = CLICommands(None)
        cli_commands.create_test_structure()
        console.print("[green]Created basic test structure.[/green]")

    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]

    if verbose:
        cmd.append("-v")
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=term-missing", "--cov-report=html"])
    if parallel:
        cmd.extend(["-n", "auto"])
    if fail_fast:
        cmd.append("-x")

    cmd.append(f"tests/{pattern}")

    try:
        console.print(f"[blue]Executing: {' '.join(cmd)}[/blue]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running tests...", total=None)
            result = subprocess.run(cmd, capture_output=not verbose, text=True)
            progress.update(task, description="✅ Tests completed!")

        if result.returncode == 0:
            console.print("[green]🎉 All tests passed![/green]")
        else:
            console.print(f"[red]❌ Tests failed with exit code: {result.returncode}[/red]")
            if not verbose:
                console.print("[red]Error output:[/red]")
                console.print(result.stderr)

        # Parse and display test results
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines[-10:]:  # Show last 10 lines
                if line.strip():
                    if "passed" in line.lower():
                        console.print(f"[green]{line}[/green]")
                    elif "failed" in line.lower() or "error" in line.lower():
                        console.print(f"[red]{line}[/red]")
                    else:
                        console.print(line)

    except FileNotFoundError:
        console.print("[red]❌ pytest not found. Install with: pip install pytest pytest-cov pytest-asyncio[/red]")
    except Exception as e:
        console.print(f"[red]❌ Test execution failed: {e}[/red]")


@testing_app.command()
def coverage(
    format: str = typer.Option("html", help="Coverage report format: html, xml, json, term"),
    open_browser: bool = typer.Option(False, help="Open coverage report in browser"),
    min_coverage: int = typer.Option(80, help="Minimum coverage percentage")
):
    """Generate coverage report."""
    console.print("[green]Generating coverage report...[/green]")

    try:
        cmd = [sys.executable, "-m", "pytest", "--cov=.", f"--cov-report={format}"]

        if min_coverage > 0:
            cmd.extend(["--cov-fail-under", str(min_coverage)])

        console.print(f"[blue]Executing: {' '.join(cmd)}[/blue]")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            console.print("[green]✅ Coverage report generated successfully[/green]")

            # Show coverage summary
            if format == "term" or format == "term-missing":
                console.print(result.stdout)

            # Handle different formats
            if format == "html":
                report_path = Path("htmlcov/index.html")
                if report_path.exists():
                    console.print(f"[blue]HTML report: file://{report_path.absolute()}[/blue]")
                    if open_browser:
                        import webbrowser
                        webbrowser.open(f"file://{report_path.absolute()}")
                else:
                    console.print("[yellow]HTML report not found[/yellow]")

            elif format == "xml":
                xml_path = Path("coverage.xml")
                if xml_path.exists():
                    console.print(f"[blue]XML report: {xml_path.absolute()}[/blue]")

            elif format == "json":
                json_path = Path("coverage.json")
                if json_path.exists():
                    console.print(f"[blue]JSON report: {json_path.absolute()}[/blue]")

        else:
            console.print(f"[red]❌ Coverage generation failed: {result.stderr}[/red]")

    except FileNotFoundError:
        console.print("[red]❌ pytest-cov not found. Install with: pip install pytest-cov[/red]")
    except Exception as e:
        console.print(f"[red]❌ Coverage generation error: {e}[/red]")


@testing_app.command()
def benchmark(
    target: str = typer.Option("all", help="Benchmark target: all, cpu, memory, io"),
    iterations: int = typer.Option(5, help="Number of iterations"),
    output: str = typer.Option("table", help="Output format: table, json, csv")
):
    """Run benchmarks."""
    console.print("[green]Running benchmarks...[/green]")

    try:
        import time
        import psutil
        from rich.table import Table

        results = []

        def benchmark_cpu():
            """Benchmark CPU performance."""
            console.print("[blue]Benchmarking CPU...[/blue]")
            times = []
            for i in range(iterations):
                start = time.time()
                # CPU intensive task
                sum(x*x for x in range(100000))
                end = time.time()
                times.append(end - start)
                console.print(f"  Iteration {i+1}: {end-start:.4f}s")

            avg_time = sum(times) / len(times)
            results.append({
                "test": "CPU Performance",
                "metric": "time",
                "value": avg_time,
                "unit": "seconds",
                "iterations": iterations
            })
            return avg_time

        def benchmark_memory():
            """Benchmark memory operations."""
            console.print("[blue]Benchmarking memory...[/blue]")
            times = []
            for i in range(iterations):
                start = time.time()
                # Memory intensive task
                data = [x for x in range(100000)]
                del data
                end = time.time()
                times.append(end - start)
                console.print(f"  Iteration {i+1}: {end-start:.4f}s")

            avg_time = sum(times) / len(times)
            results.append({
                "test": "Memory Operations",
                "metric": "time",
                "value": avg_time,
                "unit": "seconds",
                "iterations": iterations
            })
            return avg_time

        def benchmark_io():
            """Benchmark I/O operations."""
            console.print("[blue]Benchmarking I/O...[/blue]")
            test_file = Path("benchmark_test.tmp")
            times = []
            for i in range(iterations):
                start = time.time()
                # I/O intensive task
                with open(test_file, 'w') as f:
                    f.write("x" * 100000)
                with open(test_file, 'r') as f:
                    _ = f.read()
                end = time.time()
                times.append(end - start)
                console.print(f"  Iteration {i+1}: {end-start:.4f}s")

            test_file.unlink(missing_ok=True)
            avg_time = sum(times) / len(times)
            results.append({
                "test": "I/O Operations",
                "metric": "time",
                "value": avg_time,
                "unit": "seconds",
                "iterations": iterations
            })
            return avg_time

        # Run benchmarks based on target
        if target in ["all", "cpu"]:
            benchmark_cpu()
        if target in ["all", "memory"]:
            benchmark_memory()
        if target in ["all", "io"]:
            benchmark_io()

        # Display results
        if output == "table":
            table = Table(title="Benchmark Results")
            table.add_column("Test", style="cyan")
            table.add_column("Metric", style="green")
            table.add_column("Value", style="yellow")
            table.add_column("Unit", style="blue")

            for result in results:
                table.add_row(
                    result["test"],
                    result["metric"],
                    f"{result['value']:.4f}",
                    result["unit"]
                )

            console.print(table)

        elif output == "json":
            console.print(json.dumps(results, indent=2))

        elif output == "csv":
            console.print("Test,Metric,Value,Unit,Iterations")
            for result in results:
                console.print(f"{result['test']},{result['metric']},{result['value']:.4f},{result['unit']},{result['iterations']}")

        console.print("[green]✅ Benchmarking completed![/green]")

    except Exception as e:
        console.print(f"[red]❌ Benchmarking failed: {e}[/red]")


@testing_app.command()
def quality():
    """Run quality checks (linting, type checking, etc.)."""
    console.print("[green]Running quality checks...[/green]")

    checks = [
        ("Black", ["black", "--check", "--diff", "."]),
        ("Flake8", ["flake8", "."]),
        ("MyPy", ["mypy", "."]),
        ("Bandit", ["bandit", "-r", "."])
    ]

    results = []

    for check_name, cmd in checks:
        console.print(f"[blue]Running {check_name}...[/blue]")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                status = "✅ Passed"
                color = "green"
            else:
                status = "❌ Failed"
                color = "red"
                if result.stdout:
                    console.print(f"[red]{check_name} output:[/red]")
                    console.print(result.stdout[:500])  # Limit output

            results.append((check_name, status, color))

        except subprocess.TimeoutExpired:
            results.append((check_name, "⏰ Timeout", "yellow"))
        except FileNotFoundError:
            results.append((check_name, "⚠️  Not installed", "yellow"))
        except Exception as e:
            results.append((check_name, f"❌ Error: {e}", "red"))

    # Display results
    table = Table(title="Quality Check Results")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")

    for check_name, status, color in results:
        table.add_row(check_name, f"[{color}]{status}[/{color}]")

    console.print(table)

    # Summary
    passed = sum(1 for _, status, _ in results if "✅" in status)
    total = len(results)
    if passed == total:
        console.print(f"[green]🎉 All quality checks passed! ({passed}/{total})[/green]")
    else:
        console.print(f"[yellow]⚠️  {passed}/{total} quality checks passed[/yellow]")