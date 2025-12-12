"""
Comprehensive tests for data models.

These tests validate schema finalization, serialization, backward compatibility,
and data integrity - critical before any API code is written.
"""

import json
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from agenticontrol.models import (
    CURRENT_SCHEMA_VERSION,
    EventType,
    RiskLevel,
    RiskResult,
    RunMetadata,
    RunStatus,
    TraceEvent,
    ViolationType,
    validate_schema_version,
)


class TestTraceEvent:
    """Test TraceEvent model - the core data structure."""

    def test_trace_event_creation_minimal(self):
        """Test creating a TraceEvent with minimal required fields."""
        run_id = uuid4()
        event = TraceEvent(
            run_id=run_id,
            event_type=EventType.TOOL_START,
        )
        assert event.run_id == run_id
        assert event.event_type == EventType.TOOL_START
        assert event.schema_version == CURRENT_SCHEMA_VERSION
        assert isinstance(event.timestamp, datetime)
        assert event.data == {}

    def test_trace_event_creation_full(self):
        """Test creating a TraceEvent with all fields."""
        run_id = uuid4()
        parent_id = uuid4()
        timestamp = datetime.now(timezone.utc)

        event = TraceEvent(
            run_id=run_id,
            parent_id=parent_id,
            event_type=EventType.TOOL_START,
            timestamp=timestamp,
            tool_name="search",
            tool_input='{"query": "test"}',
            tool_output='{"results": []}',
            token_count=100,
            data={"custom": "value"},
            schema_version="1.0.0",
        )

        assert event.run_id == run_id
        assert event.parent_id == parent_id
        assert event.event_type == EventType.TOOL_START
        assert event.timestamp == timestamp
        assert event.tool_name == "search"
        assert event.tool_input == '{"query": "test"}'
        assert event.tool_output == '{"results": []}'
        assert event.token_count == 100
        assert event.data == {"custom": "value"}
        assert event.schema_version == "1.0.0"

    def test_trace_event_tool_start(self):
        """Test TraceEvent for tool_start event."""
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            tool_name="database_query",
            tool_input='{"sql": "SELECT * FROM users"}',
        )
        assert event.event_type == EventType.TOOL_START
        assert event.tool_name == "database_query"
        assert event.tool_input == '{"sql": "SELECT * FROM users"}'

    def test_trace_event_llm_start(self):
        """Test TraceEvent for llm_start event."""
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.LLM_START,
            llm_prompt="What is the capital of France?",
        )
        assert event.event_type == EventType.LLM_START
        assert event.llm_prompt == "What is the capital of France?"

    def test_trace_event_llm_end_with_tokens(self):
        """Test TraceEvent for llm_end event with token count."""
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.LLM_END,
            llm_response="The capital of France is Paris.",
            token_count=15,
        )
        assert event.event_type == EventType.LLM_END
        assert event.llm_response == "The capital of France is Paris."
        assert event.token_count == 15

    def test_trace_event_timestamp_parsing(self):
        """Test timestamp parsing from various formats."""
        # ISO 8601 string
        iso_str = "2025-01-05T18:00:00Z"
        event1 = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            timestamp=iso_str,
        )
        assert isinstance(event1.timestamp, datetime)

        # datetime object
        dt = datetime.now(timezone.utc)
        event2 = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            timestamp=dt,
        )
        assert event2.timestamp == dt

    def test_trace_event_tool_input_dict_conversion(self):
        """Test that dict tool_input is converted to JSON string."""
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            tool_input={"query": "test", "limit": 10},
        )
        assert isinstance(event.tool_input, str)
        parsed = json.loads(event.tool_input)
        assert parsed == {"query": "test", "limit": 10}

    def test_trace_event_serialization(self):
        """Test serialization to JSON."""
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            tool_name="search",
            timestamp=datetime(2025, 1, 5, 18, 0, 0, tzinfo=timezone.utc),
        )
        json_str = event.model_dump_json()
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data["event_type"] == "tool_start"
        assert data["tool_name"] == "search"
        assert "run_id" in data

    def test_trace_event_deserialization(self):
        """Test deserialization from JSON."""
        run_id = str(uuid4())
        json_data = {
            "run_id": run_id,
            "event_type": "tool_start",
            "tool_name": "search",
            "timestamp": "2025-01-05T18:00:00Z",
            "schema_version": "1.0.0",
        }
        event = TraceEvent.model_validate(json_data)
        assert str(event.run_id) == run_id
        assert event.event_type == EventType.TOOL_START
        assert event.tool_name == "search"

    def test_trace_event_schema_version_default(self):
        """Test that schema_version defaults to current version."""
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
        )
        assert event.schema_version == CURRENT_SCHEMA_VERSION

    def test_trace_event_schema_version_validation(self):
        """Test schema_version pattern validation."""
        # Valid version
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            schema_version="1.0.0",
        )
        assert event.schema_version == "1.0.0"

        # Invalid pattern
        with pytest.raises(ValidationError):
            TraceEvent(
                run_id=uuid4(),
                event_type=EventType.TOOL_START,
                schema_version="invalid",
            )

    def test_trace_event_token_count_validation(self):
        """Test that token_count must be non-negative."""
        # Valid
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.LLM_END,
            token_count=0,
        )
        assert event.token_count == 0

        # Invalid (negative)
        with pytest.raises(ValidationError):
            TraceEvent(
                run_id=uuid4(),
                event_type=EventType.LLM_END,
                token_count=-1,
            )


