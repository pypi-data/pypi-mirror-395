"""Parameter schema models for validation."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class SchemaType(str, Enum):
    """JSON Schema types."""

    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


@dataclass
class ParameterSchema:
    """Parameter validation schema.

    Supports JSON Schema validation with common constraints.

    Attributes:
        name: Parameter name
        type: Parameter type (string, number, boolean, etc.)
        required: Whether parameter is required
        description: Human-readable description
        pattern: Regex pattern for string validation
        min_length: Minimum string length
        max_length: Maximum string length
        minimum: Minimum numeric value
        maximum: Maximum numeric value
        enum: Allowed values (whitelist)
        items: Schema for array items
        properties: Schema for object properties
        default: Default value if not provided
    """

    name: str
    type: SchemaType
    required: bool = False
    description: str = ""

    # String constraints
    pattern: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None

    # Numeric constraints
    minimum: Optional[float] = None
    maximum: Optional[float] = None

    # Enum constraint
    enum: Optional[list[Any]] = None

    # Array/Object constraints
    items: Optional["ParameterSchema"] = None
    properties: Optional[dict[str, "ParameterSchema"]] = None

    # Default value
    default: Any = None

    def __post_init__(self) -> None:
        """Validate schema."""
        if not self.name:
            raise ValueError("Parameter name cannot be empty")

        # Convert string type to enum
        if isinstance(self.type, str):
            self.type = SchemaType(self.type.lower())

        # Validate constraints
        if self.min_length is not None and self.min_length < 0:
            raise ValueError("min_length must be non-negative")
        if self.max_length is not None and self.max_length < 0:
            raise ValueError("max_length must be non-negative")
        if self.min_length is not None and self.max_length is not None:
            if self.min_length > self.max_length:
                raise ValueError("min_length cannot exceed max_length")

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON Schema format."""
        schema = {
            "type": self.type.value,
        }

        if self.description:
            schema["description"] = self.description
        if self.pattern:
            schema["pattern"] = self.pattern
        if self.min_length is not None:
            schema["minLength"] = self.min_length
        if self.max_length is not None:
            schema["maxLength"] = self.max_length
        if self.minimum is not None:
            schema["minimum"] = self.minimum
        if self.maximum is not None:
            schema["maximum"] = self.maximum
        if self.enum:
            schema["enum"] = self.enum
        if self.items:
            schema["items"] = self.items.to_dict()
        if self.properties:
            schema["properties"] = {k: v.to_dict() for k, v in self.properties.items()}
        if self.default is not None:
            schema["default"] = self.default

        return schema

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> "ParameterSchema":
        """Create from JSON Schema format."""
        return cls(
            name=name,
            type=SchemaType(data["type"]),
            required=data.get("required", False),
            description=data.get("description", ""),
            pattern=data.get("pattern"),
            min_length=data.get("minLength"),
            max_length=data.get("maxLength"),
            minimum=data.get("minimum"),
            maximum=data.get("maximum"),
            enum=data.get("enum"),
            items=cls.from_dict("item", data["items"]) if "items" in data else None,
            properties={
                k: cls.from_dict(k, v) for k, v in data.get("properties", {}).items()
            },
            default=data.get("default"),
        )
