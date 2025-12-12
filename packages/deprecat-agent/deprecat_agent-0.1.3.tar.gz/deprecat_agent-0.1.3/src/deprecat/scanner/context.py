"""Build minimal context payloads from Python source files."""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set


@dataclass
class ImportUsage:
    """Structured data for a single import statement."""

    module: str
    names: List[str] = field(default_factory=list)
    lineno: int = 0
    import_type: str = "import"
    snippet: str = ""
    context: str = ""
    category: str = "unknown"


@dataclass
class FileContext:
    """Per-file view of imports collected during a scan."""

    path: Path
    imports: List[ImportUsage] = field(default_factory=list)


@dataclass
class ScanResult:
    """Aggregated scan payload."""

    files: List[FileContext] = field(default_factory=list)


STDLIB_MODULES = set(getattr(sys, "stdlib_module_names", []))
SKIP_PARTS = {".venv", "venv", "__pycache__", ".deprecat"}


class ImportCollector(ast.NodeVisitor):
    """Visits AST nodes to gather import statements."""

    def __init__(self, lines: List[str], project_root: Path) -> None:
        self.lines = lines
        self.project_root = project_root
        self.imports: List[ImportUsage] = []

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for alias in node.names:
            self.imports.append(
                self._build_usage(
                    module=alias.name,
                    names=[],
                    lineno=node.lineno,
                    import_type="import",
                )
            )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        module = node.module or ""
        names = [alias.name for alias in node.names]
        self.imports.append(
            self._build_usage(
                module=module,
                names=names,
                lineno=node.lineno,
                import_type="from",
            )
        )

    def _build_usage(
        self, module: str, names: List[str], lineno: int, import_type: str
    ) -> ImportUsage:
        snippet = (
            self.lines[lineno - 1].strip() if 0 < lineno <= len(self.lines) else ""
        )
        window = 2
        start = max(lineno - 1 - window, 0)
        end = min(lineno + window, len(self.lines))
        context = "\n".join(self.lines[start:end])
        category = classify_dependency(module, self.project_root)
        return ImportUsage(
            module=module,
            names=names,
            lineno=lineno,
            import_type=import_type,
            snippet=snippet,
            context=context,
            category=category,
        )


def classify_dependency(module: str, project_root: Path) -> str:
    """Return dependency category for an import.

    Args:
        module: Module path extracted from the AST node.
        project_root: Repository root used to resolve local modules.

    Returns:
        Category label such as ``local`` or ``third_party``.
    """

    if not module:
        return "local"
    if module.startswith("."):
        return "local"
    top_level = module.split(".", 1)[0]
    if top_level in STDLIB_MODULES:
        return "stdlib"
    candidate = project_root / top_level.replace(".", "/")
    if candidate.with_suffix(".py").exists() or (candidate / "__init__.py").exists():
        return "local"
    return "third_party"


def parse_file(
    path: Path, project_root: Path, packages: Optional[Set[str]] = None
) -> FileContext:
    """Parse a Python file and return filtered import metadata.

    Args:
        path: File path to inspect.
        project_root: Repository root used for classification.
        packages: Optional allow-list of monitored packages.

    Returns:
        FileContext describing the file's imports.
    """
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    collector = ImportCollector(text.splitlines(), project_root)
    collector.visit(tree)
    imports = filter_imports(collector.imports, packages)
    return FileContext(path=path, imports=imports)


def filter_imports(
    imports: Iterable[ImportUsage], packages: Optional[Set[str]]
) -> List[ImportUsage]:
    """Filter import usages based on package selection.

    Args:
        imports: Collection of ImportUsage objects.
        packages: Optional allow-list; defaults to third-party imports.

    Returns:
        Filtered list of monitored import usages.
    """
    if packages:
        allowed = {pkg.split(".", 1)[0] for pkg in packages}
        return [
            imp
            for imp in imports
            if imp.module.split(".", 1)[0] in allowed
            and imp.category == "third_party"
        ]
    return [imp for imp in imports if imp.category == "third_party"]


def scan_paths(
    paths: Sequence[Path], project_root: Path, packages: Optional[Set[str]] = None
) -> ScanResult:
    """Scan a list of files and return structured results.

    Args:
        paths: Iterable of Python files to analyze.
        project_root: Repository root used for classification.
        packages: Optional allow-list of monitored packages.

    Returns:
        ScanResult covering all processed files.
    """
    files: List[FileContext] = []
    for path in paths:
        try:
            files.append(parse_file(path, project_root, packages))
        except (SyntaxError, UnicodeDecodeError):
            continue
    return ScanResult(files=files)


def gather_python_files(root: Path) -> List[Path]:
    """Return eligible Python files skipping venv/cache directories.

    Args:
        root: Repository root to search.

    Returns:
        List of Python file paths under the root.
    """
    files: List[Path] = []
    for path in root.rglob("*.py"):
        try:
            parts = path.relative_to(root).parts
        except ValueError:
            parts = path.parts
        if any(part in SKIP_PARTS for part in parts):
            continue
        files.append(path)
    return files
