"""Type conversion - consolidated with single compiled regex.

Converts between:
- Pydantic annotations → SlimSchema type strings
- SlimSchema type strings → msgspec types (ONE regex match)
"""

import functools
import re
from typing import Annotated, Any, get_args, get_origin

import msgspec

# Single compiled regex with named groups (checked in priority order)
TYPE_PATTERN = re.compile(
    r"(?P<str_len>str\{(?P<str_min>\d+)\.\.(?P<str_max>\d+)\})"
    r"|(?P<num_range>(?P<num_min>-?\d+\.?\d*)\.\.(?P<num_max>-?\d+\.?\d*))"
    r"|(?P<regex>/(?P<pattern>[^/]+)/)"
    r"|(?P<enum>(?P<enum_values>.+\|.+))"
    r"|(?P<tuple>tuple\[(?P<tuple_inner>.+)\])"
    r"|(?P<frozenset>frozenset\[(?P<frozenset_inner>.+)\])"
    r"|(?P<set_bracket>set\[(?P<set_bracket_inner>.+)\])"
    r"|(?P<array>list\[(?P<array_inner>.+)\]|list)"
    r"|(?P<set>\{(?P<set_inner>[^:]+)\})"
    r"|(?P<format>email|url|date|datetime|uuid)"
    r"|(?P<primitive>str|int|float|bool|boolean|obj|any|dict|num|string|integer|number|object)"
)

FORMAT_PATTERNS = {
    "email": r"^[^@]+@[^@]+\.[^@]+$",
    "url": r"^https?://",
    "date": r"^\d{4}-\d{2}-\d{2}$",
    "datetime": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
    "uuid": r"^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$",
}

PRIMITIVE_TYPES = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "boolean": bool,  # Alias for bool (JSON Schema compatibility)
    "obj": dict,
    "any": Any,
    "dict": dict,  # Alias for obj
    "num": float,  # Alias for float (or int|float)
    # Common aliases (JSON Schema, TypeScript, etc.)
    "string": str,
    "integer": int,
    "number": float,
    "object": dict,
}

# Reserved types for auto-detection (Union vs Enum)
RESERVED_TYPES = {
    # Primitives
    "str", "int", "float", "bool", "boolean", "obj", "any", "dict", "num",
    "string", "integer", "number", "object",  # Common aliases
    # Formats
    "email", "url", "uuid", "date", "datetime",
}

# Canonical type mappings for normalization
TYPE_ALIASES = {
    # Canonical forms (map to themselves)
    "str": "str",
    "int": "int",
    "float": "float",
    "bool": "bool",
    "obj": "obj",
    "any": "any",
    # Common aliases → canonical
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "object": "obj",
    # Existing aliases → canonical
    "dict": "obj",
    "num": "float",
}


def normalize_type(type_expr: str) -> str:
    """Normalize type expressions to canonical forms.

    Converts type aliases to their canonical forms:
    - boolean → bool
    - string → str
    - integer → int
    - number → float
    - object → obj
    - dict → obj
    - num → float

    Also handles complex types recursively (list[string] → list[str]).

    Args:
        type_expr: Type expression to normalize

    Returns:
        Normalized type expression

    Examples:
        >>> normalize_type("boolean")
        'bool'
        >>> normalize_type("list[string]")
        'list[str]'
        >>> normalize_type("dict{integer, string}")
        'dict{int, str}'
    """
    type_expr = type_expr.strip()

    # Handle inline objects: {field:type, ...}
    if type_expr.startswith("{") and type_expr.endswith("}") and ":" in type_expr:
        inner = type_expr[1:-1]
        items = _split_annotation_items(inner)
        normalized_items = []
        for item in items:
            if ":" not in item:
                continue
            name_part, type_part = item.split(":", 1)
            # Recursively normalize the type part (handles defaults too)
            normalized_type = _normalize_type_with_default(type_part.strip())
            normalized_items.append(f"{name_part.strip()}:{normalized_type}")
        return "{" + ",".join(normalized_items) + "}"

    # Handle dict sugar: dict{KeyType, ValueType}
    if type_expr.startswith("dict{") and type_expr.endswith("}"):
        inner = type_expr[5:-1]
        parts = _split_annotation_items(inner)
        if len(parts) == 2:
            key_type = normalize_type(parts[0].strip())
            val_type = normalize_type(parts[1].strip())
            return f"dict{{{key_type}, {val_type}}}"

    # Handle list[type]
    if type_expr.startswith("list[") and type_expr.endswith("]"):
        inner = type_expr[5:-1]
        normalized_inner = normalize_type(inner)
        return f"list[{normalized_inner}]"

    # Handle set[type]
    if type_expr.startswith("set[") and type_expr.endswith("]"):
        inner = type_expr[4:-1]
        normalized_inner = normalize_type(inner)
        return f"set[{normalized_inner}]"

    # Handle frozenset[type]
    if type_expr.startswith("frozenset[") and type_expr.endswith("]"):
        inner = type_expr[10:-1]
        normalized_inner = normalize_type(inner)
        return f"frozenset[{normalized_inner}]"

    # Handle tuple[type1, type2, ...]
    if type_expr.startswith("tuple[") and type_expr.endswith("]"):
        inner = type_expr[6:-1]
        parts = _split_annotation_items(inner)
        normalized_parts = [normalize_type(p.strip()) for p in parts]
        return f"tuple[{', '.join(normalized_parts)}]"

    # Handle pipe-delimited (union/enum)
    if "|" in type_expr:
        parts = [p.strip() for p in type_expr.split("|")]
        # Only normalize if all parts are reserved types (Union)
        # Don't normalize enum literals
        all_reserved = all(is_reserved_type(part) for part in parts)
        if all_reserved:
            normalized_parts = [TYPE_ALIASES.get(p, p) for p in parts]
            return " | ".join(normalized_parts)
        return type_expr

    # Simple type alias
    return TYPE_ALIASES.get(type_expr, type_expr)


