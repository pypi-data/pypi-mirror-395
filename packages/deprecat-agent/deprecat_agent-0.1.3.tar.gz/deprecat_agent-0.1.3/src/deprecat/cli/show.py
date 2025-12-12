"""CLI command for displaying scan indexes."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

from deprecat.scanner.indexer import list_indexes, read_index

console = Console()


def _render_timestamps(entries) -> None:
    table = Table(title="Available Index Snapshots")
    table.add_column("Timestamp")
    table.add_column("Files")
    table.add_column("Path")
    for entry in entries:
        table.add_row(entry["timestamp"], str(entry["file_count"]), entry["path"])
    console.print(table)


def _render_snapshot(data: dict, limit: Optional[int] = 10) -> None:
    table = Table(title=f"Index Snapshot {data['timestamp']}")
    table.add_column("File")
    table.add_column("Imports")
    files = data.get("files", [])
    display_slice = files if limit is None else files[:limit]
    for file_ctx in display_slice:
        modules = [imp["module"] for imp in file_ctx.get("imports", [])]
        table.add_row(file_ctx["path"], ", ".join(modules[:5]) or "<none>")
    console.print(table)
    if limit is not None:
        remaining = len(files) - limit
        if remaining > 0:
            console.print(f"[dim]{remaining} more files not shown...[/dim]")


def show_command(
    target: Path,
    list_timestamps: bool,
    timestamp: Optional[str],
    limit: Optional[int],
) -> int:
    entries = list_indexes(target)
    if not entries:
        console.print("[yellow]No index snapshots found. Run `deprecat scan` first.[/yellow]")
        return 1
    if list_timestamps:
        _render_timestamps(entries)
        return 0
    if timestamp is None:
        timestamp = entries[0]["timestamp"]
    try:
        data = read_index(target, timestamp)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1
    _render_snapshot(data, limit=limit)
    return 0
