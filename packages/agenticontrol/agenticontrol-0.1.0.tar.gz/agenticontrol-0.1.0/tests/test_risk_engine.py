"""
Comprehensive tests for Risk Engine.

Tests Policy V0 checks, Loop Detection (Rule A & B), and Cost Monitor.
Focus on false positive prevention and normalization precision.
"""

import json
from datetime import datetime

import pytest

from agenticontrol.exceptions import LoopDetectedError, PolicyV0ViolationError
from agenticontrol.models import RiskLevel, ViolationType
from agenticontrol.risk_engine import RiskEngine


class TestPolicyV0Checks:
    """Test Policy V0 dangerous pattern detection."""

    def test_check_tool_input_safe_input(self):
        """Test that safe inputs are not blocked."""
        engine = RiskEngine()
        result = engine.check_tool_input("SELECT * FROM users WHERE id = 1")
        assert result.should_block is False
        assert result.risk_level == RiskLevel.LOW

    def test_check_tool_input_drop_table(self):
        """Test that DROP TABLE is blocked."""
        engine = RiskEngine()
        result = engine.check_tool_input("DROP TABLE users")
        assert result.should_block is True
        assert result.risk_level == RiskLevel.HIGH
        assert result.violation_type == ViolationType.POLICY_VIOLATION

    def test_check_tool_input_drop_database(self):
        """Test that DROP DATABASE is blocked."""
        engine = RiskEngine()
        result = engine.check_tool_input("DROP DATABASE production")
        assert result.should_block is True

    def test_check_tool_input_truncate_table(self):
        """Test that TRUNCATE TABLE is blocked."""
        engine = RiskEngine()
        result = engine.check_tool_input("TRUNCATE TABLE logs")
        assert result.should_block is True

    def test_check_tool_input_dangerous_delete(self):
        """Test that dangerous DELETE commands are blocked."""
        engine = RiskEngine()
        result = engine.check_tool_input("DELETE FROM users WHERE 1=1")
        assert result.should_block is True

    def test_check_tool_input_rm_rf(self):
        """Test that rm -rf / is blocked."""
        engine = RiskEngine()
        result = engine.check_tool_input("rm -rf /")
        assert result.should_block is True

    def test_check_tool_input_case_insensitive(self):
        """Test that pattern matching is case-insensitive."""
        engine = RiskEngine()
        result = engine.check_tool_input("drop table users")
        assert result.should_block is True

    def test_check_tool_input_empty_string(self):
        """Test that empty string is not blocked."""
        engine = RiskEngine()
        result = engine.check_tool_input("")
        assert result.should_block is False

    def test_check_tool_input_none(self):
        """Test that None input is handled."""
        engine = RiskEngine()
        result = engine.check_tool_input(None)
        assert result.should_block is False


