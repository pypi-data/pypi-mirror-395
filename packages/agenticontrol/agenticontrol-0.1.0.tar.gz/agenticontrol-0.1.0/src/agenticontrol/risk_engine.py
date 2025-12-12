"""
Risk Engine for AGENTICONTROL V0 MVP.

Synchronous blocking checks that run in-memory with zero latency.
This is the gatekeeper that enforces the most critical controls.

All functions in this module must be:
- Synchronous (no async/await)
- Zero-latency (no I/O operations)
- Pure Python (no external dependencies beyond standard library)
"""

import json
import re
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from agenticontrol.exceptions import LoopDetectedError, PolicyV0ViolationError
from agenticontrol.models import RiskLevel, RiskResult, ViolationType


class RiskEngine:
    """
    Risk engine for synchronous blocking checks.

    This engine performs Policy V0 checks, Loop Detection, and Cost Monitoring.
    All checks are synchronous and run in-memory for zero latency.
    """

    def __init__(self, loop_detection_window: int = 5):
        """
        Initialize the risk engine.

        Args:
            loop_detection_window: Number of previous actions to check for loops (default: 5)
        """
        self.loop_detection_window = loop_detection_window
        self._run_contexts: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"actions": [], "token_count": 0, "cost": 0.0}
        )

        # Policy V0: Dangerous patterns to block
        # These patterns are compiled once for performance
        self._dangerous_patterns = [
            # SQL dangerous commands
            re.compile(r'\bDROP\s+TABLE\b', re.IGNORECASE),
            re.compile(r'\bDROP\s+DATABASE\b', re.IGNORECASE),
            re.compile(r'\bTRUNCATE\s+TABLE\b', re.IGNORECASE),
            re.compile(r'\bDELETE\s+FROM\s+\w+\s+WHERE\s+1\s*=\s*1\b', re.IGNORECASE),
            re.compile(r'\bDELETE\s+FROM\s+\w+\s*;\s*$', re.IGNORECASE),
            # File system dangerous operations
            re.compile(r'rm\s+-rf\s+/', re.IGNORECASE),
            re.compile(r'del\s+/[sf]\s+/q', re.IGNORECASE),
            # PII patterns (common sensitive data patterns)
            re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),  # SSN pattern
            re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b'),  # Credit card pattern
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),  # Email (in SQL context)
        ]

        # Model pricing (tokens per USD) - configurable
        # Default: GPT-4 pricing (approximate)
        self._model_rates = {
            "default": {"input": 0.00003, "output": 0.00006},  # $30/$60 per 1M tokens
            "gpt-4": {"input": 0.00003, "output": 0.00006},
            "gpt-3.5-turbo": {"input": 0.0000015, "output": 0.000002},
        }

    def check_tool_input(self, input_str: str) -> RiskResult:
        """
        Policy V0: Check tool input against dangerous patterns.

        This is a synchronous, zero-latency check that blocks dangerous operations
        like SQL DROP TABLE, DELETE commands, and PII patterns.

        Args:
            input_str: The input string to check (tool arguments, SQL query, etc.)

        Returns:
            RiskResult with should_block=True if dangerous pattern detected

        Example:
            >>> engine = RiskEngine()
            >>> result = engine.check_tool_input("DROP TABLE users")
            >>> result.should_block
            True
        """
        if not input_str:
            return RiskResult(
                should_block=False,
                reason="Empty input",
                risk_level=RiskLevel.LOW,
                violation_type=ViolationType.POLICY_VIOLATION,
            )

        # Normalize input for checking (lowercase, strip whitespace)
        normalized_input = input_str.lower().strip()

        # Check against dangerous patterns
        for pattern in self._dangerous_patterns:
            if pattern.search(input_str):  # Use original for regex matching
                matched_pattern = pattern.pattern
                return RiskResult(
                    should_block=True,
                    reason=f"Dangerous pattern detected: {matched_pattern[:50]}...",
                    risk_level=RiskLevel.HIGH,
                    violation_type=ViolationType.POLICY_VIOLATION,
                    detected_at=datetime.utcnow(),
                )

        return RiskResult(
            should_block=False,
            reason="No dangerous patterns detected",
            risk_level=RiskLevel.LOW,
            violation_type=ViolationType.POLICY_VIOLATION,
        )

    def _normalize_tool_signature(self, tool_name: str, tool_input: str) -> str:
        """
        Normalize tool signature for comparison.

        This is the KEY to preventing false positives in loop detection.
        Normalization includes:
        - JSON-sorted keys
        - Whitespace-stripped values
        - Lowercase comparison
        - Remove variable data (timestamps, UUIDs, IDs)

        Args:
            tool_name: Name of the tool
            tool_input: Input arguments (JSON string or dict)

        Returns:
            Normalized signature string for comparison
        """
        try:
            # Parse JSON if string
            if isinstance(tool_input, str):
                try:
                    input_dict = json.loads(tool_input)
                except json.JSONDecodeError:
                    # If not JSON, treat as plain string
                    normalized = tool_input.lower().strip()
                    return f"{tool_name.lower()}:{normalized}"
            else:
                input_dict = tool_input

            if not isinstance(input_dict, dict):
                normalized = str(input_dict).lower().strip()
                return f"{tool_name.lower()}:{normalized}"

            # Normalize dictionary: sort keys, strip whitespace, lowercase values
            normalized_dict = {}
            for key, value in sorted(input_dict.items()):
                normalized_key = key.lower().strip()
                if isinstance(value, str):
                    # Remove variable data patterns (UUIDs, timestamps, IDs)
                    normalized_value = self._remove_variable_data(value)
                    normalized_dict[normalized_key] = normalized_value.lower().strip()
                elif isinstance(value, (int, float)):
                    # Keep numeric values as-is (they're part of the signature)
                    normalized_dict[normalized_key] = value
                else:
                    normalized_dict[normalized_key] = str(value).lower().strip()

            # Create normalized signature
            normalized_str = json.dumps(normalized_dict, sort_keys=True)
            return f"{tool_name.lower()}:{normalized_str}"

        except Exception:
            # Fallback: simple normalization
            normalized = str(tool_input).lower().strip()
            return f"{tool_name.lower()}:{normalized}"

    def _remove_variable_data(self, text: str) -> str:
        """
        Remove variable data patterns from text (UUIDs, timestamps).

        This helps prevent false positives when comparing tool inputs that
        differ only in variable data like UUIDs or timestamps.
        
        NOTE: We do NOT remove user_123 patterns as these represent legitimate
        iteration over different entities, not loops.

        Args:
            text: Text to clean

        Returns:
            Text with variable data patterns replaced
        """
        # Remove UUIDs (full UUID pattern)
        text = re.sub(
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            '<UUID>',
            text,
            flags=re.IGNORECASE,
        )

        # Remove timestamps (ISO 8601 format)
        text = re.sub(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?', '<TIMESTAMP>', text)
        # Remove Unix timestamps (10+ digits)
        text = re.sub(r'\b\d{10,}\b', '<TIMESTAMP>', text)

        return text

    def _normalize_llm_prompt(self, prompt: str) -> str:
        """
        Normalize LLM prompt for comparison.

        Normalization includes:
        - Lowercase
        - Whitespace collapse
        - Remove variable data (timestamps, IDs)

        Args:
            prompt: LLM prompt text

        Returns:
            Normalized prompt string
        """
        if not prompt:
            return ""

        # Remove variable data first
        normalized = self._remove_variable_data(prompt)

        # Lowercase and collapse whitespace
        normalized = normalized.lower()
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        return normalized

    def check_loop(
        self, run_id: str, current_action: Dict[str, Any], rule: str = "A"
    ) -> RiskResult:
        """
        Loop Detection: Check for repetitive patterns in agent execution.

        This implements Rule A (Identical Thought) and Rule B (Identical Tool Call).
        Rule C (Pattern Repetition Trap) is planned for post-MVP.

        Args:
            run_id: Unique identifier for the agent run
            current_action: Current action being checked
                Must contain: 'type' ('tool_start' or 'llm_start'), 'tool_name' (if tool),
                'input' or 'prompt' (depending on type)
            rule: Which rule to apply ('A' for LLM, 'B' for tool, 'both' for both)

        Returns:
            RiskResult with should_block=True if loop detected

        Example:
            >>> engine = RiskEngine()
            >>> action = {'type': 'tool_start', 'tool_name': 'search', 'input': '{"query": "test"}'}
            >>> result = engine.check_loop("run_123", action, rule="B")
        """
        run_context = self._run_contexts[run_id]

        # Normalize current action signature
        action_type = current_action.get("type")
        normalized_signature = None

        # Rule A: Identical Thought Detection (LLM prompts)
        if rule in ("A", "both") and action_type == "llm_start":
            prompt = current_action.get("prompt") or current_action.get("input", "")
            normalized_signature = self._normalize_llm_prompt(prompt)

            if normalized_signature:
                # Count how many times we've seen this exact signature
                count = sum(
                    1
                    for a in run_context["actions"]
                    if a.get("type") == "llm_start"
                    and a.get("normalized_signature") == normalized_signature
                )

                # Trigger if we've seen it N times (current call makes it N+1)
                if count >= self.loop_detection_window:
                    return RiskResult(
                        should_block=True,
                        reason=f"Loop detected (Rule A): Identical LLM prompt repeated {count + 1} times. "
                        f"Prompt: {prompt[:100]}...",
                        risk_level=RiskLevel.HIGH,
                        violation_type=ViolationType.LOOP_DETECTED,
                        detected_at=datetime.utcnow(),
                    )

        # Rule B: Identical Tool Call Detection
        if rule in ("B", "both") and action_type == "tool_start":
            tool_name = current_action.get("tool_name", "")
            tool_input = current_action.get("input", "")

            if not tool_name:
                return RiskResult(
                    should_block=False,
                    reason="No tool name provided",
                    risk_level=RiskLevel.LOW,
                    violation_type=ViolationType.LOOP_DETECTED,
                )

            normalized_signature = self._normalize_tool_signature(tool_name, tool_input)

            if normalized_signature:
                # Count how many times we've seen this exact signature
                count = sum(
                    1
                    for a in run_context["actions"]
                    if a.get("type") == "tool_start"
                    and a.get("normalized_signature") == normalized_signature
                )

                # Trigger if we've seen it N times (current call makes it N+1)
                if count >= self.loop_detection_window:
                    return RiskResult(
                        should_block=True,
                        reason=f"Loop detected (Rule B): Tool '{tool_name}' called {count + 1} times "
                        f"with identical arguments: {tool_input[:100]}...",
                        risk_level=RiskLevel.HIGH,
                        violation_type=ViolationType.LOOP_DETECTED,
                        detected_at=datetime.utcnow(),
                    )

        # Store action in history for future checks
        if normalized_signature:
            action_record = {
                "type": action_type,
                "tool_name": current_action.get("tool_name"),
                "normalized_signature": normalized_signature,
                "timestamp": datetime.utcnow(),
            }
            run_context["actions"].append(action_record)

            # Keep only last N actions (sliding window)
            if len(run_context["actions"]) > self.loop_detection_window * 2:
                run_context["actions"] = run_context["actions"][-self.loop_detection_window * 2 :]

        return RiskResult(
            should_block=False,
            reason="No loop detected",
            risk_level=RiskLevel.LOW,
            violation_type=ViolationType.LOOP_DETECTED,
        )

    def monitor_cost(
        self, token_count: int, run_id: str, model: str = "default", is_input: bool = True
    ) -> None:
        """
        Monitor and accumulate cost for agent runs.

        This accumulates token count and calculates USD cost based on model rates.
        Can be called synchronously or asynchronously (non-blocking).

        Args:
            token_count: Number of tokens used
            run_id: Unique identifier for the agent run
            model: Model name (default: "default")
            is_input: Whether these are input tokens (True) or output tokens (False)

        Example:
            >>> engine = RiskEngine()
            >>> engine.monitor_cost(1000, "run_123", model="gpt-4", is_input=True)
            >>> engine.get_run_cost("run_123")
            0.03
        """
        if token_count <= 0:
            return

        run_context = self._run_contexts[run_id]
        run_context["token_count"] += token_count

        # Get model rates (default if not found)
        rates = self._model_rates.get(model, self._model_rates["default"])
        rate = rates["input"] if is_input else rates["output"]

        # Calculate cost increment
        cost_increment = token_count * rate
        run_context["cost"] += cost_increment

    def get_run_cost(self, run_id: str) -> float:
        """
        Get accumulated cost for a run.

        Args:
            run_id: Unique identifier for the agent run

        Returns:
            Total cost in USD
        """
        return self._run_contexts[run_id]["cost"]

    def get_run_token_count(self, run_id: str) -> int:
        """
        Get accumulated token count for a run.

        Args:
            run_id: Unique identifier for the agent run

        Returns:
            Total token count
        """
        return self._run_contexts[run_id]["token_count"]

    def clear_run_context(self, run_id: str) -> None:
        """
        Clear run context (useful for cleanup).

        Args:
            run_id: Unique identifier for the agent run
        """
        if run_id in self._run_contexts:
            del self._run_contexts[run_id]

    def set_model_rate(self, model: str, input_rate: float, output_rate: float) -> None:
        """
        Set custom model pricing rates.

        Args:
            model: Model name
            input_rate: Cost per input token (USD)
            output_rate: Cost per output token (USD)
        """
        self._model_rates[model] = {"input": input_rate, "output": output_rate}


# Global instance (can be overridden for testing)
_default_engine: Optional[RiskEngine] = None


def get_risk_engine() -> RiskEngine:
    """
    Get the default risk engine instance.

    Returns:
        RiskEngine instance
    """
    global _default_engine
    if _default_engine is None:
        _default_engine = RiskEngine()
    return _default_engine

