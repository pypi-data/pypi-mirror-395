"""Tests for the FastAPI backend."""

from __future__ import annotations

from fastapi.testclient import TestClient

from deprecat.backends.models import (
    AnalysisRequest,
    FileContextPayload,
    ImportUsagePayload,
)
from deprecat.backends.server import create_app
from deprecat.backends.utils import get_logger

logger = get_logger(__name__)


def test_health_endpoint() -> None:
    """Backend should expose a healthy status endpoint."""
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_endpoint_returns_suggestions() -> None:
    """Posting a minimal request returns mock suggestions."""
    app = create_app()
    client = TestClient(app)
    payload = AnalysisRequest(
        timestamp="20240101-0000",
        root="/repo",
        packages=["vendor_sdk"],
        files=[
            FileContextPayload(
                path="src/app.py",
                imports=[
                    ImportUsagePayload(
                        module="vendor_sdk",
                        names=[],
                        lineno=10,
                        import_type="import",
                        snippet="import vendor_sdk",
                        context="import vendor_sdk",
                        category="third_party",
                    )
                ],
            )
        ],
    )

    response = client.post("/analyze", json=payload.model_dump())
    assert response.status_code == 200
    data = response.json()
    logger.info(f"Payload data: {data}")
    assert data["status"] == "ok"
    assert data["suggestions"], "Expected at least one suggestion"
