"""
HTTP Streaming client for Event Streamer SDK.

This module provides a streaming client that connects to the Event Streamer
service's HTTP streaming endpoints to receive real-time event data.
"""

import asyncio
import json
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import aiohttp
from pydantic import ValidationError

from event_streamer_schemas import (
    BulkBatchAcknowledgmentRequest,
    BulkBatchAcknowledgmentResponse,
    ClientHeartbeatRequest,
    ClientHeartbeatResponse,
    ProcessingStatusResponse,
    StreamingError,
    StreamingEventBatch,
    StreamingHeartbeat,
)

if TYPE_CHECKING:
    from .client import EventStreamer


class StreamingClient:
    """HTTP Streaming client for receiving real-time events."""

    def __init__(
        self,
        event_streamer: "EventStreamer",
        subscription_id: int,
        resume_token: str | None = None,
        client_metadata: dict[str, Any] | None = None,
        auto_acknowledge: bool = True,
        batch_ack_interval: float = 3.0,
    ) -> None:
        """
        Initialize the streaming client.

        Args:
            event_streamer: The EventStreamer client instance
            subscription_id: ID of the subscription to stream
            resume_token: Optional resume token to continue from specific position
            client_metadata: Optional client metadata
            auto_acknowledge: Whether to automatically acknowledge events after handler execution
                (default: True)
            batch_ack_interval: Interval in seconds to send batch acknowledgments (default: 3.0)
        """
        self.event_streamer = event_streamer
        self.subscription_id = subscription_id
        self.resume_token = resume_token
        self.client_metadata = client_metadata or {}
        self.auto_acknowledge = auto_acknowledge

        # Connection state
        self.connection_id: str | None = None
        self.stream_url: str | None = None
        self.current_resume_token: str | None = None
        self.is_connected = False
        self.is_running = False

        # Event handlers
        self._event_handlers: dict[str, Callable[[list[dict[str, Any]]], Awaitable[None]]] = {}
        self._global_handler: Callable[[dict[str, Any]], Awaitable[None]] | None = None
        self._heartbeat_handler: Callable[[StreamingHeartbeat], Awaitable[None]] | None = None
        self._error_handler: Callable[[StreamingError], Awaitable[None]] | None = None

        # Streaming task
        self._streaming_task: asyncio.Task[None] | None = None

        # Batch acknowledgment state
        self._pending_batch_ids: list[str] = []
        self._batch_ack_interval: float = batch_ack_interval
        self._batch_ack_task: asyncio.Task[None] | None = None

        # Heartbeat state
        self._heartbeat_interval: float = 30.0  # Send heartbeat every 30 seconds
        self._heartbeat_task: asyncio.Task[None] | None = None
        self._heartbeat_sequence: int = 0

    async def connect(self) -> None:
        """Establish streaming connection using the new single endpoint."""
        if self.is_connected:
            return

        # Build the new single endpoint URL
        base_url = f"{self.event_streamer.service_url}/subscriptions/{self.subscription_id}/stream"

        # Apply resume token if available
        if self.resume_token:
            self.stream_url = f"{base_url}?resume_token={self.resume_token}"
            print(
                f"Streaming connection configured with resume token for "
                f"subscription {self.subscription_id}"
            )
        else:
            self.stream_url = base_url
            print(f"Streaming connection configured for subscription {self.subscription_id}")

        # Set connection as ready - the actual connection happens when streaming starts
        self.is_connected = True

    async def resume(self, resume_token: str) -> None:
        """Resume streaming from a specific position using the new single endpoint."""
        if self.is_connected:
            await self.disconnect()

        # Build the new single endpoint URL with resume token
        self.stream_url = (
            f"{self.event_streamer.service_url}/subscriptions/{self.subscription_id}/stream"
            f"?resume_token={resume_token}"
        )
        self.current_resume_token = resume_token
        self.is_connected = True

        print(f"Streaming resume configured for subscription {self.subscription_id}")

    async def start_streaming(self) -> None:
        """Start streaming events."""
        if not self.is_connected:
            await self.connect()

        if self.is_running:
            return

        # Note: The server will automatically start processing when the streaming connection
        # is established, so we don't need to check processing status beforehand

        self.is_running = True
        self._streaming_task = asyncio.create_task(self._stream_events())

        # Start batch acknowledgment task if auto_acknowledge is enabled
        if self.auto_acknowledge:
            self._batch_ack_task = asyncio.create_task(self._batch_acknowledgment_loop())

        # Start heartbeat task
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

    async def stop_streaming(self) -> None:
        """Stop streaming events."""
        if not self.is_running:
            return

        self.is_running = False
        if self._streaming_task:
            self._streaming_task.cancel()
            try:
                await self._streaming_task
            except asyncio.CancelledError:
                pass
            self._streaming_task = None

        # Stop batch acknowledgment task
        if self._batch_ack_task:
            self._batch_ack_task.cancel()
            try:
                await self._batch_ack_task
            except asyncio.CancelledError:
                pass
            self._batch_ack_task = None

        # Stop heartbeat task
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
            self._heartbeat_task = None

    async def disconnect(self) -> None:
        """Disconnect from streaming."""
        await self.stop_streaming()
        self.is_connected = False
        self.connection_id = None
        self.stream_url = None

    async def _trigger_error_callback(
        self,
        error_code: str,
        error_message: str,
        recoverable: bool = True,
    ) -> None:
        """
        Programmatically trigger the on_error callback for connection-level errors.

        This allows the client to be notified of errors that don't come from
        server-sent error messages (e.g., heartbeat failures, connection drops,
        stream errors like TransferEncodingError).

        Args:
            error_code: Error code identifying the type of error
            error_message: Human-readable error message
            recoverable: Whether the client should attempt to recover/reconnect
        """
        if self._error_handler:
            try:
                error = StreamingError(
                    type="error",
                    connection_id=self.connection_id or "unknown",
                    subscription_id=self.subscription_id,
                    error_code=error_code,
                    error_message=error_message,
                    timestamp=datetime.now(UTC).isoformat(),
                    recoverable=recoverable,
                )
                await self._error_handler(error)
            except Exception as e:
                print(f"Error in error callback: {e}")

    async def _stream_events(self) -> None:
        """Main streaming loop."""
        if not self.stream_url:
            raise ValueError("Stream URL not available")

        timeout = aiohttp.ClientTimeout(total=None)  # No timeout for streaming

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.stream_url) as response:
                    if response.status != 200:
                        raise aiohttp.ClientError(f"Streaming failed with status {response.status}")

                    # Extract connection ID from response headers
                    connection_id_header = response.headers.get("X-Connection-Id")
                    if connection_id_header:
                        self.connection_id = connection_id_header
                        print(f"Connection ID extracted from headers: {self.connection_id}")

                    # Read streaming response line by line for NDJSON format
                    async for line_bytes in (
                        response.content
                    ):  # this iterates each time there is a yield from the server.
                        if not self.is_running:
                            break

                        # Decode and strip the line
                        line_str = line_bytes.decode("utf-8").strip()
                        if not line_str:
                            continue

                        try:
                            await self._process_streaming_message(line_str)
                        except Exception as e:
                            print(f"Error processing streaming message: {e}")
                            continue

        except asyncio.CancelledError:
            print("Streaming cancelled")
        except Exception as e:
            error_type = type(e).__name__
            print(f"Streaming error ({error_type}): {e}")

            # Trigger error callback so client can handle recovery
            await self._trigger_error_callback(
                error_code="STREAM_ERROR",
                error_message=f"Stream error ({error_type}): {e}",
                recoverable=True,
            )

            self.is_running = False
            self.is_connected = False

    async def _process_streaming_message(self, message: str) -> None:
        """Process a streaming message."""
        try:
            data = json.loads(message)
            message_type = data.get("type")

            if message_type == "event_batch":
                await self._handle_event_batch(data)
            elif message_type == "heartbeat":
                await self._handle_heartbeat(data)
            elif message_type == "error":
                await self._handle_error(data)
            else:
                print(f"Unknown message type: {message_type}")

        except json.JSONDecodeError as e:
            print(f"Failed to parse streaming message: {e}")
        except Exception as e:
            print(f"Error processing streaming message: {e}")

    async def _handle_event_batch(self, data: dict[str, Any]) -> None:
        """Handle event batch message."""
        try:
            batch = StreamingEventBatch(**data)

            # Update resume token
            self.current_resume_token = batch.resume_token

            # Process events
            batch_success = True
            for event_name, event_list in batch.events.items():
                try:
                    # Call event handler
                    if event_name in self._event_handlers:
                        await self._event_handlers[event_name](event_list)
                    elif self._global_handler:
                        await self._global_handler({event_name: event_list})

                except Exception as e:
                    print(f"Error handling {event_name} events: {e}")
                    batch_success = False
                    # Don't auto-acknowledge if any handler failed
                    break

            # Auto-acknowledge the entire batch if enabled and all handlers succeeded
            if self.auto_acknowledge and batch_success:
                await self._auto_acknowledge_batch(batch)

        except ValidationError as e:
            print(f"Invalid event batch: {e}")
        except Exception as e:
            print(f"Error handling event batch: {e}")

    async def _handle_heartbeat(self, data: dict[str, Any]) -> None:
        """Handle heartbeat message."""
        try:
            heartbeat = StreamingHeartbeat(**data)
            if self._heartbeat_handler:
                await self._heartbeat_handler(heartbeat)
        except ValidationError as e:
            print(f"Invalid heartbeat: {e}")
        except Exception as e:
            print(f"Error handling heartbeat: {e}")

    async def _handle_error(self, data: dict[str, Any]) -> None:
        """Handle error message."""
        try:
            error = StreamingError(**data)
            if self._error_handler:
                await self._error_handler(error)
            else:
                print(f"Streaming error: {error.error_message}")
        except ValidationError as e:
            print(f"Invalid error message: {e}")
        except Exception as e:
            print(f"Error handling error message: {e}")

    async def _auto_acknowledge_batch(self, batch: StreamingEventBatch) -> None:
        """Automatically acknowledge batch after successful handler execution."""
        try:
            # Add batch to pending acknowledgment queue instead of sending immediately
            self._pending_batch_ids.append(batch.batch_id)
        except Exception as e:
            print(f"Failed to auto-acknowledge batch {batch.batch_id}: {e}")

    def on_event(
        self, event_name: str
    ) -> Callable[
        [Callable[[list[dict[str, Any]]], Awaitable[None]]],
        Callable[[list[dict[str, Any]]], Awaitable[None]],
    ]:
        """
        Decorator to register event handler for specific event type.

        Args:
            event_name: Name of the event to handle (e.g., "Transfer")

        Returns:
            Decorator function

        Example:
            @client.on_event("Transfer")
            async def handle_transfers(events):
                for event in events:
                    print(f"Transfer: {event}")
        """

        def decorator(
            func: Callable[[list[dict[str, Any]]], Awaitable[None]],
        ) -> Callable[[list[dict[str, Any]]], Awaitable[None]]:
            self._event_handlers[event_name] = func
            return func

        return decorator

    def on_all_events(self, handler: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
        """
        Register global event handler that receives all events.

        Args:
            handler: Function to handle all events

        Example:
            @client.on_all_events
            async def handle_all_events(events):
                for event_name, event_list in events.items():
                    print(f"Event {event_name}: {event_list}")
        """
        self._global_handler = handler

    def on_heartbeat(self, handler: Callable[[StreamingHeartbeat], Awaitable[None]]) -> None:
        """
        Register heartbeat handler.

        Args:
            handler: Function to handle heartbeat messages
        """
        self._heartbeat_handler = handler

    def on_error(self, handler: Callable[[StreamingError], Awaitable[None]]) -> None:
        """
        Register error handler.

        Args:
            handler: Function to handle error messages
        """
        self._error_handler = handler

    def get_current_resume_token(self) -> str | None:
        """Get the current resume token."""
        return self.current_resume_token

    async def acknowledge_batch(self, batch_id: str) -> None:
        """
        Acknowledge receipt of a batch of events.

        Args:
            batch_id: ID of the batch to acknowledge

        Raises:
            RuntimeError: If no active connection exists
            Exception: If acknowledgment fails
        """
        if not self.connection_id:
            raise RuntimeError("No active streaming connection")

        try:
            # Acknowledge the batch via the event streamer client using new endpoint
            await self.event_streamer._request(
                "POST",
                f"/subscriptions/{self.subscription_id}/stream/{self.connection_id}/ack/batch",
                json={"batch_id": batch_id},
            )
        except Exception as e:
            print(f"Failed to acknowledge batch {batch_id}: {e}")
            raise

    async def acknowledge_batch_bulk(self, batch_ids: list[str]) -> BulkBatchAcknowledgmentResponse:
        """
        Acknowledge receipt of multiple batches of events.

        Args:
            batch_ids: List of batch IDs to acknowledge

        Returns:
            BulkBatchAcknowledgmentResponse: Response containing acknowledgment results

        Raises:
            RuntimeError: If no active connection exists
            Exception: If acknowledgment fails
        """
        if not self.connection_id:
            raise RuntimeError("No active streaming connection")

        request = BulkBatchAcknowledgmentRequest(
            batch_ids=batch_ids,
            connection_id=self.connection_id,
        )

        try:
            # Send bulk acknowledgment request using new endpoint
            response = await self.event_streamer._request(
                "POST",
                f"/subscriptions/{self.subscription_id}/stream/{self.connection_id}/ack/batch/bulk",
                json=request.model_dump(),
            )
            return BulkBatchAcknowledgmentResponse(**response)
        except Exception as e:
            print(f"Failed to acknowledge batch bulk: {e}")
            raise

    async def _batch_acknowledgment_loop(self) -> None:
        """Background task to send batch acknowledgments every few seconds."""
        while self.is_running:
            try:
                # Wait for the interval
                await asyncio.sleep(self._batch_ack_interval)

                # Send acknowledgments if we have pending batches
                if self._pending_batch_ids:
                    batch_ids_to_ack = self._pending_batch_ids.copy()
                    self._pending_batch_ids.clear()

                    try:
                        response = await self.acknowledge_batch_bulk(batch_ids_to_ack)
                        print(
                            f"Acknowledged {response.acknowledged_batches}/"
                            f"{response.total_batches} batches "
                            f"({response.total_events_acknowledged} events)"
                        )

                        # If some batches failed, add them back to pending queue
                        if response.failed_batch_ids:
                            self._pending_batch_ids.extend(response.failed_batch_ids)

                    except Exception as e:
                        error_msg = str(e).lower()
                        print(f"Batch acknowledgment failed: {e}")

                        # Check for "Connection not found" - server removed our connection
                        connection_gone = (
                            "connection not found" in error_msg
                            or "does not exist" in error_msg
                            or "404" in error_msg
                        )
                        if connection_gone:
                            print(f"Connection {self.connection_id} gone - stopping client")
                            # Trigger error callback so client can handle recovery
                            await self._trigger_error_callback(
                                error_code="CONNECTION_LOST",
                                error_message=(
                                    f"Connection {self.connection_id} not found on server "
                                    "(bulk ack failed)"
                                ),
                                recoverable=True,
                            )
                            self.is_running = False
                            break

                        # Add batches back to pending queue for retry (for other errors)
                        self._pending_batch_ids.extend(batch_ids_to_ack)

            except asyncio.CancelledError:
                # Send any remaining acknowledgments before stopping
                if self._pending_batch_ids:
                    try:
                        await self.acknowledge_batch_bulk(self._pending_batch_ids)
                    except Exception as e:
                        print(f"Failed to send final batch acknowledgments: {e}")
                break
            except Exception as e:
                print(f"Error in batch acknowledgment loop: {e}")
                # Continue the loop despite errors

    async def _heartbeat_loop(self) -> None:
        """Background task to send heartbeats periodically."""
        while self.is_running:
            try:
                # Wait for the interval
                await asyncio.sleep(self._heartbeat_interval)

                # Send heartbeat if we have a connection
                if self.connection_id:
                    try:
                        await self.send_heartbeat()
                    except Exception as e:
                        error_msg = str(e).lower()
                        print(f"Failed to send heartbeat: {e}")

                        # Check for "Connection not found" - server removed our connection
                        # This typically happens when heartbeat times out on server side
                        connection_gone = (
                            "connection not found" in error_msg
                            or "does not exist" in error_msg
                            or "404" in error_msg
                        )
                        if connection_gone:
                            print(f"Connection {self.connection_id} gone - stopping client")
                            # Trigger error callback so client can handle recovery
                            await self._trigger_error_callback(
                                error_code="CONNECTION_LOST",
                                error_message=(
                                    f"Connection {self.connection_id} not found on server "
                                    f"(heartbeat failed)"
                                ),
                                recoverable=True,
                            )
                            self.is_running = False
                            break
                        # Continue sending heartbeats for other errors

            except asyncio.CancelledError:
                print("Heartbeat loop cancelled")
                break
            except Exception as e:
                print(f"Error in heartbeat loop: {e}")
                # Continue the loop despite errors

    async def send_heartbeat(self) -> ClientHeartbeatResponse:
        """
        Send a heartbeat to maintain connection health.

        Returns:
            ClientHeartbeatResponse: The server's heartbeat response

        Raises:
            RuntimeError: If no active connection exists
            Exception: If heartbeat fails
        """
        if not self.connection_id:
            raise RuntimeError("No active streaming connection")

        self._heartbeat_sequence += 1
        from datetime import datetime

        request = ClientHeartbeatRequest(
            timestamp=datetime.now(UTC).isoformat(), sequence_number=self._heartbeat_sequence
        )

        try:
            # Send heartbeat request
            response = await self.event_streamer._request(
                "POST", f"/stream/{self.connection_id}/heartbeat", json=request.model_dump()
            )
            return ClientHeartbeatResponse(**response)
        except Exception as e:
            print(f"Failed to send heartbeat (seq {self._heartbeat_sequence}): {e}")
            raise

    async def check_processing_status(self) -> ProcessingStatusResponse:
        """
        Check if the subscription is currently being processed.

        Returns:
            ProcessingStatusResponse: Processing status information

        Raises:
            Exception: If status check fails
        """
        try:
            response = await self.event_streamer._request(
                "GET", f"/subscriptions/{self.subscription_id}/processing-status"
            )
            return ProcessingStatusResponse(**response)
        except Exception as e:
            print(f"Failed to check processing status for subscription {self.subscription_id}: {e}")
            raise

    async def __aenter__(self) -> "StreamingClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.disconnect()
