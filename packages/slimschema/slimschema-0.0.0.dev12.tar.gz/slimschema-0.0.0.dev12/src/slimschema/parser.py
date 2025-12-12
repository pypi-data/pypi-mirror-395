"""Parser for SlimSchema YAML format.

Converts SlimSchema YAML to IR using functional approach.
"""

import re
from io import StringIO
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError
from ruamel.yaml.error import YAMLError
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError

from .core import Field, Schema


class SchemaParseError(ValueError):
    """Raised when schema YAML cannot be parsed.

    This is a user-friendly wrapper around YAML parser exceptions.
    """
    pass


def _detect_common_issues(yaml_str: str) -> str | None:
    """Pre-flight check for common schema syntax issues.

    Returns helpful error message if issue detected, None otherwise.
    """
    # Check for tabs (YAML doesn't allow them)
    for i, line in enumerate(yaml_str.split('\n'), 1):
        if '\t' in line:
            return f"Line {i}: YAML doesn't support tabs - use spaces for indentation"

    # Check for old [type] syntax without quotes (common migration issue)
    # Pattern: field: [type] (not quoted, not part of a default value)
    for i, line in enumerate(yaml_str.split('\n'), 1):
        # Skip lines with quotes or that are part of default values
        if '"' in line or "'" in line:
            continue
        if '=' in line:  # Has default, might be intentional
            continue

        # Look for pattern like "field: [type]" or "field: [/pattern/]"
        if re.search(r':\s*\[[\w/^$\[\]{}().*+?\\-]+\]', line):
            field_name = line.split(':')[0].strip()
            return (f"Line {i}: Array syntax should be 'list[type]', not '[type]'. "
                   f"Try: {field_name}: list[...] or use quotes: \"{field_name}: '[...]'\"")

    return None


def parse_slimschema(yaml_str: str) -> Schema:
    """Parse SlimSchema YAML to IR.

    Args:
        yaml_str: YAML string in SlimSchema format

    Returns:
        Schema IR

    Raises:
        SchemaParseError: If the schema YAML is invalid

    Examples:
        >>> schema = parse_slimschema('''
        ... # Person
        ... name: str
        ... age: 18..120
        ... email?: email  # Contact email
        ... ''')
        >>> schema.name
        'Person'
        >>> len(schema.fields)
        3
    """
    # Pre-flight check for common issues
    issue = _detect_common_issues(yaml_str)
    if issue:
        raise SchemaParseError(issue)

    try:
        # Extract schema name from top comment
        name = _extract_name(yaml_str)

        # Extract field comments
        comments = _extract_comments(yaml_str)

        # Parse YAML structure
        yaml = YAML()
        yaml.preserve_quotes = True

        data = yaml.load(StringIO(yaml_str))

        if data is None:
            return Schema(fields=[], name=name)

        # Parse object fields
        fields = []
        for field_name, field_value in data.items():
            # Strip both prefix markers to lookup comment by clean name
            clean_field_name = field_name
            if clean_field_name.startswith("_?") or clean_field_name.startswith("?_"):
                clean_field_name = clean_field_name[2:]
            elif clean_field_name.startswith("_") or clean_field_name.startswith("?"):
                clean_field_name = clean_field_name[1:]
            field = _parse_field(
                field_name, field_value, comments.get(clean_field_name)
            )
            fields.append(field)

        return Schema(fields=fields, name=name)

    except DuplicateKeyError as e:
        # Extract field name from error message if possible
        error_msg = str(e)
        if 'duplicate key' in error_msg.lower():
            raise SchemaParseError("Duplicate field name in schema - each field must have a unique name") from e
        raise SchemaParseError(f"Invalid schema: {e}") from e

    except ScannerError as e:
        error_msg = str(e).lower()
        if 'found character' in error_msg and 'that cannot start any token' in error_msg:
            raise SchemaParseError("Invalid YAML syntax - check for special characters or formatting issues") from e
        raise SchemaParseError(f"YAML syntax error: {e}") from e

    except ParserError as e:
        error_msg = str(e).lower()

        # Detect unclosed braces/brackets
        if 'flow mapping' in error_msg or 'flow sequence' in error_msg:
            if "expected ',' or '}'" in error_msg:
                raise SchemaParseError("Unclosed braces in inline object - check your {...} syntax") from e
            if "expected ',' or ']'" in error_msg:
                raise SchemaParseError("Invalid array syntax - use list[type] instead of [type]") from e

        raise SchemaParseError(f"YAML parsing failed: {e}") from e

    except AttributeError as e:
        # This usually happens when YAML structure is invalid (e.g., missing colons)
        if "'str' object has no attribute 'items'" in str(e):
            raise SchemaParseError("Invalid YAML format - check that all fields use 'name: type' format with colons") from e
        raise SchemaParseError(f"Schema structure error: {e}") from e

    except YAMLError as e:
        # Catch-all for other YAML errors
        raise SchemaParseError(f"Invalid YAML: {e}") from e


