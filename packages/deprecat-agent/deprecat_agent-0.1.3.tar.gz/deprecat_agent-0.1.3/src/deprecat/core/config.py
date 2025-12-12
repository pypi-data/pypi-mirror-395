"""Persisted configuration helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Sequence

from .paths import ensure_runtime_dirs, runtime_root


@dataclass
class DeprecatConfig:
    """Serializable configuration state."""

    monitored_packages: List[str] = field(default_factory=list)
    scan_frequency_days: int = 7


def config_path(base: Optional[Path] = None) -> Path:
    """Return the config file location.

    Args:
        base: Optional repository root override.

    Returns:
        Path pointing to `.deprecat/config.json`.
    """
    return runtime_root(base) / "config.json"


def load_config(base: Optional[Path] = None) -> DeprecatConfig:
    """Load configuration from disk.

    Args:
        base: Optional repository root override.

    Returns:
        Parsed DeprecatConfig (defaults applied if file missing).
    """
    path = config_path(base)
    if not path.exists():
        return DeprecatConfig()
    data = json.loads(path.read_text(encoding="utf-8"))
    return DeprecatConfig(
        monitored_packages=data.get("monitored_packages", []),
        scan_frequency_days=data.get("scan_frequency_days", 7),
    )


def save_config(config: DeprecatConfig, base: Optional[Path] = None) -> None:
    """Write configuration to disk.

    Args:
        config: Configuration payload to persist.
        base: Optional repository root override.
    """
    ensure_runtime_dirs(base)
    path = config_path(base)
    path.write_text(
        json.dumps(
            {
                "monitored_packages": config.monitored_packages,
                "scan_frequency_days": config.scan_frequency_days,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def resolve_packages(
    cli_packages: Optional[Sequence[str]], base: Optional[Path] = None
) -> List[str]:
    """Resolve the package allow-list.

    Args:
        cli_packages: Sequence provided on the CLI, if any.
        base: Optional repository root override.

    Returns:
        Sorted list of monitored packages.
    """
    if cli_packages:
        return sorted({pkg.split(".", 1)[0] for pkg in cli_packages if pkg})
    return load_config(base).monitored_packages

