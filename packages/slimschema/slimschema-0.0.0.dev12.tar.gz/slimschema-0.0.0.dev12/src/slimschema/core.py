"""Core IR (Intermediate Representation) for SlimSchema.

Uses simple dataclasses to represent schemas in a format-agnostic way.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Field:
    """A single field in a schema.

    Args:
        name: Field name
        type: Type expression as string (e.g., "str", "int", "18..120", "list[str]")
        optional: Whether field is optional (ends with ?)
        hidden: Whether field is hidden from prompts (ends with !)
        description: Optional description from inline comments
        annotation: Optional round-trip type hint (e.g., "Set[int]")
        default: Optional default value expression (e.g., "0", "now", "list")

    Examples:
        >>> Field(name="age", type="18..120", optional=False)
        >>> Field(name="email", type="email", optional=True, description="Contact email")
        >>> Field(name="created", type="datetime", default="now")
        >>> Field(name="id", type="str", hidden=True, default="uuid")
    """

    name: str
    type: str
    optional: bool = False
    hidden: bool = False
    description: str | None = None
    annotation: str | None = None
    default: str | None = None


@dataclass(frozen=True)
class Schema:
    """SlimSchema definition.

    Args:
        fields: List of fields in the schema
        name: Optional schema name from top comment
        defs: Optional schema definitions

    Examples:
        >>> Schema(fields=[
        ...     Field(name="name", type="str"),
        ...     Field(name="age", type="int"),
        ... ], name="Person")
    """

    fields: list[Field]
    name: str | None = None
    defs: dict[str, "Schema"] = field(default_factory=dict)

    def __str__(self) -> str:
        """Return YAML representation."""
        from .generator import to_yaml

        return to_yaml(self)

    def __repr__(self) -> str:
        """Return YAML representation."""
        return self.__str__()


@dataclass(frozen=True)
class ValidationResult:
    """Result of a validation operation.

    Args:
        valid: Whether the data passed validation
        data: The validated data (None if validation failed)
        errors: ValidationError object or None
        schema: The schema that was used for validation

    Examples:
        >>> result = ValidationResult(
        ...     valid=True,
        ...     data={"name": "Alice", "age": 30},
        ...     errors=None,
        ...     schema=schema
        ... )
        >>> if result.valid:
        ...     print(f"Data: {result.data}")
        >>>
        >>> # Also supports tuple unpacking for backward compatibility
        >>> data, error = result
    """

    valid: bool
    data: Any | None = None
    errors: Any = None  # ValidationError object or None
    schema: "Schema | None" = None

    def __iter__(self):
        """Support tuple unpacking: (data, error).

        Returns:
            data: Validated data (None if invalid)
            error: Error string (None if valid)
        """
        if self.valid:
            yield self.data
            yield None
        else:
            yield None
            yield str(self.errors) if self.errors else "Validation failed"


# Type aliases for common patterns
PrimitiveTypes = {"str", "int", "num", "bool", "obj"}
FormatTypes = {"email", "url", "date", "datetime", "uuid"}
