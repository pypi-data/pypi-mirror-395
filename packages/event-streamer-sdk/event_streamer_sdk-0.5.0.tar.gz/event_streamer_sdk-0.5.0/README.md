# Event Streamer SDK

A comprehensive Python SDK for interacting with the Event Streamer blockchain event monitoring service. This SDK provides a simple and powerful way to subscribe to blockchain events and receive them via HTTP streaming connections with enterprise-grade features.

## What's New in v0.4.0

- 🤖 **Auto-Acknowledgment**: Configurable automatic event acknowledgment with batch processing
- 🔄 **Circuit Breaker Management**: Monitor and control RPC circuit breakers for resilience
- ⚙️ **Chain Configuration**: Full CRUD operations for blockchain chain configurations
- 🏗️ **Enhanced Tuple Support**: Complete ABI parsing with nested tuples and complex structures
- 📊 **Processing Status Monitoring**: Real-time subscription processing status checks
- 💗 **Client Heartbeats**: Bi-directional heartbeat system for connection health monitoring
- 🚀 **Bulk Operations**: Efficient bulk batch acknowledgment for high-throughput scenarios
- 🛡️ **Enhanced Error Handling**: Comprehensive error types with recovery patterns

## Features

- 🔗 **Simple API Client**: Easy subscription management with typed responses
- 🌊 **HTTP Streaming**: Real-time event delivery via HTTP streaming connections
- 🔄 **Resume Capability**: Automatic resume from last processed position
- 🔒 **Type Safety**: Full type hints and Pydantic model validation
- ⚡ **Async/Await**: Modern async Python patterns throughout
- 🎯 **Decorator Pattern**: Clean event handler registration
- 🛡️ **Error Handling**: Comprehensive error handling and connection management
- 💓 **Health Monitoring**: Built-in heartbeat and connection health tracking
- 📝 **ABI Parsing**: Built-in contract ABI parsing with full tuple support
- 🤖 **Auto-Acknowledgment**: Configurable automatic event acknowledgment
- 🔄 **Circuit Breaker Management**: Monitor and control RPC circuit breakers
- ⚙️ **Chain Configuration**: CRUD operations for blockchain chain configs
- 📊 **Processing Status**: Real-time subscription processing monitoring
- 🚀 **Bulk Operations**: Efficient bulk batch acknowledgment

## Installation

```bash
# Using UV (recommended)
uv add event-streamer-sdk

# Using pip
pip install event-streamer-sdk

# Development installation
git clone https://github.com/dcentralab/event-streamer-sdk
cd event-streamer-sdk
uv sync --dev
```

## Quick Start

### HTTP Streaming Example

```python
import asyncio
from event_streamer_sdk import EventStreamer
from event_streamer_sdk.models.subscriptions import SubscriptionCreate
from event_streamer_sdk.models.abi import ABIEvent, ABIInput

async def main():
    # Initialize the client
    async with EventStreamer(
        service_url="http://localhost:8000",
        subscriber_id="my-app"
    ) as client:

        # Create a subscription
        subscription = SubscriptionCreate(
            topic0="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            event_signature=ABIEvent(
                type="event",
                name="Transfer",
                inputs=[
                    ABIInput(name="from", type="address", indexed=True),
                    ABIInput(name="to", type="address", indexed=True),
                    ABIInput(name="value", type="uint256", indexed=False)
                ]
            ),
            addresses=["0xA0b86a33E6417b3c4555ba476F04245600306D5D"],
            start_block=19000000,
            end_block=19010000,
            chain_id=1,
            subscriber_id="my-app"
        )

        result = await client.create_subscription(subscription)
        print(f"Created subscription: {result.id}")

        # Create streaming client with auto-acknowledgment
        streaming_client = client.create_streaming_client(
            subscription_id=result.id,
            client_metadata={"version": "1.0.0"},
            auto_acknowledge=True  # Automatically acknowledge events after processing
        )

        # Register event handlers
        @streaming_client.on_event("Transfer")
        async def handle_transfers(events):
            for event in events:
                print(f"Transfer: {event['from']} -> {event['to']}: {event['value']}")

        # Start streaming
        await streaming_client.start_streaming()

        # Keep running to receive events
        try:
            while streaming_client.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            await streaming_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

### Resume Capability Example

```python
import asyncio
from event_streamer_sdk import EventStreamer