class TestLoopDetectionRuleB:
    """Test Loop Detection Rule B: Identical Tool Call."""

    def test_no_loop_different_tools(self):
        """Test that different tools don't trigger loop detection."""
        engine = RiskEngine()
        run_id = "test_run_1"

        # Different tools
        action1 = {"type": "tool_start", "tool_name": "search", "input": '{"query": "test"}'}
        action2 = {"type": "tool_start", "tool_name": "database", "input": '{"query": "test"}'}

        result1 = engine.check_loop(run_id, action1, rule="B")
        assert result1.should_block is False

        result2 = engine.check_loop(run_id, action2, rule="B")
        assert result2.should_block is False

    def test_no_loop_different_arguments(self):
        """Test that different arguments don't trigger loop detection."""
        engine = RiskEngine()
        run_id = "test_run_2"

        # Same tool, different arguments
        action1 = {"type": "tool_start", "tool_name": "search", "input": '{"query": "user_123"}'}
        action2 = {"type": "tool_start", "tool_name": "search", "input": '{"query": "user_124"}'}

        result1 = engine.check_loop(run_id, action1, rule="B")
        assert result1.should_block is False

        result2 = engine.check_loop(run_id, action2, rule="B")
        assert result2.should_block is False

    def test_loop_detected_identical_tool_calls(self):
        """Test that identical tool calls trigger loop detection."""
        engine = RiskEngine()
        run_id = "test_run_3"

        # Same tool with identical arguments (5 times)
        action = {"type": "tool_start", "tool_name": "search", "input": '{"query": "test"}'}

        for i in range(5):
            result = engine.check_loop(run_id, action, rule="B")
            assert result.should_block is False  # First 5 should pass

        # 6th identical call should trigger loop detection
        result = engine.check_loop(run_id, action, rule="B")
        assert result.should_block is True
        assert result.violation_type == ViolationType.LOOP_DETECTED
        assert "Rule B" in result.reason
        assert "search" in result.reason

    def test_loop_detection_normalization(self):
        """Test that normalization prevents false positives."""
        engine = RiskEngine()
        run_id = "test_run_4"

        # Same query with different whitespace/formatting
        action1 = {"type": "tool_start", "tool_name": "search", "input": '{"query": "test"}'}
        action2 = {"type": "tool_start", "tool_name": "search", "input": '{"query":"test"}'}  # No spaces
        action3 = {"type": "tool_start", "tool_name": "search", "input": '{"query": "test"}'}  # Same as action1

        result1 = engine.check_loop(run_id, action1, rule="B")
        assert result1.should_block is False

        result2 = engine.check_loop(run_id, action2, rule="B")
        assert result2.should_block is False

        # After 5 identical calls, should trigger
        for _ in range(4):
            engine.check_loop(run_id, action3, rule="B")

        result3 = engine.check_loop(run_id, action3, rule="B")
        assert result3.should_block is True  # Should detect loop (normalized signatures match)

    def test_loop_detection_with_variable_data(self):
        """Test that variable data (UUIDs, timestamps) doesn't prevent loop detection."""
        engine = RiskEngine()
        run_id = "test_run_5"

        # Same query with different UUIDs (should be normalized to same signature)
        action1 = {
            "type": "tool_start",
            "tool_name": "search",
            "input": '{"query": "test", "user_id": "123e4567-e89b-12d3-a456-426614174000"}',
        }
        action2 = {
            "type": "tool_start",
            "tool_name": "search",
            "input": '{"query": "test", "user_id": "987e6543-e21b-34d5-b789-123456789012"}',
        }

        # These should be considered identical after normalization (UUIDs removed)
        result1 = engine.check_loop(run_id, action1, rule="B")
        assert result1.should_block is False

        # After 5 calls, should trigger loop detection
        for _ in range(4):
            engine.check_loop(run_id, action2, rule="B")

        result2 = engine.check_loop(run_id, action2, rule="B")
        # Should detect loop because normalized signatures match (UUIDs removed)
        assert result2.should_block is True

    def test_loop_detection_legitimate_iteration(self):
        """Test that legitimate iteration (different IDs) doesn't trigger loop."""
        engine = RiskEngine()
        run_id = "test_run_6"

        # Same tool, but iterating over different items (different IDs)
        for i in range(10):
            action = {
                "type": "tool_start",
                "tool_name": "get_user",
                "input": json.dumps({"user_id": f"user_{i}"}),
            }
            result = engine.check_loop(run_id, action, rule="B")
            # Should NOT trigger because user_id differs (not normalized away)
            assert result.should_block is False

    def test_loop_detection_window(self):
        """Test that loop detection uses sliding window correctly."""
        engine = RiskEngine(loop_detection_window=3)
        run_id = "test_run_7"

        # Create pattern: A, B, C, A, B, C (should not trigger with window=3)
        actions = [
            {"type": "tool_start", "tool_name": "action_a", "input": '{"step": "a"}'},
            {"type": "tool_start", "tool_name": "action_b", "input": '{"step": "b"}'},
            {"type": "tool_start", "tool_name": "action_c", "input": '{"step": "c"}'},
        ]

        # First cycle
        for action in actions:
            result = engine.check_loop(run_id, action, rule="B")
            assert result.should_block is False

        # Second cycle (pattern repeats)
        for action in actions:
            result = engine.check_loop(run_id, action, rule="B")
            # Should not trigger because window is only 3, and we're checking individual tools
            assert result.should_block is False


