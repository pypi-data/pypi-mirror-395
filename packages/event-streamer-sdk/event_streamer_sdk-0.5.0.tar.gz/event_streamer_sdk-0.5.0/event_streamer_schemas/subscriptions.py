from pydantic import BaseModel, Field

from .abi import ABIEvent


class SubscriptionCreate(BaseModel):
    """Schema for creating a new subscription."""

    topic0: str = Field(
        description="Event topic0 hash (66 characters including 0x)",
        examples=["0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"],
        min_length=66,
        max_length=66,
    )
    event_signature: ABIEvent = Field(description="ABI event signature definition")
    addresses: list[str] = Field(
        description="List of contract addresses to monitor (42 characters each including 0x)",
        examples=[
            [
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
            ]
        ],
        default=[],
    )
    start_block: int = Field(
        description="Starting block number for monitoring", examples=[19000000], ge=0
    )
    end_block: int | None = Field(
        description="Ending block number for monitoring (optional for ongoing monitoring)",
        examples=[19500000],
        default=None,
        ge=0,
    )
    chain_id: int = Field(description="Blockchain chain ID", examples=[1, 137, 8453], ge=1)
    subscriber_id: str = Field(
        description="Unique identifier for the subscriber", examples=["user_123", "service_abc"]
    )


class SubscriptionUpdate(BaseModel):
    """Schema for updating an existing subscription."""

    topic0: str | None = Field(
        description="Event topic0 hash (66 characters including 0x)",
        default=None,
        min_length=66,
        max_length=66,
    )
    event_signature: ABIEvent | None = Field(
        description="ABI event signature definition", default=None
    )
    addresses: list[str] | None = Field(
        description="List of contract addresses to monitor (42 characters each including 0x)",
        default=None,
    )
    start_block: int | None = Field(
        description="Starting block number for monitoring", default=None, ge=0
    )
    end_block: int | None = Field(
        description="Ending block number for monitoring", default=None, ge=0
    )
    chain_id: int | None = Field(description="Blockchain chain ID", default=None, ge=1)
    subscriber_id: str | None = Field(
        description="Unique identifier for the subscriber", default=None
    )
    # Streaming fields
    is_streaming: bool | None = Field(
        description="Whether this subscription uses streaming delivery", default=None
    )
    streaming_status: str | None = Field(description="Current streaming status", default=None)


class SubscriptionResponse(BaseModel):
    """Schema for subscription response."""

    id: int = Field(description="Unique subscription ID", examples=[1])
    topic0: str = Field(
        description="Event topic0 hash",
        examples=["0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"],
    )
    event_signature: ABIEvent = Field(description="ABI event signature definition")
    addresses: list[str] = Field(
        description="List of contract addresses being monitored",
        examples=[["0x1234567890123456789012345678901234567890"]],
    )
    start_block: int = Field(description="Starting block number", examples=[19000000])
    end_block: int | None = Field(description="Ending block number", examples=[19500000])
    last_processed_block: int | None = Field(
        description="Last block number that was processed for this subscription",
        examples=[19250000],
        default=None,
    )
    chain_id: int = Field(description="Blockchain chain ID", examples=[1])
    subscriber_id: str = Field(description="Subscriber identifier", examples=["user_123"])
    # Streaming fields
    is_streaming: bool = Field(description="Whether this subscription uses streaming delivery")
    streaming_status: str = Field(description="Current streaming status", examples=["active"])
    resume_token: str | None = Field(
        description="Token for resuming streaming from last position", default=None
    )
    last_event_id: str | None = Field(description="ID of the last event delivered", default=None)
    events_delivered: int = Field(description="Total number of events delivered", examples=[1500])
    created_at: str = Field(
        description="Creation timestamp in ISO format", examples=["2024-05-23T10:30:00.000Z"]
    )
    updated_at: str = Field(
        description="Last update timestamp in ISO format", examples=["2024-05-23T10:30:00.000Z"]
    )


class SubscriptionListResponse(BaseModel):
    """Schema for listing subscriptions."""

    subscriptions: list[SubscriptionResponse] = Field(
        description="List of subscriptions", examples=[[]]
    )
    total: int = Field(description="Total number of subscriptions", examples=[10])
    page: int = Field(description="Current page number", examples=[1])
    page_size: int = Field(description="Number of items per page", examples=[20])
