"""Pytest configuration for sandboxed temp directories."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Generator

import pytest

from deprecat.core.paths import ensure_runtime_dirs, temp_dir


@pytest.fixture(scope="session", autouse=True)
def configure_tmpdir() -> Generator[None, None, None]:
    root = Path.cwd()
    ensure_runtime_dirs(root)
    tmp_root = temp_dir(root)
    tmp_root.mkdir(parents=True, exist_ok=True)
    for env in ("TMPDIR", "TEMP", "TMP"):
        os.environ[env] = str(tmp_root)
    yield
    for child in tmp_root.glob("pytest-of-*"):
        shutil.rmtree(child, ignore_errors=True)
