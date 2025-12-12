"""Review CLI for displaying stored backend suggestions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from deprecat.backends.utils import get_logger

console = Console()

logger = get_logger(__name__)


def _analyses_dir(root: Path) -> Path:
    return root / ".deprecat" / "analyses"


def _load_analysis(root: Path, timestamp: str) -> dict:
    path = _analyses_dir(root) / f"analysis-{timestamp}.json"
    if not path.exists():
        raise FileNotFoundError(f"No analysis stored for timestamp {timestamp}")
    return json.loads(path.read_text(encoding="utf-8"))


def list_analyses(root: Path) -> list[tuple[str, Path]]:
    directory = _analyses_dir(root)
    if not directory.exists():
        return []
    entries = []
    for path in sorted(directory.glob("analysis-*.json"), reverse=True):
        entries.append((path.stem.replace("analysis-", ""), path))
    return entries


def review_command(
    target: Path,
    timestamp: Optional[str],
    diff_index: Optional[int],
) -> int:
    """Render stored suggestions and optionally display the selected diff."""

    entries = list_analyses(target)
    if not entries:
        console.print(
            "[yellow]No analysis files found. Run `deprecat analyze` first.[/yellow]"
        )
        return 1
    selected_ts = timestamp or entries[0][0]
    try:
        payload = _load_analysis(target, selected_ts)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    suggestions = payload.get("suggestions", [])
    if not suggestions:
        console.print(
            f"[yellow]Analysis {selected_ts} produced no suggestions.[/yellow]"
        )
        return 0

    table = Table(title=f"Analysis Summary ({selected_ts})")
    table.add_column("#", justify="right")
    table.add_column("File")
    table.add_column("Summary")
    table.add_column("Verification")
    for idx, suggestion in enumerate(suggestions, start=1):
        plan = "\n".join(suggestion.get("verification_plan", [])) or "<none>"
        table.add_row(str(idx), suggestion["file"], suggestion["summary"], plan)
    console.print(table)

    if diff_index is None:
        return 0

    logger.info(f"Suggetions acquired: {suggestions}")
    if not (1 <= diff_index <= len(suggestions)):
        console.print("[red]Invalid diff index provided.[/red]")
        return 1
    suggestion = suggestions[diff_index - 1]
    syntax = Syntax(
        suggestion["diff"],
        "diff",
        theme="ansi_dark",
        line_numbers=False,
    )
    panel = Panel(syntax, title=f"Diff for {suggestion['file']}", expand=True)
    console.print(panel)
    return 0
