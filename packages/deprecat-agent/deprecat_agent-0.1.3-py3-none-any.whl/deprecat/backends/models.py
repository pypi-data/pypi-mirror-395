"""Pydantic models shared by the backend service and CLI."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ImportUsagePayload(BaseModel):
    """Represents a single import statement found by the scanner.

    Attributes:
        module: Module name imported (top-level or dotted path).
        names: Items imported from the module (for `from` statements).
        lineno: Line number where the import occurs.
        import_type: Either ``import`` or ``from``.
        snippet: Single-line snippet for the import.
        context: Multi-line context window surrounding the import.
        category: ``stdlib``, ``local``, or ``third_party`` classification.
    """

    module: str
    names: List[str] = Field(default_factory=list)
    lineno: int
    import_type: Literal["import", "from"]
    snippet: str
    context: str
    category: Literal["local", "stdlib", "third_party", "unknown"]


class FileContextPayload(BaseModel):
    """Scanner payload for a single file."""

    path: str
    imports: List[ImportUsagePayload] = Field(default_factory=list)


class AnalysisRequest(BaseModel):
    """Request body sent from the CLI to the backend service."""

    timestamp: str
    root: str
    files: List[FileContextPayload]
    packages: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class PatchSuggestion(BaseModel):
    """Suggested patch/diff returned by the backend."""

    file: str
    summary: str
    diff: str
    verification_plan: List[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    """Response envelope from the backend."""

    status: Literal["ok", "error"]
    suggestions: List[PatchSuggestion] = Field(default_factory=list)
    message: Optional[str] = None
