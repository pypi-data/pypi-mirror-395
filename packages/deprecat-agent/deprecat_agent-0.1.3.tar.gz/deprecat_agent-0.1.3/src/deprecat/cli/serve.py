"""Helpers for running the backend server via the CLI."""

from __future__ import annotations

import typer
import uvicorn


def serve_backend_command(host: str, port: int, reload: bool) -> None:
    """Run the FastAPI backend using uvicorn.

    Args:
        host: Host interface to bind.
        port: Port to bind.
        reload: Whether to enable auto-reload (development only).
    """

    try:
        uvicorn.run(
            "deprecat.backends.server:app",
            host=host,
            port=port,
            reload=reload,
        )
    except KeyboardInterrupt:
        raise typer.Exit(code=0) from None
