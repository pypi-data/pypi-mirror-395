"""
API Response Models for Event Streamer service.

These models handle API responses, error handling, and metrics
across all endpoints in the Event Streamer ecosystem.
"""

from typing import Any

from pydantic import BaseModel, Field

# Common Error Response Models


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str = Field(description="Error message", examples=["Subscription not found"])
    detail: str | None = Field(description="Detailed error information", default=None)
    timestamp: str | None = Field(
        description="Error timestamp in ISO format",
        examples=["2024-05-23T10:30:00.000Z"],
        default=None,
    )


# Health and Status Models


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(description="Service health status", examples=["healthy"])
    timestamp: str = Field(
        description="Current timestamp in ISO format", examples=["2024-05-23T10:30:00.000Z"]
    )


class SchemasResponse(BaseModel):
    """Database schemas response model."""

    schemas: list[str] = Field(
        description="List of available database schemas",
        examples=[["public", "event_streamer", "information_schema"]],
    )
    timestamp: str = Field(
        description="Current timestamp in ISO format", examples=["2024-05-23T10:30:00.000Z"]
    )


# Chain Configuration Models


class ChainInfo(BaseModel):
    """Chain information model."""

    chain_id: int = Field(description="Chain ID", examples=[1])
    name: str = Field(description="Chain name", examples=["ethereum"])
    historical_rpc_configured: bool = Field(
        description="Whether historical RPC is configured", examples=[True]
    )
    live_websocket_configured: bool = Field(
        description="Whether live WebSocket is configured", examples=[True]
    )


class ChainsResponse(BaseModel):
    """Supported chains response model."""

    supported_chains: list[ChainInfo] = Field(description="List of supported chains")
    total_chains: int = Field(description="Total number of supported chains", examples=[4])
    timestamp: str = Field(
        description="Timestamp of the response", examples=["2024-05-23T10:30:00.000Z"]
    )


class ChainConfigRequest(BaseModel):
    """Request model for creating/updating chain configuration."""

    chain_id: int = Field(description="Chain ID", examples=[1])
    name: str = Field(description="Chain name", examples=["ethereum"])
    historical_rpc_url: str = Field(
        description="Historical RPC URL",
        examples=["https://eth-mainnet.alchemyapi.io/v2/your-api-key"],
    )
    live_websocket_url: str = Field(
        description="Live WebSocket URL",
        examples=["wss://eth-mainnet.alchemyapi.io/v2/your-api-key"],
    )
    historical_max_chunk_size: int = Field(
        default=10000, description="Maximum chunk size for historical processing"
    )
    historical_max_retries: int = Field(
        default=3, description="Maximum retries for historical processing"
    )
    historical_max_concurrent: int = Field(
        default=5, description="Maximum concurrent historical processors"
    )
    historical_progress_interval: int = Field(default=100, description="Progress update interval")
    live_max_retries: int = Field(default=5, description="Maximum retries for live connections")
    live_retry_delay: int = Field(default=5, description="Delay between retry attempts")
    live_reconnect_delay: int = Field(default=30, description="Delay before reconnect attempts")
    live_enable_gap_detection: bool = Field(default=True, description="Enable gap detection")
    live_max_gap_size: int = Field(default=1000, description="Maximum gap size to backfill")
    live_block_check_interval: int = Field(default=10, description="Block check interval")
    live_gap_fill_chunk_size: int = Field(default=100, description="Gap fill chunk size")


class ChainConfigResponse(BaseModel):
    """Response model for chain configuration operations."""

    message: str = Field(description="Response message")
    chain_id: int = Field(description="Chain ID")
    timestamp: str = Field(description="Response timestamp")


class ChainListResponse(BaseModel):
    """Response model for chain list."""

    chains: dict[int, dict[str, Any]] = Field(description="Dictionary of chain configurations")
    total_chains: int = Field(description="Total number of chains")
    timestamp: str = Field(description="Response timestamp")


