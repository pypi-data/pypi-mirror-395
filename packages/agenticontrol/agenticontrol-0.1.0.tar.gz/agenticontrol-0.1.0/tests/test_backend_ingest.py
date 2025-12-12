"""
Tests for backend ingestion endpoint.

Tests the FastAPI ingestion endpoint without requiring actual Supabase/Clerk setup.
"""

import json
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

# Mock dependencies before importing
import sys
sys.modules['supabase'] = MagicMock()
sys.modules['clerk_sdk_python'] = MagicMock()
sys.modules['jwt'] = MagicMock()

# Now import the app
try:
    from backend.app.main import app
    _APP_AVAILABLE = True
except ImportError as e:
    _APP_AVAILABLE = False
    print(f"Warning: Could not import backend app: {e}")


@pytest.mark.skipif(not _APP_AVAILABLE, reason="Backend dependencies not installed")
class TestIngestEndpoint:
    """Test trace ingestion endpoint."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "service" in response.json()

    def test_ingest_trace_no_supabase(self, client):
        """Test ingestion endpoint without Supabase (local mode)."""
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
        assert "count" in data

    @patch("backend.app.api.v1.ingest.create_client")
    def test_ingest_trace_with_supabase(self, mock_create_client, client):
        """Test ingestion endpoint with Supabase."""
        # Mock Supabase client
        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_create_client.return_value = mock_supabase

        # Set environment variables
        import os
        os.environ["SUPABASE_URL"] = "https://test.supabase.co"
        os.environ["SUPABASE_KEY"] = "test-key"

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

        # Verify Supabase was called
        mock_table.insert.assert_called()

    def test_ingest_trace_multiple_events(self, client):
        """Test ingestion with multiple events."""
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

    def test_ingest_trace_invalid_payload(self, client):
        """Test ingestion with invalid payload."""
        payload = {"events": "not a list"}

        response = client.post("/api/v1/ingest/trace", json=payload)
        # Should return 422 validation error
        assert response.status_code == 422

    def test_ingest_trace_empty_events(self, client):
        """Test ingestion with empty events list."""
        payload = {"events": []}

        response = client.post("/api/v1/ingest/trace", json=payload)
        assert response.status_code == 202
        data = response.json()
        assert data["count"] == 0

