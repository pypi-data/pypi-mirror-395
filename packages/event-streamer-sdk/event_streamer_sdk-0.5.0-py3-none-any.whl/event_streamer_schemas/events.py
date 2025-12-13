from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """Base class for all events."""

    chain_id: int = Field(
        ..., description="The chain id in which the event occurred.", examples=[1]
    )
    block_number: int = Field(
        ..., description="The block number in which the event occurred.", examples=[12345678]
    )
    transaction_index: int = Field(
        ..., description="The index of the transaction in the given block_number.", examples=[72]
    )
    transaction_hash: str = Field(
        ...,
        description="The hash of the transaction in which the event occurred.",
        examples=["0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"],
        min_length=66,
        max_length=66,
    )
    log_index: int = Field(
        ..., description="The index of the log in the transaction.", examples=[0]
    )
    address: str = Field(
        ...,
        description="The address of the contract that emitted the event.",
        min_length=42,
        max_length=42,
        examples=["0x1234567890abcdef1234567890abcdef12345678"],
    )
    transaction_from: str = Field(
        ...,
        description="The address of the sender of the transaction.",
        min_length=42,
        max_length=42,
        examples=["0x1234567890abcdef1234567890abcdef12345678"],
    )
    transaction_to: str = Field(
        ...,
        description="The address of the receiver of the transaction.",
        min_length=42,
        max_length=42,
        examples=["0x1234567890abcdef1234567890abcdef12345678"],
    )
