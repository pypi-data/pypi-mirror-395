"""
ABI parsing utilities for Event Streamer SDK.

This module provides functionality to parse contract JSON ABI and extract
ABIEvent structures for use in the Event Streamer system. Features include:

- Complete ABI parsing with validation
- Event extraction from contract ABIs
- Support for complex tuple/struct components with nested structures
- Recursive tuple validation and parsing
- Array of tuples support
- Comprehensive error handling and validation

Tuple Support:
The parser fully supports Solidity tuple types, including:
- Simple tuples with basic types (uint256, address, bool, etc.)
- Nested tuples (structs within structs)
- Arrays of tuples (tuple[])
- Complex DeFi protocol structures

Example:
    >>> from event_streamer_sdk.abi_parser import extract_abi_event
    >>> abi_json = '''[{
    ...     "type": "event",
    ...     "name": "Transfer",
    ...     "inputs": [{
    ...         "name": "data",
    ...         "type": "tuple",
    ...         "components": [
    ...             {"name": "amount", "type": "uint256"},
    ...             {"name": "token", "type": "address"}
    ...         ]
    ...     }]
    ... }]'''
    >>> event = extract_abi_event(abi_json, "Transfer")
    >>> tuple_input = event.inputs[0]
    >>> print(f"Components: {len(tuple_input.components)}")
    Components: 2
"""

import json
from typing import Any

from .exceptions import EventStreamerValidationError
from .models.abi import ABIEvent, ABIInput


class ABIParsingError(EventStreamerValidationError):
    """Exception raised when ABI parsing fails."""

    pass