async def main():
    async with EventStreamer(
        service_url="http://localhost:8000",
        subscriber_id="my-app"
    ) as client:

        # Create streaming client with resume token and custom batch acknowledgment interval
        streaming_client = client.create_streaming_client(
            subscription_id=123,
            resume_token="rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi...",
            client_metadata={"version": "1.0.0"},
            auto_acknowledge=True,
            batch_ack_interval=5.0  # Send acknowledgments every 5 seconds
        )

        @streaming_client.on_event("Transfer")
        async def handle_transfers(events):
            for event in events:
                print(f"Transfer: {event['from']} -> {event['to']}: {event['value']}")

        # Optional: Handle heartbeats
        @streaming_client.on_heartbeat
        async def handle_heartbeat(heartbeat):
            print(f"Heartbeat: {heartbeat.timestamp}")

        # Optional: Handle errors
        @streaming_client.on_error
        async def handle_error(error):
            print(f"Error: {error.error_message}")

        # Start streaming
        await streaming_client.start_streaming()

        # Keep running and save resume token periodically
        try:
            while streaming_client.is_running:
                current_token = streaming_client.get_current_resume_token()
                # Save token to persistent storage
                await asyncio.sleep(30)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            await streaming_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## ABI Parsing

The SDK includes built-in ABI parsing functionality to make it easy to extract event definitions from contract ABIs without manually constructing `ABIEvent` objects.

### Extract Specific Event

```python
async def main():
    async with EventStreamer(
        service_url="http://localhost:8000",
        subscriber_id="my-app"
    ) as client:

        # Example ERC20 contract ABI
        erc20_abi = '''[
            {
                "type": "event",
                "name": "Transfer",
                "inputs": [
                    {"indexed": true, "name": "from", "type": "address"},
                    {"indexed": true, "name": "to", "type": "address"},
                    {"indexed": false, "name": "value", "type": "uint256"}
                ]
            }
        ]'''

        # Extract the Transfer event
        transfer_event = client.extract_abi_event(erc20_abi, "Transfer")

        # Use in subscription
        subscription = SubscriptionCreate(
            topic0="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            event_signature=transfer_event,  # Use parsed event
            addresses=["0x..."],
            start_block=19000000,
            chain_id=1
        )
```

### Extract All Events

```python
# Extract all events from an ABI
all_events = client.extract_abi_events(erc20_abi)
transfer_event = all_events["Transfer"]
approval_event = all_events["Approval"]
```

### Complex Tuple Support

The SDK fully supports complex tuple structures common in DeFi protocols:

```python
# Example: Uniswap V3 position event with nested tuples
uniswap_abi = '''[{
    "type": "event",
    "name": "PositionUpdated",
    "inputs": [{
        "name": "position",
        "type": "tuple",
        "components": [
            {"name": "liquidity", "type": "uint128"},
            {"name": "tickLower", "type": "int24"},
            {"name": "tickUpper", "type": "int24"},
            {
                "name": "fees",
                "type": "tuple",
                "components": [
                    {"name": "token0", "type": "uint256"},
                    {"name": "token1", "type": "uint256"}
                ]
            }
        ]
    }]
}]'''

# Extract event with nested tuple structure
position_event = client.extract_abi_event(uniswap_abi, "PositionUpdated")
print(f"Tuple components: {len(position_event.inputs[0].components)}")
```

### Error Handling

```python
try:
    event = client.extract_abi_event(abi_json, "NonExistentEvent")
except Exception as e:
    print(f"Event not found: {e}")
    # Error message includes available events

# Parse complete contract ABI with validation
try:
    parsed_abi = client.parse_contract_abi(contract_abi)
    events = parsed_abi["events"]
    functions = parsed_abi["functions"]
except Exception as e:
    print(f"ABI parsing failed: {e}")
```

