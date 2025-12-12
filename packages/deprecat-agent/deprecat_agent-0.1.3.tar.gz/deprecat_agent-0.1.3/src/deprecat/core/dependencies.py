"""Dependency discovery helpers."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import List, Set

EXPRESSION = re.compile(r"^[A-Za-z0-9_.-]+")


def normalize_requirement(requirement: str) -> str:
    """Return canonical package name from a requirement string."""
    match = EXPRESSION.match(requirement.strip())
    return match.group(0).lower() if match else requirement.strip().lower()


def _read_dependencies_from_pyproject(path: Path) -> List[str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project", {})
    deps = list(project.get("dependencies", []))
    optional = project.get("optional-dependencies", {})
    for values in optional.values():
        deps.extend(values)
    return [normalize_requirement(dep) for dep in deps]


def discover_available_tpas(project_root: Path) -> List[str]:
    """Return a sorted set of dependencies declared in project manifests."""
    candidates: Set[str] = set()
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        candidates.update(_read_dependencies_from_pyproject(pyproject))
    return sorted(candidates)