class ABIParser:
    """
    Parser for contract ABI JSON to extract event definitions.

    This class handles parsing of contract ABI JSON strings and extracting
    event definitions that can be used with the Event Streamer system.
    """

    def __init__(self):
        """Initialize the ABI parser."""
        pass

    def parse_abi_json(self, abi_json: str) -> list[dict[str, Any]]:
        """
        Parse ABI JSON string into a list of ABI elements.

        Args:
            abi_json: JSON string containing contract ABI

        Returns:
            List of ABI elements as dictionaries

        Raises:
            ABIParsingError: If JSON is invalid or malformed
        """
        try:
            abi_data = json.loads(abi_json)
        except json.JSONDecodeError as e:
            raise ABIParsingError(f"Invalid JSON in ABI: {e}") from e

        if not isinstance(abi_data, list):
            raise ABIParsingError("ABI must be a JSON array")

        if not abi_data:
            raise ABIParsingError("ABI cannot be empty")

        # Validate each element has required fields
        for i, element in enumerate(abi_data):
            if not isinstance(element, dict):
                raise ABIParsingError(f"ABI element {i} must be an object")

            if "type" not in element:
                raise ABIParsingError(f"ABI element {i} missing 'type' field")

        return abi_data

    def extract_events_from_abi(self, abi_data: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        """
        Extract event definitions from parsed ABI data.

        Args:
            abi_data: List of ABI elements as dictionaries

        Returns:
            Dictionary mapping event names to event definitions

        Raises:
            ABIParsingError: If events are invalid or malformed
        """
        events = {}

        for element in abi_data:
            if element.get("type") == "event":
                event_name = element.get("name")

                if not event_name:
                    raise ABIParsingError("Event definition missing 'name' field")

                if not isinstance(event_name, str):
                    raise ABIParsingError("Event name must be a string")

                if event_name in events:
                    raise ABIParsingError(f"Duplicate event name: {event_name}")

                # Validate event structure
                self._validate_event_structure(element)

                events[event_name] = element

        return events

    def _validate_event_structure(self, event_def: dict[str, Any]) -> None:
        """
        Validate the structure of an event definition.

        Args:
            event_def: Event definition dictionary

        Raises:
            ABIParsingError: If event structure is invalid
        """
        # Check required fields
        if "name" not in event_def:
            raise ABIParsingError("Event definition missing 'name' field")

        # Validate inputs array
        inputs = event_def.get("inputs", [])
        if not isinstance(inputs, list):
            raise ABIParsingError("Event 'inputs' must be an array")

        # Validate each input
        for i, input_def in enumerate(inputs):
            if not isinstance(input_def, dict):
                raise ABIParsingError(f"Event input {i} must be an object")

            if "type" not in input_def:
                raise ABIParsingError(f"Event input {i} missing 'type' field")

            if not isinstance(input_def["type"], str):
                raise ABIParsingError(f"Event input {i} 'type' must be a string")

            # Validate indexed field if present
            if "indexed" in input_def and not isinstance(input_def["indexed"], bool):
                raise ABIParsingError(f"Event input {i} 'indexed' must be a boolean")

            # Validate name field if present
            if "name" in input_def and not isinstance(input_def["name"], str):
                raise ABIParsingError(f"Event input {i} 'name' must be a string")

            # Validate components for tuple types
            if "components" in input_def:
                self._validate_components(input_def["components"], f"Event input {i}")

    def _validate_components(self, components_def: Any, context: str) -> None:
        """
        Validate tuple/struct components structure.

        Args:
            components_def: Components definition to validate
            context: Context string for error messages (e.g., "Event input 0")

        Raises:
            ABIParsingError: If component validation fails
        """
        if components_def is None:
            return

        if not isinstance(components_def, list):
            raise ABIParsingError(f"{context} components must be an array")

        # Validate each component recursively
        for i, component_def in enumerate(components_def):
            if not isinstance(component_def, dict):
                raise ABIParsingError(f"{context} component {i} must be an object")

            if "type" not in component_def:
                raise ABIParsingError(f"{context} component {i} missing 'type' field")

            if not isinstance(component_def["type"], str):
                raise ABIParsingError(f"{context} component {i} 'type' must be a string")

            # Validate name field if present
            if "name" in component_def and not isinstance(component_def["name"], str):
                raise ABIParsingError(f"{context} component {i} 'name' must be a string")

            # Validate indexed field if present
            if "indexed" in component_def and not isinstance(component_def["indexed"], bool):
                raise ABIParsingError(f"{context} component {i} 'indexed' must be a boolean")

            # Recursively validate nested components
            if "components" in component_def:
                self._validate_components(component_def["components"], f"{context} component {i}")

    def _convert_components(self, components_def: Any) -> list[ABIInput] | None:
        """
        Convert tuple/struct components to ABIInput objects.

        Args:
            components_def: Components definition (list of dictionaries or None)

        Returns:
            List of ABIInput objects for components, or None if no components

        Raises:
            ABIParsingError: If component validation fails
        """
        if components_def is None:
            return None

        if not isinstance(components_def, list):
            raise ABIParsingError("Components must be an array")

        if not components_def:  # Empty list
            return []

        converted_components = []
        for i, component_def in enumerate(components_def):
            if not isinstance(component_def, dict):
                raise ABIParsingError(f"Component {i} must be an object")

            if "type" not in component_def:
                raise ABIParsingError(f"Component {i} missing 'type' field")

            if not isinstance(component_def["type"], str):
                raise ABIParsingError(f"Component {i} 'type' must be a string")

            # Validate name field if present
            if "name" in component_def and not isinstance(component_def["name"], str):
                raise ABIParsingError(f"Component {i} 'name' must be a string")

            # Recursively handle nested components (for nested tuples)
            nested_components = self._convert_components(component_def.get("components"))

            component = ABIInput(
                name=component_def.get("name"),
                type=component_def["type"],
                indexed=component_def.get("indexed", False),
                internalType=component_def.get("internalType"),
                components=nested_components,
            )
            converted_components.append(component)

        return converted_components

    def convert_to_abi_event(self, event_def: dict[str, Any]) -> ABIEvent:
        """
        Convert a raw event definition to an ABIEvent object.

        Args:
            event_def: Raw event definition dictionary

        Returns:
            ABIEvent object

        Raises:
            ABIParsingError: If conversion fails
        """
        try:
            # Convert inputs to ABIInput objects
            inputs = []
            for input_def in event_def.get("inputs", []):
                abi_input = ABIInput(
                    name=input_def.get("name"),
                    type=input_def["type"],
                    indexed=input_def.get("indexed", False),
                    internalType=input_def.get("internalType"),
                    components=self._convert_components(input_def.get("components")),
                )
                inputs.append(abi_input)

            # Create ABIEvent object
            abi_event = ABIEvent(
                type="event",
                name=event_def["name"],
                inputs=inputs,
                anonymous=event_def.get("anonymous", False),
            )

            return abi_event

        except Exception as e:
            raise ABIParsingError(
                f"Failed to convert event '{event_def.get('name', 'unknown')}': {e}"
            ) from e

    def extract_abi_event(self, abi_json: str, event_name: str) -> ABIEvent:
        """
        Extract a specific event from ABI JSON.

        Args:
            abi_json: JSON string containing contract ABI
            event_name: Name of the event to extract

        Returns:
            ABIEvent object for the specified event

        Raises:
            ABIParsingError: If parsing fails or event not found
        """
        # Parse the ABI JSON
        abi_data = self.parse_abi_json(abi_json)

        # Extract all events
        events = self.extract_events_from_abi(abi_data)

        # Find the specific event
        if event_name not in events:
            available_events = list(events.keys())
            raise ABIParsingError(
                f"Event '{event_name}' not found in ABI. Available events: {available_events}"
            )

        # Convert to ABIEvent
        return self.convert_to_abi_event(events[event_name])

    def extract_abi_events(self, abi_json: str) -> dict[str, ABIEvent]:
        """
        Extract all events from ABI JSON.

        Args:
            abi_json: JSON string containing contract ABI

        Returns:
            Dictionary mapping event names to ABIEvent objects

        Raises:
            ABIParsingError: If parsing fails
        """
        # Parse the ABI JSON
        abi_data = self.parse_abi_json(abi_json)

        # Extract all events
        events = self.extract_events_from_abi(abi_data)

        # Convert all events to ABIEvent objects
        abi_events = {}
        for event_name, event_def in events.items():
            abi_events[event_name] = self.convert_to_abi_event(event_def)

        return abi_events

    def parse_contract_abi(self, abi_json: str) -> dict[str, Any]:
        """
        Parse complete contract ABI and return structured data.

        Args:
            abi_json: JSON string containing contract ABI

        Returns:
            Dictionary containing parsed ABI data with events, functions, etc.

        Raises:
            ABIParsingError: If parsing fails
        """
        # Parse the ABI JSON
        abi_data = self.parse_abi_json(abi_json)

        # Categorize ABI elements
        result = {
            "events": {},
            "functions": {},
            "constructor": None,
            "fallback": None,
            "receive": None,
            "errors": {},
            "raw": abi_data,
        }

        for element in abi_data:
            element_type = element.get("type")

            if element_type == "event":
                event_name = element.get("name")
                if event_name:
                    result["events"][event_name] = element

            elif element_type == "function":
                function_name = element.get("name")
                if function_name:
                    # Handle function overloading by using signature
                    if function_name not in result["functions"]:
                        result["functions"][function_name] = []
                    result["functions"][function_name].append(element)

            elif element_type == "constructor":
                result["constructor"] = element

            elif element_type == "fallback":
                result["fallback"] = element

            elif element_type == "receive":
                result["receive"] = element

            elif element_type == "error":
                error_name = element.get("name")
                if error_name:
                    result["errors"][error_name] = element

        return result


# Default parser instance
_default_parser = ABIParser()


# Convenience functions that use the default parser
def extract_abi_event(abi_json: str, event_name: str) -> ABIEvent:
    """
    Extract a specific event from ABI JSON using the default parser.

    Args:
        abi_json: JSON string containing contract ABI
        event_name: Name of the event to extract

    Returns:
        ABIEvent object for the specified event
    """
    return _default_parser.extract_abi_event(abi_json, event_name)


def extract_abi_events(abi_json: str) -> dict[str, ABIEvent]:
    """
    Extract all events from ABI JSON using the default parser.

    Args:
        abi_json: JSON string containing contract ABI

    Returns:
        Dictionary mapping event names to ABIEvent objects
    """
    return _default_parser.extract_abi_events(abi_json)


def parse_contract_abi(abi_json: str) -> dict[str, Any]:
    """
    Parse complete contract ABI using the default parser.

    Args:
        abi_json: JSON string containing contract ABI

    Returns:
        Dictionary containing parsed ABI data
    """
    return _default_parser.parse_contract_abi(abi_json)