### Supported ABI Features

- ✅ **Event definitions**: Full support for event parsing
- ✅ **Indexed parameters**: Correctly handles indexed/non-indexed inputs
- ✅ **Array types**: Supports `uint256[]`, `address[]`, etc.
- ✅ **Anonymous events**: Handles anonymous event flag
- ✅ **Complex types**: Support for most Solidity types
- ✅ **Tuple components**: Full support for nested tuples and structs
- ✅ **Array of tuples**: Supports `tuple[]` and complex array structures
- ✅ **Nested structures**: Deep tuple validation with recursive parsing
- ✅ **Error handling**: Clear error messages with available events

## API Reference

### EventStreamer

The main client class for interacting with the Event Streamer service.

```python
class EventStreamer:
    def __init__(
        self,
        service_url: str,
        subscriber_id: str,
        *,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
    )
```

#### Subscription Management

```python
# Create a subscription
async def create_subscription(self, subscription: SubscriptionCreate) -> SubscriptionResponse

# List subscriptions
async def list_subscriptions(self, page: int = 1, page_size: int = 20) -> SubscriptionListResponse

# Get a specific subscription
async def get_subscription(self, subscription_id: int) -> SubscriptionResponse

# Update a subscription
async def update_subscription(self, subscription_id: int, update: SubscriptionUpdate) -> SubscriptionResponse

# Delete a subscription
async def delete_subscription(self, subscription_id: int) -> bool
```

#### Streaming Client Creation

```python
# Create a streaming client for a subscription
def create_streaming_client(
    self,
    subscription_id: int,
    *,
    resume_token: str | None = None,
    client_metadata: dict[str, Any] | None = None,
    auto_acknowledge: bool = True,
    batch_ack_interval: float = 3.0,
) -> StreamingClient
```

#### ABI Parsing Methods

```python
# Extract specific event from contract ABI
def extract_abi_event(self, abi_json: str, event_name: str) -> ABIEvent

# Extract all events from contract ABI
def extract_abi_events(self, abi_json: str) -> dict[str, ABIEvent]

# Parse complete contract ABI with structured data
def parse_contract_abi(self, abi_json: str) -> dict[str, Any]
```

#### Circuit Breaker Management

```python
# Get status of all circuit breakers
async def get_circuit_breaker_status(self) -> CircuitBreakerStatusResponse

# Get circuit breaker health summary
async def get_circuit_breaker_health(self) -> CircuitBreakerHealthResponse

# Get detailed metrics for specific circuit breaker
async def get_circuit_breaker_metrics(self, name: str) -> CircuitBreakerMetrics

# Reset all circuit breakers to closed state
async def reset_all_circuit_breakers(self) -> CircuitBreakerResetResponse

# Reset specific circuit breaker
async def reset_circuit_breaker(self, name: str) -> CircuitBreakerResetResponse

# Get circuit breaker configuration
async def get_circuit_breaker_config(self) -> CircuitBreakerConfigResponse
```

#### Chain Configuration Management

```python
# Get all active chain configurations
async def get_all_chains(self) -> ChainListResponse

# Get chain configuration statistics
async def get_chain_stats(self) -> ChainStatsResponse

# Get specific chain configuration
async def get_chain(self, chain_id: int) -> ChainConfigResponse

# Create new chain configuration
async def create_chain(self, config: ChainConfigRequest) -> ChainConfigResponse

# Update existing chain configuration
async def update_chain(self, chain_id: int, config: ChainConfigRequest) -> ChainConfigResponse

# Delete (deactivate) chain configuration
async def delete_chain(self, chain_id: int) -> ChainConfigResponse

# Refresh chain configurations from database
async def refresh_chains(self) -> ChainConfigResponse
```

### StreamingClient

The streaming client handles real-time event delivery via HTTP streaming connections.

#### Connection Management