def _normalize_type_with_default(type_expr: str) -> str:
    """Normalize type expression that may include a default value."""
    # Split on " = " while respecting braces
    type_part, default_part = _split_on_equals_respecting_braces(type_expr)
    normalized_type = normalize_type(type_part)
    if default_part:
        return f"{normalized_type} = {default_part}"
    return normalized_type


def is_reserved_type(token: str) -> bool:
    """Check if token is a reserved type or constraint pattern.

    Reserved types include:
    - Primitives: str, int, float, bool, obj, any, dict, num
    - Formats: email, url, uuid, date, datetime
    - Constraints: ranges (1..10), string length (str{3..10}), regex (/.../), arrays ([...])

    This is used to distinguish Unions (str | int) from Enums (active | inactive).

    Args:
        token: The type token to check

    Returns:
        True if the token is a reserved type or constraint pattern

    Examples:
        >>> is_reserved_type("str")
        True
        >>> is_reserved_type("email")
        True
        >>> is_reserved_type("1..10")
        True
        >>> is_reserved_type("active")
        False
    """
    token = token.strip()

    # Remove quotes if present - quoted strings are always literals
    if (token.startswith('"') and token.endswith('"')) or \
       (token.startswith("'") and token.endswith("'")):
        return False

    # Check if it's in the reserved types set
    if token in RESERVED_TYPES:
        return True

    # Check if it matches any constraint pattern
    # Use the same regex pattern to check
    match = TYPE_PATTERN.fullmatch(token)
    if match:
        # If it matches any pattern group, it's a reserved type
        return True

    return False


