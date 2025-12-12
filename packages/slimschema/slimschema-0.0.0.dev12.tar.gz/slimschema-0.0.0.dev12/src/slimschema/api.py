"""Public API for SlimSchema."""

from typing import Any

from .core import Schema
from .defaults import DefaultValueError, evaluate_default
from .errors import ValidationError
from .parser import parse_slimschema


def _apply_defaults(data: dict, schema: Schema) -> dict:
    """Apply default values to missing fields in data.

    Args:
        data: The JSON data (will not be modified)
        schema: Schema with default values

    Returns:
        New dict with defaults applied
    """
    from datetime import date, datetime

    from .types import parse_inline_object_def

    result = data.copy()

    # 1. Apply top-level defaults for missing fields.
    for field in schema.fields:
        if field.name in result or field.default is None:
            continue

        try:
            default_value = evaluate_default(field.default, field.type)

            if isinstance(default_value, datetime):
                default_value = default_value.isoformat()
            elif isinstance(default_value, date):
                default_value = default_value.isoformat()

            result[field.name] = default_value
        except DefaultValueError:
            # If default evaluation fails, skip it (validation will catch missing field).
            pass

    # 2. Auto-create top-level inline objects if all nested fields have defaults/are optional
    for field in schema.fields:
        if field.name in result:
            continue

        # Check if this is an inline object that can be fully constructed from defaults
        if isinstance(field.type, str) and field.type.startswith("{"):
            nested_specs = parse_inline_object_def(field.type)
            can_construct = all(
                nested_default is not None or nested_optional
                for _, _, nested_default, nested_optional in nested_specs
            )

            if can_construct and nested_specs:
                # Create empty dict and apply nested defaults
                result[field.name] = _apply_inline_defaults({}, field.type)

    # 3. Recursively apply defaults inside inline object fields that are present.
    for field in schema.fields:
        if field.name not in result:
            continue

        value = result[field.name]

        # Inline object syntax: "{name:type,...}" – treat as nested schema for defaults.
        if isinstance(value, dict) and isinstance(field.type, str) and field.type.startswith("{"):
            result[field.name] = _apply_inline_defaults(value, field.type)

    return result


def _apply_inline_defaults(data: dict, type_expr: str) -> dict:
    """Apply defaults inside an inline object type to a nested dict.

    The inline syntax looks like:
        "{secret:/^[A-Z]{4..9}$/=\"UNDEFINED\",tracking:dict{[1-9], /^[A-Z]\\-$/}=dict}"

    We deserialize this into field specs, apply defaults for missing keys,
    and recurse for nested inline objects.
    """
    from datetime import date, datetime

    from .types import parse_inline_object_def

    result = data.copy()
    field_specs = parse_inline_object_def(type_expr)

    for name, field_type, default_expr, optional in field_specs:
        # 1. Apply default for missing nested keys.
        if name not in result and default_expr is not None:
            try:
                default_value = evaluate_default(default_expr, field_type)

                if isinstance(default_value, datetime):
                    default_value = default_value.isoformat()
                elif isinstance(default_value, date):
                    default_value = default_value.isoformat()

                result[name] = default_value
            except DefaultValueError:
                # Skip invalid nested defaults; validation will surface issues if any.
                pass

        # 2. Auto-create nested inline objects if all nested fields have defaults/are optional
        if name not in result and isinstance(field_type, str) and field_type.startswith("{"):
            # Check if this nested object can be fully constructed from defaults
            nested_specs = parse_inline_object_def(field_type)
            can_construct = all(
                nested_default is not None or nested_optional
                for _, _, nested_default, nested_optional in nested_specs
            )

            if can_construct and nested_specs:
                # Create empty dict and apply nested defaults
                result[name] = _apply_inline_defaults({}, field_type)

        # 3. Recurse into nested inline objects that are present.
        if name in result and isinstance(result[name], dict) and isinstance(field_type, str) and field_type.startswith("{"):
            result[name] = _apply_inline_defaults(result[name], field_type)

    return result


def to_schema(obj: Any) -> Schema:
    """Convert any schema format to SlimSchema intermediate representation.

    Accepts YAML strings, Pydantic models, msgspec Structs, or Schema objects.
    This is the universal entry point for working with schemas.

    Args:
        obj: Your schema in any supported format

    Returns:
        Schema object (intermediate representation)

    Examples:
        >>> # From YAML string
        >>> schema = to_schema("name: str\\nage: 18..120")

        >>> # From Pydantic model
        >>> from pydantic import BaseModel
        >>> class User(BaseModel):
        ...     name: str
        ...     age: int
        >>> schema = to_schema(User)

        >>> # From msgspec Struct
        >>> import msgspec
        >>> class Product(msgspec.Struct):
        ...     title: str
        ...     price: float
        >>> schema = to_schema(Product)

        >>> # Already a Schema - returns as-is
        >>> schema2 = to_schema(schema)
        >>> schema is schema2
        True
    """
    if isinstance(obj, Schema):
        return obj

    if isinstance(obj, str):
        return parse_slimschema(obj)

    if isinstance(obj, type):
        # Pydantic model
        if hasattr(obj, "model_fields"):
            from .adapters.pydantic import from_pydantic
            return from_pydantic(obj)

        # msgspec Struct
        if hasattr(obj, "__struct_fields__"):
            from .adapters.msgspec_adapter import from_msgspec
            return from_msgspec(obj)

    raise TypeError(f"Cannot convert {type(obj).__name__} to Schema")


