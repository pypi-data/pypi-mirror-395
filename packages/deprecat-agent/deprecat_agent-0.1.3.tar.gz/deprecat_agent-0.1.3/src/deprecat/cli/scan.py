"""CLI entry for scanning a project and writing index snapshots."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from rich.console import Console
from rich.table import Table

from deprecat.core.config import resolve_packages
from deprecat.core.paths import ensure_runtime_dirs
from deprecat.scanner.context import gather_python_files, scan_paths
from deprecat.scanner.indexer import write_index

console = Console()


def execute_scan(target: Path, packages: Optional[List[str]]) -> Tuple[dict, int]:
    ensure_runtime_dirs(target)
    files = gather_python_files(target)
    package_set = set(packages or [])
    result = scan_paths(files, project_root=target, packages=package_set or None)
    entry, _ = write_index(result, target)
    return entry, len(result.files)


def scan_command(target: Path, packages_option: Optional[List[str]]) -> int:
    packages = resolve_packages(packages_option, target)
    entry, file_count = execute_scan(target, packages)
    table = Table(title=f"Scan Complete ({entry['timestamp']})")
    table.add_column("Snapshot", justify="left")
    table.add_column("Value", justify="left")
    table.add_row("Timestamp", entry["timestamp"])
    table.add_row("Files Indexed", str(file_count))
    table.add_row("Manifest Path", entry["path"])
    console.print(table)
    return 0
