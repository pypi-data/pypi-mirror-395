"""
Data Models for AGENTICONTROL V0 MVP.

CRITICAL: This schema must be finalized before any API code is written.
This is the foundation of the data moat. Changing the schema after collecting
thousands of traces is extremely costly.

Schema Version: 1.0.0
Last Updated: 2025-01-05
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class EventType(str, Enum):
    """Types of trace events that can be recorded."""

    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    LLM_START = "llm_start"
    LLM_END = "llm_end"
    ERROR = "error"


class RunStatus(str, Enum):
    """Status of an agent run."""

    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    BLOCKED = "blocked"


class RiskLevel(str, Enum):
    """Risk level for detected issues."""

    LOW = "low"
    HIGH = "high"


class ViolationType(str, Enum):
    """Type of policy violation detected."""

    POLICY_VIOLATION = "policy_violation"
    LOOP_DETECTED = "loop_detected"
    COST_THRESHOLD = "cost_threshold"


class TraceEvent(BaseModel):
    """
    Standardized unit of all agent activity.

    This is the core data structure for tracing agent execution. All events
    are uniform for both Terminal Viewer and Cloud API consumption.

    Schema Version: 1.0.0
    PII-Safe: This model does not store sensitive user data in plain text.
    All PII should be hashed or tokenized before storage.

    Example:
        >>> event = TraceEvent(
        ...     run_id=uuid4(),
        ...     event_type=EventType.TOOL_START,
        ...     tool_name="search",
        ...     tool_input='{"query": "test"}',
        ...     timestamp=datetime.now()
        ... )
        >>> event.model_dump_json()
    """

    # Core identification fields
    run_id: UUID = Field(
        ...,
        description="Unique identifier for the agent run this event belongs to",
    )
    parent_id: Optional[UUID] = Field(
        None,
        description="Parent event ID for hierarchical event relationships",
    )
    event_type: EventType = Field(
        ...,
        description="Type of event (tool_start, tool_end, llm_start, llm_end, error)",
    )

    # Timestamp
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="ISO 8601 timestamp of when the event occurred",
    )

    # Event-specific data fields (optional, populated based on event_type)
    tool_name: Optional[str] = Field(
        None,
        description="Name of the tool being called (for tool_start/tool_end events)",
        max_length=255,
    )
    tool_input: Optional[str] = Field(
        None,
        description="Input arguments to the tool (JSON string, for tool_start events)",
    )
    tool_output: Optional[str] = Field(
        None,
        description="Output from the tool (for tool_end events)",
    )
    llm_prompt: Optional[str] = Field(
        None,
        description="Prompt sent to LLM (for llm_start events)",
    )
    llm_response: Optional[str] = Field(
        None,
        description="Response from LLM (for llm_end events)",
    )
    token_count: Optional[int] = Field(
        None,
        ge=0,
        description="Number of tokens used (for llm_end events)",
    )

    # Flexible data field for additional context
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional flexible JSON data for event context",
    )

    # Schema versioning - CRITICAL for future migrations
    schema_version: str = Field(
        default="1.0.0",
        description="Schema version for backward compatibility and migrations",
        pattern=r"^\d+\.\d+\.\d+$",
    )

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v: Any) -> datetime:
        """Parse timestamp from various formats."""
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            # Try ISO 8601 format
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid timestamp format: {v}")
        raise ValueError(f"Invalid timestamp type: {type(v)}")

    @field_validator("tool_input", "tool_output", mode="before")
    @classmethod
    def validate_json_strings(cls, v: Any) -> Optional[str]:
        """Validate that tool_input/output are strings if provided."""
        if v is None:
            return None
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            import json

            return json.dumps(v)
        raise ValueError(f"tool_input/output must be string or dict, got {type(v)}")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "run_id": "123e4567-e89b-12d3-a456-426614174000",
                "parent_id": "123e4567-e89b-12d3-a456-426614174001",
                "event_type": "tool_start",
                "timestamp": "2025-01-05T18:00:00Z",
                "tool_name": "search",
                "tool_input": '{"query": "test"}',
                "schema_version": "1.0.0",
                "data": {},
            }
        }
    )

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize datetime to ISO 8601 string."""
        return value.isoformat()

    @field_serializer("run_id", "parent_id", check_fields=False)
    def serialize_uuid(self, value: UUID | None) -> str | None:
        """Serialize UUID to string."""
        return str(value) if value else None


