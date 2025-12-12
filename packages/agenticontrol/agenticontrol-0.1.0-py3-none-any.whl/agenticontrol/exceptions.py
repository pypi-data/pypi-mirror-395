"""
Custom exceptions for AGENTICONTROL.

All exceptions are designed for clean CLI display - no messy tracebacks.
"""

from datetime import datetime
from typing import Optional


class PolicyViolationError(Exception):
    """
    Base exception for policy violations.

    Raised when blocking checks fail. This exception is designed to halt
    agent execution immediately with a clean, user-friendly message.

    Example:
        >>> raise PolicyViolationError(
        ...     violation_type="policy_violation",
        ...     reason="Dangerous SQL command detected",
        ...     risk_level="high"
        ... )
    """

    def __init__(
        self,
        violation_type: str,
        reason: str,
        risk_level: str = "high",
        detected_at: Optional[datetime] = None,
    ):
        """
        Initialize PolicyViolationError.

        Args:
            violation_type: Type of violation (e.g., "policy_violation", "loop_detected")
            reason: Human-readable reason for the violation
            risk_level: Risk level ("low" or "high")
            detected_at: When the violation was detected (defaults to now)
        """
        self.violation_type = violation_type
        self.reason = reason
        self.risk_level = risk_level
        self.detected_at = detected_at or datetime.utcnow()
        super().__init__(self.reason)

    def __str__(self) -> str:
        """
        Return clean, user-friendly error message.

        Returns:
            Formatted error message suitable for CLI display
        """
        return f"🛑 AgentiControl Blocked: [{self.violation_type}] - {self.reason}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return (
            f"PolicyViolationError("
            f"violation_type={self.violation_type!r}, "
            f"reason={self.reason!r}, "
            f"risk_level={self.risk_level!r}, "
            f"detected_at={self.detected_at!r})"
        )


class PolicyV0ViolationError(PolicyViolationError):
    """
    Exception for Policy V0 violations.

    Raised when dangerous patterns are detected in tool inputs
    (e.g., SQL DROP TABLE, DELETE commands, PII patterns).

    Example:
        >>> raise PolicyV0ViolationError(
        ...     reason="Dangerous SQL command detected: DROP TABLE users"
        ... )
    """

    def __init__(self, reason: str, detected_at: Optional[datetime] = None):
        """
        Initialize PolicyV0ViolationError.

        Args:
            reason: Human-readable reason for the violation
            detected_at: When the violation was detected (defaults to now)
        """
        super().__init__(
            violation_type="policy_violation",
            reason=reason,
            risk_level="high",
            detected_at=detected_at,
        )

    def __str__(self) -> str:
        """Return clean error message for Policy V0 violations."""
        return f"🛑 AgentiControl Blocked: [Policy V0] - {self.reason}"


class LoopDetectedError(PolicyViolationError):
    """
    Exception for loop detection violations.

    Raised when repetitive patterns are detected in agent execution
    (identical tool calls or LLM prompts repeated N times).

    Example:
        >>> raise LoopDetectedError(
        ...     reason="Loop detected: tool 'search' called 6 times with identical arguments"
        ... )
    """

    def __init__(
        self,
        reason: str,
        rule: str = "unknown",
        detected_at: Optional[datetime] = None,
    ):
        """
        Initialize LoopDetectedError.

        Args:
            reason: Human-readable reason showing the detected loop pattern
            rule: Which loop detection rule triggered (e.g., "Rule A", "Rule B")
            detected_at: When the violation was detected (defaults to now)
        """
        self.rule = rule
        super().__init__(
            violation_type="loop_detected",
            reason=reason,
            risk_level="high",
            detected_at=detected_at,
        )

    def __str__(self) -> str:
        """Return clean error message for loop detection."""
        return f"🛑 AgentiControl Blocked: [Loop Detection - {self.rule}] - {self.reason}"


class CostThresholdExceededError(PolicyViolationError):
    """
    Exception for cost threshold violations.

    Raised when agent execution exceeds cost thresholds.

    Example:
        >>> raise CostThresholdExceededError(
        ...     reason="Cost threshold exceeded: $10.00 (current: $12.50)"
        ... )
    """

    def __init__(
        self,
        reason: str,
        current_cost: float,
        threshold: float,
        detected_at: Optional[datetime] = None,
    ):
        """
        Initialize CostThresholdExceededError.

        Args:
            reason: Human-readable reason for the violation
            current_cost: Current cost in USD
            threshold: Cost threshold in USD
            detected_at: When the violation was detected (defaults to now)
        """
        self.current_cost = current_cost
        self.threshold = threshold
        super().__init__(
            violation_type="cost_threshold",
            reason=reason,
            risk_level="high",
            detected_at=detected_at,
        )

    def __str__(self) -> str:
        """Return clean error message for cost threshold violations."""
        return f"🛑 AgentiControl Blocked: [Cost Threshold] - {self.reason}"

