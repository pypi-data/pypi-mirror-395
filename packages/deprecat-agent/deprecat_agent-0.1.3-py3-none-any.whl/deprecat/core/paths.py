"""Utilities for resolving project directories used by the CLI."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional


def project_root() -> Path:
    """Return the working tree root (assumes CLI runs from repo root)."""
    return Path.cwd()


def runtime_root(base: Optional[Path] = None) -> Path:
    """Location for runtime data (logs, checkpoints)."""
    root = project_root() if base is None else base
    return root / ".deprecat"


def logs_dir(base: Optional[Path] = None) -> Path:
    return runtime_root(base) / "logs"


def checkpoints_dir(base: Optional[Path] = None) -> Path:
    return runtime_root(base) / "checkpoints"


def temp_dir(base: Optional[Path] = None) -> Path:
    return runtime_root(base) / "tmp"


def index_dir(base: Optional[Path] = None) -> Path:
    """Directory containing timestamped index snapshots."""
    return runtime_root(base) / "indexes"


def index_file(timestamp: Optional[str] = None, base: Optional[Path] = None) -> Path:
    """Return the path for a timestamped index JSON snapshot."""
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return index_dir(base) / f"index-{timestamp}.json"


def index_manifest(base: Optional[Path] = None) -> Path:
    """Manifest path listing available index snapshots."""
    return index_dir(base) / "manifest.json"


def env_file(base: Optional[Path] = None) -> Path:
    root = project_root() if base is None else base
    return root / ".env"


def ensure_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def ensure_runtime_dirs(base: Optional[Path] = None) -> None:
    root = project_root() if base is None else base
    ensure_dirs(
        [
            runtime_root(root),
            logs_dir(root),
            checkpoints_dir(root),
            temp_dir(root),
            index_dir(root),
        ]
    )