def to_msgspec_type(type_expr: str, annotation: str | None = None):
    """Convert SlimSchema type string to msgspec type (single regex match)."""
    annotated_type = _annotation_to_msgspec(annotation)
    if annotated_type is not None:
        return annotated_type

    type_expr = type_expr.strip()

    # Inline object syntax: {name:str,age:int}
    # Treat as plain dict for now (shape not yet enforced).
    if type_expr.startswith("{") and type_expr.endswith("}"):
        inner = type_expr[1:-1]
        # Legacy set syntax uses {type} with no ":", keep that path intact.
        if ":" in inner:
            return dict

    # Dict sugar syntax: dict{K,V} → plain dict
    if type_expr.startswith("dict{") and type_expr.endswith("}"):
        return dict

    match = TYPE_PATTERN.fullmatch(type_expr)

    if not match:
        return str  # Default fallback

    # String length
    if match.group("str_len"):
        min_len = int(match.group("str_min"))
        max_len = int(match.group("str_max"))
        return Annotated[str, msgspec.Meta(min_length=min_len, max_length=max_len)]

    # Numeric range
    if match.group("num_range"):
        min_val = match.group("num_min")
        max_val = match.group("num_max")
        is_float = "." in min_val or "." in max_val
        if is_float:
            return Annotated[float, msgspec.Meta(ge=float(min_val), le=float(max_val))]
        return Annotated[int, msgspec.Meta(ge=int(min_val), le=int(max_val))]

    # Regex pattern
    if match.group("regex"):
        pattern = match.group("pattern")
        return Annotated[str, msgspec.Meta(pattern=pattern)]

    # Format types
    if match.group("format"):
        fmt = match.group("format")
        return Annotated[str, msgspec.Meta(pattern=FORMAT_PATTERNS[fmt])]

    # Pipe-delimited: Union or Enum (auto-detect based on reserved types)
    if match.group("enum"):
        from typing import Literal

        parts = [v.strip() for v in match.group("enum_values").split("|")]

        # Auto-detection: if ALL parts are reserved types, treat as Union
        # Otherwise, treat as Enum (Literal)
        all_reserved = all(is_reserved_type(part) for part in parts)

        if all_reserved:
            # Union type: str | int | email, etc.
            union_types = [to_msgspec_type(part) for part in parts]
            # Create Union of the types using | operator
            if len(union_types) == 1:
                return union_types[0]
            # Use reduce to create Union dynamically: type1 | type2 | type3
            result = union_types[0]
            for t in union_types[1:]:
                result = result | t  # type: ignore
            return result
        else:
            # Enum type: active | inactive, etc.
            # Strip quotes from literal values if present
            values = []
            for v in parts:
                v_stripped = v.strip()
                if (v_stripped.startswith('"') and v_stripped.endswith('"')) or \
                   (v_stripped.startswith("'") and v_stripped.endswith("'")):
                    # Remove quotes
                    values.append(v_stripped[1:-1])
                else:
                    values.append(v_stripped)
            # Note: Literal[values] where values=('a','b','c') creates Literal['a','b','c']
            # (multiple string values), NOT Literal[('a','b','c')] (single tuple value).
            # Python's subscript operator passes the tuple directly to __class_getitem__.
            return Literal[tuple(values)]  # type: ignore

    # Set with bracket syntax: set[int]
    if match.group("set_bracket"):
        inner_type = match.group("set_bracket_inner")
        inner = to_msgspec_type(inner_type)
        return set[inner]  # type: ignore

    # FrozenSet: frozenset[int]
    if match.group("frozenset"):
        inner_type = match.group("frozenset_inner")
        inner = to_msgspec_type(inner_type)
        return frozenset[inner]  # type: ignore

    # Tuple: tuple[float, float] or tuple[int, ...]
    if match.group("tuple"):
        inner_str = match.group("tuple_inner")
        # Handle variable-length tuple: tuple[int, ...]
        if inner_str.endswith(", ..."):
            base_type = inner_str[:-5].strip()  # Remove ", ..."
            inner = to_msgspec_type(base_type)
            return tuple[inner, ...]  # type: ignore
        # Handle fixed-length tuple: tuple[float, float]
        else:
            parts = _split_annotation_items(inner_str)
            if len(parts) == 1:
                inner = to_msgspec_type(parts[0])
                return tuple[inner]  # type: ignore
            else:
                inner_types = tuple(to_msgspec_type(p) for p in parts)
                return tuple[inner_types]  # type: ignore

    # Array
    if match.group("array"):
        inner_type = match.group("array_inner")
        if inner_type:
            inner = to_msgspec_type(inner_type)
            return list[inner]  # type: ignore
        else:
            return list  # Bare "list" type

    # Set (legacy syntax with braces: {int})
    if match.group("set"):
        inner = match.group("set_inner")
        if ":" in inner:
            return dict  # Inline object
        return set[to_msgspec_type(inner)]  # type: ignore

    # Primitive
    if match.group("primitive"):
        return PRIMITIVE_TYPES[match.group("primitive")]

    return str


