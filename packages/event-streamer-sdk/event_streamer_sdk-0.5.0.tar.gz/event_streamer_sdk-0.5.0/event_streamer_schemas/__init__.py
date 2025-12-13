"""
Event Streamer Schemas - Shared Pydantic models for Event Streamer ecosystem.

This package contains all the shared Pydantic schemas used by both the main
Event Streamer service and the Event Streamer SDK. This ensures consistency
and eliminates duplication across the ecosystem.
"""

from .abi import ABIEvent, ABIInput
from .api import (
    ChainConfigRequest,
    ChainConfigResponse,
    ChainInfo,
    ChainListResponse,
    ChainMetrics,
    ChainsResponse,
    ChainStatsResponse,
    ConnectionHealth,
    ErrorResponse,
    GapDetectionResponse,
    HealthResponse,
    MetricsResponse,
    SchemasResponse,
)
from .circuit_breaker import (
    CircuitBreakerConfigResponse,
    CircuitBreakerHealthResponse,
    CircuitBreakerMetrics,
    CircuitBreakerResetResponse,
    CircuitBreakerStatus,
    CircuitBreakerStatusResponse,
    RpcClientStatus,
)
from .confirmations import ConfirmationRequest, ConfirmationResponse
from .events import BaseEvent
from .streaming import (
    BatchAcknowledgmentRequest,
    BatchAcknowledgmentResponse,
    BulkBatchAcknowledgmentRequest,
    BulkBatchAcknowledgmentResponse,
    ClientHeartbeatRequest,
    ClientHeartbeatResponse,
    ProcessingStatusResponse,
    ResumeRequest,
    ResumeResponse,
    StreamingConnectionRequest,
    StreamingConnectionResponse,
    StreamingError,
    StreamingEventBatch,
    StreamingEventData,
    StreamingHeartbeat,
    StreamingMetricsResponse,
)
from .subscriptions import (
    SubscriptionCreate,
    SubscriptionListResponse,
    SubscriptionResponse,
    SubscriptionUpdate,
)

__version__ = "0.1.0"

__all__ = [
    # ABI models
    "ABIEvent",
    "ABIInput",
    # API response models
    "ErrorResponse",
    "HealthResponse",
    "SchemasResponse",
    "ChainInfo",
    "ChainsResponse",
    "ChainConfigRequest",
    "ChainConfigResponse",
    "ChainListResponse",
    "ChainStatsResponse",
    "ChainMetrics",
    "MetricsResponse",
    "GapDetectionResponse",
    "ConnectionHealth",
    # Circuit breaker models
    "CircuitBreakerConfigResponse",
    "CircuitBreakerHealthResponse",
    "CircuitBreakerMetrics",
    "CircuitBreakerResetResponse",
    "CircuitBreakerStatus",
    "CircuitBreakerStatusResponse",
    "RpcClientStatus",
    # Confirmation models
    "ConfirmationRequest",
    "ConfirmationResponse",
    # Event models
    "BaseEvent",
    # Subscription models
    "SubscriptionCreate",
    "SubscriptionListResponse",
    "SubscriptionResponse",
    "SubscriptionUpdate",
    # Streaming models
    "StreamingConnectionRequest",
    "StreamingConnectionResponse",
    "ResumeRequest",
    "ResumeResponse",
    "StreamingEventData",
    "StreamingEventBatch",
    "StreamingHeartbeat",
    "StreamingError",
    "StreamingMetricsResponse",
    "BatchAcknowledgmentRequest",
    "BatchAcknowledgmentResponse",
    "BulkBatchAcknowledgmentRequest",
    "BulkBatchAcknowledgmentResponse",
    "ClientHeartbeatRequest",
    "ClientHeartbeatResponse",
    "ProcessingStatusResponse",
]
