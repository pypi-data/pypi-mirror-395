"""Parameter validation logic."""

import re
from typing import Any, Optional

from .models import ParameterSchema, SchemaType


class ValidationError(Exception):
    """Raised when parameter validation fails."""

    pass


class ParameterValidator:
    """Validates tool parameters against schemas."""

    def validate(self, value: Any, schema: ParameterSchema) -> Any:
        """Validate and coerce parameter value.

        Args:
            value: Parameter value to validate
            schema: Validation schema

        Returns:
            Validated and coerced value

        Raises:
            ValidationError: If validation fails
        """
        # Handle None/missing values
        if value is None:
            if schema.required:
                raise ValidationError(f"Parameter '{schema.name}' is required")
            return schema.default

        # Type-specific validation
        if schema.type == SchemaType.STRING:
            return self._validate_string(value, schema)
        elif schema.type == SchemaType.NUMBER:
            return self._validate_number(value, schema)
        elif schema.type == SchemaType.INTEGER:
            return self._validate_integer(value, schema)
        elif schema.type == SchemaType.BOOLEAN:
            return self._validate_boolean(value, schema)
        elif schema.type == SchemaType.ARRAY:
            return self._validate_array(value, schema)
        elif schema.type == SchemaType.OBJECT:
            return self._validate_object(value, schema)
        else:
            return value

    def _validate_string(self, value: Any, schema: ParameterSchema) -> str:
        """Validate string parameter."""
        # Coerce to string
        if not isinstance(value, str):
            value = str(value)

        # Enum check
        if schema.enum and value not in schema.enum:
            raise ValidationError(
                f"Parameter '{schema.name}' must be one of {schema.enum}, got '{value}'"
            )

        # Length checks
        if schema.min_length is not None and len(value) < schema.min_length:
            raise ValidationError(
                f"Parameter '{schema.name}' must be at least {schema.min_length} characters, got {len(value)}"
            )
        if schema.max_length is not None and len(value) > schema.max_length:
            raise ValidationError(
                f"Parameter '{schema.name}' must be at most {schema.max_length} characters, got {len(value)}"
            )

        # Pattern check
        if schema.pattern and not re.match(schema.pattern, value):
            raise ValidationError(
                f"Parameter '{schema.name}' does not match pattern '{schema.pattern}'"
            )

        return value

    def _validate_number(self, value: Any, schema: ParameterSchema) -> float:
        """Validate number parameter."""
        # Coerce to float
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Parameter '{schema.name}' must be a number, got {type(value).__name__}"
            )

        # Range checks
        if schema.minimum is not None and value < schema.minimum:
            raise ValidationError(
                f"Parameter '{schema.name}' must be >= {schema.minimum}, got {value}"
            )
        if schema.maximum is not None and value > schema.maximum:
            raise ValidationError(
                f"Parameter '{schema.name}' must be <= {schema.maximum}, got {value}"
            )

        return value

    def _validate_integer(self, value: Any, schema: ParameterSchema) -> int:
        """Validate integer parameter."""
        # Coerce to int
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Parameter '{schema.name}' must be an integer, got {type(value).__name__}"
            )

        # Range checks
        if schema.minimum is not None and value < schema.minimum:
            raise ValidationError(
                f"Parameter '{schema.name}' must be >= {schema.minimum}, got {value}"
            )
        if schema.maximum is not None and value > schema.maximum:
            raise ValidationError(
                f"Parameter '{schema.name}' must be <= {schema.maximum}, got {value}"
            )

        return value

    def _validate_boolean(self, value: Any, schema: ParameterSchema) -> bool:
        """Validate boolean parameter."""
        # Coerce common boolean representations
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lower = value.lower()
            if lower in ("true", "yes", "1", "on"):
                return True
            if lower in ("false", "no", "0", "off"):
                return False

        raise ValidationError(
            f"Parameter '{schema.name}' must be a boolean, got '{value}'"
        )

    def _validate_array(self, value: Any, schema: ParameterSchema) -> list:
        """Validate array parameter."""
        if not isinstance(value, list):
            raise ValidationError(
                f"Parameter '{schema.name}' must be an array, got {type(value).__name__}"
            )

        # Validate items if schema provided
        if schema.items:
            validated = []
            for i, item in enumerate(value):
                item_schema = ParameterSchema(
                    name=f"{schema.name}[{i}]",
                    type=schema.items.type,
                    pattern=schema.items.pattern,
                    min_length=schema.items.min_length,
                    max_length=schema.items.max_length,
                    minimum=schema.items.minimum,
                    maximum=schema.items.maximum,
                    enum=schema.items.enum,
                )
                validated.append(self.validate(item, item_schema))
            return validated

        return value

    def _validate_object(self, value: Any, schema: ParameterSchema) -> dict:
        """Validate object parameter."""
        if not isinstance(value, dict):
            raise ValidationError(
                f"Parameter '{schema.name}' must be an object, got {type(value).__name__}"
            )

        # Validate properties if schema provided
        if schema.properties:
            validated = {}
            for key, prop_schema in schema.properties.items():
                validated[key] = self.validate(value.get(key), prop_schema)
            return validated

        return value

    def validate_parameters(
        self, params: dict[str, Any], schemas: dict[str, ParameterSchema]
    ) -> dict[str, Any]:
        """Validate multiple parameters.

        Args:
            params: Parameter values
            schemas: Parameter schemas

        Returns:
            Validated parameters

        Raises:
            ValidationError: If any validation fails
        """
        validated = {}
        for name, schema in schemas.items():
            value = params.get(name)
            validated[name] = self.validate(value, schema)
        return validated
