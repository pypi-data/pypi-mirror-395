import re
from typing import Literal, cast

# Import eth_typing types
from eth_typing import (
    ABI,
    TypeStr,
)
from eth_typing import (
    ABIComponent as EthABIComponent,
)
from eth_typing import (
    ABIComponentIndexed as EthABIComponentIndexed,
)
from eth_typing import (
    ABIConstructor as EthABIConstructor,
)
from eth_typing import (
    ABIError as EthABIError,
)
from eth_typing import (
    ABIEvent as EthABIEvent,
)
from eth_typing import (
    ABIFallback as EthABIFallback,
)
from eth_typing import (
    ABIFunction as EthABIFunction,
)
from eth_typing import (
    ABIReceive as EthABIReceive,
)
from pydantic import BaseModel, Field, field_validator


class ABIInput(BaseModel):
    """Schema for function/event inputs and outputs, compatible with eth_typing.ABIComponent"""

    name: str | None = None
    type: TypeStr
    indexed: bool | None = False  # For events (ABIComponentIndexed)
    internalType: str | None = None
    components: list["ABIInput"] | None = None  # For tuples/structs

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Comprehensive validation for Solidity types"""
        # Remove array suffixes for base type validation
        base_type = re.sub(r"\[.*?\]", "", v)

        # Validate array notation if present
        if "[" in v:
            # Find all array brackets and their contents
            array_matches = re.findall(r"\[([^\]]*)\]", v)
            for match in array_matches:
                if match:  # Non-empty bracket content (fixed-size array)
                    try:
                        size = int(match)
                        if size <= 0:
                            raise ValueError(f"Invalid array size: {size}")
                    except ValueError as e:
                        if "invalid literal" in str(e):
                            raise ValueError(f"Invalid array size: {match}") from e
                        else:
                            raise  # Re-raise our custom error
                # Empty brackets [] are valid (dynamic arrays)

        # Elementary types validation
        if base_type in ["address", "bool", "string", "bytes"]:
            return v

        # Fixed-size bytes (bytes1 to bytes32)
        if re.match(r"^bytes([1-9]|[12]\d|3[0-2])$", base_type):
            return v

        # Integer types (uint8 to uint256, int8 to int256)
        uint_match = re.match(r"^uint(\d+)$", base_type)
        int_match = re.match(r"^int(\d+)$", base_type)

        if uint_match:
            bits = int(uint_match.group(1))
            if bits % 8 != 0 or bits < 8 or bits > 256:
                raise ValueError(f"Invalid bit size {bits} for {base_type}")
            return v
        elif int_match:
            bits = int(int_match.group(1))
            if bits % 8 != 0 or bits < 8 or bits > 256:
                raise ValueError(f"Invalid bit size {bits} for {base_type}")
            return v

        # Generic uint/int (equivalent to uint256/int256)
        if base_type in ["uint", "int"]:
            return v

        # Fixed point numbers (not commonly used)
        if re.match(r"^u?fixed\d+x\d+$", base_type):
            return v

        # Tuple types
        if base_type == "tuple":
            return v

        # Function types
        if base_type.startswith("function"):
            return v

        raise ValueError(f"Invalid Solidity type: {base_type}")

    def to_eth_typing_component(self) -> EthABIComponent:
        """Convert to eth_typing.ABIComponent format"""
        result: EthABIComponent = {"type": self.type}
        if self.name is not None:
            result["name"] = self.name
        if self.components is not None:
            result["components"] = [comp.to_eth_typing_component() for comp in self.components]
        return result

    def to_eth_typing_component_indexed(self) -> EthABIComponentIndexed:
        """Convert to eth_typing.ABIComponentIndexed format (for events)"""
        result: EthABIComponentIndexed = {
            "type": self.type,
            "indexed": self.indexed or False,
        }
        if self.name is not None:
            result["name"] = self.name
        if self.components is not None:
            result["components"] = [comp.to_eth_typing_component() for comp in self.components]
        return result

    @classmethod
    def from_eth_typing_component(cls, component: EthABIComponent) -> "ABIInput":
        """Create from eth_typing.ABIComponent"""
        return cls(
            name=component.get("name"),
            type=component["type"],
            components=[
                cls.from_eth_typing_component(comp) for comp in component.get("components", [])
            ]
            if component.get("components")
            else None,
        )

    @classmethod
    def from_eth_typing_component_indexed(cls, component: EthABIComponentIndexed) -> "ABIInput":
        """Create from eth_typing.ABIComponentIndexed"""
        return cls(
            name=component.get("name"),
            type=component["type"],
            indexed=component.get("indexed", False),
            components=[
                cls.from_eth_typing_component(comp) for comp in component.get("components", [])
            ]
            if component.get("components")
            else None,
        )


class ABIEvent(BaseModel):
    """Schema for contract events, compatible with eth_typing.ABIEvent"""

    type: Literal["event"]
    name: str
    inputs: list[ABIInput] = Field(default_factory=list)
    anonymous: bool = False

    def to_eth_typing(self) -> EthABIEvent:
        """Convert to eth_typing.ABIEvent format"""
        result: EthABIEvent = {
            "type": "event",
            "name": self.name,
            "anonymous": self.anonymous,  # Always include anonymous field
        }
        if self.inputs:
            result["inputs"] = [inp.to_eth_typing_component_indexed() for inp in self.inputs]
        return result

    @classmethod
    def from_eth_typing(cls, event: EthABIEvent) -> "ABIEvent":
        """Create from eth_typing.ABIEvent"""
        return cls(
            type="event",
            name=event["name"],
            inputs=[
                ABIInput.from_eth_typing_component_indexed(inp) for inp in event.get("inputs", [])
            ],
            anonymous=event.get("anonymous", False),
        )


class ABIFunction(BaseModel):
    """Schema for contract functions, compatible with eth_typing.ABIFunction"""

    type: Literal["function"]
    name: str
    inputs: list[ABIInput] = Field(default_factory=list)
    outputs: list[ABIInput] = Field(default_factory=list)
    stateMutability: Literal["pure", "view", "nonpayable", "payable"]
    constant: bool | None = None  # Deprecated, but still seen
    payable: bool | None = None  # Deprecated, but still seen

    def to_eth_typing(self) -> EthABIFunction:
        """Convert to eth_typing.ABIFunction format"""
        result: EthABIFunction = {
            "type": "function",
            "name": self.name,
            "stateMutability": self.stateMutability,
            "payable": self.payable or False,
            "constant": self.constant or False,
        }
        if self.inputs:
            result["inputs"] = [inp.to_eth_typing_component() for inp in self.inputs]
        if self.outputs:
            result["outputs"] = [out.to_eth_typing_component() for out in self.outputs]
        return result

    @classmethod
    def from_eth_typing(cls, function: EthABIFunction) -> "ABIFunction":
        """Create from eth_typing.ABIFunction"""
        return cls(
            type="function",
            name=function["name"],
            inputs=[ABIInput.from_eth_typing_component(inp) for inp in function.get("inputs", [])],
            outputs=[
                ABIInput.from_eth_typing_component(out) for out in function.get("outputs", [])
            ],
            stateMutability=function.get("stateMutability", "nonpayable"),
            constant=function.get("constant"),
            payable=function.get("payable"),
        )


class ABIConstructor(BaseModel):
    """Schema for contract constructor, compatible with eth_typing.ABIConstructor"""

    type: Literal["constructor"]
    inputs: list[ABIInput] = Field(default_factory=list)
    stateMutability: Literal["nonpayable", "payable"] | None = "nonpayable"
    payable: bool | None = None  # Deprecated

    def to_eth_typing(self) -> EthABIConstructor:
        """Convert to eth_typing.ABIConstructor format"""
        result: EthABIConstructor = {
            "type": "constructor",
            "payable": self.payable or False,
        }
        if self.inputs:
            result["inputs"] = [inp.to_eth_typing_component() for inp in self.inputs]
        return result

    @classmethod
    def from_eth_typing(cls, constructor: EthABIConstructor) -> "ABIConstructor":
        """Create from eth_typing.ABIConstructor"""
        return cls(
            type="constructor",
            inputs=[
                ABIInput.from_eth_typing_component(inp) for inp in constructor.get("inputs", [])
            ],
            payable=constructor.get("payable"),
        )


class ABIFallback(BaseModel):
    """Schema for fallback function, compatible with eth_typing.ABIFallback"""

    type: Literal["fallback"]
    stateMutability: Literal["nonpayable", "payable"]
    payable: bool | None = None  # Deprecated

    def to_eth_typing(self) -> EthABIFallback:
        """Convert to eth_typing.ABIFallback format"""
        return {
            "type": "fallback",
            "payable": self.payable or False,
        }

    @classmethod
    def from_eth_typing(cls, fallback: EthABIFallback) -> "ABIFallback":
        """Create from eth_typing.ABIFallback"""
        return cls(
            type="fallback",
            stateMutability="payable" if fallback.get("payable") else "nonpayable",
            payable=fallback.get("payable"),
        )


class ABIReceive(BaseModel):
    """Schema for receive function, compatible with eth_typing.ABIReceive"""

    type: Literal["receive"]
    stateMutability: Literal["payable"]

    def to_eth_typing(self) -> EthABIReceive:
        """Convert to eth_typing.ABIReceive format"""
        return {
            "type": "receive",
            "payable": True,
        }

    @classmethod
    def from_eth_typing(cls, receive: EthABIReceive) -> "ABIReceive":
        """Create from eth_typing.ABIReceive"""
        return cls(
            type="receive",
            stateMutability="payable",
        )


class ABIError(BaseModel):
    """Schema for custom errors (Solidity 0.8.4+), compatible with eth_typing.ABIError"""

    type: Literal["error"]
    name: str
    inputs: list[ABIInput] = Field(default_factory=list)

    def to_eth_typing(self) -> EthABIError:
        """Convert to eth_typing.ABIError format"""
        result: EthABIError = {
            "type": "error",
            "name": self.name,
        }
        if self.inputs:
            result["inputs"] = [inp.to_eth_typing_component() for inp in self.inputs]
        return result

    @classmethod
    def from_eth_typing(cls, error: EthABIError) -> "ABIError":
        """Create from eth_typing.ABIError"""
        return cls(
            type="error",
            name=error["name"],
            inputs=[ABIInput.from_eth_typing_component(inp) for inp in error.get("inputs", [])],
        )


# Union type for any ABI element
ABIElement = ABIEvent | ABIFunction | ABIConstructor | ABIFallback | ABIReceive | ABIError


class ContractABI(BaseModel):
    """Complete contract ABI, compatible with eth_typing.ABI"""

    abi: list[ABIElement]

    def to_eth_typing(self) -> ABI:
        """Convert to eth_typing.ABI format"""
        return [element.to_eth_typing() for element in self.abi]

    @classmethod
    def from_eth_typing(cls, abi: ABI) -> "ContractABI":
        """Create from eth_typing.ABI"""
        elements = []
        for element in abi:
            element_type = element["type"]
            if element_type == "event":
                elements.append(ABIEvent.from_eth_typing(cast(EthABIEvent, element)))
            elif element_type == "function":
                elements.append(ABIFunction.from_eth_typing(cast(EthABIFunction, element)))
            elif element_type == "constructor":
                elements.append(ABIConstructor.from_eth_typing(cast(EthABIConstructor, element)))
            elif element_type == "fallback":
                elements.append(ABIFallback.from_eth_typing(cast(EthABIFallback, element)))
            elif element_type == "receive":
                elements.append(ABIReceive.from_eth_typing(cast(EthABIReceive, element)))
            elif element_type == "error":
                elements.append(ABIError.from_eth_typing(cast(EthABIError, element)))
            else:
                raise ValueError(f"Unknown ABI element type: {element_type}")

        return cls(abi=elements)


# Enable forward references for recursive models
ABIInput.model_rebuild()
