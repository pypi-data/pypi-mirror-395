"""
Event Streamer SDK

A Python SDK for interacting with the Event Streamer blockchain event monitoring service.
"""

from .client import EventStreamer
from .exceptions import EventStreamerAuthError, EventStreamerConnectionError, EventStreamerSDKError
from .streaming_client import StreamingClient

__version__ = "0.4.0"
__all__ = [
    "EventStreamer",
    "StreamingClient",
    "EventStreamerSDKError",
    "EventStreamerConnectionError",
    "EventStreamerAuthError",
]
