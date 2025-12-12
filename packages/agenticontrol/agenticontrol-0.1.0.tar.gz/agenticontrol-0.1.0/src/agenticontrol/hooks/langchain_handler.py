"""
LangChain callback handler for AGENTICONTROL.

This handler intercepts LangChain agent execution and performs:
1. Synchronous blocking checks (Policy V0, Loop Detection)
2. Asynchronous non-blocking logging (trace events to cloud)
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from langchain_core.callbacks import BaseCallbackHandler

from agenticontrol.client import AgenticontrolClient
from agenticontrol.exceptions import LoopDetectedError, PolicyV0ViolationError
from agenticontrol.models import EventType, TraceEvent
from agenticontrol.risk_engine import RiskEngine, get_risk_engine

# Optional terminal viewer import (may not be available in all environments)
try:
    from agenticontrol.local.viewer import get_viewer
    _VIEWER_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    _VIEWER_AVAILABLE = False
    get_viewer = None


class AgenticontrolCallbackHandler(BaseCallbackHandler):
    """
    LangChain callback handler for AGENTICONTROL.

    This handler integrates with LangChain agents to provide:
    - Synchronous blocking checks (Policy V0, Loop Detection)
    - Asynchronous trace event logging
    - Cost monitoring

    Example:
        >>> from langchain.agents import initialize_agent
        >>> handler = AgenticontrolCallbackHandler(
        ...     api_url="https://api.agenticontrol.com",
        ...     api_key="your-key"
        ... )
        >>> agent = initialize_agent(tools, llm, callbacks=[handler])
        >>> result = agent.run("Your query")
    """

    def __init__(
        self,
        run_id: Optional[UUID] = None,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        risk_engine: Optional[RiskEngine] = None,
        enable_blocking: bool = True,
        enable_logging: bool = True,
    ):
        """
        Initialize the callback handler.

        Args:
            run_id: Unique identifier for this agent run (auto-generated if None)
            api_url: Base URL for AGENTICONTROL API (optional for local-only mode)
            api_key: API key for authentication (optional)
            risk_engine: RiskEngine instance (uses default if None)
            enable_blocking: Whether to enable synchronous blocking checks
            enable_logging: Whether to enable async trace logging
        """
        super().__init__()
        self.run_id = run_id or uuid4()
        self.risk_engine = risk_engine or get_risk_engine()
        self.enable_blocking = enable_blocking
        self.enable_logging = enable_logging

        # Initialize async client for logging
        self.client: Optional[AgenticontrolClient] = None
        if enable_logging and api_url:
            self.client = AgenticontrolClient(api_url=api_url, api_key=api_key)

        # Terminal viewer (optional, for local debugging)
        self.viewer = None
        if _VIEWER_AVAILABLE and get_viewer:
            try:
                self.viewer = get_viewer()
            except Exception:
                # Viewer not available, continue without it
                pass

        # Track current tool/LLM context for event correlation
        self._current_tool_id: Optional[UUID] = None
        self._current_llm_id: Optional[UUID] = None

    def _log_event_async(self, event: TraceEvent) -> None:
        """
        Log event asynchronously (non-blocking).

        This creates a fire-and-forget task that doesn't block execution.
        Also sends events to terminal viewer if available.

        Args:
            event: TraceEvent to log
        """
        # Send to terminal viewer if available (synchronous, very fast)
        if self.viewer:
            try:
                self.viewer.add_event(event)
            except Exception:
                # Viewer error shouldn't break execution
                pass

        # Send to cloud API if enabled
        if not self.enable_logging or not self.client:
            return

        # Fire-and-forget async logging
        try:
            loop = asyncio.get_running_loop()
            # Event loop is running - create task
            asyncio.create_task(self._log_event_task(event))
        except RuntimeError:
            # No event loop - use client's internal handling
            if self.client:
                self.client.log_event(event)

    async def _log_event_task(self, event: TraceEvent) -> None:
        """Async task wrapper for logging."""
        if self.client:
            self.client.log_event(event)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        run_id: Optional[UUID] = None,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Called when a tool starts execution.

        This performs:
        1. Synchronous blocking checks (Policy V0, Loop Detection)
        2. Asynchronous trace event logging

        Args:
            serialized: Serialized tool information
            input_str: Tool input arguments
            run_id: LangChain run ID
            parent_run_id: Parent run ID
            **kwargs: Additional arguments
        """
        tool_name = serialized.get("name", "unknown_tool")

        # --- SYNCHRONOUS BLOCKING CHECKS ---
        if self.enable_blocking:
            try:
                # Policy V0: Check tool input for dangerous patterns
                policy_check = self.risk_engine.check_tool_input(input_str)
                if policy_check.should_block:
                    raise PolicyV0ViolationError(
                        reason=policy_check.reason, detected_at=policy_check.detected_at
                    )

                # Loop Detection: Check for repetitive tool calls
                current_action = {
                    "type": "tool_start",
                    "tool_name": tool_name,
                    "input": input_str,
                }
                loop_check = self.risk_engine.check_loop(
                    str(self.run_id), current_action, rule="B"
                )
                if loop_check.should_block:
                    raise LoopDetectedError(
                        reason=loop_check.reason,
                        rule="Rule B",
                        detected_at=loop_check.detected_at,
                    )

            except (PolicyV0ViolationError, LoopDetectedError) as e:
                # Display blocked event in viewer if available
                if self.viewer:
                    try:
                        self.viewer.add_blocked_event(e)
                    except Exception:
                        pass
                # Re-raise to halt agent execution
                raise

        # --- ASYNCHRONOUS NON-BLOCKING LOGGING ---
        tool_event_id = uuid4()
        self._current_tool_id = tool_event_id

        event = TraceEvent(
            run_id=self.run_id,
            parent_id=parent_run_id,
            event_type=EventType.TOOL_START,
            tool_name=tool_name,
            tool_input=input_str,
            timestamp=datetime.utcnow(),
        )

        self._log_event_async(event)

    def on_tool_end(
        self,
        output: str,
        run_id: Optional[UUID] = None,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Called when a tool finishes execution.

        Args:
            output: Tool output
            run_id: LangChain run ID
            parent_run_id: Parent run ID
            **kwargs: Additional arguments
        """
        if not self.enable_logging:
            return

        event = TraceEvent(
            run_id=self.run_id,
            parent_id=self._current_tool_id or parent_run_id,
            event_type=EventType.TOOL_END,
            tool_output=str(output)[:10000],  # Truncate very long outputs
            timestamp=datetime.utcnow(),
        )

        self._log_event_async(event)
        self._current_tool_id = None

    def on_tool_error(
        self,
        error: Exception,
        run_id: Optional[UUID] = None,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Called when a tool execution errors.

        Args:
            error: Exception that occurred
            run_id: LangChain run ID
            parent_run_id: Parent run ID
            **kwargs: Additional arguments
        """
        if not self.enable_logging:
            return

        event = TraceEvent(
            run_id=self.run_id,
            parent_id=self._current_tool_id or parent_run_id,
            event_type=EventType.ERROR,
            data={"error_type": type(error).__name__, "error_message": str(error)},
            timestamp=datetime.utcnow(),
        )

        self._log_event_async(event)
        self._current_tool_id = None

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        run_id: Optional[UUID] = None,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Called when an LLM starts execution.

        This performs:
        1. Synchronous loop detection (Rule A)
        2. Asynchronous trace event logging

        Args:
            serialized: Serialized LLM information
            prompts: List of prompts sent to LLM
            run_id: LangChain run ID
            parent_run_id: Parent run ID
            **kwargs: Additional arguments
        """
        prompt = prompts[0] if prompts else ""

        # --- SYNCHRONOUS BLOCKING CHECKS ---
        if self.enable_blocking:
            try:
                # Loop Detection: Check for repetitive LLM prompts (Rule A)
                current_action = {
                    "type": "llm_start",
                    "prompt": prompt,
                }
                loop_check = self.risk_engine.check_loop(
                    str(self.run_id), current_action, rule="A"
                )
                if loop_check.should_block:
                    raise LoopDetectedError(
                        reason=loop_check.reason,
                        rule="Rule A",
                        detected_at=loop_check.detected_at,
                    )

            except LoopDetectedError as e:
                # Display blocked event in viewer if available
                if self.viewer:
                    try:
                        self.viewer.add_blocked_event(e)
                    except Exception:
                        pass
                # Re-raise to halt agent execution
                raise

        # --- ASYNCHRONOUS NON-BLOCKING LOGGING ---
        llm_event_id = uuid4()
        self._current_llm_id = llm_event_id

        event = TraceEvent(
            run_id=self.run_id,
            parent_id=parent_run_id,
            event_type=EventType.LLM_START,
            llm_prompt=prompt,
            timestamp=datetime.utcnow(),
        )

        self._log_event_async(event)

    def on_llm_end(
        self,
        response: Any,
        run_id: Optional[UUID] = None,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Called when an LLM finishes execution.

        This also monitors token usage for cost tracking.

        Args:
            response: LLM response
            run_id: LangChain run ID
            parent_run_id: Parent run ID
            **kwargs: Additional arguments (may include token_usage)
        """
        if not self.enable_logging:
            return

        # Extract token usage if available
        token_usage = kwargs.get("token_usage", {})
        token_count = None
        if isinstance(token_usage, dict):
            token_count = token_usage.get("total_tokens") or (
                token_usage.get("prompt_tokens", 0) + token_usage.get("completion_tokens", 0)
            )

        # Monitor cost if token count available
        if token_count:
            self.risk_engine.monitor_cost(
                token_count, str(self.run_id), model=kwargs.get("model", "default")
            )

        # Extract response text
        response_text = ""
        if hasattr(response, "content"):
            response_text = str(response.content)
        elif isinstance(response, str):
            response_text = response
        else:
            response_text = str(response)

        event = TraceEvent(
            run_id=self.run_id,
            parent_id=self._current_llm_id or parent_run_id,
            event_type=EventType.LLM_END,
            llm_response=response_text[:10000],  # Truncate very long responses
            token_count=token_count,
            timestamp=datetime.utcnow(),
        )

        self._log_event_async(event)
        self._current_llm_id = None

    def on_llm_error(
        self,
        error: Exception,
        run_id: Optional[UUID] = None,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Called when an LLM execution errors.

        Args:
            error: Exception that occurred
            run_id: LangChain run ID
            parent_run_id: Parent run ID
            **kwargs: Additional arguments
        """
        if not self.enable_logging:
            return

        event = TraceEvent(
            run_id=self.run_id,
            parent_id=self._current_llm_id or parent_run_id,
            event_type=EventType.ERROR,
            data={"error_type": type(error).__name__, "error_message": str(error)},
            timestamp=datetime.utcnow(),
        )

        self._log_event_async(event)
        self._current_llm_id = None

    async def flush(self) -> None:
        """Flush all pending trace events."""
        if self.client:
            await self.client.flush()

    async def close(self) -> None:
        """Close the handler and flush remaining events."""
        if self.client:
            await self.client.close()

