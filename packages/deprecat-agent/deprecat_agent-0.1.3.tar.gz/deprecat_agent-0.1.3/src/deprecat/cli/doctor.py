"""Environment verification command."""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

from rich.console import Console
from rich.table import Table

from deprecat.core.paths import (
    checkpoints_dir,
    ensure_runtime_dirs,
    env_file,
    logs_dir,
)
from deprecat.core.settings import Settings, get_settings

console = Console()


class Status:
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str

    @property
    def ok(self) -> bool:
        return self.status in {Status.PASS, Status.WARN}


PRIVACY_NOTICE = (
    "Deprecat performs scanning locally and only uploads minimal AST-derived context to Gemini 3. "
    "Review the prompts before sending proprietary code."
)


def _check_python_version(min_major: int = 3, min_minor: int = 11) -> CheckResult:
    current = sys.version_info
    if (current.major, current.minor) >= (min_major, min_minor):
        return CheckResult(
            "Python", Status.PASS, f"Running {platform.python_version()}"
        )
    return CheckResult(
        "Python",
        Status.FAIL,
        f"Python {min_major}.{min_minor}+ required, found {platform.python_version()}",
    )


def _check_env_file(path: Path) -> CheckResult:
    if path.exists():
        return CheckResult(".env", Status.PASS, f"Found {path}")
    return CheckResult(
        ".env", Status.WARN, "Missing .env file (using shell environment only)"
    )


def _check_api_key(settings: Settings) -> CheckResult:
    if settings.google_ai_studio_api_key:
        return CheckResult(
            "Gemini Key", Status.PASS, "GOOGLE_AI_STUDIO_API_KEY detected"
        )
    return CheckResult(
        "Gemini Key",
        Status.WARN,
        "GOOGLE_AI_STUDIO_API_KEY not configured; CLI will prompt before remote calls",
    )


def _check_logs_dir(path: Path) -> CheckResult:
    ensure_runtime_dirs()
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        return CheckResult(
            "Log Directory", Status.FAIL, f"Cannot write to {path}: {exc}"
        )
    return CheckResult("Log Directory", Status.PASS, f"Writable at {path}")


def _check_checkpoints_dir(path: Path) -> CheckResult:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return CheckResult("Checkpoints", Status.FAIL, f"Cannot access {path}: {exc}")
    return CheckResult("Checkpoints", Status.PASS, f"Store hand-off notes in {path}")


def run_doctor() -> List[CheckResult]:
    """Run health checks and return their results."""
    ensure_runtime_dirs()
    settings = get_settings()
    results = [
        _check_python_version(),
        _check_env_file(env_file()),
        _check_api_key(settings),
        _check_logs_dir(logs_dir()),
        _check_checkpoints_dir(checkpoints_dir()),
    ]
    return results


def render_results(results: Iterable[CheckResult]) -> None:
    table = Table(title="Deprecat Doctor Summary")
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Details")

    for result in results:
        style = {
            Status.PASS: "green",
            Status.WARN: "yellow",
            Status.FAIL: "red",
        }[result.status]
        table.add_row(result.name, f"[{style}]{result.status}[/{style}]", result.detail)

    console.print(table)
    console.print(f"[cyan]{PRIVACY_NOTICE}[/cyan]")


def log_results(results: Iterable[CheckResult]) -> None:
    log_path = logs_dir() / "doctor.log"
    log_entry = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "overall": "PASS" if all(r.ok for r in results) else "WARN",
        "results": [asdict(r) for r in results],
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(log_entry) + "\n")


def doctor_command() -> int:
    results = run_doctor()
    render_results(results)
    log_results(results)
    if any(r.status == Status.FAIL for r in results):
        console.print("[red]One or more critical checks failed.[/red]")
        return 1
    return 0
