"""Safe default value evaluation for SlimSchema.

Supports:
- Literals: 0, "test", true, null, [], {}
- Time functions: now, today
- Random functions: uuid, random, randint(min, max)
- Collection factories: list, dict, set
"""

import ast
import random as random_module
import uuid as uuid_module
from collections.abc import Callable
from datetime import date, datetime
from typing import Any


class DefaultValueError(Exception):
    """Error parsing or evaluating a default value."""

    pass


def _eval_literal(expr: str) -> Any:
    """Safely evaluate a literal expression.

    Args:
        expr: String like "0", "'test'", "[]", etc.
        Supports both Python (True/False/None) and YAML (true/false/null) literals.

    Returns:
        Evaluated literal value

    Raises:
        ValueError: If not a valid literal
    """
    # Normalize YAML boolean/null literals to Python equivalents
    normalized = expr.strip()
    if normalized == "true":
        return True
    elif normalized == "false":
        return False
    elif normalized == "null":
        return None

    try:
        return ast.literal_eval(normalized)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid literal: {expr}") from e


def _extract_range_bounds(type_expr: str) -> tuple[float | None, float | None]:
    """Extract range bounds from type expression.

    Args:
        type_expr: Type like "18..65" or "-10.5..35.2" or "int"

    Returns:
        (min, max) tuple, or (None, None) if no range found

    Examples:
        >>> _extract_range_bounds("18..65")
        (18, 65)
        >>> _extract_range_bounds("-10.5..35.2")
        (-10.5, 35.2)
        >>> _extract_range_bounds("int")
        (None, None)
    """
    if ".." not in type_expr:
        return None, None

    try:
        parts = type_expr.split("..")
        if len(parts) != 2:
            return None, None

        min_val = float(parts[0].strip())
        max_val = float(parts[1].strip())
        return min_val, max_val
    except (ValueError, AttributeError):
        return None, None


def _extract_enum_values(type_expr: str) -> list[str] | None:
    """Extract enum values from type expression.

    Args:
        type_expr: Type like "red | green | blue" or "str"

    Returns:
        List of enum values, or None if not an enum

    Examples:
        >>> _extract_enum_values("red | green | blue")
        ['red', 'green', 'blue']
        >>> _extract_enum_values("active | inactive")
        ['active', 'inactive']
        >>> _extract_enum_values("str")
        None
    """
    if "|" not in type_expr:
        return None

    # Split on | and strip whitespace
    values = [v.strip() for v in type_expr.split("|")]

    # Filter out empty strings
    values = [v for v in values if v]

    return values if values else None


