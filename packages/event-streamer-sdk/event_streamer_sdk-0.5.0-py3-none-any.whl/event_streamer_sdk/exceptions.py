"""
Custom exceptions for Event Streamer SDK.
"""


class EventStreamerSDKError(Exception):
    """Base exception for Event Streamer SDK errors."""

    pass


class EventStreamerConnectionError(EventStreamerSDKError):
    """Raised when connection to Event Streamer service fails."""

    pass


class EventStreamerAuthError(EventStreamerSDKError):
    """Raised when authentication with Event Streamer service fails."""

    pass


class EventStreamerTimeoutError(EventStreamerSDKError):
    """Raised when request to Event Streamer service times out."""

    pass


class EventStreamerValidationError(EventStreamerSDKError):
    """Raised when request validation fails."""

    pass


class EventStreamerSubscriptionError(EventStreamerSDKError):
    """Raised when subscription operations fail."""

    pass
