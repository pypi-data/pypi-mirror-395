"""Schema inference from data - infer SlimSchema from JSON examples."""

import re
from dataclasses import dataclass
from typing import Any

from .core import Field, Schema

# Compile regex patterns once for performance
_EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
_URL_RE = re.compile(r"^https?://")
_UUID_RE = re.compile(r"^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$", re.I)
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


@dataclass
class InferenceConfig:
    """Configuration for from_data() schema inference.

    Args:
        detect_enums: Enable enum detection for string fields
        detect_ranges: Enable range detection for numeric fields
        detect_formats: Enable format detection (email, url, uuid, date, datetime)
        max_samples: Maximum number of records to process (None = all)
        max_nesting_depth: Maximum depth for recursive object inference
        enum_max_cardinality: Maximum unique values for enum detection
        int_range_max_delta: Maximum range size for int range detection
        float_range_max_delta: Maximum range size for float range detection

    Examples:
        >>> # Disable enum detection
        >>> config = InferenceConfig(detect_enums=False)
        >>> schema = from_data(data, config=config)

        >>> # Process only first 100 records
        >>> config = InferenceConfig(max_samples=100)
        >>> schema = from_data(data, config=config)

        >>> # Allow more unique values for enums
        >>> config = InferenceConfig(enum_max_cardinality=10)
        >>> schema = from_data(data, config=config)
    """

    # Master switches
    detect_enums: bool = True
    detect_ranges: bool = True
    detect_formats: bool = True

    # Safety guardrails
    max_samples: int | None = None  # None = process all
    max_nesting_depth: int = 10

    # Enum detection
    enum_max_cardinality: int = 5

    # Range detection
    int_range_max_delta: int = 200
    float_range_max_delta: float = 10_000.0


def from_data(
    data: list[dict] | dict,
    name: str | None = None,
    config: InferenceConfig | None = None,
) -> Schema:
    """Infer a schema from example JSON data.

    Automatically detects types, ranges, enums, and formats by analyzing your data.
    Great for bootstrapping schemas or understanding existing datasets.

    Args:
        data: Your example data (single dict or list of dicts)
        name: Optional name for the generated schema
        config: Optional InferenceConfig to control detection behavior

    Returns:
        Schema object with inferred types and constraints

    Examples:
        >>> # Basic usage - infer from examples
        >>> examples = [
        ...     {"name": "Alice", "age": 30, "status": "active"},
        ...     {"name": "Bob", "age": 25, "status": "draft"},
        ... ]
        >>> schema = from_data(examples, name="User")
        >>> print(schema)
        # User
        name: str
        age: 25..30
        status: active | draft

        >>> # Detects formats automatically
        >>> data = {"email": "alice@example.com", "created": "2024-01-15"}
        >>> schema = from_data(data)
        >>> [f.type for f in schema.fields]
        ['email', 'date']

        >>> # Customize inference behavior
        >>> config = InferenceConfig(detect_enums=False, max_samples=100)
        >>> schema = from_data(large_dataset, config=config)
    """
    if config is None:
        config = InferenceConfig()

    # Normalize to list
    if isinstance(data, dict):
        data = [data]

    if not data:
        return Schema(fields=[], name=name)

    # Apply max_samples limit
    if config.max_samples is not None and len(data) > config.max_samples:
        data = data[: config.max_samples]

    # Gather all field values
    field_values: dict[str, list[Any]] = {}
    for item in data:
        for key, value in item.items():
            if key not in field_values:
                field_values[key] = []
            field_values[key].append(value)

    # Infer field types
    fields = []
    for field_name, values in field_values.items():
        # Check if field is optional (missing in some examples)
        num_examples = len(data)
        num_values = len([v for v in values if v is not None])
        optional = num_values < num_examples

        # Infer type from non-null values
        non_null = [v for v in values if v is not None]
        if not non_null:
            # All values are null - default to str as most permissive type
            field_type = "str"
        else:
            field_type = _infer_type(non_null, config, depth=0)

        fields.append(
            Field(
                name=field_name,
                type=field_type,
                optional=optional,
            )
        )

    return Schema(fields=fields, name=name)