def to_pydantic_type(type_expr: str, annotation: str | None = None):
    """Convert SlimSchema type string to Pydantic-compatible type.

    Similar to to_msgspec_type but uses Pydantic's Field constraints
    instead of msgspec.Meta, ensuring patterns and other constraints
    are preserved in Pydantic's JSON Schema output.
    """
    from pydantic import Field as PydanticField

    annotated_type = _annotation_to_pydantic(annotation)
    if annotated_type is not None:
        return annotated_type

    type_expr = type_expr.strip()

    # Inline object syntax: {name:str,age:int}
    # Treat as plain dict for now (shape not yet enforced).
    if type_expr.startswith("{") and type_expr.endswith("}"):
        inner = type_expr[1:-1]
        # Legacy set syntax uses {type} with no ":", keep that path intact.
        if ":" in inner:
            return dict

    # Dict sugar syntax: dict{K,V} → plain dict
    if type_expr.startswith("dict{") and type_expr.endswith("}"):
        return dict

    match = TYPE_PATTERN.fullmatch(type_expr)

    if not match:
        return str  # Default fallback

    # String length
    if match.group("str_len"):
        min_len = int(match.group("str_min"))
        max_len = int(match.group("str_max"))
        return Annotated[str, PydanticField(min_length=min_len, max_length=max_len)]

    # Numeric range
    if match.group("num_range"):
        min_val = match.group("num_min")
        max_val = match.group("num_max")
        is_float = "." in min_val or "." in max_val
        if is_float:
            return Annotated[float, PydanticField(ge=float(min_val), le=float(max_val))]
        return Annotated[int, PydanticField(ge=int(min_val), le=int(max_val))]

    # Regex pattern
    if match.group("regex"):
        pattern = match.group("pattern")
        return Annotated[str, PydanticField(pattern=pattern)]

    # Format types
    if match.group("format"):
        fmt = match.group("format")
        return Annotated[str, PydanticField(pattern=FORMAT_PATTERNS[fmt])]

    # Pipe-delimited: Union or Enum (auto-detect based on reserved types)
    if match.group("enum"):
        from typing import Literal

        parts = [v.strip() for v in match.group("enum_values").split("|")]

        # Auto-detection: if ALL parts are reserved types, treat as Union
        # Otherwise, treat as Enum (Literal)
        all_reserved = all(is_reserved_type(part) for part in parts)

        if all_reserved:
            # Union type: str | int | email, etc.
            union_types = [to_pydantic_type(part) for part in parts]
            # Create Union of the types using | operator
            if len(union_types) == 1:
                return union_types[0]
            # Use reduce to create Union dynamically: type1 | type2 | type3
            result = union_types[0]
            for t in union_types[1:]:
                result = result | t  # type: ignore
            return result
        else:
            # Enum type: active | inactive, etc.
            # Strip quotes from literal values if present
            values = []
            for v in parts:
                v_stripped = v.strip()
                if (v_stripped.startswith('"') and v_stripped.endswith('"')) or \
                   (v_stripped.startswith("'") and v_stripped.endswith("'")):
                    # Remove quotes
                    values.append(v_stripped[1:-1])
                else:
                    values.append(v_stripped)
            return Literal[tuple(values)]  # type: ignore

    # Set with bracket syntax: set[int]
    if match.group("set_bracket"):
        inner_type = match.group("set_bracket_inner")
        inner = to_pydantic_type(inner_type)
        return set[inner]  # type: ignore

    # FrozenSet: frozenset[int]
    if match.group("frozenset"):
        inner_type = match.group("frozenset_inner")
        inner = to_pydantic_type(inner_type)
        return frozenset[inner]  # type: ignore

    # Tuple: tuple[float, float] or tuple[int, ...]
    if match.group("tuple"):
        inner_str = match.group("tuple_inner")
        # Handle variable-length tuple: tuple[int, ...]
        if inner_str.endswith(", ..."):
            base_type = inner_str[:-5].strip()  # Remove ", ..."
            inner = to_pydantic_type(base_type)
            return tuple[inner, ...]  # type: ignore
        # Handle fixed-length tuple: tuple[float, float]
        else:
            parts = _split_annotation_items(inner_str)
            if len(parts) == 1:
                inner = to_pydantic_type(parts[0])
                return tuple[inner]  # type: ignore
            else:
                inner_types = tuple(to_pydantic_type(p) for p in parts)
                return tuple[inner_types]  # type: ignore

    # Array
    if match.group("array"):
        inner_type = match.group("array_inner")
        if inner_type:
            inner = to_pydantic_type(inner_type)
            return list[inner]  # type: ignore
        else:
            return list  # Bare "list" type

    # Set (legacy syntax with braces: {int})
    if match.group("set"):
        inner = match.group("set_inner")
        if ":" in inner:
            return dict  # Inline object
        return set[to_pydantic_type(inner)]  # type: ignore

    # Primitive
    if match.group("primitive"):
        return PRIMITIVE_TYPES[match.group("primitive")]

    return str


