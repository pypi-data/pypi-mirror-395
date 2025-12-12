"""Helpers for writing and reading scan indexes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from deprecat.core.paths import ensure_runtime_dirs, index_file, index_manifest
from deprecat.scanner.context import FileContext, ImportUsage, ScanResult


def _serialize_import(imp: ImportUsage) -> Dict[str, Any]:
    return {
        "module": imp.module,
        "names": imp.names,
        "lineno": imp.lineno,
        "import_type": imp.import_type,
        "snippet": imp.snippet,
        "context": imp.context,
        "category": imp.category,
    }


def _serialize_file(ctx: FileContext, root: Path) -> Dict[str, Any]:
    relative = ctx.path.relative_to(root)
    return {
        "path": str(relative),
        "imports": [_serialize_import(imp) for imp in ctx.imports],
    }


def serialize_scan_result(
    result: ScanResult, root: Path, timestamp: str
) -> Dict[str, Any]:
    return {
        "timestamp": timestamp,
        "root": str(root),
        "file_count": len(result.files),
        "files": [_serialize_file(ctx, root) for ctx in result.files],
    }


def _manifest_entry(path: Path, data: Dict[str, Any], root: Path) -> Dict[str, Any]:
    return {
        "timestamp": data["timestamp"],
        "file_count": data["file_count"],
        "path": str(path.relative_to(root)),
    }


def _load_manifest(manifest_path: Path) -> List[Dict[str, Any]]:
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return []


def _write_manifest(entries: List[Dict[str, Any]], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def write_index(
    result: ScanResult, root: Path, timestamp: Optional[str] = None
) -> Tuple[Dict[str, Any], Path]:
    ensure_runtime_dirs(root)
    path = index_file(timestamp=timestamp, base=root)
    timestamp = path.stem.replace("index-", "")
    data = serialize_scan_result(result, root, timestamp)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    manifest_path = index_manifest(root)
    entries = _load_manifest(manifest_path)
    entry = _manifest_entry(path, data, root)
    entries = [
        existing for existing in entries if existing["timestamp"] != entry["timestamp"]
    ]
    entries.append(entry)
    entries.sort(key=lambda item: item["timestamp"], reverse=True)
    _write_manifest(entries, manifest_path)
    return entry, path


def list_indexes(root: Path) -> List[Dict[str, Any]]:
    manifest_path = index_manifest(root)
    entries = _load_manifest(manifest_path)
    entries.sort(key=lambda item: item["timestamp"], reverse=True)
    return entries


def read_index(root: Path, timestamp: str) -> Dict[str, Any]:
    manifest = list_indexes(root)
    match = next((entry for entry in manifest if entry["timestamp"] == timestamp), None)
    if match is None:
        raise FileNotFoundError(f"No index with timestamp {timestamp}")
    path = root / match["path"]
    return json.loads(path.read_text(encoding="utf-8"))