class TestRunMetadata:
    """Test RunMetadata model."""

    def test_run_metadata_creation(self):
        """Test creating RunMetadata with required fields."""
        run_id = uuid4()
        start_time = datetime.now(timezone.utc)

        metadata = RunMetadata(
            run_id=run_id,
            agent_type="langchain_agent",
            start_time=start_time,
            status=RunStatus.RUNNING,
        )

        assert metadata.run_id == run_id
        assert metadata.agent_type == "langchain_agent"
        assert metadata.start_time == start_time
        assert metadata.status == RunStatus.RUNNING
        assert metadata.user_id is None
        assert metadata.end_time is None

    def test_run_metadata_with_user_id(self):
        """Test RunMetadata with user_id."""
        metadata = RunMetadata(
            run_id=uuid4(),
            agent_type="langchain_agent",
            start_time=datetime.now(timezone.utc),
            status=RunStatus.RUNNING,
            user_id="user_123",
        )
        assert metadata.user_id == "user_123"

    def test_run_metadata_with_costs(self):
        """Test RunMetadata with token count and cost."""
        metadata = RunMetadata(
            run_id=uuid4(),
            agent_type="langchain_agent",
            start_time=datetime.now(timezone.utc),
            status=RunStatus.SUCCESS,
            total_tokens=1000,
            estimated_cost=0.05,
        )
        assert metadata.total_tokens == 1000
        assert metadata.estimated_cost == 0.05

    def test_run_metadata_end_time_validation(self):
        """Test that end_time must be after start_time."""
        start_time = datetime.now(timezone.utc)
        end_time = start_time.replace(second=start_time.second + 1)

        # Valid
        metadata = RunMetadata(
            run_id=uuid4(),
            agent_type="langchain_agent",
            start_time=start_time,
            end_time=end_time,
            status=RunStatus.SUCCESS,
        )
        assert metadata.end_time == end_time

        # Invalid (end_time before start_time)
        with pytest.raises(ValidationError):
            RunMetadata(
                run_id=uuid4(),
                agent_type="langchain_agent",
                start_time=end_time,
                end_time=start_time,
                status=RunStatus.SUCCESS,
            )

    def test_run_metadata_status_enum(self):
        """Test all RunStatus enum values."""
        for status in RunStatus:
            metadata = RunMetadata(
                run_id=uuid4(),
                agent_type="langchain_agent",
                start_time=datetime.now(timezone.utc),
                status=status,
            )
            assert metadata.status == status


