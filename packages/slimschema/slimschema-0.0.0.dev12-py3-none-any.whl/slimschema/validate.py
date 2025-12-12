"""Validation using msgspec."""

import re

import msgspec

from .core import Schema, ValidationResult
from .errors import ValidationError
from .types import to_msgspec_type


def validate(data: dict | list, schema: Schema) -> ValidationResult:
    """Validate data against schema, collecting ALL errors.

    Args:
        data: Data to validate
        schema: Schema to validate against

    Returns:
        ValidationResult with all errors collected
    """
    errors = ValidationError()

    # Must be a dict for object schemas
    if not isinstance(data, dict):
        errors.add("$", ValidationError.TYPE, "expected object")
        return ValidationResult(valid=False, data=None, errors=errors, schema=schema)

    # Collect field sets
    seen_fields = set(data.keys())
    required_fields = {f.name for f in schema.fields if not f.optional}
    all_fields = {f.name for f in schema.fields}

    # Check for missing required fields
    for field_name in required_fields:
        if field_name not in data:
            errors.add(f"$.{field_name}", ValidationError.MISSING)

    # Check for extra fields (always reject for YAML/string schemas)
    for field_name in seen_fields:
        if field_name not in all_fields:
            errors.add(f"$.{field_name}", ValidationError.EXTRA)

    # Validate each field individually to collect all errors
    validated_data = {}
    for field in schema.fields:
        if field.name not in data:
            continue  # Already recorded as missing if required

        value = data[field.name]
        field_path = f"$.{field.name}"

        field_type_str = field.type if isinstance(field.type, str) else str(field.type)
        stripped_type = field_type_str.strip()

        # 1) Inline object syntax: {name:type,...} (must contain ':')
        if stripped_type.startswith("{") and stripped_type.endswith("}") and ":" in stripped_type:
            if not isinstance(value, dict):
                errors.add(field_path, ValidationError.TYPE, "expected object")
                continue

            from .core import Field as CoreField
            from .types import parse_inline_object_def

            # Build a nested Schema from the inline definition
            sub_fields = []
            for sub_name, sub_type, _sub_default, sub_optional in parse_inline_object_def(field_type_str):
                sub_fields.append(CoreField(name=sub_name, type=sub_type, optional=sub_optional))

            sub_schema = Schema(fields=sub_fields, name=f"{schema.name}.{field.name}" if schema.name else None)
            sub_result = validate(value, sub_schema)

            if not sub_result.valid and sub_result.errors:
                # Re-map nested paths: "$.secret" -> "$.state.secret"
                for path, err_list in sub_result.errors._by_path.items():
                    suffix = path.lstrip("$")  # ".secret"
                    new_path = f"{field_path}{suffix}"
                    for err_type, msg in err_list:
                        errors.add(new_path, err_type, msg)
            else:
                validated_data[field.name] = sub_result.data

            continue

        # 2) dict{KeyType, ValueType} sugar
        if stripped_type.startswith("dict{") and stripped_type.endswith("}"):
            from .types import parse_dict_sugar

            if not isinstance(value, dict):
                errors.add(field_path, ValidationError.TYPE, "expected dict")
                continue

            parts = parse_dict_sugar(field_type_str)
            if not parts:
                # Malformed dict sugar - fall back to generic dict validation
                try:
                    dict_type = to_msgspec_type("obj", field.annotation)
                    validated_data[field.name] = msgspec.convert(value, type=dict_type)
                except (msgspec.ValidationError, TypeError, ValueError) as e:
                    errors.add(field_path, ValidationError.TYPE, str(e))
                continue

            key_type_str, value_type_str = parts

            try:
                key_type = to_msgspec_type(key_type_str)
                value_type = to_msgspec_type(value_type_str)
            except (ValueError, TypeError, KeyError):
                # If we can't interpret types, just pass through the dict
                validated_data[field.name] = value
                continue

            validated_dict = {}
            dict_has_errors = False

            for k, v in value.items():
                # Validate key (with JSON string → number coercion when appropriate)
                try:
                    valid_key = msgspec.convert(k, type=key_type)
                except (msgspec.ValidationError, TypeError, ValueError) as e:
                    # For JSON, object keys are always strings – try numeric coercion
                    if isinstance(k, str):
                        try:
                            numeric_k = int(k)
                        except ValueError:
                            dict_has_errors = True
                            errors.add(field_path, ValidationError.TYPE, f"invalid key {k}: {_clean_msg(str(e))}")
                            continue

                        try:
                            valid_key = msgspec.convert(numeric_k, type=key_type)
                        except (msgspec.ValidationError, TypeError, ValueError) as e2:
                            dict_has_errors = True
                            errors.add(field_path, ValidationError.TYPE, f"invalid key {k}: {_clean_msg(str(e2))}")
                            continue
                    else:
                        dict_has_errors = True
                        errors.add(field_path, ValidationError.TYPE, f"invalid key {k}: {_clean_msg(str(e))}")
                        continue

                # Validate value
                try:
                    valid_value = msgspec.convert(v, type=value_type)
                    validated_dict[valid_key] = valid_value
                except (msgspec.ValidationError, TypeError, ValueError) as e:
                    dict_has_errors = True
                    errors.add(f"{field_path}.{k}", ValidationError.TYPE, _clean_msg(str(e)))

            if not dict_has_errors:
                validated_data[field.name] = validated_dict

            continue

        # 3) Handle list[{inline_object}] syntax
        list_inline_match = re.match(r'^list\[\{(.+)\}\]$', stripped_type)
        if list_inline_match:
            # Extract inline object definition: list[{name:str, count:int}] -> {name:str, count:int}
            inline_def = '{' + list_inline_match.group(1) + '}'

            if not isinstance(value, list):
                errors.add(field_path, ValidationError.TYPE, "expected list")
                continue

            from .core import Field as CoreField
            from .types import parse_inline_object_def

            # Build schema from inline definition
            sub_fields = []
            for sub_name, sub_type, _sub_default, sub_optional in parse_inline_object_def(inline_def):
                sub_fields.append(CoreField(name=sub_name, type=sub_type, optional=sub_optional))

            sub_schema = Schema(fields=sub_fields, name=f"{schema.name}.{field.name}[]" if schema.name else None)

            # Validate each element in the list
            validated_list = []
            list_has_errors = False

            for idx, item in enumerate(value):
                if not isinstance(item, dict):
                    errors.add(f"{field_path}[{idx}]", ValidationError.TYPE, "expected object")
                    list_has_errors = True
                    continue

                item_result = validate(item, sub_schema)

                if not item_result.valid and item_result.errors:
                    # Re-map nested paths: "$.field" -> "$.items[0].field"
                    for path, err_list in item_result.errors._by_path.items():
                        suffix = path.lstrip("$")  # ".field"
                        new_path = f"{field_path}[{idx}]{suffix}"
                        for err_type, msg in err_list:
                            errors.add(new_path, err_type, msg)
                    list_has_errors = True
                else:
                    validated_list.append(item_result.data)

            if not list_has_errors:
                validated_data[field.name] = validated_list

            continue

        # 4) Standard field validation (existing behavior)
        # Convert field type definition to msgspec type
        try:
            field_type = to_msgspec_type(field.type, field.annotation)
        except (ValueError, TypeError, KeyError) as e:
            errors.add(field_path, ValidationError.TYPE, f"Invalid type definition: {e}")
            continue

        # Validate and convert the value
        try:
            validated_value = msgspec.convert(value, type=field_type)
            validated_data[field.name] = validated_value
        except (msgspec.ValidationError, TypeError, ValueError) as e:
            error_msg = str(e)

            if "missing required field" in error_msg.lower():
                errors.add(field_path, ValidationError.MISSING, _clean_msg(error_msg))
            elif "invalid enum value" in error_msg.lower():
                errors.add(field_path, ValidationError.ENUM, _clean_msg(error_msg))
            elif "expected" in error_msg.lower() and (">" in error_msg or "<" in error_msg):
                errors.add(field_path, ValidationError.RANGE, _clean_msg(error_msg))
            elif "expected `" in error_msg.lower():
                errors.add(field_path, ValidationError.TYPE, _clean_msg(error_msg))
            else:
                errors.add(field_path, ValidationError.FORMAT, _clean_msg(error_msg))

    # Convert sets and frozensets to lists for JSON Patch compatibility
    # Sets are validated by msgspec (uniqueness enforced), then converted to lists
    # This allows JSON Patch operations like /path/- to work while maintaining uniqueness semantics
    for field in schema.fields:
        if field.name in validated_data:
            value = validated_data[field.name]
            # Handle both legacy {type} and modern set[type] / frozenset[type] syntax
            if isinstance(value, (set, frozenset)):
                validated_data[field.name] = list(value)

    if errors:
        return ValidationResult(valid=False, data=None, errors=errors, schema=schema)

    return ValidationResult(valid=True, data=validated_data, errors=None, schema=schema)


def _clean_msg(msg: str) -> str:
    """Clean up msgspec error messages for brevity."""
    # Remove common prefixes
    msg = msg.replace("Expected `", "expected ")
    msg = msg.replace("`, got `", ", got ")
    msg = msg.replace("`", "")
    return msg
