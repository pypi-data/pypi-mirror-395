"""
Circuit breaker models for Event Streamer schemas.

These models define the structure for circuit breaker monitoring and management API responses.
"""

from typing import Any

from pydantic import BaseModel, Field


class CircuitBreakerMetrics(BaseModel):
    """Circuit breaker metrics and statistics."""

    name: str = Field(description="Circuit breaker name")
    failure_count: int = Field(description="Total number of failures")
    success_count: int = Field(description="Total number of successes")
    consecutive_failures: int = Field(description="Current consecutive failures")
    consecutive_successes: int = Field(description="Current consecutive successes")
    total_calls: int = Field(description="Total number of calls")
    half_open_calls: int = Field(description="Number of calls in half-open state")
    last_failure_time: str | None = Field(description="Timestamp of last failure")
    last_success_time: str | None = Field(description="Timestamp of last success")
    state_transitions: dict[str, int] = Field(description="State transition counters")
    success_rate: float = Field(description="Success rate percentage")
    failure_rate: float = Field(description="Failure rate percentage")


class CircuitBreakerStatus(BaseModel):
    """Circuit breaker status information."""

    state: str = Field(description="Current circuit breaker state")
    failure_count: int = Field(description="Total failures")
    success_count: int = Field(description="Total successes")
    consecutive_failures: int = Field(description="Consecutive failures")
    consecutive_successes: int = Field(description="Consecutive successes")
    total_calls: int = Field(description="Total calls")
    last_failure_time: str | None = Field(description="Last failure timestamp")
    last_success_time: str | None = Field(description="Last success timestamp")
    state_transitions: dict[str, int] = Field(description="State transitions")


class RpcClientStatus(BaseModel):
    """RPC client circuit breaker status."""

    state: str = Field(description="Circuit breaker state")
    metrics: dict[str, Any] = Field(description="Circuit breaker metrics")
    is_healthy: bool = Field(description="Whether circuit breaker is healthy")


class CircuitBreakerStatusResponse(BaseModel):
    """Response model for circuit breaker status endpoint."""

    circuit_breakers: dict[str, CircuitBreakerStatus] = Field(
        description="Circuit breakers indexed by name"
    )
    rpc_clients: dict[str, dict[str, RpcClientStatus]] = Field(
        description="RPC client circuit breakers indexed by chain"
    )
    summary: dict[str, Any] = Field(description="Summary statistics")


class CircuitBreakerHealthResponse(BaseModel):
    """Response model for circuit breaker health endpoint."""

    overall_health: str = Field(description="Overall health status")
    health_percentage: float = Field(description="Health percentage")
    total_circuit_breakers: int = Field(description="Total number of circuit breakers")
    healthy_circuit_breakers: int = Field(description="Number of healthy circuit breakers")
    unhealthy_circuit_breakers: int = Field(description="Number of unhealthy circuit breakers")
    rpc_clients: dict[str, dict[str, Any]] = Field(description="RPC client health status")
    last_updated: str = Field(description="Last updated timestamp")


class CircuitBreakerResetResponse(BaseModel):
    """Response model for circuit breaker reset endpoints."""

    message: str = Field(description="Reset operation message")
    status: str = Field(description="Reset operation status")


class CircuitBreakerConfigResponse(BaseModel):
    """Response model for circuit breaker configuration endpoint."""

    failure_threshold: int = Field(description="Failure threshold")
    recovery_timeout: int = Field(description="Recovery timeout in seconds")
    success_threshold: int = Field(description="Success threshold")
    timeout: int = Field(description="Operation timeout in seconds")
    half_open_max_calls: int = Field(description="Maximum calls in half-open state")