def _annotation_to_pydantic(annotation: str | None):
    """Convert optional :: annotation to Pydantic type."""
    if not annotation:
        return None

    match = re.fullmatch(r"(Set|FrozenSet|Tuple)\[(.*)\]", annotation.strip())
    if not match:
        return None

    kind, inner = match.group(1), match.group(2)
    parts = _split_annotation_items(inner)

    if kind == "Set":
        if len(parts) != 1:
            return None
        inner_type = to_pydantic_type(parts[0])
        return set[inner_type]  # type: ignore

    if kind == "FrozenSet":
        if len(parts) != 1:
            return None
        inner_type = to_pydantic_type(parts[0])
        return frozenset[inner_type]  # type: ignore

    # Tuple
    if len(parts) == 2 and parts[1].strip() == "...":
        inner_type = to_pydantic_type(parts[0])
        return tuple[(inner_type, ...)]  # type: ignore

    inner_types = tuple(to_pydantic_type(part) for part in parts)
    return tuple[inner_types]  # type: ignore


def from_pydantic_field(field_info) -> tuple[str, str | None]:
    """Convert Pydantic field to SlimSchema type string and annotation."""
    annotation = field_info.annotation

    # Check for constraints in metadata
    min_length = max_length = None
    ge = le = None

    if hasattr(field_info, "metadata"):
        for constraint in field_info.metadata:
            # String length constraints
            if hasattr(constraint, "min_length"):
                min_length = constraint.min_length
            if hasattr(constraint, "max_length"):
                max_length = constraint.max_length
            # Numeric constraints
            if hasattr(constraint, "ge"):
                ge = constraint.ge
            if hasattr(constraint, "le"):
                le = constraint.le

    # Return constraint types
    if min_length and max_length:
        return f"str{{{min_length}..{max_length}}}", None
    if ge is not None and le is not None:
        return f"{ge}..{le}", None

    # Basic types
    for name, typ in PRIMITIVE_TYPES.items():
        if annotation == typ:
            return name, None

    # Check for Literal (enum) and Union
    origin = get_origin(annotation)
    if origin is not None:
        # Import types locally to avoid circular imports
        import types
        from typing import Literal, Union

        if origin is Literal:
            # Extract literal values and create pipe-delimited enum
            args = get_args(annotation)
            # Convert all values to strings for consistency
            enum_values = " | ".join(str(v) for v in args)
            return enum_values, None

        # Handle Union types (both typing.Union and types.UnionType from |)
        if origin is Union or (hasattr(types, 'UnionType') and origin is types.UnionType):
            # Extract union members and create pipe-delimited type union
            args = get_args(annotation)
            # Filter out None (for Optional types)
            non_none_args = [arg for arg in args if arg is not type(None)]

            if len(non_none_args) == 0:
                return "str", None

            # Convert each type to SlimSchema notation, preserving annotations
            union_parts = []
            union_annotations = []
            for arg in non_none_args:
                arg_type, arg_ann = from_pydantic_field(type("_", (), {"annotation": arg, "metadata": []})())
                union_parts.append(arg_type)
                # Preserve annotation for containers (set, frozenset, tuple)
                union_annotations.append(arg_ann or arg_type)

            # Join with pipe
            union_str = " | ".join(union_parts)

            # If any member has a different annotation, preserve it
            if any(ann != part for ann, part in zip(union_annotations, union_parts)):
                return union_str, f"Union[{', '.join(union_annotations)}]"
            else:
                return union_str, None

        return _from_container_annotation(origin, annotation)

    return "str", None


def _annotation_to_msgspec(annotation: str | None):
    """Convert optional :: annotation to msgspec type."""
    if not annotation:
        return None

    match = re.fullmatch(r"(Set|FrozenSet|Tuple)\[(.*)\]", annotation.strip())
    if not match:
        return None

    kind, inner = match.group(1), match.group(2)
    parts = _split_annotation_items(inner)

    if kind == "Set":
        if len(parts) != 1:
            return None
        inner_type = to_msgspec_type(parts[0])
        return set[inner_type]  # type: ignore

    if kind == "FrozenSet":
        if len(parts) != 1:
            return None
        inner_type = to_msgspec_type(parts[0])
        return frozenset[inner_type]  # type: ignore

    # Tuple
    if len(parts) == 2 and parts[1].strip() == "...":
        inner_type = to_msgspec_type(parts[0])
        return tuple[(inner_type, ...)]  # type: ignore

    inner_types = tuple(to_msgspec_type(part) for part in parts)
    return tuple[inner_types]  # type: ignore