class TestLoopDetectionRuleA:
    """Test Loop Detection Rule A: Identical Thought (LLM prompts)."""

    def test_no_loop_different_prompts(self):
        """Test that different LLM prompts don't trigger loop detection."""
        engine = RiskEngine()
        run_id = "test_run_8"

        action1 = {"type": "llm_start", "prompt": "What is the capital of France?"}
        action2 = {"type": "llm_start", "prompt": "What is the capital of Germany?"}

        result1 = engine.check_loop(run_id, action1, rule="A")
        assert result1.should_block is False

        result2 = engine.check_loop(run_id, action2, rule="A")
        assert result2.should_block is False

    def test_loop_detected_identical_prompts(self):
        """Test that identical LLM prompts trigger loop detection."""
        engine = RiskEngine()
        run_id = "test_run_9"

        action = {"type": "llm_start", "prompt": "What is the capital of France?"}

        # First 5 should pass
        for _ in range(5):
            result = engine.check_loop(run_id, action, rule="A")
            assert result.should_block is False

        # 6th identical prompt should trigger
        result = engine.check_loop(run_id, action, rule="A")
        assert result.should_block is True
        assert result.violation_type == ViolationType.LOOP_DETECTED
        assert "Rule A" in result.reason

    def test_loop_detection_prompt_normalization(self):
        """Test that prompt normalization works correctly."""
        engine = RiskEngine()
        run_id = "test_run_10"

        # Same prompt with different whitespace
        action1 = {"type": "llm_start", "prompt": "What is the capital of France?"}
        action2 = {"type": "llm_start", "prompt": "What  is  the  capital  of  France?"}  # Extra spaces

        result1 = engine.check_loop(run_id, action1, rule="A")
        assert result1.should_block is False

        # After 5 calls, should trigger (normalized signatures match)
        for _ in range(4):
            engine.check_loop(run_id, action2, rule="A")

        result2 = engine.check_loop(run_id, action2, rule="A")
        assert result2.should_block is True  # Should detect loop (normalized prompts match)

    def test_loop_detection_prompt_with_timestamps(self):
        """Test that timestamps in prompts are normalized away."""
        engine = RiskEngine()
        run_id = "test_run_11"

        # Same prompt with different timestamps
        action1 = {"type": "llm_start", "prompt": "Current time: 2025-01-05T10:00:00. What is the capital?"}
        action2 = {"type": "llm_start", "prompt": "Current time: 2025-01-05T11:00:00. What is the capital?"}

        result1 = engine.check_loop(run_id, action1, rule="A")
        assert result1.should_block is False

        # After 5 calls, should trigger (timestamps normalized away)
        for _ in range(4):
            engine.check_loop(run_id, action2, rule="A")

        result2 = engine.check_loop(run_id, action2, rule="A")
        assert result2.should_block is True  # Should detect loop (timestamps removed)


