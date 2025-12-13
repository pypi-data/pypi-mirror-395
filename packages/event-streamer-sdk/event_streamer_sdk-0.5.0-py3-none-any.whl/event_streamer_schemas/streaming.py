"""
Streaming models for Event Streamer service.

These models handle streaming connection management,
resume capabilities, and streaming event delivery.
"""

from typing import Any

from pydantic import BaseModel, Field


class StreamingConnectionRequest(BaseModel):
    """Request model for creating a streaming connection."""

    subscription_id: int = Field(description="ID of the subscription to stream", examples=[123])
    resume_token: str | None = Field(
        default=None,
        description="Optional resume token to continue from specific position",
        examples=["rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi..."],
    )
    client_metadata: dict[str, str | int | bool] | None = Field(
        default=None,
        description="Optional client metadata",
        examples=[{"client_version": "1.0.0", "features": ["resume", "heartbeat"]}],
    )


class StreamingConnectionResponse(BaseModel):
    """Response model for streaming connection creation."""

    connection_id: str = Field(
        description="Unique connection identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    subscription_id: int = Field(description="ID of the subscription", examples=[123])
    stream_url: str = Field(
        description="URL to connect to for streaming events",
        examples=["http://localhost:8000/stream/550e8400-e29b-41d4-a716-446655440000"],
    )
    resume_token: str = Field(
        description="Initial resume token for this position",
        examples=["rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi..."],
    )
    heartbeat_interval: int = Field(description="Heartbeat interval in seconds", examples=[30])
    connection_timeout: int = Field(description="Connection timeout in seconds", examples=[300])
    established_at: str = Field(
        description="Connection establishment timestamp",
        examples=["2024-01-01T12:00:00Z"],
    )
    message: str = Field(
        description="Success message", examples=["Streaming connection established"]
    )


class ResumeRequest(BaseModel):
    """Request model for resuming a stream."""

    resume_token: str = Field(
        description="Resume token to continue streaming from",
        examples=["rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi..."],
    )
    client_metadata: dict[str, str | int | bool] | None = Field(
        default=None,
        description="Optional client metadata",
        examples=[{"client_version": "1.0.0"}],
    )


class ResumeResponse(BaseModel):
    """Response model for stream resume."""

    connection_id: str = Field(
        description="New connection identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    subscription_id: int = Field(description="ID of the subscription", examples=[123])
    stream_url: str = Field(
        description="URL to connect to for streaming events",
        examples=["http://localhost:8000/stream/550e8400-e29b-41d4-a716-446655440000"],
    )
    resume_position: dict[str, str | int] = Field(
        description="Position information from the resume token",
        examples=[
            {
                "token_type": "event",
                "event_id": "event_123",
                "created_at": "2024-01-01T12:00:00Z",
            }
        ],
    )
    events_missed: int = Field(description="Number of events potentially missed", examples=[0])
    message: str = Field(description="Success message", examples=["Stream resumed successfully"])


class StreamingEventData(BaseModel):
    """Schema for individual streaming event data."""

    # Event-specific decoded data (dynamic fields)
    # This will contain the actual event parameters like 'from', 'to', 'value' for Transfer events

    # Metadata fields that are always present in delivered events
    block_number: int = Field(
        description="Block number where the event occurred", examples=[19000001]
    )
    transaction_hash: str = Field(
        description="Transaction hash", examples=["0xabcdef1234567890abcdef1234567890abcdef12"]
    )
    log_index: int = Field(description="Log index within the transaction", examples=[0])
    address: str = Field(
        description="Contract address that emitted the event",
        examples=["0xA0b86a33E6417b3c4555ba476F04245600306D5D"],
    )
    timestamp: str | None = Field(
        description="Block timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
        default=None,
    )

    class Config:
        extra = "allow"  # Allow additional fields for event-specific data


class StreamingEventBatch(BaseModel):
    """Schema for a batch of streaming events."""

    type: str = Field(description="Message type", examples=["event_batch"], default="event_batch")
    response_id: str = Field(
        description="Unique response ID for this batch",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    subscription_id: int = Field(description="ID of the subscription", examples=[123])
    connection_id: str = Field(
        description="Connection identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    resume_token: str = Field(
        description="Resume token for this batch position",
        examples=["rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi..."],
    )
    events: dict[str, list[dict[str, Any]]] = Field(
        description="Event data grouped by event name",
        examples=[
            {
                "Transfer": [
                    {
                        "from": "0x1234567890123456789012345678901234567890",
                        "to": "0x0987654321098765432109876543210987654321",
                        "value": "1000000000000000000",
                        "block_number": 19000001,
                        "transaction_hash": "0xabcdef...",
                        "log_index": 0,
                        "address": "0xA0b86a33E6417b3c4555ba476F04245600306D5D",
                    }
                ]
            }
        ],
    )
    batch_size: int = Field(description="Number of events in this batch", examples=[5])
    timestamp: str = Field(
        description="Batch timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )
    batch_id: str = Field(
        description="Unique batch identifier for acknowledgment",
        examples=["batch_550e8400-e29b-41d4-a716-446655440000"],
    )


class BatchAcknowledgmentRequest(BaseModel):
    """Request model for acknowledging a batch of events."""

    batch_id: str = Field(
        description="ID of the batch to acknowledge",
        examples=["batch_550e8400-e29b-41d4-a716-446655440000"],
    )


class BatchAcknowledgmentResponse(BaseModel):
    """Response model for batch acknowledgment."""

    acknowledged: bool = Field(description="Whether acknowledgment succeeded", examples=[True])
    batch_id: str = Field(
        description="ID of the acknowledged batch",
        examples=["batch_550e8400-e29b-41d4-a716-446655440000"],
    )
    events_acknowledged: int = Field(
        description="Number of events acknowledged",
        examples=[25],
    )
    connection_id: str = Field(
        description="Connection that acknowledged the batch",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    timestamp: str = Field(
        description="Acknowledgment timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )
    resume_token: str | None = Field(
        default=None,
        description="New resume token after this acknowledgment",
        examples=["rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi..."],
    )


class BulkBatchAcknowledgmentRequest(BaseModel):
    """Request model for acknowledging multiple batches at once."""

    batch_ids: list[str] = Field(
        description="List of batch IDs to acknowledge",
        examples=[
            [
                "batch_550e8400-e29b-41d4-a716-446655440000",
                "batch_660e8400-e29b-41d4-a716-446655440001",
                "batch_770e8400-e29b-41d4-a716-446655440002",
            ]
        ],
    )
    connection_id: str = Field(
        description="Connection ID that is acknowledging the batches",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class BulkBatchAcknowledgmentResponse(BaseModel):
    """Response model for bulk batch acknowledgment."""

    total_batches: int = Field(
        description="Total number of batches processed",
        examples=[3],
    )
    acknowledged_batches: int = Field(
        description="Number of batches successfully acknowledged",
        examples=[3],
    )
    failed_batches: int = Field(
        description="Number of batches that failed to acknowledge",
        examples=[0],
    )
    failed_batch_ids: list[str] = Field(
        description="List of batch IDs that failed to acknowledge",
        examples=[],
    )
    total_events_acknowledged: int = Field(
        description="Total number of events acknowledged across all batches",
        examples=[75],
    )
    connection_id: str = Field(
        description="Connection that acknowledged the batches",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    timestamp: str = Field(
        description="Acknowledgment timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )
    resume_token: str | None = Field(
        default=None,
        description="New resume token after this acknowledgment",
        examples=["rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi..."],
    )


class StreamingHeartbeat(BaseModel):
    """Schema for streaming heartbeat messages."""

    type: str = Field(description="Message type", examples=["heartbeat"])
    connection_id: str = Field(
        description="Connection identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    subscription_id: int = Field(description="ID of the subscription", examples=[123])
    timestamp: str = Field(
        description="Heartbeat timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )


class ClientHeartbeatRequest(BaseModel):
    """Request model for client heartbeat."""

    timestamp: str = Field(
        description="Client timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )
    sequence_number: int | None = Field(
        default=None,
        description="Optional sequence number for debugging",
        examples=[1234],
    )


class ClientHeartbeatResponse(BaseModel):
    """Response model for client heartbeat acknowledgment."""

    acknowledged: bool = Field(
        description="Whether the heartbeat was acknowledged", examples=[True]
    )
    server_timestamp: str = Field(
        description="Server timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )
    connection_id: str = Field(
        description="Connection identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class StreamingError(BaseModel):
    """Schema for streaming error messages."""

    type: str = Field(description="Message type", examples=["error"])
    connection_id: str = Field(
        description="Connection identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    subscription_id: int = Field(description="ID of the subscription", examples=[123])
    error_code: str = Field(
        description="Error code", examples=["CONNECTION_LOST", "INVALID_RESUME_TOKEN"]
    )
    error_message: str = Field(
        description="Human-readable error message",
        examples=["Connection lost due to network timeout"],
    )
    timestamp: str = Field(
        description="Error timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )
    recoverable: bool = Field(
        default=True,
        description="Whether the client should attempt to recover/reconnect",
        examples=[True],
    )


class StreamingMetricsResponse(BaseModel):
    """Response model for streaming metrics."""

    # Connection statistics
    total_connections: int = Field(description="Total number of connections", examples=[150])
    active_connections: int = Field(description="Number of active connections", examples=[145])
    connections_by_status: dict[str, int] = Field(
        description="Connections grouped by health status",
        examples=[{"healthy": 140, "warning": 8, "critical": 2, "failed": 0}],
    )

    # Event delivery statistics
    events_queued: int = Field(description="Total events queued for delivery", examples=[45000])
    events_delivered: int = Field(description="Total events delivered", examples=[44500])
    delivery_failures: int = Field(description="Total delivery failures", examples=[500])
    delivery_success_rate: float = Field(description="Delivery success rate", examples=[0.989])

    # Resume token statistics
    tokens_generated: int = Field(description="Total resume tokens generated", examples=[1250])
    tokens_used: int = Field(description="Total resume tokens used", examples=[89])
    tokens_expired: int = Field(description="Total expired tokens", examples=[156])

    # Health monitoring statistics
    health_checks_performed: int = Field(
        description="Total health checks performed", examples=[25000]
    )
    connections_auto_closed: int = Field(
        description="Connections automatically closed", examples=[12]
    )

    # Per-subscription metrics
    subscriptions_with_connections: int = Field(
        description="Subscriptions with active connections", examples=[75]
    )
    avg_connections_per_subscription: float = Field(
        description="Average connections per subscription", examples=[1.93]
    )

    # Performance metrics
    avg_event_delivery_time: float = Field(
        description="Average event delivery time in seconds", examples=[0.045]
    )
    avg_connection_uptime: float = Field(
        description="Average connection uptime in hours", examples=[4.2]
    )

    # Configuration
    heartbeat_interval: int = Field(description="Heartbeat interval in seconds", examples=[30])
    connection_timeout: int = Field(description="Connection timeout in seconds", examples=[300])

    # Healthy connections sample
    healthy_connections: list[dict[str, Any]] = Field(
        description="Sample of healthy connections",
        examples=[[]],
    )

    # Timestamp
    timestamp: str = Field(
        description="Metrics timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )


class ProcessingStatusResponse(BaseModel):
    """Response for checking if a subscription's processing is active."""

    subscription_id: int = Field(description="The subscription ID", examples=[123])
    is_processing: bool = Field(
        description="Whether the subscription is currently being processed", examples=[True]
    )
    connection_count: int = Field(
        description="Number of active connections for this subscription", examples=[2]
    )
    timestamp: str = Field(
        description="Timestamp of the status check in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
    )