def to_data(response: str, schema_obj: Any) -> tuple[Any, str | None]:
    """Extract and validate JSON from LLM response.

    Args:
        response: LLM response text (supports JSON tags, code fences, etc.)
        schema_obj: YAML string, Schema, Pydantic model, or msgspec Struct

    Returns:
        (data, error) tuple:
        - data: Validated object/dict (None if validation fails)
        - error: Grouped error message (None if validation succeeds)

    Examples:
        >>> # YAML schema validation
        >>> yaml = "name: str\\nage: 18..120"
        >>> data, err = to_data('{"name": "Alice", "age": 30}', yaml)
        >>> data
        {'name': 'Alice', 'age': 30}

        >>> # Multiple errors collected
        >>> data, err = to_data('{"extra": "field"}', yaml)
        >>> print(err)
        Missing required fields: name, age
        Unknown fields: extra

        >>> # Pydantic model validation
        >>> from pydantic import BaseModel
        >>> class User(BaseModel):
        ...     name: str
        ...     age: int
        >>> user, err = to_data('<json>{"name": "Bob", "age": 25}</json>', User)
        >>> user.name
        'Bob'

    Notes:
        - For YAML/string schemas: Always rejects extra fields
        - For Pydantic models: Respects model's ConfigDict(extra=...) setting
        - For msgspec Structs: Respects struct's forbid_unknown_fields setting
    """
    from .extract import extract_structured_data

    # Extract structured data (supports JSON, CSV, XML, YAML)
    result = extract_structured_data(response)
    if result is None:
        return None, "No valid structured data (JSON, CSV, XML, YAML) found in response"

    json_data, detected_format = result

    # msgspec Struct - use msgspec directly (respects struct's forbid_unknown_fields)
    if isinstance(schema_obj, type) and hasattr(schema_obj, "__struct_fields__"):
        try:
            import msgspec

            instance = msgspec.convert(json_data, type=schema_obj)
            return instance, None
        except (msgspec.ValidationError, TypeError, ValueError) as e:
            # Convert msgspec error to our format
            errors = ValidationError()
            _parse_msgspec_error(str(e), errors)
            return None, str(errors)

    # Pydantic model - use Pydantic validation directly (preserves custom validators)
    if isinstance(schema_obj, type) and hasattr(schema_obj, "model_fields"):
        try:
            instance = schema_obj.model_validate(json_data)
            return instance, None
        except Exception as e:
            errors = ValidationError()
            _parse_pydantic_error(e, errors)
            return None, str(errors)

    # YAML string or Schema - use our validation (always rejects extra fields)
    try:
        schema = to_schema(schema_obj)
    except Exception as e:
        # Surface schema issues as a concise error instead of a traceback
        return None, f"Invalid schema: {e}"

    try:
        import msgspec

        from .validate import validate

        # Apply defaults before validation (only for dict/object data)
        if isinstance(json_data, dict):
            json_data_with_defaults = _apply_defaults(json_data, schema)
        else:
            # CSV/arrays can't have defaults applied - validate as-is
            json_data_with_defaults = json_data

        # Validate the data
        result = validate(json_data_with_defaults, schema)

        if not result.valid:
            return None, str(result.errors)

        return result.data, None
    except ImportError:
        return None, "msgspec is required for validation"


def _parse_msgspec_error(error_str: str, errors: ValidationError) -> None:
    """Parse msgspec error string into ValidationError."""
    # msgspec typically gives single errors like:
    # "Object missing required field `name`"
    # "Expected `int`, got `str` - at `$.age`"
    if "missing required field" in error_str.lower():
        # Extract field name
        import re
        if match := re.search(r"`(\w+)`", error_str):
            field = match.group(1)
            errors.add(f"$.{field}", ValidationError.MISSING)
    elif "expected" in error_str.lower():
        # Try to extract path
        import re
        path = "$"
        if match := re.search(r"at `([^`]+)`", error_str):
            path = match.group(1)

        if ">" in error_str or "<" in error_str:
            errors.add(path, ValidationError.RANGE, error_str)
        else:
            errors.add(path, ValidationError.TYPE, error_str)
    else:
        errors.add("$", ValidationError.FORMAT, error_str)


