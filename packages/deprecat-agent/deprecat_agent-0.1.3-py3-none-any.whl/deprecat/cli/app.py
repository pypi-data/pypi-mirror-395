"""Typer application entry point."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from deprecat.core.config import (
    DeprecatConfig,
    config_path,
    load_config,
    save_config,
)
from deprecat.core.dependencies import discover_available_tpas

from .analyze import analyze_command
from .doctor import doctor_command
from .scan import scan_command
from .review import review_command
from .serve import serve_backend_command
from .show import show_command

app = typer.Typer(add_completion=False, help="Developer tooling for the deprecat CLI")
console = Console()


@app.callback()
def cli() -> None:
    """Deprecat command group."""


@app.command()
def doctor() -> None:
    """Verify local environment, credentials, and runtime directories."""
    exit_code = doctor_command()
    raise typer.Exit(code=exit_code)


@app.command()
def scan(
    target: Path = typer.Argument(
        Path("."), exists=True, file_okay=False, resolve_path=True
    ),
    packages: Optional[str] = typer.Option(
        None,
        "--packages",
        "-p",
        help="Comma-separated list of third-party packages to monitor",
    ),
) -> None:
    """Scan a project and write a timestamped index snapshot."""
    package_list = (
        [pkg.strip() for pkg in packages.split(",") if pkg.strip()]
        if packages
        else None
    )
    exit_code = scan_command(target, package_list)
    raise typer.Exit(code=exit_code)


@app.command()
def init(
    target: Path = typer.Argument(
        Path("."), exists=True, file_okay=False, resolve_path=True
    ),
) -> None:
    """Guide the user through configuring monitored packages and scan cadence."""
    available = discover_available_tpas(target)
    if available:
        typer.echo("Detected third-party dependencies:")
        for tpa in available:
            typer.echo(f"  - {tpa}")
    else:
        typer.echo("No dependencies detected; enter packages manually.")
    package_input = typer.prompt(
        "Enter comma-separated packages to monitor",
        default=",".join(available[:3]) if available else "sentry-sdk",
    )
    frequency_input = typer.prompt("Scan frequency in days", default="7")
    packages = sorted({pkg.strip() for pkg in package_input.split(",") if pkg.strip()})
    try:
        frequency = max(1, int(frequency_input))
    except ValueError:
        frequency = 7
    config = DeprecatConfig(
        monitored_packages=packages,
        scan_frequency_days=frequency,
    )
    save_config(config, target)
    typer.echo(
        f"Configuration saved to {config_path(target).relative_to(target)} with {len(packages)} packages."
    )


@app.command()
def config(
    target: Path = typer.Argument(
        Path("."), exists=True, file_okay=False, resolve_path=True
    ),
    packages: Optional[str] = typer.Option(
        None, "--packages", "-p", help="Overwrite monitored packages"
    ),
    frequency: Optional[int] = typer.Option(
        None, "--frequency", "-f", help="Overwrite scan frequency (days)"
    ),
    show_only: bool = typer.Option(
        False, "--show", "-s", help="Only display settings without modifications"
    ),
) -> None:
    """Display or update configuration."""
    config_data = load_config(target)
    updated = False
    if packages is not None:
        config_data.monitored_packages = sorted(
            {pkg.strip() for pkg in packages.split(",") if pkg.strip()}
        )
        updated = True
    if frequency is not None:
        config_data.scan_frequency_days = max(1, frequency)
        updated = True
    if updated and not show_only:
        save_config(config_data, target)
    table = Table(title="Deprecat Configuration")
    table.add_column("Setting")
    table.add_column("Value")
    table.add_row(
        "Monitored Packages",
        ", ".join(config_data.monitored_packages) or "<none>",
    )
    table.add_row("Scan Frequency (days)", str(config_data.scan_frequency_days))
    table.add_row(
        "Config Path",
        str(config_path(target).relative_to(target)),
    )
    console.print(table)
    raise typer.Exit(code=0)


@app.command()
def packages(
    target: Path = typer.Argument(
        Path("."), exists=True, file_okay=False, resolve_path=True
    ),
) -> None:
    """Show discovered dependencies and highlight monitored packages."""
    available = discover_available_tpas(target)
    config_data = load_config(target)
    monitored = set(config_data.monitored_packages)
    if not available:
        typer.echo(
            "No dependencies detected. Run `deprecat init` or provide packages manually."
        )
        raise typer.Exit(code=0)
    table = Table(title="Available Dependencies")
    table.add_column("Package")
    table.add_column("Status")
    for dep in available:
        status = "MONITORED" if dep in monitored else ""
        table.add_row(dep, status)
    console.print(table)


@app.command()
def analyze(
    target: Path = typer.Argument(
        Path("."), exists=True, file_okay=False, resolve_path=True
    ),
    endpoint: str = typer.Option(
        "http://127.0.0.1:8080", "--endpoint", help="Backend base URL"
    ),
    timestamp: Optional[str] = typer.Option(
        None, "--timestamp", help="Specific snapshot to analyze"
    ),
) -> None:
    """Send the latest scan to the backend and display results."""

    exit_code = analyze_command(target, endpoint, timestamp)
    raise typer.Exit(code=exit_code)


@app.command()
def review(
    target: Path = typer.Argument(
        Path("."), exists=True, file_okay=False, resolve_path=True
    ),
    timestamp: Optional[str] = typer.Option(
        None, "--timestamp", help="Analysis timestamp to display"
    ),
    diff_index: Optional[int] = typer.Option(
        None, "--diff-index", "-d", help="Show the nth diff (1-based)"
    ),
) -> None:
    """View stored backend suggestions and optionally show diffs."""

    exit_code = review_command(target, timestamp, diff_index)
    raise typer.Exit(code=exit_code)


@app.command("serve")
def serve_backend(
    host: str = typer.Option("127.0.0.1", help="Interface to bind the backend server"),
    port: int = typer.Option(8080, help="Port to bind the backend server"),
    reload: bool = typer.Option(
        False, "--reload", help="Enable auto-reload (development only)"
    ),
) -> None:
    """Run the FastAPI backend locally."""

    serve_backend_command(host=host, port=port, reload=reload)


@app.command()
def show(
    target: Path = typer.Argument(
        Path("."), exists=True, file_okay=False, resolve_path=True
    ),
    timestamps: bool = typer.Option(
        False, "--timestamps", "-t", help="List available index snapshots"
    ),
    timestamp: Optional[str] = typer.Option(
        None, "--timestamp", help="Show a specific snapshot"
    ),
    limit: Optional[int] = typer.Option(
        10, "--limit", help="Number of files to display"
    ),
    show_all: bool = typer.Option(False, "--all", help="Display every indexed file"),
) -> None:
    """Display indexed imports or list available timestamps."""
    effective_limit = None if show_all else limit
    exit_code = show_command(target, timestamps, timestamp, effective_limit)
    raise typer.Exit(code=exit_code)


def main() -> None:
    app()