class RunMetadata(BaseModel):
    """
    High-level metadata for an agent run.

    Used for the Runs Table view and run-level analytics.

    Example:
        >>> metadata = RunMetadata(
        ...     run_id=uuid4(),
        ...     agent_type="langchain_agent",
        ...     start_time=datetime.now(),
        ...     status=RunStatus.RUNNING
        ... )
    """

    run_id: UUID = Field(
        ...,
        description="Unique identifier for this agent run",
    )
    agent_type: str = Field(
        ...,
        description="Type of agent (e.g., 'langchain_agent', 'custom_agent')",
        max_length=100,
    )
    user_id: Optional[str] = Field(
        None,
        description="User ID from authentication system (Clerk user ID)",
        max_length=255,
    )
    start_time: datetime = Field(
        ...,
        description="When the agent run started",
    )
    end_time: Optional[datetime] = Field(
        None,
        description="When the agent run completed (None if still running)",
    )
    status: RunStatus = Field(
        ...,
        description="Current status of the run",
    )
    total_tokens: Optional[int] = Field(
        None,
        ge=0,
        description="Total tokens consumed during this run",
    )
    estimated_cost: Optional[float] = Field(
        None,
        ge=0.0,
        description="Estimated cost in USD for this run",
    )

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate that end_time is after start_time if provided."""
        if v is not None and "start_time" in info.data:
            if v < info.data["start_time"]:
                raise ValueError("end_time must be after start_time")
        return v

    model_config = ConfigDict()

    @field_serializer("start_time", "end_time")
    def serialize_datetime(self, value: datetime | None) -> str | None:
        """Serialize datetime to ISO 8601 string."""
        return value.isoformat() if value else None

    @field_serializer("run_id")
    def serialize_uuid(self, value: UUID) -> str:
        """Serialize UUID to string."""
        return str(value)


class RiskResult(BaseModel):
    """
    Output of the Policy/Heuristic Engines.

    Represents the result of a risk check (Policy V0, Loop Detection, Cost Monitor).

    Example:
        >>> risk = RiskResult(
        ...     should_block=True,
        ...     reason="Dangerous SQL command detected: DROP TABLE",
        ...     risk_level=RiskLevel.HIGH,
        ...     violation_type=ViolationType.POLICY_VIOLATION
        ... )
    """

    should_block: bool = Field(
        ...,
        description="Whether this risk should block agent execution",
    )
    reason: str = Field(
        ...,
        description="Human-readable reason for the risk assessment",
        max_length=1000,
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Severity level of the risk",
    )
    detected_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this risk was detected",
    )
    violation_type: ViolationType = Field(
        ...,
        description="Type of violation detected",
    )

    model_config = ConfigDict()

    @field_serializer("detected_at")
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO 8601 string."""
        return value.isoformat()

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"[{self.risk_level.upper()}] {self.reason}"


# Schema versioning constants
CURRENT_SCHEMA_VERSION = "1.0.0"
SUPPORTED_SCHEMA_VERSIONS = ["1.0.0"]


def validate_schema_version(version: str) -> bool:
    """
    Validate that a schema version is supported.

    Args:
        version: Schema version string (e.g., "1.0.0")

    Returns:
        True if version is supported, False otherwise

    Example:
        >>> validate_schema_version("1.0.0")
        True
        >>> validate_schema_version("2.0.0")
        False
    """
    return version in SUPPORTED_SCHEMA_VERSIONS

