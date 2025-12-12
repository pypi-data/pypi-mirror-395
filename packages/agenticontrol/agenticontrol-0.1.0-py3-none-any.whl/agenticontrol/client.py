"""
Async HTTP client for AGENTICONTROL cloud uplink.

Non-blocking event logging to the cloud API. All HTTP operations are
asynchronous and fire-and-forget to ensure zero impact on agent execution.
"""

import asyncio
import json
from typing import List, Optional
from uuid import uuid4

import aiohttp

from agenticontrol.models import TraceEvent


class AgenticontrolClient:
    """
    Async HTTP client for uploading trace events to the cloud API.

    This client batches events and sends them asynchronously without blocking
    the agent execution. All HTTP operations are fire-and-forget.
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        batch_size: int = 10,
        batch_timeout: float = 2.0,
    ):
        """
        Initialize the async client.

        Args:
            api_url: Base URL for the AGENTICONTROL API (e.g., "https://api.agenticontrol.com")
            api_key: API key for authentication (optional for local-only mode)
            batch_size: Number of events to batch before sending
            batch_timeout: Maximum time to wait before sending a batch (seconds)
        """
        self.api_url = api_url
        self.api_key = api_key
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout

        # Internal queue for batching events
        self._event_queue: List[TraceEvent] = []
        self._queue_lock = asyncio.Lock()
        self._batch_task: Optional[asyncio.Task] = None
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _send_batch(self, events: List[TraceEvent]) -> None:
        """
        Send a batch of events to the cloud API.

        This is a fire-and-forget operation. Errors are logged but don't
        propagate to the caller.

        Args:
            events: List of TraceEvent objects to send
        """
        if not self.api_url or not events:
            return

        try:
            session = await self._get_session()
            url = f"{self.api_url.rstrip('/')}/api/v1/ingest/trace"

            # Prepare payload
            payload = [event.model_dump(mode="json") for event in events]

            # Prepare headers
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Send async POST request (fire-and-forget)
            async with session.post(url, json=payload, headers=headers) as response:
                # We don't wait for or check the response - fire-and-forget
                if response.status not in (200, 202):
                    # Log error but don't raise (non-blocking)
                    error_text = await response.text()
                    print(
                        f"⚠️  AgentiControl: Failed to upload {len(events)} events: "
                        f"{response.status} - {error_text[:100]}"
                    )

        except Exception as e:
            # Log error but don't raise (non-blocking)
            print(f"⚠️  AgentiControl: Error uploading events: {e}")

    async def _batch_worker(self) -> None:
        """
        Background worker that periodically sends batched events.

        This runs in the background and sends events when either:
        - Batch size is reached, or
        - Batch timeout expires
        """
        while True:
            try:
                # Wait for batch timeout or batch size
                await asyncio.sleep(self.batch_timeout)

                async with self._queue_lock:
                    if len(self._event_queue) > 0:
                        # Send batch
                        batch = self._event_queue[: self.batch_size]
                        self._event_queue = self._event_queue[self.batch_size :]

                        # Send asynchronously (fire-and-forget)
                        asyncio.create_task(self._send_batch(batch))

            except asyncio.CancelledError:
                # Flush remaining events before shutdown
                async with self._queue_lock:
                    if self._event_queue:
                        await self._send_batch(self._event_queue)
                        self._event_queue = []
                break
            except Exception as e:
                # Log error but continue
                print(f"⚠️  AgentiControl: Batch worker error: {e}")

    def log_event(self, event: TraceEvent) -> None:
        """
        Log a trace event asynchronously (non-blocking).

        This method adds the event to an internal queue and returns immediately.
        Events are batched and sent in the background.

        Args:
            event: TraceEvent to log

        Example:
            >>> client = AgenticontrolClient(api_url="https://api.agenticontrol.com")
            >>> event = TraceEvent(run_id=uuid4(), event_type=EventType.TOOL_START)
            >>> client.log_event(event)  # Returns immediately, uploads in background
        """
        if not self.api_url:
            # Local-only mode - no upload
            return

        # Add to queue (synchronous operation, very fast)
        try:
            # Try to get the event loop
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # No event loop - create one in a thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Add event to queue
        if loop.is_running():
            # Event loop is running - add to queue synchronously
            asyncio.create_task(self._add_event_to_queue(event))
        else:
            # No event loop running - start one
            loop.run_until_complete(self._add_event_to_queue(event))
            # Start batch worker if not already started
            if self._batch_task is None or self._batch_task.done():
                self._batch_task = loop.create_task(self._batch_worker())

    async def _add_event_to_queue(self, event: TraceEvent) -> None:
        """Add event to queue and trigger batch send if needed."""
        async with self._queue_lock:
            self._event_queue.append(event)

            # If batch size reached, send immediately
            if len(self._event_queue) >= self.batch_size:
                batch = self._event_queue[: self.batch_size]
                self._event_queue = self._event_queue[self.batch_size :]
                # Send asynchronously (fire-and-forget)
                asyncio.create_task(self._send_batch(batch))

    def log_events_batch(self, events: List[TraceEvent]) -> None:
        """
        Log multiple trace events as a batch (non-blocking).

        Args:
            events: List of TraceEvent objects to log
        """
        for event in events:
            self.log_event(event)

    async def flush(self) -> None:
        """
        Flush all pending events immediately.

        This is useful for cleanup or when you want to ensure all events
        are sent before shutdown.
        """
        async with self._queue_lock:
            if self._event_queue:
                await self._send_batch(self._event_queue)
                self._event_queue = []

    async def close(self) -> None:
        """Close the client and flush remaining events."""
        # Cancel batch worker
        if self._batch_task and not self._batch_task.done():
            self._batch_task.cancel()
            try:
                await self._batch_task
            except asyncio.CancelledError:
                pass

        # Flush remaining events
        await self.flush()

        # Close session
        if self._session and not self._session.closed:
            await self._session.close()

    def __del__(self):
        """Cleanup on deletion."""
        if self._session and not self._session.closed:
            # Try to close session (best effort)
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self._session.close())
                else:
                    loop.run_until_complete(self._session.close())
            except Exception:
                pass

