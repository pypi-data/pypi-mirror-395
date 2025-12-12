"""FastAPI application exposing the analysis endpoints."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from deprecat.backends.models import (
    AnalysisRequest,
    AnalysisResponse,
    PatchSuggestion,
)
from deprecat.backends.utils import get_logger


def create_app() -> FastAPI:
    """Create and configure the FastAPI instance.

    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(title="deprecat", version="0.1.0")
    logger = get_logger(__name__)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", response_model=dict)
    def healthcheck() -> dict:
        """Return a trivial status payload."""

        return {"status": "ok"}

    @app.post("/analyze", response_model=AnalysisResponse)
    def analyze(request: AnalysisRequest) -> AnalysisResponse:
        """Mocked analysis endpoint.

        Args:
            request: Scanner payload posted by the CLI.

        Returns:
            AnalysisResponse containing stubbed patch suggestions.
        """

        suggestions: List[PatchSuggestion] = []
        for file_ctx in request.files:
            if not file_ctx.imports:
                continue
            top_import = file_ctx.imports[0]
            summary = (
                f"Review usage of `{top_import.module}` in {file_ctx.path} "
                f"(line {top_import.lineno})."
            )
            diff_lines = [
                f"--- a/{file_ctx.path}",
                f"+++ b/{file_ctx.path}",
                "@@",
                f"-{top_import.snippet}",
                f"+{top_import.snippet}  # TODO: adjust for updated API",
                "",
                "# Mocked diff only: replace deprecated call",
            ]
            plan = [
                "Run pytest for affected modules.",
                f"Validate HTTP contracts mocking `{top_import.module}`.",
            ]
            suggestions.append(
                PatchSuggestion(
                    file=file_ctx.path,
                    summary=summary,
                    diff="\n".join(diff_lines),
                    verification_plan=plan,
                )
            )
        logger.info("Processed /analyze request with %s files", len(request.files))
        return AnalysisResponse(status="ok", suggestions=suggestions)

    return app


app = create_app()
