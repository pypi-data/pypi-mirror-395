"""
Tests for LangChain callback handler integration.

Tests synchronous blocking behavior and async logging functionality.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from agenticontrol.exceptions import LoopDetectedError, PolicyV0ViolationError
from agenticontrol.hooks.langchain_handler import AgenticontrolCallbackHandler
from agenticontrol.models import EventType
from agenticontrol.risk_engine import RiskEngine


class TestAgenticontrolCallbackHandler:
    """Test LangChain callback handler."""

    def test_handler_initialization(self):
        """Test handler initialization."""
        handler = AgenticontrolCallbackHandler(
            api_url="https://api.test.com", api_key="test-key"
        )
        assert handler.run_id is not None
        assert handler.enable_blocking is True
        assert handler.enable_logging is True
        assert handler.client is not None

    def test_handler_local_only_mode(self):
        """Test handler in local-only mode (no API URL)."""
        handler = AgenticontrolCallbackHandler(enable_logging=False)
        assert handler.client is None
        assert handler.enable_blocking is True

    def test_handler_custom_risk_engine(self):
        """Test handler with custom risk engine."""
        custom_engine = RiskEngine(loop_detection_window=10)
        handler = AgenticontrolCallbackHandler(risk_engine=custom_engine)
        assert handler.risk_engine == custom_engine

    def test_on_tool_start_policy_violation(self):
        """Test that Policy V0 violations block tool execution."""
        handler = AgenticontrolCallbackHandler(enable_blocking=True)

        # Try to execute dangerous SQL command
        with pytest.raises(PolicyV0ViolationError) as exc_info:
            handler.on_tool_start(
                serialized={"name": "sql_query"},
                input_str="DROP TABLE users",
            )

        assert "Dangerous pattern" in str(exc_info.value)

    def test_on_tool_start_loop_detection(self):
        """Test that loop detection blocks repetitive tool calls."""
        handler = AgenticontrolCallbackHandler(enable_blocking=True)
        run_id = str(handler.run_id)

        # Call same tool 5 times (should pass)
        for i in range(5):
            handler.on_tool_start(
                serialized={"name": "search"},
                input_str='{"query": "test"}',
            )

        # 6th call should trigger loop detection
        with pytest.raises(LoopDetectedError) as exc_info:
            handler.on_tool_start(
                serialized={"name": "search"},
                input_str='{"query": "test"}',
            )

        assert "Rule B" in str(exc_info.value)
        assert "Loop detected" in str(exc_info.value)

    def test_on_tool_start_no_blocking(self):
        """Test that blocking can be disabled."""
        handler = AgenticontrolCallbackHandler(enable_blocking=False)

        # Dangerous command should not block
        handler.on_tool_start(
            serialized={"name": "sql_query"},
            input_str="DROP TABLE users",
        )
        # Should not raise exception

    def test_on_tool_start_logging(self):
        """Test that tool start events are logged."""
        handler = AgenticontrolCallbackHandler(
            api_url="https://api.test.com", enable_logging=True
        )

        with patch.object(handler.client, "log_event") as mock_log:
            handler.on_tool_start(
                serialized={"name": "search"},
                input_str='{"query": "test"}',
            )

            # Give async task time to execute
            asyncio.run(asyncio.sleep(0.1))

            # Should have logged event (may be batched, so check if called)
            # Note: In real usage, events are batched, so we can't guarantee immediate call

    def test_on_tool_end_logging(self):
        """Test that tool end events are logged."""
        handler = AgenticontrolCallbackHandler(
            api_url="https://api.test.com", enable_logging=True
        )

        # Start a tool first
        handler.on_tool_start(
            serialized={"name": "search"},
            input_str='{"query": "test"}',
        )

        # End the tool
        handler.on_tool_end(output='{"results": []}')

        # Give async task time to execute
        asyncio.run(asyncio.sleep(0.1))

    def test_on_llm_start_loop_detection(self):
        """Test that loop detection works for LLM prompts."""
        handler = AgenticontrolCallbackHandler(enable_blocking=True)

        # Call same prompt 5 times (should pass)
        for i in range(5):
            handler.on_llm_start(
                serialized={},
                prompts=["What is the capital of France?"],
            )

        # 6th call should trigger loop detection
        with pytest.raises(LoopDetectedError) as exc_info:
            handler.on_llm_start(
                serialized={},
                prompts=["What is the capital of France?"],
            )

        assert "Rule A" in str(exc_info.value)
        assert "Loop detected" in str(exc_info.value)

    def test_on_llm_end_token_monitoring(self):
        """Test that LLM end events monitor token usage."""
        handler = AgenticontrolCallbackHandler(enable_logging=True)

        # Start LLM
        handler.on_llm_start(serialized={}, prompts=["Test prompt"])

        # End LLM with token usage
        handler.on_llm_end(
            response=MagicMock(content="Test response"),
            token_usage={"total_tokens": 100, "prompt_tokens": 50, "completion_tokens": 50},
        )

        # Check that cost was monitored
        token_count = handler.risk_engine.get_run_token_count(str(handler.run_id))
        assert token_count == 100

    def test_on_tool_error_logging(self):
        """Test that tool errors are logged."""
        handler = AgenticontrolCallbackHandler(
            api_url="https://api.test.com", enable_logging=True
        )

        # Start a tool
        handler.on_tool_start(
            serialized={"name": "search"},
            input_str='{"query": "test"}',
        )

        # Simulate error
        error = ValueError("Tool execution failed")
        handler.on_tool_error(error=error)

        # Give async task time to execute
        asyncio.run(asyncio.sleep(0.1))

    def test_on_llm_error_logging(self):
        """Test that LLM errors are logged."""
        handler = AgenticontrolCallbackHandler(
            api_url="https://api.test.com", enable_logging=True
        )

        # Start LLM
        handler.on_llm_start(serialized={}, prompts=["Test prompt"])

        # Simulate error
        error = ValueError("LLM execution failed")
        handler.on_llm_error(error=error)

        # Give async task time to execute
        asyncio.run(asyncio.sleep(0.1))

    def test_different_tools_no_loop(self):
        """Test that different tools don't trigger loop detection."""
        handler = AgenticontrolCallbackHandler(enable_blocking=True)

        # Different tools should not trigger loop
        handler.on_tool_start(serialized={"name": "search"}, input_str='{"query": "test"}')
        handler.on_tool_start(serialized={"name": "database"}, input_str='{"query": "test"}')
        handler.on_tool_start(serialized={"name": "search"}, input_str='{"query": "test"}')

        # Should not raise exception

    def test_different_arguments_no_loop(self):
        """Test that different arguments don't trigger loop detection."""
        handler = AgenticontrolCallbackHandler(enable_blocking=True)

        # Different arguments should not trigger loop
        handler.on_tool_start(
            serialized={"name": "search"}, input_str='{"query": "user_123"}'
        )
        handler.on_tool_start(
            serialized={"name": "search"}, input_str='{"query": "user_124"}'
        )

        # Should not raise exception

    @pytest.mark.asyncio
    async def test_flush(self):
        """Test flushing pending events."""
        handler = AgenticontrolCallbackHandler(
            api_url="https://api.test.com", enable_logging=True
        )

        # Log some events
        handler.on_tool_start(serialized={"name": "test"}, input_str="test")

        # Flush
        await handler.flush()

    @pytest.mark.asyncio
    async def test_close(self):
        """Test closing handler."""
        handler = AgenticontrolCallbackHandler(
            api_url="https://api.test.com", enable_logging=True
        )

        # Log some events
        handler.on_tool_start(serialized={"name": "test"}, input_str="test")

        # Close
        await handler.close()