def _parse_pydantic_error(exception: Exception, errors: ValidationError) -> None:
    """Parse Pydantic ValidationError into our ValidationError."""
    from pydantic import ValidationError as PydanticValidationError

    if not isinstance(exception, PydanticValidationError):
        # Generic error
        errors.add("$", ValidationError.FORMAT, str(exception))
        return

    # Pydantic errors have .errors() method returning list of dicts
    for err in exception.errors():
        # Build JSON path from location
        loc = err.get("loc", ())
        if loc:
            path = "$." + ".".join(str(part) for part in loc)
        else:
            path = "$"

        # Categorize by error type
        err_type = err.get("type", "")
        msg = err.get("msg", "")

        if "missing" in err_type:
            errors.add(path, ValidationError.MISSING)
        elif "extra" in err_type:
            errors.add(path, ValidationError.EXTRA)
        elif "enum" in err_type or "literal" in err_type:
            errors.add(path, ValidationError.ENUM, msg)
        elif "type" in err_type:
            errors.add(path, ValidationError.TYPE, msg)
        elif err_type.startswith("value_error"):
            errors.add(path, ValidationError.FORMAT, msg)
        elif "greater" in err_type or "less" in err_type:
            errors.add(path, ValidationError.RANGE, msg)
        else:
            errors.add(path, ValidationError.FORMAT, msg)


def to_pydantic(schema_input: Any) -> type:
    """Create a Pydantic model class from your schema.

    Takes any schema format and returns a Pydantic BaseModel class.
    Use this when you want Pydantic's validation features or ecosystem integration.

    Args:
        schema_input: Your schema (YAML string, Schema, Pydantic model, or msgspec Struct)

    Returns:
        Pydantic BaseModel class ready to use

    Examples:
        >>> # From YAML - creates a Pydantic model
        >>> yaml = "# User\\nname: str\\nage: 18..120"
        >>> UserModel = to_pydantic(yaml)
        >>> user = UserModel(name="Alice", age=30)
        >>> user.name
        'Alice'

        >>> # Now you can use Pydantic features
        >>> user.model_dump()
        {'name': 'Alice', 'age': 30}

        >>> # Already Pydantic - returns as-is
        >>> to_pydantic(UserModel) is UserModel
        True

        >>> # With defaults
        >>> yaml_with_defaults = "name: str\\nage: int = 18"
        >>> UserModel = to_pydantic(yaml_with_defaults)
        >>> user = UserModel(name="Bob")
        >>> user.age
        18
    """
    from pydantic import Field as PydanticField
    from pydantic import create_model

    from .core import Field as CoreField
    from .core import Schema as CoreSchema
    from .defaults import DefaultValueError, parse_default_value
    from .types import parse_inline_object_def, to_pydantic_type

    # If already Pydantic, return as-is
    if isinstance(schema_input, type) and hasattr(schema_input, "model_fields"):
        return schema_input

    # Convert to Schema IR
    schema = to_schema(schema_input)

    # Build Pydantic field definitions
    fields = {}
    for field in schema.fields:
        field_type_str = field.type if isinstance(field.type, str) else str(field.type)
        stripped_type = field_type_str.strip()

        # Inline object syntax: {name:type,...} – model as nested Pydantic class
        if stripped_type.startswith("{") and stripped_type.endswith("}") and ":" in stripped_type:
            # Parse nested fields from inline definition
            sub_fields: list[CoreField] = []
            for sub_name, sub_type, sub_default, sub_optional in parse_inline_object_def(field_type_str):
                sub_fields.append(
                    CoreField(
                        name=sub_name,
                        type=sub_type,
                        optional=sub_optional,
                        default=sub_default,
                    )
                )

            nested_schema = CoreSchema(
                fields=sub_fields,
                name=f"{schema.name}_{field.name}" if schema.name else field.name.capitalize(),
            )
            nested_model = to_pydantic(nested_schema)
            py_type = nested_model
        else:
            py_type = to_pydantic_type(field.type, field.annotation)

        # Determine the default value
        if field.default is not None:
            # Parse the default expression
            try:
                default_value, is_factory = parse_default_value(field.default, field.type)

                if is_factory:
                    # Use default_factory for callable/mutable defaults
                    if field.optional:
                        fields[field.name] = (py_type | None, PydanticField(default_factory=default_value))
                    else:
                        fields[field.name] = (py_type, PydanticField(default_factory=default_value))
                else:
                    # Use plain default for immutable values
                    if field.optional:
                        fields[field.name] = (py_type | None, default_value)
                    else:
                        fields[field.name] = (py_type, default_value)
            except DefaultValueError:
                # If default parsing fails, treat as required field
                if field.optional:
                    fields[field.name] = (py_type | None, None)
                else:
                    fields[field.name] = (py_type, ...)
        elif field.optional:
            # Optional with no default
            fields[field.name] = (py_type | None, None)
        else:
            # Required field
            fields[field.name] = (py_type, ...)

    # Create Pydantic model with schema name
    model_name = schema.name or "DynamicModel"
    return create_model(model_name, **fields)


