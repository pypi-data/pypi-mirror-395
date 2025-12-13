"""Tests for ABI parsing functionality in the EventStreamer SDK."""

import pytest

from event_streamer_sdk import EventStreamer
from event_streamer_sdk.abi_parser import ABIParsingError


class TestABIParsing:
    """Test suite for ABI parsing functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = EventStreamer(
            service_url="http://localhost:8000", subscriber_id="test-subscriber"
        )

        self.erc20_abi = """[
            {
                "type": "event",
                "name": "Transfer",
                "inputs": [
                    {"indexed": true, "name": "from", "type": "address"},
                    {"indexed": true, "name": "to", "type": "address"},
                    {"indexed": false, "name": "value", "type": "uint256"}
                ]
            },
            {
                "type": "event",
                "name": "Approval",
                "inputs": [
                    {"indexed": true, "name": "owner", "type": "address"},
                    {"indexed": true, "name": "spender", "type": "address"},
                    {"indexed": false, "name": "value", "type": "uint256"}
                ]
            },
            {
                "type": "function",
                "name": "transfer",
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"}
                ],
                "outputs": [{"name": "", "type": "bool"}]
            }
        ]"""

    def test_extract_abi_event_success(self):
        """Test successful extraction of a specific event from ABI."""
        event = self.client.extract_abi_event(self.erc20_abi, "Transfer")

        assert event.name == "Transfer"
        assert event.type == "event"
        assert event.anonymous is False
        assert len(event.inputs) == 3

        # Check inputs
        from_input = event.inputs[0]
        assert from_input.name == "from"
        assert from_input.type == "address"
        assert from_input.indexed is True

        to_input = event.inputs[1]
        assert to_input.name == "to"
        assert to_input.type == "address"
        assert to_input.indexed is True

        value_input = event.inputs[2]
        assert value_input.name == "value"
        assert value_input.type == "uint256"
        assert value_input.indexed is False

    def test_extract_abi_event_not_found(self):
        """Test error when event is not found in ABI."""
        with pytest.raises(ABIParsingError) as exc_info:
            self.client.extract_abi_event(self.erc20_abi, "NonExistentEvent")

        assert "NonExistentEvent" in str(exc_info.value)
        assert "not found in ABI" in str(exc_info.value)
        assert "Transfer" in str(exc_info.value)  # Should list available events

    def test_extract_abi_events_all(self):
        """Test extraction of all events from ABI."""
        events = self.client.extract_abi_events(self.erc20_abi)

        assert len(events) == 2
        assert "Transfer" in events
        assert "Approval" in events

        # Check Transfer event
        transfer_event = events["Transfer"]
        assert transfer_event.name == "Transfer"
        assert len(transfer_event.inputs) == 3

        # Check Approval event
        approval_event = events["Approval"]
        assert approval_event.name == "Approval"
        assert len(approval_event.inputs) == 3

    def test_invalid_json(self):
        """Test error handling for invalid JSON."""
        with pytest.raises(ABIParsingError) as exc_info:
            self.client.extract_abi_event("{invalid json}", "Transfer")

        assert "Invalid JSON" in str(exc_info.value)

    def test_empty_abi(self):
        """Test error handling for empty ABI."""
        with pytest.raises(ABIParsingError) as exc_info:
            self.client.extract_abi_event("[]", "Transfer")

        assert "cannot be empty" in str(exc_info.value)

    def test_abi_with_no_events(self):
        """Test error when ABI contains no events."""
        function_only_abi = """[
            {
                "type": "function",
                "name": "transfer",
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"}
                ],
                "outputs": [{"name": "", "type": "bool"}]
            }
        ]"""

        with pytest.raises(ABIParsingError) as exc_info:
            self.client.extract_abi_event(function_only_abi, "Transfer")

        assert "not found in ABI" in str(exc_info.value)

    def test_complex_event_with_arrays(self):
        """Test parsing complex event with array types."""
        complex_abi = """[
            {
                "type": "event",
                "name": "ComplexEvent",
                "inputs": [
                    {"indexed": true, "name": "user", "type": "address"},
                    {"indexed": false, "name": "amounts", "type": "uint256[]"},
                    {"indexed": false, "name": "addresses", "type": "address[]"},
                    {"indexed": true, "name": "id", "type": "bytes32"}
                ]
            }
        ]"""

        event = self.client.extract_abi_event(complex_abi, "ComplexEvent")

        assert event.name == "ComplexEvent"
        assert len(event.inputs) == 4

        # Check array types
        amounts_input = event.inputs[1]
        assert amounts_input.name == "amounts"
        assert amounts_input.type == "uint256[]"
        assert amounts_input.indexed is False

        addresses_input = event.inputs[2]
        assert addresses_input.name == "addresses"
        assert addresses_input.type == "address[]"
        assert addresses_input.indexed is False

    def test_anonymous_event(self):
        """Test parsing anonymous event."""
        anonymous_abi = """[
            {
                "type": "event",
                "name": "AnonymousEvent",
                "anonymous": true,
                "inputs": [
                    {"indexed": true, "name": "user", "type": "address"},
                    {"indexed": false, "name": "value", "type": "uint256"}
                ]
            }
        ]"""

        event = self.client.extract_abi_event(anonymous_abi, "AnonymousEvent")

        assert event.name == "AnonymousEvent"
        assert event.anonymous is True
        assert len(event.inputs) == 2

    def test_event_with_no_inputs(self):
        """Test parsing event with no inputs."""
        no_inputs_abi = """[
            {
                "type": "event",
                "name": "SimpleEvent",
                "inputs": []
            }
        ]"""

        event = self.client.extract_abi_event(no_inputs_abi, "SimpleEvent")

        assert event.name == "SimpleEvent"
        assert len(event.inputs) == 0

    def test_duplicate_event_names(self):
        """Test error handling for duplicate event names in ABI."""
        duplicate_abi = """[
            {
                "type": "event",
                "name": "Transfer",
                "inputs": [
                    {"indexed": true, "name": "from", "type": "address"},
                    {"indexed": true, "name": "to", "type": "address"},
                    {"indexed": false, "name": "value", "type": "uint256"}
                ]
            },
            {
                "type": "event",
                "name": "Transfer",
                "inputs": [
                    {"indexed": true, "name": "sender", "type": "address"},
                    {"indexed": false, "name": "amount", "type": "uint256"}
                ]
            }
        ]"""

        with pytest.raises(ABIParsingError) as exc_info:
            self.client.extract_abi_events(duplicate_abi)

        assert "Duplicate event name" in str(exc_info.value)
        assert "Transfer" in str(exc_info.value)

    def test_event_missing_required_fields(self):
        """Test error handling for events missing required fields."""
        invalid_abi = """[
            {
                "type": "event",
                "inputs": [
                    {"indexed": true, "name": "user", "type": "address"}
                ]
            }
        ]"""

        with pytest.raises(ABIParsingError) as exc_info:
            self.client.extract_abi_events(invalid_abi)

        assert "missing 'name' field" in str(exc_info.value)

    def test_input_missing_type(self):
        """Test error handling for inputs missing type field."""
        invalid_input_abi = """[
            {
                "type": "event",
                "name": "InvalidEvent",
                "inputs": [
                    {"indexed": true, "name": "user"}
                ]
            }
        ]"""

        with pytest.raises(ABIParsingError) as exc_info:
            self.client.extract_abi_events(invalid_input_abi)

        assert "missing 'type' field" in str(exc_info.value)

    def test_extract_from_actual_contract_abi(self):
        """Test with a real-world contract ABI structure."""
        # This is a simplified version of an actual Uniswap V2 Pair ABI
        uniswap_abi = """[
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "amount0In",
                        "type": "uint256"
                    },
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "amount1In",
                        "type": "uint256"
                    },
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "amount0Out",
                        "type": "uint256"
                    },
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "amount1Out",
                        "type": "uint256"
                    },
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    }
                ],
                "name": "Swap",
                "type": "event"
            }
        ]"""

        event = self.client.extract_abi_event(uniswap_abi, "Swap")

        assert event.name == "Swap"
        assert len(event.inputs) == 6
        assert event.anonymous is False

        # Check that internalType is handled (should be ignored for now)
        sender_input = event.inputs[0]
        assert sender_input.name == "sender"
        assert sender_input.type == "address"
        assert sender_input.indexed is True