def _parse_function_call(expr: str) -> tuple[str, tuple[Any, ...], dict[str, Any]]:
    """Parse a function call expression safely.

    Args:
        expr: Function call like "randint(1, 100)" or "uuid()"

    Returns:
        (function_name, args, kwargs) tuple

    Raises:
        ValueError: If not a valid function call
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {expr}") from e

    if not isinstance(tree.body, ast.Call):
        raise ValueError(f"Not a function call: {expr}")

    # Extract function name
    if not isinstance(tree.body.func, ast.Name):
        raise ValueError(f"Complex function calls not supported: {expr}")

    func_name = tree.body.func.id

    # Extract arguments (must be literals only - but can be lists/dicts of literals)
    args = []
    for arg in tree.body.args:
        if isinstance(arg, ast.Constant):
            args.append(arg.value)
        elif isinstance(arg, ast.UnaryOp) and isinstance(arg.op, ast.USub):
            # Handle negative numbers like -1
            if isinstance(arg.operand, ast.Constant):
                val = arg.operand.value
                args.append(-val)
            else:
                raise ValueError(f"Non-literal argument in {expr}")
        elif isinstance(arg, (ast.List, ast.Tuple, ast.Dict, ast.Set)):
            # Handle literal collections - use ast.literal_eval for safety
            arg_code = ast.get_source_segment(expr, arg)
            if arg_code:
                try:
                    args.append(_eval_literal(arg_code))
                except ValueError:
                    raise ValueError(f"Non-literal collection in {expr}")
            else:
                raise ValueError(f"Could not extract collection argument in {expr}")
        else:
            raise ValueError(f"Non-literal argument in {expr}: only constants and literal collections allowed")

    # Extract keyword arguments
    kwargs = {}
    for keyword in tree.body.keywords:
        if isinstance(keyword.value, ast.Constant):
            kwargs[keyword.arg] = keyword.value.value
        else:
            raise ValueError(f"Non-literal keyword argument in {expr}")

    return func_name, tuple(args), kwargs


def _create_type_aware_random(field_type: str) -> Callable[[], Any]:
    """Create a random function based on field type and constraints.

    Args:
        field_type: SlimSchema type like "int", "18..65", "red | green | blue"

    Returns:
        Function that generates random value of appropriate type

    Examples:
        >>> # Range constraints
        >>> fn = _create_type_aware_random("18..65")
        >>> val = fn()
        >>> 18 <= val <= 65
        True
        >>> # Enum constraints
        >>> fn = _create_type_aware_random("red | green | blue")
        >>> fn() in ["red", "green", "blue"]
        True
    """
    # Check for enum values first
    enum_values = _extract_enum_values(field_type)
    if enum_values:
        return lambda: random_module.choice(enum_values)

    # Check for range bounds
    min_val, max_val = _extract_range_bounds(field_type)
    if min_val is not None and max_val is not None:
        # Check if bounds are integers
        if isinstance(min_val, float) and min_val.is_integer() and isinstance(max_val, float) and max_val.is_integer():
            # Integer range
            return lambda: random_module.randint(int(min_val), int(max_val))
        else:
            # Float range
            return lambda: random_module.uniform(min_val, max_val)

    # Extract base type for non-constrained types
    base_type = field_type.split("{")[0].strip()

    if base_type == "int":
        # For int without range, use large range
        return lambda: random_module.randint(0, 1000000)
    elif base_type in ("num", "float"):
        # For numeric types, return random float [0, 1)
        return random_module.random
    elif base_type == "str":
        # For strings, return random UUID as string
        return lambda: str(uuid_module.uuid4())
    elif base_type == "bool":
        # For booleans, return random choice
        return lambda: random_module.choice([True, False])
    else:
        # Default: random float
        return random_module.random


# Registry of safe default functions
# Format: name -> (factory_function, requires_field_type)
_SAFE_FUNCTIONS: dict[str, tuple[Callable, bool]] = {
    # Collections (always factories to avoid mutable default trap)
    "list": (list, False),
    "dict": (dict, False),
    "set": (set, False),

    # Time-based
    "now": (datetime.now, False),
    "today": (date.today, False),

    # UUID
    "uuid": (lambda: str(uuid_module.uuid4()), False),
    "uuid4": (lambda: str(uuid_module.uuid4()), False),

    # Random - requires field type for type-aware behavior
    "random": (None, True),  # Special case, handled separately
}

# Functions that accept arguments
_SAFE_FUNCTION_CALLS: dict[str, Callable] = {
    "randint": random_module.randint,
    "choice": random_module.choice,
    "uniform": random_module.uniform,
}


def parse_default_value(
    default_expr: str,
    field_type: str | None = None
) -> tuple[Any, bool]:
    """Parse a default value expression safely.

    Args:
        default_expr: Default expression like "0", "now", "randint(1, 100)"
        field_type: Optional SlimSchema type for type-aware defaults

    Returns:
        (value, is_factory) tuple:
        - value: The value or a callable factory function
        - is_factory: True if value is a callable that should be invoked per-instance

    Raises:
        DefaultValueError: If expression is invalid or unsafe

    Examples:
        >>> parse_default_value("0")
        (0, False)
        >>> parse_default_value("list")
        (<built-in function list>, True)
        >>> val, is_factory = parse_default_value("now")
        >>> is_factory
        True
        >>> parse_default_value("randint(1, 100)")  # doctest: +SKIP
        (<function>, True)
    """
    default_expr = default_expr.strip()

    if not default_expr:
        raise DefaultValueError("Empty default expression")

    # 1. Try literal evaluation first
    try:
        value = _eval_literal(default_expr)
        # Check if mutable - these must be treated as factories
        if isinstance(value, (list, dict, set)):
            # Return a factory that creates a fresh instance
            return (lambda val=value: val.copy() if hasattr(val, 'copy') else list(val) if isinstance(val, (list, set)) else dict(val), True)
        # Immutable literal
        return (value, False)
    except ValueError:
        # Not a literal, continue to function parsing
        pass

    # 2. Check if it's a simple function name (no parens)
    if "(" not in default_expr:
        func_name = default_expr.strip()

        # Special case: type-aware random
        if func_name == "random":
            if field_type is None:
                # No field type, use default random float
                return (random_module.random, True)
            else:
                # Create type-aware random function
                return (_create_type_aware_random(field_type), True)

        # Check registry
        if func_name in _SAFE_FUNCTIONS:
            factory, requires_type = _SAFE_FUNCTIONS[func_name]
            if requires_type and field_type is None:
                raise DefaultValueError(f"Function '{func_name}' requires field type")
            return (factory, True)

        raise DefaultValueError(f"Unknown default function: {func_name}")

    # 3. Parse function call with arguments
    try:
        func_name, args, kwargs = _parse_function_call(default_expr)
    except ValueError as e:
        raise DefaultValueError(str(e)) from e

    # Check if function is allowed
    if func_name not in _SAFE_FUNCTION_CALLS:
        raise DefaultValueError(f"Function '{func_name}' is not allowed in defaults")

    # Create a factory that calls the function with parsed args
    base_func = _SAFE_FUNCTION_CALLS[func_name]

    def factory():
        return base_func(*args, **kwargs)

    return (factory, True)


def evaluate_default(
    default_expr: str,
    field_type: str | None = None
) -> Any:
    """Evaluate a default value expression and return the result.

    This is a convenience function that parses and immediately evaluates
    the default expression.

    Args:
        default_expr: Default expression
        field_type: Optional SlimSchema type

    Returns:
        The evaluated default value

    Examples:
        >>> evaluate_default("42")
        42
        >>> evaluate_default("list")
        []
        >>> isinstance(evaluate_default("now"), datetime)
        True
    """
    value, is_factory = parse_default_value(default_expr, field_type)
    if is_factory:
        return value()
    return value