```python
# Connect to streaming endpoint
async def connect() -> None

# Start streaming events
async def start_streaming() -> None

# Stop streaming events
async def stop_streaming() -> None

# Disconnect from streaming
async def disconnect() -> None

# Resume from a specific position
async def resume(resume_token: str) -> None

# Get current resume token
def get_current_resume_token() -> str | None

# Check subscription processing status
async def check_processing_status() -> ProcessingStatusResponse

# Send client heartbeat
async def send_heartbeat() -> ClientHeartbeatResponse

# Acknowledge single batch
async def acknowledge_batch(batch_id: str) -> None

# Acknowledge multiple batches (bulk operation)
async def acknowledge_batch_bulk(batch_ids: list[str]) -> BulkBatchAcknowledgmentResponse
```

#### Event Handler Registration

```python
# Handle specific event types
@client.on_event("Transfer")
async def handle_transfers(events: List[Dict[str, Any]]):
    for event in events:
        # Process event
        pass

# Handle all events
@client.on_all_events
async def handle_all_events(events: Dict[str, List[Dict[str, Any]]]):
    for event_name, event_list in events.items():
        # Process events by type
        pass

# Handle heartbeat messages
@client.on_heartbeat
async def handle_heartbeat(heartbeat: StreamingHeartbeat):
    print(f"Heartbeat: {heartbeat.timestamp}")

# Handle error messages
@client.on_error
async def handle_error(error: StreamingError):
    print(f"Error: {error.error_message}")
```

### Models

#### SubscriptionCreate

```python
class SubscriptionCreate(BaseModel):
    topic0: str                    # Event signature hash
    event_signature: ABIEvent      # ABI event definition
    addresses: List[str] = []      # Contract addresses (empty = all)
    start_block: int               # Starting block number
    end_block: Optional[int] = None # Ending block (None = live)
    chain_id: int                  # Blockchain network ID
    subscriber_id: str             # Your service identifier
```

#### ABIEvent

```python
class ABIEvent(BaseModel):
    type: Literal["event"]
    name: str                      # Event name
    inputs: List[ABIInput] = []    # Event parameters
    anonymous: bool = False
```

#### ABIInput

```python
class ABIInput(BaseModel):
    name: Optional[str] = None     # Parameter name
    type: str                      # Solidity type (e.g., "address", "uint256")
    indexed: Optional[bool] = False # Whether parameter is indexed
```

## Event Data Format

Events are delivered via streaming in batches with the following format:

```python
{
    "type": "event_batch",
    "response_id": "550e8400-e29b-41d4-a716-446655440000",
    "subscription_id": 123,
    "connection_id": "conn_550e8400-e29b-41d4-a716-446655440000",
    "resume_token": "rt_eyJzdWJzY3JpcHRpb25faWQiOjEyMywi...",
    "events": {
        "Transfer": [
            {
                # Event-specific fields
                "from": "0x1234567890123456789012345678901234567890",
                "to": "0x0987654321098765432109876543210987654321",
                "value": "1000000000000000000",

                # Metadata fields
                "block_number": 19000001,
                "transaction_hash": "0xabcdef...",
                "log_index": 0,
                "address": "0xA0b86a33E6417b3c4555ba476F04245600306D5D",
                "timestamp": "2024-05-23T10:30:00.000Z"
            }
        ]
    },
    "batch_size": 1,
    "timestamp": "2024-05-23T10:30:00.000Z"
}
```

### Streaming Message Types

The streaming connection delivers different types of messages:

#### Event Batch

Contains actual blockchain events for processing.

#### Heartbeat

Periodic heartbeat messages to maintain connection health:

```python
{
    "type": "heartbeat",
    "connection_id": "conn_550e8400-e29b-41d4-a716-446655440000",
    "subscription_id": 123,
    "timestamp": "2024-05-23T10:30:00.000Z"
}
```

#### Error Messages

Error notifications and connection issues:

```python
{
    "type": "error",
    "connection_id": "conn_550e8400-e29b-41d4-a716-446655440000",
    "subscription_id": 123,
    "error_code": "CONNECTION_LOST",
    "error_message": "Connection lost due to network timeout",
    "timestamp": "2024-05-23T10:30:00.000Z"
}
```

## Supported Chains

The SDK supports all chains configured in your Event Streamer service:

The SDK supports all chains configured in your Event Streamer service. Common supported chains include:

- **Ethereum Mainnet** (Chain ID: 1)
- **Polygon** (Chain ID: 137)
- **Base** (Chain ID: 8453)
- **Arbitrum One** (Chain ID: 42161)
- **Optimism** (Chain ID: 10)
- **Avalanche** (Chain ID: 43114)
- **Binance Smart Chain** (Chain ID: 56)

You can query available chains using:

```python
chains = await client.get_all_chains()
for chain in chains.chains:
    print(f"Chain {chain.chain_id}: {chain.name} - Status: {chain.status}")
```

## Error Handling

The SDK provides comprehensive error handling:

```python
from event_streamer_sdk.exceptions import (
    EventStreamerSDKError,           # Base exception
    EventStreamerConnectionError,    # Connection issues
    EventStreamerAuthError,          # Authentication errors
    EventStreamerTimeoutError,       # Request timeouts
    EventStreamerValidationError,    # Validation errors
    EventStreamerSubscriptionError,  # Subscription errors
)

try:
    subscription = await client.create_subscription(subscription_data)
except EventStreamerValidationError as e:
    print(f"Invalid subscription data: {e}")
except EventStreamerConnectionError as e:
    print(f"Connection failed: {e}")
except EventStreamerSubscriptionError as e:
    print(f"Subscription operation failed: {e}")
except EventStreamerTimeoutError as e:
    print(f"Request timed out: {e}")
except EventStreamerAuthError as e:
    print(f"Authentication failed: {e}")

# Circuit breaker error handling
try:
    status = await client.get_circuit_breaker_status()
except EventStreamerConnectionError as e:
    print(f"Failed to get circuit breaker status: {e}")
    # Circuit breakers may be open - check individual services

# Chain configuration error handling
try:
    chain = await client.get_chain(999)  # Non-existent chain
except EventStreamerConnectionError as e:
    if "404" in str(e):
        print("Chain not found")
    else:
        print(f"Service error: {e}")

# Streaming error handling with recovery
@streaming_client.on_error
async def handle_streaming_error(error):
    if error.error_code == "SUBSCRIPTION_NOT_FOUND":
        print("Subscription deleted - recreating...")
        # Recreate subscription and restart streaming
    elif error.error_code == "CIRCUIT_BREAKER_OPEN":
        print("Circuit breaker open - waiting for recovery...")
        await asyncio.sleep(30)
        # Retry connection
    elif error.error_code == "RATE_LIMITED":
        print("Rate limited - backing off...")
        await asyncio.sleep(60)
    else:
        print(f"Unhandled error: {error.error_message}")
```

## Circuit Breaker Management

The SDK provides comprehensive circuit breaker monitoring and control to ensure system resilience:

```python
# Monitor circuit breaker status
status = await client.get_circuit_breaker_status()
print(f"Circuit breakers: {len(status.circuit_breakers)}")
for cb_name, cb_status in status.circuit_breakers.items():
    print(f"  {cb_name}: {cb_status.state} (failures: {cb_status.failure_count})")

# Check overall system health
health = await client.get_circuit_breaker_health()
print(f"Healthy RPC clients: {health.healthy_rpcs}/{health.total_rpcs}")
if health.unhealthy_chains:
    print(f"Unhealthy chains: {health.unhealthy_chains}")

# Get detailed metrics for specific circuit breaker
metrics = await client.get_circuit_breaker_metrics("ethereum_rpc")
print(f"Success rate: {metrics.success_rate:.2%}")
print(f"Average response time: {metrics.average_response_time:.2f}ms")

# Reset circuit breakers when needed
reset_result = await client.reset_all_circuit_breakers()
print(f"Reset {reset_result.reset_count} circuit breakers")

# Reset specific circuit breaker
await client.reset_circuit_breaker("polygon_rpc")
print("Polygon RPC circuit breaker reset")
```

