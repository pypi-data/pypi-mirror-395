"""
Integration tests for backend API endpoints.

Tests FastAPI endpoints with TestClient.
"""

import json
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

try:
    from backend.app.main import app
    _BACKEND_AVAILABLE = True
except ImportError:
    _BACKEND_AVAILABLE = False
    app = None


@pytest.mark.skipif(not _BACKEND_AVAILABLE, reason="Backend dependencies not installed")
class TestBackendAPI:
    """Test backend API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "agenticontrol-api"

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data

    def test_ingest_trace_single_event(self, client):
        """Test ingestion endpoint with single event."""
        payload = {
            "events": [
                {
                    "run_id": str(uuid4()),
                    "event_type": "tool_start",
                    "timestamp": "2025-01-05T18:00:00Z",
                    "tool_name": "search",
                    "tool_input": '{"query": "test"}',
                }
            ]
        }

        response = client.post("/api/v1/ingest/trace", json=payload)
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "accepted"
        assert data["count"] == 1

    def test_ingest_trace_multiple_events(self, client):
        """Test ingestion endpoint with multiple events."""
        payload = {
            "events": [
                {
                    "run_id": str(uuid4()),
                    "event_type": "tool_start",
                    "timestamp": "2025-01-05T18:00:00Z",
                    "tool_name": "search",
                },
                {
                    "run_id": str(uuid4()),
                    "event_type": "tool_end",
                    "timestamp": "2025-01-05T18:00:01Z",
                    "tool_output": '{"results": []}',
                },
            ]
        }

        response = client.post("/api/v1/ingest/trace", json=payload)
        assert response.status_code == 202
        data = response.json()
        assert data["count"] == 2

    def test_ingest_trace_empty_events(self, client):
        """Test ingestion endpoint with empty events list."""
        payload = {"events": []}

        response = client.post("/api/v1/ingest/trace", json=payload)
        assert response.status_code == 202
        data = response.json()
        assert data["count"] == 0

    def test_ingest_trace_invalid_payload(self, client):
        """Test ingestion endpoint with invalid payload."""
        payload = {"events": "not a list"}

        response = client.post("/api/v1/ingest/trace", json=payload)
        assert response.status_code == 422  # Validation error

    def test_ingest_trace_missing_required_fields(self, client):
        """Test ingestion endpoint with missing required fields."""
        payload = {
            "events": [
                {
                    "event_type": "tool_start",
                    # Missing run_id and timestamp
                }
            ]
        }

        response = client.post("/api/v1/ingest/trace", json=payload)
        assert response.status_code == 422  # Validation error

    def test_ingest_trace_with_all_fields(self, client):
        """Test ingestion endpoint with all optional fields."""
        payload = {
            "events": [
                {
                    "run_id": str(uuid4()),
                    "parent_id": str(uuid4()),
                    "event_type": "llm_end",
                    "timestamp": "2025-01-05T18:00:00Z",
                    "llm_prompt": "What is the capital of France?",
                    "llm_response": "The capital of France is Paris.",
                    "token_count": 15,
                    "data": {"custom": "value"},
                    "schema_version": "1.0.0",
                }
            ]
        }

        response = client.post("/api/v1/ingest/trace", json=payload)
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "accepted"

    def test_api_docs_available(self, client):
        """Test that API docs are available."""
        response = client.get("/docs")
        assert response.status_code == 200

        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi = response.json()
        assert "openapi" in openapi
        assert "/api/v1/ingest/trace" in str(openapi)

