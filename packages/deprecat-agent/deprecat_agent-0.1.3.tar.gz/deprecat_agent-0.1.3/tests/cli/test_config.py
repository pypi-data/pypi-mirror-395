"""Tests for init and config commands."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from deprecat.cli.app import app

runner = CliRunner()


def test_init_and_config(tmp_path: Path) -> None:
    """Init should write monitored packages and config should display them."""
    result = runner.invoke(
        app,
        [
            "init",
            str(tmp_path),
        ],
        input="vendor_sdk, stripe\n5\n",
    )
    assert result.exit_code == 0
    config_output = runner.invoke(app, ["config", str(tmp_path), "--show"])
    assert "vendor_sdk" in config_output.stdout
    assert "5" in config_output.stdout


def test_config_updates_packages(tmp_path: Path) -> None:
    """Config command should update monitored packages non-interactively."""
    runner.invoke(
        app,
        ["config", str(tmp_path), "--packages", "stripe,snowflake", "--frequency", "10"],
    )
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
dependencies = ["stripe", "snowflake"]
""",
        encoding="utf-8",
    )
    result = runner.invoke(app, ["config", str(tmp_path), "--show"])
    assert "stripe" in result.stdout and "snowflake" in result.stdout
    assert "10" in result.stdout
    packages_output = runner.invoke(app, ["packages", str(tmp_path)])
    assert "stripe" in packages_output.stdout
