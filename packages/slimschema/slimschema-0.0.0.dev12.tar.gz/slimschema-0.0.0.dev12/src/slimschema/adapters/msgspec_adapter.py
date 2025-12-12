"""msgspec adapter - convert msgspec Structs to SlimSchema."""

from ..core import Field, Schema

# Mapping of Python types to SlimSchema type strings
BASIC_TYPES = {
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
    dict: "obj",
}


def from_msgspec(struct_class):
    """Convert msgspec Struct to SlimSchema.

    Args:
        struct_class: msgspec Struct class

    Returns:
        SlimSchema
    """
    import msgspec

    if not isinstance(struct_class, type) or not issubclass(struct_class, msgspec.Struct):
        raise TypeError(f"Expected msgspec.Struct, got {type(struct_class)}")

    fields = []
    annotations = struct_class.__annotations__

    for field_name in struct_class.__struct_fields__:
        annotation = annotations[field_name]

        # Check if optional (union with None)
        optional = False
        if hasattr(annotation, "__origin__") and annotation.__origin__ is type(None) | type:
            optional = True
            # Get the non-None type
            args = getattr(annotation, "__args__", ())
            annotation = next((a for a in args if a is not type(None)), annotation)

        # Convert to SlimSchema type string
        type_str, type_annotation = _msgspec_annotation_to_slimschema(annotation)

        fields.append(
            Field(
                name=field_name,
                type=type_str,
                optional=optional,
                description=None,
                annotation=type_annotation,
            )
        )

    return Schema(fields=fields, name=struct_class.__name__)


def _msgspec_annotation_to_slimschema(annotation) -> tuple[str, str | None]:
    """Convert msgspec annotation to SlimSchema type string."""
    from typing import get_args, get_origin

    # Basic types
    if annotation in BASIC_TYPES:
        return BASIC_TYPES[annotation], None

    # Containers
    origin = get_origin(annotation)
    if origin is list:
        args = get_args(annotation)
        if args:
            inner = _msgspec_annotation_to_slimschema(args[0])
            return f"list[{inner[0]}]", None
        return "list", None

    if origin is set:
        args = get_args(annotation)
        if args:
            inner = _msgspec_annotation_to_slimschema(args[0])
            return f"set[{inner[0]}]", None
        return "set[str]", None

    if origin is frozenset:
        args = get_args(annotation)
        if args:
            inner = _msgspec_annotation_to_slimschema(args[0])
            return f"frozenset[{inner[0]}]", None
        return "frozenset[str]", None

    if origin is tuple:
        args = get_args(annotation)
        if len(args) == 2 and args[1] is Ellipsis:
            inner = _msgspec_annotation_to_slimschema(args[0])
            return f"tuple[{inner[0]}, ...]", None

        tuple_parts = []
        for arg in args:
            inner = _msgspec_annotation_to_slimschema(arg)
            tuple_parts.append(inner[0])

        if tuple_parts:
            return f"tuple[{', '.join(tuple_parts)}]", None

    return "str", None