class ChainStatsResponse(BaseModel):
    """Response model for chain configuration statistics."""

    loaded: bool = Field(description="Whether chain configurations are loaded")
    total_chains: int = Field(description="Total number of chains")
    supported_chain_ids: list[int] = Field(description="List of supported chain IDs")
    last_refresh: str = Field(description="Last refresh timestamp")
    timestamp: str = Field(description="Response timestamp")


# Metrics Models


class ChainMetrics(BaseModel):
    """Per-chain metrics model."""

    chain_id: int = Field(description="Chain ID", examples=[1])
    name: str = Field(description="Chain name", examples=["ethereum"])
    subscriptions: int = Field(description="Number of subscriptions for this chain", examples=[6])
    events_processed: int = Field(description="Events processed for this chain", examples=[1200])
    active_tasks: int = Field(description="Active processing tasks for this chain", examples=[2])
    max_concurrent: int = Field(description="Maximum concurrent tasks for this chain", examples=[5])
    live_subscriptions: int = Field(
        description="Number of live subscriptions for this chain", examples=[3]
    )
    live_events_processed: int = Field(
        description="Live events processed for this chain", examples=[300]
    )
    live_processor_running: bool = Field(
        description="Whether live processor is running for this chain", examples=[True]
    )


class MetricsResponse(BaseModel):
    """API metrics response model."""

    total_subscriptions: int = Field(description="Total number of subscriptions", examples=[10])
    active_subscriptions: int = Field(description="Number of active subscriptions", examples=[8])
    historical_subscriptions: int = Field(
        description="Number of historical subscriptions", examples=[5]
    )
    live_subscriptions: int = Field(description="Number of live subscriptions", examples=[3])
    hybrid_subscriptions: int = Field(description="Number of hybrid subscriptions", examples=[2])
    completed_historical: int = Field(
        description="Number of completed historical subscriptions", examples=[2]
    )
    in_progress_historical: int = Field(
        description="Number of in-progress historical subscriptions", examples=[3]
    )
    processing_active: bool = Field(
        description="Whether background processing is active", examples=[True]
    )
    events_processed: int = Field(description="Total events processed", examples=[1500])
    supported_chains: list[int] = Field(
        description="List of supported chain IDs", examples=[[1, 137, 8453, 42161]]
    )
    by_chain: dict[str, ChainMetrics] = Field(description="Per-chain metrics")
    timestamp: str = Field(
        description="Current timestamp in ISO format", examples=["2024-05-23T10:30:00.000Z"]
    )


# Debug Models


class GapDetectionResponse(BaseModel):
    """Gap detection debug response model."""

    chain_id: int = Field(description="Chain ID", examples=[1])
    gap_detection_triggered: bool = Field(
        description="Whether gap detection was triggered", examples=[True]
    )
    gaps_found: int = Field(description="Number of gaps found", examples=[2])
    gap_details: list[dict[str, Any]] = Field(
        description="Details of gaps found", examples=[[{"start": 100, "end": 150, "size": 51}]]
    )
    current_block: int = Field(description="Current blockchain block", examples=[22622100])
    last_processed_blocks: dict[str, int] = Field(
        description="Last processed block per subscription", examples=[{"37": 22622070}]
    )
    processor_status: dict[str, Any] = Field(description="Live processor status")
    timestamp: str = Field(description="Timestamp", examples=["2024-05-23T10:30:00.000Z"])


# Streaming Health Models


class ConnectionHealth(BaseModel):
    """Model for connection health information."""

    connection_id: str = Field(description="Connection identifier")
    subscription_id: int = Field(description="Subscription ID")
    status: str = Field(
        description="Health status", examples=["healthy", "warning", "critical", "failed"]
    )
    last_heartbeat: str = Field(description="Last heartbeat timestamp")
    events_sent: int = Field(description="Total events sent")
    error_rate: float = Field(description="Error rate (0.0 to 1.0)")
    uptime_seconds: int = Field(description="Connection uptime in seconds")
