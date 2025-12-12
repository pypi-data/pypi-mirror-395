"""Tests for scan and show commands."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from deprecat.cli.app import app

runner = CliRunner()


def _create_sample_repo(base: Path) -> None:
    pkg = base / "sample"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "app.py").write_text(
        "import os\nfrom math import ceil\nimport vendor_sdk\n", encoding="utf-8"
    )


def test_scan_creates_manifest(tmp_path) -> None:
    _create_sample_repo(tmp_path)
    result = runner.invoke(app, ["scan", str(tmp_path)])
    assert result.exit_code == 0
    manifest = tmp_path / ".deprecat/indexes/manifest.json"
    assert manifest.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data[0]["file_count"] == 2


def test_show_lists_timestamps(tmp_path) -> None:
    _create_sample_repo(tmp_path)
    runner.invoke(app, ["scan", str(tmp_path)])
    result = runner.invoke(app, ["show", str(tmp_path), "--timestamps"])
    assert result.exit_code == 0
    manifest = json.loads(
        (tmp_path / ".deprecat/indexes/manifest.json").read_text(encoding="utf-8")
    )
    ts = manifest[0]["timestamp"]
    detail = runner.invoke(app, ["show", str(tmp_path), "--timestamp", ts])
    assert detail.exit_code == 0
    assert "Index Snapshot" in detail.stdout


def test_scan_with_package_filter(tmp_path) -> None:
    _create_sample_repo(tmp_path)
    runner.invoke(app, ["scan", str(tmp_path), "--packages", "vendor_sdk"])
    manifest = json.loads(
        (tmp_path / ".deprecat/indexes/manifest.json").read_text(encoding="utf-8")
    )
    index_path = tmp_path / manifest[0]["path"]
    snapshot = json.loads(index_path.read_text(encoding="utf-8"))
    app_file = next(
        file_ctx
        for file_ctx in snapshot["files"]
        if file_ctx["path"].endswith("app.py")
    )
    imports = app_file["imports"]
    assert imports and all(
        imp["module"].startswith("vendor_sdk") for imp in imports
    )