class TestRiskResult:
    """Test RiskResult model."""

    def test_risk_result_creation(self):
        """Test creating RiskResult with required fields."""
        risk = RiskResult(
            should_block=True,
            reason="Dangerous SQL command detected",
            risk_level=RiskLevel.HIGH,
            violation_type=ViolationType.POLICY_VIOLATION,
        )

        assert risk.should_block is True
        assert risk.reason == "Dangerous SQL command detected"
        assert risk.risk_level == RiskLevel.HIGH
        assert risk.violation_type == ViolationType.POLICY_VIOLATION
        assert isinstance(risk.detected_at, datetime)

    def test_risk_result_should_not_block(self):
        """Test RiskResult that should not block."""
        risk = RiskResult(
            should_block=False,
            reason="Low risk pattern detected",
            risk_level=RiskLevel.LOW,
            violation_type=ViolationType.POLICY_VIOLATION,
        )
        assert risk.should_block is False
        assert risk.risk_level == RiskLevel.LOW

    def test_risk_result_string_representation(self):
        """Test RiskResult string representation."""
        risk = RiskResult(
            should_block=True,
            reason="Test reason",
            risk_level=RiskLevel.HIGH,
            violation_type=ViolationType.LOOP_DETECTED,
        )
        str_repr = str(risk)
        assert "HIGH" in str_repr
        assert "Test reason" in str_repr

    def test_risk_result_all_violation_types(self):
        """Test all ViolationType enum values."""
        for violation_type in ViolationType:
            risk = RiskResult(
                should_block=True,
                reason=f"Test {violation_type}",
                risk_level=RiskLevel.HIGH,
                violation_type=violation_type,
            )
            assert risk.violation_type == violation_type


class TestSchemaVersioning:
    """Test schema versioning functionality."""

    def test_validate_schema_version(self):
        """Test schema version validation."""
        assert validate_schema_version("1.0.0") is True
        assert validate_schema_version("2.0.0") is False

    def test_current_schema_version(self):
        """Test that CURRENT_SCHEMA_VERSION is valid."""
        assert validate_schema_version(CURRENT_SCHEMA_VERSION) is True


class TestBackwardCompatibility:
    """Test backward compatibility scenarios."""

    def test_trace_event_without_schema_version(self):
        """Test that TraceEvent works without explicit schema_version."""
        # Should default to current version
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
        )
        assert event.schema_version == CURRENT_SCHEMA_VERSION

    def test_trace_event_with_old_schema_version(self):
        """Test handling of old schema versions."""
        # Should accept old version if in SUPPORTED_SCHEMA_VERSIONS
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            schema_version="1.0.0",
        )
        assert event.schema_version == "1.0.0"

    def test_serialization_preserves_schema_version(self):
        """Test that serialization preserves schema_version."""
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            schema_version="1.0.0",
        )
        json_str = event.model_dump_json()
        data = json.loads(json_str)
        assert data["schema_version"] == "1.0.0"


class TestPIISafety:
    """Test PII-safe design requirements."""

    def test_trace_event_no_sensitive_fields(self):
        """Test that TraceEvent doesn't have obvious PII fields."""
        # Verify no fields like 'email', 'ssn', 'credit_card', etc.
        event_fields = set(TraceEvent.model_fields.keys())
        sensitive_fields = {"email", "ssn", "credit_card", "password", "secret"}
        assert not sensitive_fields.intersection(event_fields)

    def test_run_metadata_user_id_optional(self):
        """Test that user_id is optional (can be hashed/tokenized)."""
        metadata = RunMetadata(
            run_id=uuid4(),
            agent_type="langchain_agent",
            start_time=datetime.now(timezone.utc),
            status=RunStatus.RUNNING,
        )
        # user_id should be None, not required
        assert metadata.user_id is None

