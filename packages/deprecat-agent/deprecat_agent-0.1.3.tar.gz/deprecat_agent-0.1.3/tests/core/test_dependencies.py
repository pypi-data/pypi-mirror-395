"""Tests for dependency discovery utilities."""

from __future__ import annotations

from pathlib import Path

from deprecat.core.dependencies import (
    discover_available_tpas,
    normalize_requirement,
)


def test_normalize_requirement_handles_versions() -> None:
    assert normalize_requirement("Foo-Bar>=1.0") == "foo-bar"
    assert normalize_requirement("baz_extra[http]~=2.0") == "baz_extra"


def test_discover_available_tpas(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
dependencies = [
  "Foo-Bar>=1.0",
  "baz_extra[http]~=2.0",
]
[project.optional-dependencies]
dev = [
  "pytest",
]
""",
        encoding="utf-8",
    )
    deps = discover_available_tpas(tmp_path)
    assert deps == ["baz_extra", "foo-bar", "pytest"]
