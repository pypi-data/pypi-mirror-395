"""Generator for SlimSchema YAML format.

Converts IR to SlimSchema YAML using functional approach.
"""

from .core import Schema
from .types import normalize_type


def to_yaml(schema: Schema, *, show_defaults: bool = True, show_hidden: bool = True) -> str:
    """Convert schema to compact YAML format.

    Generates human-readable SlimSchema YAML perfect for LLM prompts.
    Typically 5-10x smaller than JSON Schema.

    Args:
        schema: Schema object (use to_schema() to convert other formats first)
        show_defaults: Whether to include default values in output (default: True)
        show_hidden: Whether to include system-managed fields (_) in output (default: True)

    Returns:
        Compact YAML string

    Examples:
        >>> from slimschema import Schema, Field
        >>> schema = Schema(fields=[
        ...     Field(name="name", type="str", description="Full name"),
        ...     Field(name="age", type="18..120"),
        ...     Field(name="email", type="email", optional=True),
        ... ], name="Person")
        >>> print(to_yaml(schema))
        # Person
        name: str  # Full name
        age: 18..120
        ?email: email

        >>> # Use with any schema format
        >>> from slimschema import to_schema
        >>> yaml_output = to_yaml(to_schema("name: str\\nage: int"))

        >>> # With defaults
        >>> schema_with_defaults = Schema(fields=[
        ...     Field(name="age", type="int", default="0"),
        ... ])
        >>> print(to_yaml(schema_with_defaults))
        age: int = 0
        >>> print(to_yaml(schema_with_defaults, show_defaults=False))
        age: int

        >>> # System-managed fields
        >>> schema_with_hidden = Schema(fields=[
        ...     Field(name="id", type="str", hidden=True, default="uuid"),
        ...     Field(name="name", type="str"),
        ... ])
        >>> print(to_yaml(schema_with_hidden, show_hidden=False))
        name: str
    """
    lines = []

    # Add schema name as top comment
    if schema.name:
        lines.append(f"# {schema.name}")

    # Generate fields
    for field in schema.fields:
        # Skip hidden fields if show_hidden is False
        if field.hidden and not show_hidden:
            continue

        # Apply prefix markers to field name (can have both: _?field)
        # Canonical order: underscore first, then question mark
        name = field.name
        if field.optional:
            name = "?" + name
        if field.hidden:
            name = "_" + name

        # Build type expression with optional default
        # Normalize type aliases to canonical forms
        type_expr = normalize_type(field.type)
        if show_defaults and field.default is not None:
            type_expr = f"{type_expr} = {field.default}"

        comment_parts = []

        if field.description:
            comment_parts.append(field.description)
        if field.annotation:
            comment_parts.append(f":: {field.annotation}")

        if comment_parts:
            comment = "  ".join(comment_parts)
            lines.append(f"{name}: {type_expr}  # {comment}")
        else:
            lines.append(f"{name}: {type_expr}")

    return "\n".join(lines)
