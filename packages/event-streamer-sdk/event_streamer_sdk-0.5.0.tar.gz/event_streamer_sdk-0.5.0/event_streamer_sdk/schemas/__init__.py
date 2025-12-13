"""
Event Streamer Schemas - Shared Pydantic models for Event Streamer ecosystem.

This package contains all the shared Pydantic schemas used by both the main
Event Streamer service and the Event Streamer SDK. This ensures consistency
and eliminates duplication across the ecosystem.
"""

from event_streamer_schemas import (
    ABIEvent,
    ABIInput,
    BaseEvent,
    ConfirmationRequest,
    ConfirmationResponse,
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
]
