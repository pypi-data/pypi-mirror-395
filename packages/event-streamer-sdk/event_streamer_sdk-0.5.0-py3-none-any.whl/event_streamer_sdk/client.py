"""
Main EventStreamer client for interacting with Event Streamer service.
"""

from typing import Any

import aiohttp

from event_streamer_schemas import (
    ABIEvent,
    ChainConfigRequest,
    ChainConfigResponse,
    ChainListResponse,
    ChainStatsResponse,
)

from .exceptions import (
    EventStreamerConnectionError,
    EventStreamerSubscriptionError,
    EventStreamerTimeoutError,
    EventStreamerValidationError,
)
from .models.circuit_breaker import (
    CircuitBreakerConfigResponse,
    CircuitBreakerHealthResponse,
    CircuitBreakerMetrics,
    CircuitBreakerResetResponse,
    CircuitBreakerStatusResponse,
)
from .models.subscriptions import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from .streaming_client import StreamingClient


class EventStreamer:
    """Main SDK client for interacting with Event Streamer service."""

    def __init__(
        self,
        service_url: str,
        subscriber_id: str,
        *,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
    ):
        """
        Initialize the EventStreamer client.

        Args:
            service_url: Base URL of the Event Streamer service
            subscriber_id: Unique identifier for this subscriber
            timeout: Request timeout in seconds
            headers: Optional additional headers for requests
        """
        self.service_url = service_url.rstrip("/")
        self.subscriber_id = subscriber_id
        self.timeout = timeout
        self.headers = headers or {}
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "EventStreamer":
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_session(self) -> None:
        """Ensure the HTTP session is initialized."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers=self.headers,
            )

    async def close(self) -> None:
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a request to the Event Streamer service."""
        await self._ensure_session()

        if not self.session:
            raise EventStreamerConnectionError("HTTP session not initialized")

        url = f"{self.service_url}{endpoint}"

        try:
            async with self.session.request(method, url, json=json, params=params) as response:
                response_text = await response.text()

                if response.status >= 500:
                    error_text = response_text or f"HTTP {response.status}"
                    raise EventStreamerConnectionError(f"Service error: {error_text}")
                elif response.status >= 400:
                    error_text = response_text or f"HTTP {response.status}"
                    raise EventStreamerValidationError(f"Request error: {error_text}")

                # Handle 204 No Content responses
                if response.status == 204:
                    return {}  # Return empty dict for 204 responses

                return await response.json()  # type: ignore[no-any-return]

        except TimeoutError:
            raise EventStreamerTimeoutError(f"Request to {url} timed out")
        except aiohttp.ClientError as e:
            raise EventStreamerConnectionError(f"Connection error: {str(e)}")

    async def create_subscription(self, subscription: SubscriptionCreate) -> SubscriptionResponse:
        """
        Create a new subscription.

        Args:
            subscription: The subscription configuration

        Returns:
            The created subscription with assigned ID

        Raises:
            EventStreamerSubscriptionError: If subscription creation fails
        """
        subscription_data = subscription.model_dump()
        subscription_data["subscriber_id"] = self.subscriber_id

        try:
            response = await self._request("POST", "/subscriptions", json=subscription_data)
            return SubscriptionResponse(**response)
        except (
            EventStreamerConnectionError,
            EventStreamerTimeoutError,
            EventStreamerValidationError,
        ) as e:
            # Re-raise as subscription error with more context
            raise EventStreamerSubscriptionError(f"Failed to create subscription: {str(e)}")

    async def get_subscription(self, subscription_id: int) -> SubscriptionResponse:
        """
        Get a subscription by ID.

        Args:
            subscription_id: ID of the subscription to retrieve

        Returns:
            The subscription data

        Raises:
            EventStreamerSubscriptionError: If subscription not found
        """
        try:
            response = await self._request(
                "GET",
                f"/subscriptions/{subscription_id}",
                params={"subscriber_id": self.subscriber_id},
            )
            return SubscriptionResponse(**response)
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerSubscriptionError(f"Subscription {subscription_id} not found")
            raise

    async def update_subscription(
        self, subscription_id: int, updates: SubscriptionUpdate
    ) -> SubscriptionResponse:
        """
        Update a subscription.

        Args:
            subscription_id: ID of the subscription to update
            updates: The subscription updates

        Returns:
            The updated subscription

        Raises:
            EventStreamerSubscriptionError: If update fails
        """
        update_data = updates.model_dump(exclude_unset=True)
        try:
            response = await self._request(
                "PUT", f"/subscriptions/{subscription_id}", json=update_data
            )
            return SubscriptionResponse(**response)
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerSubscriptionError(f"Subscription {subscription_id} not found")
            raise EventStreamerSubscriptionError(f"Failed to update subscription: {str(e)}")

    async def delete_subscription(self, subscription_id: int) -> None:
        """
        Delete a subscription.

        Args:
            subscription_id: ID of the subscription to delete

        Raises:
            EventStreamerSubscriptionError: If deletion fails
        """
        try:
            await self._request("DELETE", f"/subscriptions/{subscription_id}")
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerSubscriptionError(f"Subscription {subscription_id} not found")
            raise EventStreamerSubscriptionError(f"Failed to delete subscription: {str(e)}")

    def create_streaming_client(
        self,
        subscription_id: int,
        *,
        resume_token: str | None = None,
        client_metadata: dict[str, Any] | None = None,
        auto_acknowledge: bool = True,
    ) -> StreamingClient:
        """
        Create a streaming client for a subscription.

        Args:
            subscription_id: ID of the subscription to stream
            resume_token: Optional resume token to continue from specific position
            client_metadata: Optional client metadata
            auto_acknowledge: Whether to automatically acknowledge events after handler execution
                (default: True)

        Returns:
            Configured streaming client
        """
        return StreamingClient(
            event_streamer=self,
            subscription_id=subscription_id,
            resume_token=resume_token,
            client_metadata=client_metadata,
            auto_acknowledge=auto_acknowledge,
        )

    # ABI Parsing Methods

    def extract_abi_event(self, abi_json: str, event_name: str) -> ABIEvent:
        """
        Extract a specific event from contract ABI JSON.

        Args:
            abi_json: JSON string containing contract ABI
            event_name: Name of the event to extract

        Returns:
            ABIEvent object for the specified event

        Raises:
            EventStreamerValidationError: If ABI parsing fails or event not found

        Example:
            >>> erc20_abi = '''[
            ...     {
            ...         "type": "event",
            ...         "name": "Transfer",
            ...         "inputs": [
            ...             {"indexed": true, "name": "from", "type": "address"},
            ...             {"indexed": true, "name": "to", "type": "address"},
            ...             {"indexed": false, "name": "value", "type": "uint256"}
            ...         ]
            ...     }
            ... ]'''
            >>> transfer_event = client.extract_abi_event(erc20_abi, "Transfer")
        """
        from .abi_parser import extract_abi_event

        return extract_abi_event(abi_json, event_name)

    def extract_abi_events(self, abi_json: str) -> dict[str, ABIEvent]:
        """
        Extract all events from contract ABI JSON.

        Args:
            abi_json: JSON string containing contract ABI

        Returns:
            Dictionary mapping event names to ABIEvent objects

        Raises:
            EventStreamerValidationError: If ABI parsing fails

        Example:
            >>> erc20_abi = '''[
            ...     {"type": "event", "name": "Transfer", "inputs": [...]},
            ...     {"type": "event", "name": "Approval", "inputs": [...]}
            ... ]'''
            >>> events = client.extract_abi_events(erc20_abi)
            >>> transfer_event = events["Transfer"]
            >>> approval_event = events["Approval"]
        """
        from .abi_parser import extract_abi_events

        return extract_abi_events(abi_json)

    def parse_contract_abi(self, abi_json: str) -> dict[str, Any]:
        """
        Parse complete contract ABI and return structured data.

        Args:
            abi_json: JSON string containing contract ABI

        Returns:
            Dictionary containing parsed ABI data with events, functions, etc.
            Structure:
            {
                "events": {event_name: event_definition},
                "functions": {function_name: [function_overloads]},
                "constructor": constructor_definition,
                "fallback": fallback_definition,
                "receive": receive_definition,
                "errors": {error_name: error_definition},
                "raw": original_abi_data
            }

        Raises:
            EventStreamerValidationError: If ABI parsing fails

        Example:
            >>> abi_json = '''[
            ...     {"type": "event", "name": "Transfer", "inputs": [...]},
            ...     {"type": "function", "name": "transfer", "inputs": [...]}
            ... ]'''
            >>> parsed = client.parse_contract_abi(abi_json)
            >>> events = parsed["events"]
            >>> functions = parsed["functions"]
        """
        from .abi_parser import parse_contract_abi

        return parse_contract_abi(abi_json)

    # Circuit Breaker Management Methods

    async def get_circuit_breaker_status(self) -> CircuitBreakerStatusResponse:
        """
        Get status of all circuit breakers.

        Returns:
            Circuit breaker status information

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", "/api/circuit-breakers/status")
            return CircuitBreakerStatusResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to get circuit breaker status: {str(e)}")

    async def get_circuit_breaker_health(self) -> CircuitBreakerHealthResponse:
        """
        Get circuit breaker health summary.

        Returns:
            Circuit breaker health information

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", "/api/circuit-breakers/health")
            return CircuitBreakerHealthResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to get circuit breaker health: {str(e)}")

    async def get_circuit_breaker_metrics(self, name: str) -> CircuitBreakerMetrics:
        """
        Get detailed metrics for a specific circuit breaker.

        Args:
            name: Name of the circuit breaker

        Returns:
            Circuit breaker metrics

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", f"/api/circuit-breakers/{name}/metrics")
            return CircuitBreakerMetrics(**response)
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerConnectionError(f"Circuit breaker '{name}' not found")
            raise EventStreamerConnectionError(f"Failed to get circuit breaker metrics: {str(e)}")

    async def reset_all_circuit_breakers(self) -> CircuitBreakerResetResponse:
        """
        Reset all circuit breakers to closed state.

        Returns:
            Reset operation response

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("POST", "/api/circuit-breakers/reset")
            return CircuitBreakerResetResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to reset circuit breakers: {str(e)}")

    async def reset_circuit_breaker(self, name: str) -> CircuitBreakerResetResponse:
        """
        Reset a specific circuit breaker to closed state.

        Args:
            name: Name of the circuit breaker to reset

        Returns:
            Reset operation response

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("POST", f"/api/circuit-breakers/{name}/reset")
            return CircuitBreakerResetResponse(**response)
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerConnectionError(f"Circuit breaker '{name}' not found")
            raise EventStreamerConnectionError(f"Failed to reset circuit breaker: {str(e)}")

    async def get_circuit_breaker_config(self) -> CircuitBreakerConfigResponse:
        """
        Get circuit breaker configuration.

        Returns:
            Circuit breaker configuration

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", "/api/circuit-breakers/config")
            return CircuitBreakerConfigResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to get circuit breaker config: {str(e)}")

    # Chain Configuration Management Methods

    async def get_all_chains(self) -> ChainListResponse:
        """
        Get all active chain configurations.

        Returns:
            List of chain configurations

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", "/api/chains")
            return ChainListResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to get chain configurations: {str(e)}")

    async def get_chain_stats(self) -> ChainStatsResponse:
        """
        Get chain configuration manager statistics.

        Returns:
            Chain configuration statistics

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", "/api/chains/stats")
            return ChainStatsResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to get chain stats: {str(e)}")

    async def get_chain(self, chain_id: int) -> ChainConfigResponse:
        """
        Get configuration for a specific chain.

        Args:
            chain_id: ID of the chain

        Returns:
            Chain configuration

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", f"/api/chains/{chain_id}")
            return ChainConfigResponse(**response)
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerConnectionError(f"Chain {chain_id} not found")
            raise EventStreamerConnectionError(f"Failed to get chain configuration: {str(e)}")

    async def create_chain(self, config: ChainConfigRequest) -> ChainConfigResponse:
        """
        Create a new chain configuration.

        Args:
            config: Chain configuration to create

        Returns:
            Created chain configuration

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            config_data = config.model_dump()
            response = await self._request("POST", "/api/chains", json=config_data)
            return ChainConfigResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to create chain configuration: {str(e)}")

    async def update_chain(self, chain_id: int, config: ChainConfigRequest) -> ChainConfigResponse:
        """
        Update an existing chain configuration.

        Args:
            chain_id: ID of the chain to update
            config: Updated chain configuration

        Returns:
            Updated chain configuration

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            config_data = config.model_dump()
            response = await self._request("PUT", f"/api/chains/{chain_id}", json=config_data)
            return ChainConfigResponse(**response)
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerConnectionError(f"Chain {chain_id} not found")
            raise EventStreamerConnectionError(f"Failed to update chain configuration: {str(e)}")

    async def delete_chain(self, chain_id: int) -> ChainConfigResponse:
        """
        Delete (deactivate) a chain configuration.

        Args:
            chain_id: ID of the chain to delete

        Returns:
            Deleted chain configuration

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("DELETE", f"/api/chains/{chain_id}")
            return ChainConfigResponse(**response)
        except EventStreamerValidationError as e:
            if "404" in str(e):
                raise EventStreamerConnectionError(f"Chain {chain_id} not found")
            raise EventStreamerConnectionError(f"Failed to delete chain configuration: {str(e)}")

    async def refresh_chains(self) -> ChainConfigResponse:
        """
        Refresh chain configurations from database.

        Returns:
            Refresh operation response

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("POST", "/api/chains/refresh")
            return ChainConfigResponse(**response)
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to refresh chain configurations: {str(e)}")

    # Health Check Methods

    async def health_check(self) -> bool:
        """
        Check if the event streamer service is healthy.

        Returns:
            True if the service is healthy, False otherwise
        """
        try:
            response = await self._request("GET", "/health")
            return response.get("status") == "healthy"
        except Exception:
            return False

    async def get_health(self) -> dict[str, str]:
        """
        Get detailed health status from the event streamer service.

        Returns:
            Health status dictionary with 'status' key

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request("GET", "/health")
            return response
        except EventStreamerValidationError as e:
            raise EventStreamerConnectionError(f"Failed to get health status: {str(e)}")

    # Subscription Progress Methods

    async def get_subscription_last_processed_block(
        self, subscription_id: int, chain_id: int
    ) -> int | None:
        """
        Get the last processed block for a subscription from in-memory processors.

        This is a lightweight endpoint that doesn't hit the database - it returns
        the current processing progress directly from the historical or realtime
        processor's memory.

        Args:
            subscription_id: ID of the subscription
            chain_id: Chain ID for the subscription

        Returns:
            Last processed block number, or None if not found/not processing

        Raises:
            EventStreamerConnectionError: If request fails
        """
        try:
            response = await self._request(
                "GET",
                f"/subscriptions/{subscription_id}/last-processed-block",
                params={"chain_id": chain_id},
            )
            return response.get("last_processed_block")
        except EventStreamerValidationError as e:
            # 404 means subscription not found or not currently processing
            if "404" in str(e):
                return None
            raise EventStreamerConnectionError(
                f"Failed to get last processed block: {str(e)}"
            )