def _schema_to_inline_object(schema: Schema) -> str:
    """Convert a Schema to inline object syntax: {name:str,age:int}."""
    parts = []
    for field in schema.fields:
        optional_marker = "?" if field.optional else ""
        parts.append(f"{field.name}{optional_marker}:{field.type}")

    return "{" + ",".join(parts) + "}"


def _infer_type(values: list[Any], config: InferenceConfig, depth: int) -> str:
    """Infer SlimSchema type from a list of values.

    Args:
        values: List of non-null values (all of same field)
        config: Inference configuration
        depth: Current nesting depth (for recursion guard)

    Returns:
        SlimSchema type string
    """
    # Get Python types
    types = {type(v) for v in values}

    if len(types) > 1:
        # Mixed types - default to "obj"
        return "obj"

    value_type = types.pop()

    # Boolean
    if value_type is bool:
        return "bool"

    # Integer - detect ranges (with bounds checking)
    if value_type is int:
        if not config.detect_ranges:
            return "int"

        min_val = min(values)
        max_val = max(values)
        range_size = max_val - min_val

        # Only use range syntax for reasonable ranges
        if range_size <= config.int_range_max_delta and max_val < 1_000_000:
            return f"{min_val}..{max_val}"

        return "int"

    # Float - detect ranges (with bounds checking)
    if value_type is float:
        if not config.detect_ranges:
            return "float"

        min_val = min(values)
        max_val = max(values)
        range_size = max_val - min_val

        # Only use range syntax for reasonable ranges
        if range_size <= config.float_range_max_delta and max_val < 1_000_000:
            return f"{min_val}..{max_val}"

        return "float"

    # String - check format patterns first (single pass for performance)
    if value_type is str:
        # Format detection
        if config.detect_formats:
            # Single pass over values checking all formats at once
            is_email = is_url = is_uuid = is_date = is_datetime = True

            for v in values:
                if is_email and not _EMAIL_RE.match(v):
                    is_email = False
                if is_url and not _URL_RE.match(v):
                    is_url = False
                if is_uuid and not _UUID_RE.match(v):
                    is_uuid = False
                if is_date and not _DATE_RE.match(v):
                    is_date = False
                if is_datetime and not _DATETIME_RE.match(v):
                    is_datetime = False

                # Early exit if all formats ruled out
                if not (is_email or is_url or is_uuid or is_date or is_datetime):
                    break

            # Return the first matching format (priority order)
            if is_email:
                return "email"
            if is_url:
                return "url"
            if is_uuid:
                return "uuid"
            if is_date:
                return "date"
            if is_datetime:
                return "datetime"

        # Enum detection (after format patterns)
        if config.detect_enums:
            unique_vals = set(values)

            # Need at least 2 values to detect enum pattern
            if len(values) >= 2:
                # Conservative enum detection:
                # - Few unique values (≤ enum_max_cardinality)
                # - Values repeat OR very few unique & short
                max_length = max(len(v) for v in values)

                has_repetition = len(unique_vals) < len(values)
                very_few_unique_and_short = len(unique_vals) <= 3 and max_length <= 15

                if len(unique_vals) <= config.enum_max_cardinality and (
                    has_repetition or very_few_unique_and_short
                ):
                    return " | ".join(sorted(unique_vals))

        return "str"

    # Dict - recursively infer nested object structure
    if value_type is dict:
        # Check nesting depth guard
        if depth >= config.max_nesting_depth:
            return "obj"

        # Recursively infer schema for nested object
        nested_schema = from_data(values, config=config)

        # Pass depth + 1 to recursive calls
        # Note: from_data doesn't take depth, so we handle it here
        # by checking depth before recursing

        # Convert to inline object syntax: {name:str,age:int}
        if nested_schema.fields:
            return _schema_to_inline_object(nested_schema)

        # Fallback if no fields were inferred
        return "obj"

    # List
    if value_type is list:
        # Try to infer inner type
        all_inner = []
        for lst in values:
            all_inner.extend(lst)

        if all_inner:
            inner_type = _infer_type(all_inner, config, depth + 1)
            return f"[{inner_type}]"

        return "[]"

    return "obj"
