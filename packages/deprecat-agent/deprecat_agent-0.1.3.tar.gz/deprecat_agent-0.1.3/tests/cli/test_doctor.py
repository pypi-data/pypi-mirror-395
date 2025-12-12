"""Tests for the doctor command."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from deprecat.cli.app import app

runner = CliRunner()


def test_doctor_command_runs(monkeypatch) -> None:
    """Doctor should exit successfully and log results when credentials exist."""
    monkeypatch.setenv("GOOGLE_AI_STUDIO_API_KEY", "test-key")
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Deprecat Doctor Summary" in result.stdout
    log_path = Path(".deprecat/logs/doctor.log")
    assert log_path.exists()
    assert "Gemini" in log_path.read_text(encoding="utf-8")
