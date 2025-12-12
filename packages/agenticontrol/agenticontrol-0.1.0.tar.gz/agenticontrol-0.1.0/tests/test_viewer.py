"""
Tests for Terminal Viewer.

Tests trace event rendering and blocked event display.
"""

import time
from uuid import uuid4

import pytest

from agenticontrol.exceptions import PolicyV0ViolationError
from agenticontrol.local.viewer import TraceViewer
from agenticontrol.models import EventType, TraceEvent


class TestTraceViewer:
    """Test Terminal Viewer functionality."""

    def test_viewer_initialization(self):
        """Test viewer initialization."""
        viewer = TraceViewer()
        assert viewer.running is False
        assert viewer.event_queue is not None

    def test_add_event(self):
        """Test adding events to viewer."""
        viewer = TraceViewer()
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            tool_name="search",
            tool_input='{"query": "test"}',
        )
        viewer.add_event(event)
        assert not viewer.event_queue.empty()

    def test_add_blocked_event(self):
        """Test adding blocked events."""
        viewer = TraceViewer()
        error = PolicyV0ViolationError(reason="Dangerous SQL command detected")
        viewer.add_blocked_event(error)
        assert not viewer.event_queue.empty()

    def test_render_tool_start_event(self):
        """Test rendering tool_start events."""
        viewer = TraceViewer()
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_START,
            tool_name="search",
            tool_input='{"query": "test"}',
        )
        viewer._render_event(event)
        # Check that run tree was created
        assert len(viewer._run_trees) == 1

    def test_render_llm_start_event(self):
        """Test rendering llm_start events."""
        viewer = TraceViewer()
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.LLM_START,
            llm_prompt="What is the capital of France?",
        )
        viewer._render_event(event)
        assert len(viewer._run_trees) == 1

    def test_render_llm_end_event(self):
        """Test rendering llm_end events."""
        viewer = TraceViewer()
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.LLM_END,
            llm_response="The capital of France is Paris.",
            token_count=15,
        )
        viewer._render_event(event)
        assert len(viewer._run_trees) == 1

    def test_render_tool_end_event(self):
        """Test rendering tool_end events."""
        viewer = TraceViewer()
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.TOOL_END,
            tool_output='{"results": []}',
        )
        viewer._render_event(event)
        assert len(viewer._run_trees) == 1

    def test_render_error_event(self):
        """Test rendering error events."""
        viewer = TraceViewer()
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.ERROR,
            data={"error_message": "Tool execution failed"},
        )
        viewer._render_event(event)
        assert len(viewer._run_trees) == 1

    def test_render_blocked_event(self):
        """Test rendering blocked events."""
        viewer = TraceViewer()
        error = PolicyV0ViolationError(reason="Dangerous SQL command detected")
        # This should not raise an exception
        viewer._render_blocked_event(error)

    def test_multiple_runs(self):
        """Test rendering events from multiple runs."""
        viewer = TraceViewer()
        run_id1 = uuid4()
        run_id2 = uuid4()

        event1 = TraceEvent(
            run_id=run_id1,
            event_type=EventType.TOOL_START,
            tool_name="search",
        )
        event2 = TraceEvent(
            run_id=run_id2,
            event_type=EventType.TOOL_START,
            tool_name="database",
        )

        viewer._render_event(event1)
        viewer._render_event(event2)

        assert len(viewer._run_trees) == 2

    def test_viewer_start_stop(self):
        """Test starting and stopping viewer."""
        viewer = TraceViewer()
        viewer.start()
        assert viewer.running is True
        assert viewer._display_thread is not None

        # Give thread time to start
        time.sleep(0.1)

        viewer.stop()
        assert viewer.running is False

    def test_viewer_truncation(self):
        """Test that long text is truncated."""
        viewer = TraceViewer()
        long_prompt = "A" * 200  # Very long prompt
        event = TraceEvent(
            run_id=uuid4(),
            event_type=EventType.LLM_START,
            llm_prompt=long_prompt,
        )
        # Should not raise exception
        viewer._render_event(event)

    def test_get_viewer_singleton(self):
        """Test get_viewer singleton pattern."""
        from agenticontrol.local.viewer import get_viewer

        viewer1 = get_viewer()
        viewer2 = get_viewer()
        # Should return same instance
        assert viewer1 is viewer2

