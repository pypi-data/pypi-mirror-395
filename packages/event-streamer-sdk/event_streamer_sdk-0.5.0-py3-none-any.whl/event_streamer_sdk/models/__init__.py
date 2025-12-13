"""
Pydantic models for Event Streamer SDK.

Most models are re-exported from the bundled schemas package to ensure consistency.
SDK-specific models like EventDeliveryPayload are defined locally.
"""

# Re-export streaming models from shared schemas
from event_streamer_schemas import (
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

from .abi import ABIEvent, ABIInput
from .confirmations import ConfirmationRequest, ConfirmationResponse
from .subscriptions import (
    SubscriptionCreate,
    SubscriptionListResponse,
    SubscriptionResponse,
    SubscriptionUpdate,
)

__all__ = [
    # ABI models (re-exported from shared schemas)
    "ABIEvent",
    "ABIInput",
    # Subscription models (re-exported from shared schemas)
    "SubscriptionCreate",
    "SubscriptionUpdate",
    "SubscriptionResponse",
    "SubscriptionListResponse",
    # Confirmation models (re-exported from shared schemas)
    "ConfirmationRequest",
    "ConfirmationResponse",
    # Streaming models (re-exported from shared schemas)
    "StreamingConnectionRequest",
    "StreamingConnectionResponse",
    "ResumeRequest",
    "ResumeResponse",
    "StreamingEventData",
    "StreamingEventBatch",
    "StreamingHeartbeat",
    "StreamingError",
    "StreamingMetricsResponse",
]