## Chain Configuration Management

Manage blockchain chain configurations programmatically:

```python
# List all active chains
chains = await client.get_all_chains()
print(f"Active chains: {len(chains.chains)}")
for chain in chains.chains:
    print(f"  Chain {chain.chain_id}: {chain.name} - {chain.status}")

# Get chain statistics
stats = await client.get_chain_stats()
print(f"Total chains: {stats.total_chains}")
print(f"Active chains: {stats.active_chains}")
print(f"Healthy RPC endpoints: {stats.healthy_rpcs}")

# Get specific chain configuration
chain = await client.get_chain(1)  # Ethereum mainnet
print(f"Chain: {chain.name}")
print(f"RPC URLs: {chain.rpc_urls}")
print(f"Block time: {chain.average_block_time}s")

# Create new chain configuration
from event_streamer_schemas import ChainConfigRequest

new_chain = ChainConfigRequest(
    chain_id=137,
    name="Polygon",
    rpc_urls=["https://polygon-rpc.com"],
    average_block_time=2.0,
    max_blocks_per_request=100,
    confirmation_blocks=10
)
result = await client.create_chain(new_chain)
print(f"Created chain: {result.chain_id}")

# Refresh configurations from database
await client.refresh_chains()
print("Chain configurations refreshed")
```

## Processing Status Monitoring

Monitor real-time subscription processing status:

```python
# Check if subscription is being processed
status = await streaming_client.check_processing_status()
print(f"Subscription {status.subscription_id} processing: {status.is_processing}")
print(f"Active connections: {status.connection_count}")

# Monitor processing in a loop
import asyncio

while True:
    status = await streaming_client.check_processing_status()
    if not status.is_processing:
        print("⚠️  Subscription not being processed - may need to start streaming")

    await asyncio.sleep(30)  # Check every 30 seconds
```

## Bulk Acknowledgment

Improve performance with bulk batch acknowledgment:

```python
# Collect batch IDs for bulk acknowledgment
batch_ids = []

@streaming_client.on_event("Transfer")
async def handle_transfers(events):
    # Process events
    for event in events:
        print(f"Processing transfer: {event['transaction_hash']}")

    # Note: With auto_acknowledge=False, you need manual acknowledgment
    # The batch_id is available in the handler context
    batch_ids.append(current_batch_id)

# Periodically send bulk acknowledgments
async def bulk_ack_task():
    while streaming_client.is_running:
        if batch_ids:
            ids_to_ack = batch_ids.copy()
            batch_ids.clear()

            result = await streaming_client.acknowledge_batch_bulk(ids_to_ack)
            print(f"Acknowledged {result.acknowledged_batches} batches")
            print(f"Total events acknowledged: {result.total_events_acknowledged}")

            if result.failed_batch_ids:
                print(f"Failed to acknowledge: {result.failed_batch_ids}")
                batch_ids.extend(result.failed_batch_ids)  # Retry later

        await asyncio.sleep(5)  # Bulk acknowledge every 5 seconds

# Run bulk acknowledgment task
bulk_task = asyncio.create_task(bulk_ack_task())
```

## Best Practices

### 1. Use Context Managers

Always use the EventStreamer as an async context manager to ensure proper cleanup:

```python
async with EventStreamer(service_url, subscriber_id) as client:
    # Your code here
    pass
```

### 2. Handle Events Efficiently

Process events quickly in your handlers to avoid blocking the streaming connection:

```python
@client.on_event("Transfer")
async def handle_transfers(events):
    # Process quickly to avoid blocking
    for event in events:
        await process_event_async(event)
```

### 3. Use Specific Event Handlers

Register handlers for specific event types rather than using only the global handler:

```python
@client.on_event("Transfer")
async def handle_transfers(events):
    # Specific handling for transfers
    pass

@client.on_event("Approval")
async def handle_approvals(events):
    # Specific handling for approvals
    pass
```