def to_msgspec(schema_input: Any) -> type:
    """Create a msgspec Struct class from your schema.

    Takes any schema format and returns a msgspec Struct class.
    Use this when you want msgspec's ultra-fast JSON validation (117x faster than alternatives).

    Args:
        schema_input: Your schema (YAML string, Schema, Pydantic model, or msgspec Struct)

    Returns:
        msgspec Struct class ready to use

    Examples:
        >>> # From YAML - creates a msgspec Struct
        >>> yaml = "# User\\nname: str\\nage: 18..120"
        >>> UserStruct = to_msgspec(yaml)
        >>> import msgspec
        >>> user = msgspec.convert({"name": "Alice", "age": 30}, type=UserStruct)
        >>> user.name
        'Alice'

        >>> # msgspec is blazing fast for validation
        >>> msgspec.json.decode(b'{"name": "Bob", "age": 25}', type=UserStruct)
        UserStruct(name='Bob', age=25)

        >>> # Already msgspec - returns as-is
        >>> to_msgspec(UserStruct) is UserStruct
        True

        >>> # With defaults
        >>> yaml_with_defaults = "name: str\\nage: int = 18"
        >>> UserStruct = to_msgspec(yaml_with_defaults)
        >>> user = msgspec.convert({"name": "Charlie"}, type=UserStruct)
        >>> user.age
        18
    """
    import msgspec

    from .core import Field as CoreField
    from .core import Schema as CoreSchema
    from .defaults import DefaultValueError, parse_default_value
    from .types import parse_inline_object_def, to_msgspec_type

    # If already msgspec, return as-is
    if isinstance(schema_input, type) and hasattr(schema_input, "__struct_fields__"):
        return schema_input

    # Convert to Schema IR
    schema = to_schema(schema_input)

    # Build msgspec field annotations and defaults
    annotations = {}
    defaults = {}

    for field in schema.fields:
        field_type_str = field.type if isinstance(field.type, str) else str(field.type)
        stripped_type = field_type_str.strip()

        # Inline object syntax: {name:type,...} – model as nested msgspec Struct
        if stripped_type.startswith("{") and stripped_type.endswith("}") and ":" in stripped_type:
            sub_fields: list[CoreField] = []
            for sub_name, sub_type, sub_default, sub_optional in parse_inline_object_def(field_type_str):
                sub_fields.append(
                    CoreField(
                        name=sub_name,
                        type=sub_type,
                        optional=sub_optional,
                        default=sub_default,
                    )
                )

            nested_schema = CoreSchema(
                fields=sub_fields,
                name=f"{schema.name}_{field.name}" if schema.name else field.name.capitalize(),
            )
            field_type = to_msgspec(nested_schema)
        else:
            field_type = to_msgspec_type(field.type, field.annotation)

        # Determine default value
        if field.default is not None:
            # Parse the default expression
            try:
                default_value, is_factory = parse_default_value(field.default, field.type)

                # msgspec doesn't support factory functions like Pydantic's default_factory
                # For factories, we call them once to get a value
                # Note: This means mutable defaults will be shared across instances
                if is_factory:
                    evaluated_default = default_value()
                    # Convert datetime/date to ISO strings to match type annotations
                    from datetime import date, datetime
                    if isinstance(evaluated_default, datetime):
                        evaluated_default = evaluated_default.isoformat()
                    elif isinstance(evaluated_default, date):
                        evaluated_default = evaluated_default.isoformat()

                    if field.optional:
                        annotations[field.name] = field_type | None
                        defaults[field.name] = evaluated_default
                    else:
                        annotations[field.name] = field_type
                        defaults[field.name] = evaluated_default
                else:
                    # Plain default value
                    if field.optional:
                        annotations[field.name] = field_type | None
                        defaults[field.name] = default_value
                    else:
                        annotations[field.name] = field_type
                        defaults[field.name] = default_value
            except DefaultValueError:
                # If default parsing fails, treat as required field
                if field.optional:
                    annotations[field.name] = field_type | None
                    defaults[field.name] = None
                else:
                    annotations[field.name] = field_type
        elif field.optional:
            # Optional with no default
            annotations[field.name] = field_type | None
            defaults[field.name] = None
        else:
            # Required field
            annotations[field.name] = field_type

    # Create msgspec Struct with schema name
    struct_name = schema.name or "DynamicStruct"
    return msgspec.defstruct(
        struct_name,
        [(name, annotations[name], defaults.get(name, msgspec.NODEFAULT))
         for name in annotations]
    )