def _from_container_annotation(origin, annotation) -> tuple[str, str | None]:
    """Convert container annotations to base type and :: annotation."""
    args = get_args(annotation)

    if origin is list:
        inner = args[0] if args else Any
        inner_type, _ = from_pydantic_field(type("_", (), {"annotation": inner, "metadata": []})())
        return f"list[{inner_type}]", None

    if origin is set:
        inner = args[0] if args else Any
        inner_type, _ = from_pydantic_field(type("_", (), {"annotation": inner, "metadata": []})())
        return f"set[{inner_type}]", None

    if origin is frozenset:
        inner = args[0] if args else Any
        inner_type, _ = from_pydantic_field(type("_", (), {"annotation": inner, "metadata": []})())
        return f"frozenset[{inner_type}]", None

    if origin is tuple:
        if not args:
            return "tuple", None

        if len(args) == 2 and args[1] is Ellipsis:
            inner = args[0]
            inner_type, _ = from_pydantic_field(
                type("_", (), {"annotation": inner, "metadata": []})()
            )
            return f"tuple[{inner_type}, ...]", None

        tuple_items = []
        for item in args:
            item_type, _ = from_pydantic_field(
                type("_", (), {"annotation": item, "metadata": []})()
            )
            tuple_items.append(item_type)

        return f"tuple[{', '.join(tuple_items)}]", None

    return "str", None


def _split_annotation_items(annotation: str) -> list[str]:
    """Split annotation contents by commas while respecting nesting."""
    items: list[str] = []
    buf = []
    depth = 0

    for char in annotation:
        if char == "," and depth == 0:
            items.append("".join(buf).strip())
            buf = []
            continue

        if char in "[({":
            depth += 1
        elif char in "])}" and depth > 0:
            depth -= 1

        buf.append(char)

    if buf:
        items.append("".join(buf).strip())

    return [item for item in items if item]


@functools.lru_cache(maxsize=128)
def _split_on_equals_respecting_braces(text: str) -> tuple[str, str | None]:
    """Split text on ' = ' while respecting nested braces/brackets.

    Returns (type_expr, default_expr) where default_expr is None if no ' = ' found.

    Example:
        "{theme:str = \"dark\"} = dict" -> ("{theme:str = \"dark\"}", "dict")
        "str = \"hello\"" -> ("str", "\"hello\"")
        "int" -> ("int", None)
    """
    depth = 0
    i = 0
    while i < len(text) - 2:  # -2 because we need at least 3 chars for " = "
        char = text[i]

        # Track brace/bracket depth
        if char in "{[":
            depth += 1
        elif char in "}]":
            depth -= 1

        # Only split on " = " when not inside braces/brackets
        if depth == 0 and text[i:i+3] == " = ":
            type_part = text[:i].strip()
            default_part = text[i+3:].strip() or None
            return type_part, default_part

        i += 1

    # No " = " found at depth 0
    return text.strip(), None


def parse_inline_object_def(expr: str) -> list[tuple[str, str, str | None, bool]]:
    """Parse inline object type string into (name, type, default, optional) tuples.

    Example:
        "{name:str, age:int=18, note?:str}" ->
        [("name", "str", None, False),
         ("age", "int", "18", False),
         ("note", "str", None, True)]
    """
    expr = expr.strip()
    if not (expr.startswith("{") and expr.endswith("}")):
        return []

    inner = expr[1:-1]
    items = _split_annotation_items(inner)
    fields: list[tuple[str, str, str | None, bool]] = []

    for item in items:
        part = item.strip()
        if not part or ":" not in part:
            continue

        name_part, type_default = part.split(":", 1)
        name_part = name_part.strip()
        if not name_part:
            continue

        optional = name_part.endswith("?")
        name = name_part[:-1] if optional else name_part

        type_default = type_default.strip()

        # Split on " = " while respecting nested braces
        type_expr, default_expr = _split_on_equals_respecting_braces(type_default)

        fields.append((name, type_expr, default_expr, optional))

    return fields


def parse_dict_sugar(expr: str) -> tuple[str, str] | None:
    """Parse dict sugar syntax 'dict{KeyType, ValueType}' into component types."""
    expr = expr.strip()
    if not (expr.startswith("dict{") and expr.endswith("}")):
        return None

    inner = expr[5:-1]
    parts = _split_annotation_items(inner)
    if len(parts) != 2:
        return None

    return parts[0].strip(), parts[1].strip()