### 4. Implement Resume Token Persistence

Save resume tokens to persistent storage to resume from the correct position after restarts:

```python
# Save resume token periodically
resume_token = streaming_client.get_current_resume_token()
await save_resume_token_to_storage(subscription_id, resume_token)

# Resume from saved position
saved_token = await load_resume_token_from_storage(subscription_id)
streaming_client = client.create_streaming_client(
    subscription_id=subscription_id,
    resume_token=saved_token
)
```

### 5. Handle Connection Errors Gracefully

Implement proper error handling for connection issues:

```python
@streaming_client.on_error
async def handle_error(error):
    if error.error_code == "CONNECTION_LOST":
        # Implement reconnection logic with exponential backoff
        await reconnect_with_backoff()
    elif error.error_code == "PROCESSING_STOPPED":
        # Subscription processing stopped
        print("Processing stopped - checking status...")
        status = await streaming_client.check_processing_status()
        if not status.is_processing:
            print("Restarting processing...")
            await streaming_client.start_streaming()
    else:
        # Log and handle other errors
        print(f"Streaming error [{error.error_code}]: {error.error_message}")

# Implement exponential backoff for reconnection
import random

async def reconnect_with_backoff(max_retries=5):
    for attempt in range(max_retries):
        try:
            await streaming_client.disconnect()
            await asyncio.sleep(2 ** attempt + random.uniform(0, 1))
            await streaming_client.connect()
            await streaming_client.start_streaming()
            print(f"Reconnected successfully on attempt {attempt + 1}")
            return
        except Exception as e:
            print(f"Reconnection attempt {attempt + 1} failed: {e}")

    print("Max reconnection attempts reached")
```

### 6. Monitor Connection Health

Use both server and client heartbeats to monitor connection health:

```python
# Handle server heartbeats
@streaming_client.on_heartbeat
async def handle_server_heartbeat(heartbeat):
    # Server heartbeat received
    print(f"Server heartbeat: {heartbeat.timestamp}")
    last_server_heartbeat = heartbeat.timestamp

# Client heartbeats are sent automatically every 30 seconds
# You can also send manual heartbeats
try:
    response = await streaming_client.send_heartbeat()
    print(f"Client heartbeat acknowledged at {response.timestamp}")
except Exception as e:
    print(f"Heartbeat failed: {e}")
    # Connection may be unhealthy

# Monitor heartbeat health
heartbeat_failures = 0
max_failures = 3

async def monitor_connection_health():
    global heartbeat_failures
    while streaming_client.is_running:
        try:
            await streaming_client.send_heartbeat()
            heartbeat_failures = 0  # Reset on success
        except Exception:
            heartbeat_failures += 1
            if heartbeat_failures >= max_failures:
                print("Connection unhealthy - reconnecting...")
                await streaming_client.disconnect()
                await streaming_client.connect()
                heartbeat_failures = 0

        await asyncio.sleep(30)
```

### 7. Handle Auto-Acknowledgment

Configure automatic acknowledgment for optimal performance:

```python
# Enable auto-acknowledgment with custom interval
streaming_client = client.create_streaming_client(
    subscription_id=subscription_id,
    auto_acknowledge=True,
    batch_ack_interval=5.0  # Send acks every 5 seconds
)

# Auto-acknowledgment happens after successful handler execution
@streaming_client.on_event("Transfer")
async def handle_transfers(events):
    # Process events - if this succeeds, batch is auto-acknowledged
    for event in events:
        await process_transfer(event)
    # No manual acknowledgment needed!

# Disable auto-acknowledgment for manual control
streaming_client = client.create_streaming_client(
    subscription_id=subscription_id,
    auto_acknowledge=False
)

@streaming_client.on_event("Transfer")
async def handle_transfers_manual(events):
    # Process events
    for event in events:
        await process_transfer(event)

    # Manual acknowledgment required
    batch_id = get_current_batch_id()  # Implementation specific
    await streaming_client.acknowledge_batch(batch_id)
```
