"""Simple smoke test to ensure package installs and CLI runs."""

from __future__ import annotations

import subprocess


def test_cli_help() -> None:
    result = subprocess.run(["deprecat", "--help"], capture_output=True, text=True, check=True)
    assert "Usage" in result.stdout