class TestCostMonitor:
    """Test Cost Monitor functionality."""

    def test_monitor_cost_accumulation(self):
        """Test that costs accumulate correctly."""
        engine = RiskEngine()
        run_id = "test_run_12"

        # Monitor costs
        engine.monitor_cost(1000, run_id, model="gpt-4", is_input=True)
        engine.monitor_cost(500, run_id, model="gpt-4", is_input=False)

        token_count = engine.get_run_token_count(run_id)
        cost = engine.get_run_cost(run_id)

        assert token_count == 1500
        assert cost > 0  # Should have some cost

    def test_monitor_cost_different_models(self):
        """Test that different models use different rates."""
        engine = RiskEngine()
        run_id1 = "test_run_13"
        run_id2 = "test_run_14"

        # GPT-4 (more expensive)
        engine.monitor_cost(1000, run_id1, model="gpt-4", is_input=True)

        # GPT-3.5 (cheaper)
        engine.monitor_cost(1000, run_id2, model="gpt-3.5-turbo", is_input=True)

        cost1 = engine.get_run_cost(run_id1)
        cost2 = engine.get_run_cost(run_id2)

        assert cost1 > cost2  # GPT-4 should be more expensive

    def test_monitor_cost_zero_tokens(self):
        """Test that zero tokens don't affect cost."""
        engine = RiskEngine()
        run_id = "test_run_15"

        engine.monitor_cost(0, run_id)
        cost = engine.get_run_cost(run_id)
        assert cost == 0.0

    def test_monitor_cost_custom_rate(self):
        """Test that custom model rates work."""
        engine = RiskEngine()
        run_id = "test_run_16"

        # Set custom rate
        engine.set_model_rate("custom_model", input_rate=0.0001, output_rate=0.0002)

        engine.monitor_cost(1000, run_id, model="custom_model", is_input=True)
        cost = engine.get_run_cost(run_id)

        assert cost == 0.1  # 1000 * 0.0001

    def test_clear_run_context(self):
        """Test that clearing run context works."""
        engine = RiskEngine()
        run_id = "test_run_17"

        engine.monitor_cost(1000, run_id)
        assert engine.get_run_token_count(run_id) == 1000

        engine.clear_run_context(run_id)
        assert engine.get_run_token_count(run_id) == 0


class TestNormalization:
    """Test normalization functions for false positive prevention."""

    def test_normalize_tool_signature_json_sorting(self):
        """Test that JSON keys are sorted for consistent comparison."""
        engine = RiskEngine()
        run_id = "test_run_18"

        # Same data, different key order
        action1 = {"type": "tool_start", "tool_name": "search", "input": '{"query": "test", "limit": 10}'}
        action2 = {"type": "tool_start", "tool_name": "search", "input": '{"limit": 10, "query": "test"}'}

        result1 = engine.check_loop(run_id, action1, rule="B")
        assert result1.should_block is False

        # After 5 calls, should trigger (normalized signatures match)
        for _ in range(4):
            engine.check_loop(run_id, action2, rule="B")

        result2 = engine.check_loop(run_id, action2, rule="B")
        assert result2.should_block is True  # Should match (keys sorted)

    def test_normalize_remove_variable_data(self):
        """Test that variable data patterns are removed."""
        engine = RiskEngine()

        # Test UUID removal
        text1 = "user_123e4567-e89b-12d3-a456-426614174000"
        text2 = "user_987e6543-e21b-34d5-b789-123456789012"
        normalized1 = engine._remove_variable_data(text1)
        normalized2 = engine._remove_variable_data(text2)
        assert normalized1 == normalized2  # UUIDs should be normalized to <UUID>

        # Test timestamp removal
        text3 = "query at 2025-01-05T10:00:00"
        text4 = "query at 2025-01-05T11:00:00"
        normalized3 = engine._remove_variable_data(text3)
        normalized4 = engine._remove_variable_data(text4)
        assert normalized3 == normalized4  # Timestamps should be normalized

    def test_normalize_llm_prompt_whitespace(self):
        """Test that LLM prompt whitespace is normalized."""
        engine = RiskEngine()

        prompt1 = "What is the capital of France?"
        prompt2 = "What  is  the  capital  of  France?"  # Extra spaces
        normalized1 = engine._normalize_llm_prompt(prompt1)
        normalized2 = engine._normalize_llm_prompt(prompt2)
        assert normalized1 == normalized2  # Should match after normalization