def _parse_field(name: str, value: Any, comment: str | None) -> Field:
    """Parse a single field.

    Args:
        name: Field name (may start with _ for system-managed and/or ? for optional)
              Supports dual markers: _?field or ?_field for optional system-managed fields
        value: Field value from YAML
        comment: Optional inline comment

    Returns:
        Field IR
    """
    # Check both markers independently (supports both orders: _?field or ?_field)
    clean_name = name

    # Check for both markers (strip in any order)
    hidden = "_" in name[:2] if len(name) >= 1 and name[0] in "_?" else False
    optional = "?" in name[:2] if len(name) >= 1 and name[0] in "_?" else False

    # Strip both markers if present
    if name.startswith("_?") or name.startswith("?_"):
        clean_name = name[2:]
    elif name.startswith("_"):
        clean_name = name[1:]
    elif name.startswith("?"):
        clean_name = name[1:]

    # Validation: ensure we didn't strip the entire name
    if not clean_name:
        raise SchemaParseError(f"Invalid field name: '{name}' (only contains markers)")

    type_expr, default_expr = _parse_type(value)
    description, annotation = _split_comment(comment)

    return Field(
        name=clean_name,
        type=type_expr,
        optional=optional,
        hidden=hidden,
        description=description,
        annotation=annotation,
        default=default_expr,
    )


def _split_comment(comment: str | None) -> tuple[str | None, str | None]:
    """Split comment into description and optional type annotation."""
    if not comment:
        return None, None

    if "::" not in comment:
        return comment.strip() or None, None

    text, _, annotation = comment.partition("::")
    description = text.strip() or None
    clean_annotation = annotation.strip() or None
    return description, clean_annotation


def _parse_type(value: Any) -> tuple[str, str | None]:
    """Parse type expression and optional default from YAML value.

    Args:
        value: YAML value (string, list, dict, etc.)

    Returns:
        (type_expr, default_expr) tuple where default_expr is None if no default
    """
    if isinstance(value, str):
        value_str = value.strip()
        # Check for default value: "type = default"
        if " = " in value_str:
            type_part, default_part = value_str.split(" = ", 1)
            return type_part.strip(), default_part.strip()
        return value_str, None

    if isinstance(value, list):
        if len(value) == 0:
            return "list", None
        item_type, _ = _parse_type(value[0])  # Ignore nested defaults
        return f"list[{item_type}]", None

    if isinstance(value, dict):
        # Check for set syntax: {type} parsed as dict with single key and None value
        if len(value) == 1:
            key, val = next(iter(value.items()))
            if val is None:
                return f"{{{key}}}", None
        # Nested object type
        return _parse_object_type(value), None

    return "obj", None


def _parse_object_type(value: dict) -> str:
    """Parse nested object type to inline syntax.

    Args:
        value: Dictionary representing object fields

    Returns:
        Inline object type like '{name:type,age:type=default}'.

    Notes:
        We serialize nested defaults directly into the inline type string
        so that they can be interpreted later when applying defaults.
    """
    parts = []
    for field_name, field_value in value.items():
        # Preserve nested defaults instead of discarding them.
        field_type, default_expr = _parse_type(field_value)

        # Check for optional marker (supports both orders: _?field or ?_field)
        # Note: Hidden fields (_) in inline objects are rare and not represented in suffix style
        optional = "?" in field_name[:2] if len(field_name) >= 1 and field_name[0] in "_?" else False

        # Strip both markers if present
        if field_name.startswith("_?") or field_name.startswith("?_"):
            clean_name = field_name[2:]
        elif field_name.startswith("_"):
            clean_name = field_name[1:]
        elif field_name.startswith("?"):
            clean_name = field_name[1:]
        else:
            clean_name = field_name

        # Build inline field representation (uses suffix style for inline objects)
        # Note: inline objects use suffix ? marker for consistency with parse_inline_object_def
        suffix_marker = "?" if optional else ""

        if default_expr:
            # Use ' = ' so inline parsers can safely split type and default
            parts.append(f"{clean_name}{suffix_marker}:{field_type} = {default_expr}")
        else:
            parts.append(f"{clean_name}{suffix_marker}:{field_type}")

    return "{" + ",".join(parts) + "}"


def _extract_name(yaml_str: str) -> str | None:
    """Extract schema name from first line comment."""
    for line in yaml_str.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#"):
            name = stripped[1:].strip()
            if name:
                return name.split()[0]  # First word only
            return None
        if stripped:
            break
    return None


def _extract_comments(yaml_str: str) -> dict[str, str]:
    """Extract inline comments for fields.

    Args:
        yaml_str: YAML string

    Returns:
        Dictionary mapping field names to comments

    Examples:
        >>> _extract_comments("name: str  # Full name\\nage: int")
        {'name': 'Full name'}
    """
    comments = {}

    for line in yaml_str.split("\n"):
        if "#" not in line:
            continue

        parts = line.split("#", 1)
        if len(parts) != 2:
            continue

        key_part = parts[0].strip()
        comment = parts[1].strip()

        if ":" not in key_part:
            continue

        # Strip both markers in either order (_?field or ?_field)
        field = key_part.split(":")[0].strip()
        if field.startswith("_?") or field.startswith("?_"):
            field = field[2:]
        elif field.startswith("_") or field.startswith("?"):
            field = field[1:]

        if field and comment:
            comments[field] = comment

    return comments
