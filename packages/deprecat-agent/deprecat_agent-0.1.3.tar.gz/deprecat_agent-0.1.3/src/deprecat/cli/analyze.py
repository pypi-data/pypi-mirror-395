"""CLI helpers for sending index data to the backend service."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import httpx
from rich.console import Console
from rich.table import Table

from deprecat.backends.models import AnalysisRequest, AnalysisResponse
from deprecat.core.config import resolve_packages
from deprecat.scanner.indexer import list_indexes, read_index

console = Console()


def _analyses_dir(root: Path) -> Path:
    return root / ".deprecat" / "analyses"


def _store_analysis(root: Path, timestamp: str, payload: AnalysisResponse) -> Path:
    directory = _analyses_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"analysis-{timestamp}.json"
    path.write_text(payload.model_dump_json(indent=2), encoding="utf-8")
    return path


def analyze_command(
    target: Path,
    endpoint: str,
    timestamp: Optional[str],
    http_client: Optional[httpx.Client] = None,
) -> int:
    """Send the selected index snapshot to the backend service."""

    entries = list_indexes(target)
    if not entries:
        console.print("[yellow]No index snapshots found. Run `deprecat scan` first.[/yellow]")
        return 1
    selected_ts = timestamp or entries[0]["timestamp"]
    try:
        data = read_index(target, selected_ts)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    packages = resolve_packages(None, target)
    request_model = AnalysisRequest.model_validate(data | {"packages": packages})

    client = http_client or httpx.Client(timeout=30.0)
    close_client = http_client is None
    try:
        response = client.post(
            endpoint.rstrip("/") + "/analyze", json=request_model.model_dump()
        )
        response.raise_for_status()
        payload = AnalysisResponse(**response.json())
    except Exception as exc:  # pylint: disable=broad-except
        console.print(f"[red]Failed to contact backend: {exc}[/red]")
        return 1
    finally:
        if close_client:
            client.close()

    if not payload.suggestions:
        console.print("[yellow]No suggestions returned for this snapshot.[/yellow]")
    else:
        table = Table(title=f"Analysis Results ({selected_ts})")
        table.add_column("File")
        table.add_column("Summary")
        table.add_column("Plan")
        for suggestion in payload.suggestions:
            plan = "\n".join(suggestion.verification_plan)
            table.add_row(suggestion.file, suggestion.summary, plan or "<none>")
        console.print(table)
    stored = _store_analysis(target, selected_ts, payload)
    console.print(f"[green]Stored analysis at {stored.relative_to(target)}[/green]")
    return 0
