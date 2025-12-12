"""
Terminal Trace Viewer for AGENTICONTROL.

Real-time structured trace output for local debugging using the rich library.
Consumes events from an internal queue and renders them beautifully to the console.
"""

import asyncio
import queue
import threading
from datetime import datetime
from typing import Optional
from uuid import UUID

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.tree import Tree

from agenticontrol.exceptions import PolicyViolationError
from agenticontrol.models import EventType, RiskLevel, TraceEvent


class TraceViewer:
    """
    Terminal viewer for real-time trace visualization.

    Consumes TraceEvent objects from a queue and renders them using rich
    library for beautiful console output.

    Example:
        >>> viewer = TraceViewer()
        >>> viewer.start()
        >>> viewer.add_event(trace_event)
        >>> viewer.stop()
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the trace viewer.

        Args:
            console: Rich Console instance (creates default if None)
        """
        self.console = console or Console()
        self.event_queue: queue.Queue = queue.Queue()
        self.running = False
        self._display_thread: Optional[threading.Thread] = None
        self._tree = Tree("🔍 AgentiControl Trace Viewer")
        self._run_trees: dict[UUID, Tree] = {}

    def add_event(self, event: TraceEvent) -> None:
        """
        Add a trace event to the viewer queue.

        This is thread-safe and non-blocking.

        Args:
            event: TraceEvent to display
        """
        self.event_queue.put(event)

    def _render_event(self, event: TraceEvent) -> None:
        """
        Render a single trace event to the tree.

        Args:
            event: TraceEvent to render
        """
        run_id = event.run_id

        # Get or create run tree
        if run_id not in self._run_trees:
            run_tree = self._tree.add(f"📦 Run: {str(run_id)[:8]}...")
            self._run_trees[run_id] = run_tree
        else:
            run_tree = self._run_trees[run_id]

        # Render based on event type
        if event.event_type == EventType.LLM_START:
            prompt_preview = (
                event.llm_prompt[:100] + "..." if event.llm_prompt and len(event.llm_prompt) > 100
                else event.llm_prompt or ""
            )
            run_tree.add(f"💭 [cyan]Thought:[/cyan] {prompt_preview}")

        elif event.event_type == EventType.LLM_END:
            response_preview = (
                event.llm_response[:100] + "..." if event.llm_response and len(event.llm_response) > 100
                else event.llm_response or ""
            )
            token_info = f" ({event.token_count} tokens)" if event.token_count else ""
            run_tree.add(f"💭 [cyan]Response:[/cyan] {response_preview}{token_info}")

        elif event.event_type == EventType.TOOL_START:
            tool_name = event.tool_name or "unknown"
            input_preview = (
                event.tool_input[:80] + "..." if event.tool_input and len(event.tool_input) > 80
                else event.tool_input or ""
            )
            run_tree.add(f"🛠  [yellow]Tool:[/yellow] {tool_name} - {input_preview}")

        elif event.event_type == EventType.TOOL_END:
            output_preview = (
                event.tool_output[:100] + "..." if event.tool_output and len(event.tool_output) > 100
                else event.tool_output or ""
            )
            run_tree.add(f"→ [green]Output:[/green] {output_preview}")

        elif event.event_type == EventType.ERROR:
            error_data = event.data.get("error_message", "Unknown error")
            run_tree.add(f"❌ [red]Error:[/red] {error_data}")

    def _render_blocked_event(self, error: PolicyViolationError) -> None:
        """
        Render a blocked event (PolicyViolationError) prominently.

        Args:
            error: PolicyViolationError that blocked execution
        """
        # Create a prominent panel for blocked events
        blocked_panel = Panel(
            f"[bold red]🛑 BLOCKED[/bold red]\n\n"
            f"[red]Type:[/red] {error.violation_type}\n"
            f"[red]Reason:[/red] {error.reason}\n"
            f"[red]Risk Level:[/red] {error.risk_level}",
            title="AgentiControl Policy Violation",
            border_style="red",
            title_align="left",
        )
        self.console.print(blocked_panel)

    def _display_worker(self) -> None:
        """Worker thread that continuously renders events."""
        with Live(self._tree, console=self.console, refresh_per_second=4) as live:
            while self.running:
                try:
                    # Get event from queue (with timeout)
                    event = self.event_queue.get(timeout=0.5)

                    # Check if it's a PolicyViolationError
                    if isinstance(event, PolicyViolationError):
                        self._render_blocked_event(event)
                    elif isinstance(event, TraceEvent):
                        self._render_event(event)
                        live.update(self._tree)

                except queue.Empty:
                    # No events, update display anyway
                    live.update(self._tree)
                    continue
                except Exception as e:
                    # Log error but continue
                    self.console.print(f"[red]Viewer error:[/red] {e}")

    def start(self) -> None:
        """Start the viewer display thread."""
        if self.running:
            return

        self.running = True
        self._display_thread = threading.Thread(target=self._display_worker, daemon=True)
        self._display_thread.start()

    def stop(self) -> None:
        """Stop the viewer display thread."""
        self.running = False
        if self._display_thread:
            self._display_thread.join(timeout=2.0)

    def add_blocked_event(self, error: PolicyViolationError) -> None:
        """
        Add a blocked event (PolicyViolationError) to the viewer.

        Args:
            error: PolicyViolationError to display
        """
        self.event_queue.put(error)


# Global viewer instance
_viewer_instance: Optional[TraceViewer] = None


def get_viewer() -> TraceViewer:
    """
    Get the global viewer instance.

    Returns:
        TraceViewer instance
    """
    global _viewer_instance
    if _viewer_instance is None:
        _viewer_instance = TraceViewer()
    return _viewer_instance


def start_viewer() -> TraceViewer:
    """
    Start the global viewer instance.

    Returns:
        Started TraceViewer instance

    Example:
        >>> from agenticontrol.local.viewer import start_viewer
        >>> viewer = start_viewer()
    """
    viewer = get_viewer()
    viewer.start()
    return viewer


def stop_viewer() -> None:
    """Stop the global viewer instance."""
    global _viewer_instance
    if _viewer_instance:
        _viewer_instance.stop()
        _viewer_instance = None

