"""
Confirmation schemas for event delivery acknowledgments.
"""

from pydantic import BaseModel, Field


class ConfirmationRequest(BaseModel):
    """Schema for confirming event delivery."""

    subscription_id: int = Field(
        description="The subscription ID that received the events", examples=[123], ge=1
    )
    response_id: str = Field(
        description="The response ID from the event delivery",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class ConfirmationResponse(BaseModel):
    """Schema for confirmation response."""

    success: bool = Field(description="Whether the confirmation was successful", examples=[True])
    message: str = Field(
        description="Confirmation result message",
        examples=["Event delivery confirmed successfully"],
    )
