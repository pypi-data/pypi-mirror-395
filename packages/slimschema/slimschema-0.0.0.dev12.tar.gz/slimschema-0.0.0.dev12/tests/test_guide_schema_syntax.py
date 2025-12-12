"""Tests for Schema Syntax Guide.

This test module validates all syntax features documented in docs/guide_syntax.md.
Each test corresponds to a specific syntax example in the guide, serving as
executable documentation that proves the syntax works as documented.
"""


from slimschema import to_data
from slimschema.parser import parse_slimschema


class TestBasicTypes:
    """Test parsing of basic primitive types."""

    def test_basic_primitives(self, basic_types_schema):
        """Validate str, int, bool, float types parse correctly."""
        schema = parse_slimschema(basic_types_schema)

        assert len(schema.fields) == 4
        assert schema.fields[0].name == "name"
        assert schema.fields[0].type == "str"
        assert schema.fields[1].name == "age"
        assert schema.fields[1].type == "int"
        assert schema.fields[2].name == "active"
        assert schema.fields[2].type == "bool"
        assert schema.fields[3].name == "score"
        assert schema.fields[3].type == "float"



class TestConstraints:
    """Test constraint syntax (ranges, regex, length)."""

    def test_range_constraint_parsing(self):
        """Validate range constraint syntax: 18..120."""
        schema = parse_slimschema("age: 18..120")

        assert schema.fields[0].type == "18..120"

    def test_string_length_constraint_parsing(self):
        """Validate string length constraint syntax: str{3..20}."""
        schema = parse_slimschema("username: str{3..20}")

        assert schema.fields[0].type == "str{3..20}"

    def test_regex_constraint_parsing(self):
        """Validate regex constraint syntax: /pattern/."""
        schema = parse_slimschema("email: /^[a-z]+@[a-z]+\\.[a-z]+$/")

        assert schema.fields[0].type == "/^[a-z]+@[a-z]+\\.[a-z]+$/"



class TestInlineObjects:
    """Test inline object syntax: {name:str, age:int}."""

    def test_inline_object_with_defaults(self):
        """Validate inline objects with default values."""
        schema = parse_slimschema('config: {theme:str="light", count:int=0}')

        assert schema.fields[0].name == "config"
        assert "theme:str" in schema.fields[0].type
        assert "light" in schema.fields[0].type


class TestDictTypes:
    """Test typed dictionary syntax: dict{key_type, value_type}."""

    def test_dict_sugar_parsing(self):
        """Validate dict{str, int} syntax parses correctly."""
        schema = parse_slimschema("scores: dict{str, int}")

        assert schema.fields[0].name == "scores"
        assert "dict{str,int}" in schema.fields[0].type or "dict{str, int}" in schema.fields[0].type

    def test_dict_with_int_keys(self):
        """Validate dict{int, str} parses correctly."""
        schema = parse_slimschema("indexed: dict{int, str}")

        assert schema.fields[0].name == "indexed"
        assert "int" in schema.fields[0].type

    def test_dict_with_regex_keys(self):
        """Validate dict{/regex/, type} parses correctly."""
        schema = parse_slimschema("metadata: dict{/^[a-z]+$/, str}")

        assert schema.fields[0].name == "metadata"
        assert "dict" in schema.fields[0].type



class TestCollections:
    """Test array and collection syntax."""

    def test_simple_array_parsing(self):
        """Validate list[str] array syntax."""
        schema = parse_slimschema("tags: list[str]")

        assert schema.fields[0].name == "tags"
        assert schema.fields[0].type == "list[str]"

    def test_array_of_ints_parsing(self):
        """Validate [int] array syntax."""
        schema = parse_slimschema("scores: list[int]")

        assert schema.fields[0].type == 'list[int]'

    def test_array_of_objects_parsing(self):
        """Validate [{...}] inline object array syntax."""
        schema = parse_slimschema("items: [{id:int, name:str}]")

        assert schema.fields[0].name == "items"
        assert "[{" in schema.fields[0].type



class TestEnums:
    """Test enum syntax: value1 | value2 | value3."""

    def test_simple_enum_parsing(self):
        """Validate pipe-delimited enum syntax."""
        schema = parse_slimschema("status: active | inactive | pending")

        assert schema.fields[0].type == "active | inactive | pending"

    def test_enum_with_default(self):
        """Validate enum with default value."""
        schema = parse_slimschema('role: admin | user | guest = "guest"')

        assert schema.fields[0].type == "admin | user | guest"
        assert schema.fields[0].default == '"guest"'



class TestOptionalFields:
    """Test optional field syntax: field?."""

    def test_optional_marker_parsing(self):
        """Validate field? syntax marks field as optional."""
        schema = parse_slimschema("?email: str")

        assert schema.fields[0].name == "email"
        assert schema.fields[0].optional is True

    def test_required_field_parsing(self):
        """Validate fields without ? are required."""
        schema = parse_slimschema("email: str")

        assert schema.fields[0].name == "email"
        assert schema.fields[0].optional is False



class TestComments:
    """Test comment and annotation syntax."""

    def test_description_comment_parsing(self):
        """Validate inline comments are parsed as descriptions."""
        schema = parse_slimschema("name: str  # Full name")

        assert schema.fields[0].description == "Full name"
        assert schema.fields[0].annotation is None

    def test_type_annotation_parsing(self):
        """Validate :: annotation syntax (backward compatibility)."""
        # Old syntax still parses (for migration)
        schema = parse_slimschema("tags: list[str]  # Unique tags  :: Set[str]")
        assert schema.fields[0].description == "Unique tags"
        assert schema.fields[0].annotation == "Set[str]"

        # New syntax: use native types directly (recommended)
        schema2 = parse_slimschema("tags: set[str]  # Unique tags")
        assert schema2.fields[0].description == "Unique tags"
        assert schema2.fields[0].annotation is None  # No annotation needed!

    def test_schema_name_parsing(self):
        """Validate # SchemaName at top level."""
        schema = parse_slimschema("# Person\nname: str\nage: int")

        assert schema.name == "Person"
        assert len(schema.fields) == 2


class TestDefaults:
    """Test default value syntax: type = default."""

    def test_scalar_default_parsing(self):
        """Validate scalar default syntax."""
        schema = parse_slimschema("count: int = 0")

        assert schema.fields[0].default == "0"

    def test_boolean_default_parsing(self):
        """Validate boolean default syntax."""
        schema = parse_slimschema("active: bool = true")

        assert schema.fields[0].default == "true"

    def test_boolean_alias(self):
        """Validate 'boolean' as alias for 'bool' (JSON Schema compatibility)."""
        schema_str = "active: boolean"
        data, error = to_data('{"active": true}', schema_str)

        assert error is None
        assert data["active"] is True

    def test_boolean_alias_with_default(self):
        """Validate 'boolean' alias with default value."""
        schema_str = "active: boolean = true"
        data, error = to_data('{}', schema_str)

        assert error is None
        assert data["active"] is True

    def test_nested_boolean_alias(self):
        """Validate 'boolean' alias in nested objects."""
        schema_str = """output:
  did_find_treasure: boolean = true
  message: str"""
        data, error = to_data('{"output": {"did_find_treasure": true, "message": "Found it!"}}', schema_str)

        assert error is None
        assert data["output"]["did_find_treasure"] is True
        assert data["output"]["message"] == "Found it!"

    def test_nested_boolean_alias_with_false(self):
        """Validate 'boolean' alias with false value in nested objects."""
        schema_str = """output:
  did_find_treasure: boolean = false
  message: str"""
        data, error = to_data('{"output": {"did_find_treasure": false, "message": "Not found"}}', schema_str)

        assert error is None
        assert data["output"]["did_find_treasure"] is False
        assert data["output"]["message"] == "Not found"


class TestTypeAliasNormalization:
    """Test type alias normalization for JSON Schema / TypeScript compatibility."""

    def test_string_alias(self):
        """'string' should work as alias for 'str'."""
        schema_str = "value: string"
        data, error = to_data('{"value": "hello"}', schema_str)

        assert error is None
        assert data["value"] == "hello"

    def test_integer_alias(self):
        """'integer' should work as alias for 'int'."""
        schema_str = "value: integer"
        data, error = to_data('{"value": 42}', schema_str)

        assert error is None
        assert data["value"] == 42

    def test_number_alias(self):
        """'number' should work as alias for 'float'."""
        schema_str = "value: number"
        data, error = to_data('{"value": 3.14}', schema_str)

        assert error is None
        assert data["value"] == 3.14

    def test_object_alias(self):
        """'object' should work as alias for 'obj'."""
        schema_str = "value: object"
        data, error = to_data('{"value": {"key": "val"}}', schema_str)

        assert error is None
        assert data["value"] == {"key": "val"}

    def test_alias_normalization_roundtrip(self):
        """Aliases should normalize to canonical forms on round-trip."""
        schema_str = """value: boolean
name: string
count: integer
score: number"""

        schema = parse_slimschema(schema_str)
        regenerated = str(schema)

        # Check that aliases were normalized to canonical forms
        assert "bool" in regenerated
        assert "str" in regenerated
        assert "int" in regenerated
        assert "float" in regenerated

        # Aliases should not appear
        assert "boolean" not in regenerated
        assert "string" not in regenerated
        assert "integer" not in regenerated
        assert "number" not in regenerated

    def test_nested_alias_normalization(self):
        """Nested objects should normalize aliases."""
        schema_str = """output:
  found: boolean
  message: string"""

        schema = parse_slimschema(schema_str)
        regenerated = str(schema)

        # Should normalize to canonical forms
        assert "bool" in regenerated
        assert "str" in regenerated
        assert "boolean" not in regenerated
        assert "string" not in regenerated

    def test_complex_type_aliases(self):
        """Complex types with aliases should normalize."""
        test_cases = [
            ("items: list[string]", "list[str]"),
            ("ids: set[integer]", "set[int]"),
            ("status: boolean | string", "bool | str"),
        ]

        for schema_str, expected in test_cases:
            schema = parse_slimschema(schema_str)
            regenerated = str(schema)
            assert expected in regenerated, f"Expected '{expected}' in '{regenerated}'"

    def test_dict_sugar_alias_normalization(self):
        """Dict sugar should normalize key/value type aliases."""
        schema_str = "config: dict{string, boolean}"
        schema = parse_slimschema(schema_str)
        regenerated = str(schema)

        assert "dict{str, bool}" in regenerated

    def test_all_aliases_validate(self):
        """All type aliases should validate correctly."""
        aliases_data = [
            ("v: boolean", '{"v": true}'),
            ("v: string", '{"v": "x"}'),
            ("v: integer", '{"v": 1}'),
            ("v: number", '{"v": 1.5}'),
            ("v: object", '{"v": {}}'),
        ]

        for schema_str, data_str in aliases_data:
            data, error = to_data(data_str, schema_str)
            assert error is None, f"Failed for {schema_str}: {error}"


class TestAnyType:
    """Test the `any` type that accepts all values."""

    def test_any_type_parsing(self):
        """Validate any type parses correctly."""
        schema = parse_slimschema("value: any")

        assert schema.fields[0].type == "any"

    def test_any_accepts_string(self):
        """Any type should accept strings."""
        schema_str = "value: any"
        data, error = to_data('{"value": "hello"}', schema_str)

        assert error is None
        assert data["value"] == "hello"

    def test_any_accepts_number(self):
        """Any type should accept numbers."""
        schema_str = "value: any"
        data, error = to_data('{"value": 42}', schema_str)

        assert error is None
        assert data["value"] == 42

    def test_any_accepts_bool(self):
        """Any type should accept booleans."""
        schema_str = "value: any"
        data, error = to_data('{"value": true}', schema_str)

        assert error is None
        assert data["value"] is True

    def test_any_accepts_null(self):
        """Any type should accept null."""
        schema_str = "value: any"
        data, error = to_data('{"value": null}', schema_str)

        assert error is None
        assert data["value"] is None

    def test_any_accepts_array(self):
        """Any type should accept arrays."""
        schema_str = "value: any"
        data, error = to_data('{"value": [1, 2, 3]}', schema_str)

        assert error is None
        assert data["value"] == [1, 2, 3]

    def test_any_accepts_object(self):
        """Any type should accept objects."""
        schema_str = "value: any"
        data, error = to_data('{"value": {"key": "value"}}', schema_str)

        assert error is None
        assert data["value"] == {"key": "value"}


class TestUnions:
    """Test inline union types like `str | int`.

    Unions use the pipe operator with ALL parts being reserved types.
    If any part is not a reserved type, it's treated as an Enum instead.
    """

    def test_union_parsing(self):
        """Validate union syntax parses correctly."""
        schema = parse_slimschema("value: str | int")

        assert schema.fields[0].type == "str | int"

    def test_str_or_int_union(self):
        """Union of str | int should accept both."""
        schema_str = "value: str | int"

        # Should accept string
        data, error = to_data('{"value": "hello"}', schema_str)
        assert error is None
        assert data["value"] == "hello"

        # Should accept int
        data, error = to_data('{"value": 42}', schema_str)
        assert error is None
        assert data["value"] == 42

        # Should reject float (not in union)
        data, error = to_data('{"value": 3.14}', schema_str)
        assert error is not None

    def test_int_or_float_union(self):
        """Union of int | float should accept both."""
        schema_str = "value: int | float"

        # Should accept int
        data, error = to_data('{"value": 42}', schema_str)
        assert error is None
        assert data["value"] == 42

        # Should accept float
        data, error = to_data('{"value": 3.14}', schema_str)
        assert error is None
        assert data["value"] == 3.14

        # Should reject string
        data, error = to_data('{"value": "hello"}', schema_str)
        assert error is not None

    def test_three_way_union(self):
        """Union of str | int | bool should accept all three."""
        schema_str = "value: str | int | bool"

        data, error = to_data('{"value": "hello"}', schema_str)
        assert error is None

        data, error = to_data('{"value": 42}', schema_str)
        assert error is None

        data, error = to_data('{"value": true}', schema_str)
        assert error is None

    def test_format_union(self):
        """Union of format types creates Union type."""
        from slimschema.types import to_msgspec_type

        result_type = to_msgspec_type("email | url")
        # Should create a Union, not a Literal
        assert "Union" in str(result_type) or "|" in str(result_type)


class TestEnumAdvanced:
    """Test advanced enum features including quoted values.

    Enums are detected when at least one part is NOT a reserved type.
    Quoted strings in enums allow literal type keywords as enum values.
    """

    def test_simple_enum_validation(self):
        """Enum of active | inactive should only accept those values."""
        schema_str = "status: active | inactive"

        # Should accept "active"
        data, error = to_data('{"status": "active"}', schema_str)
        assert error is None
        assert data["status"] == "active"

        # Should accept "inactive"
        data, error = to_data('{"status": "inactive"}', schema_str)
        assert error is None
        assert data["status"] == "inactive"

        # Should reject other values
        data, error = to_data('{"status": "pending"}', schema_str)
        assert error is not None

    def test_three_value_enum(self):
        """Enum with three values."""
        schema_str = "priority: low | medium | high"

        data, error = to_data('{"priority": "low"}', schema_str)
        assert error is None

        data, error = to_data('{"priority": "medium"}', schema_str)
        assert error is None

        data, error = to_data('{"priority": "high"}', schema_str)
        assert error is None

        data, error = to_data('{"priority": "critical"}', schema_str)
        assert error is not None

    def test_quoted_enum_values(self):
        """Quoted strings in enums allow using type keywords as literals."""
        # In YAML, wrap the whole value in single quotes to preserve double quotes
        schema_str = '''status: '"str" | "int" | "bool"' '''

        # Should accept the literal strings
        data, error = to_data('{"status": "str"}', schema_str)
        assert error is None
        assert data["status"] == "str"

        data, error = to_data('{"status": "int"}', schema_str)
        assert error is None
        assert data["status"] == "int"

        data, error = to_data('{"status": "bool"}', schema_str)
        assert error is None
        assert data["status"] == "bool"

    def test_mixed_detection_is_enum(self):
        """Mixed reserved and non-reserved creates Enum, not Union.

        Important edge case: str | custom creates Literal["str", "custom"]
        because "custom" is not a reserved type.
        """
        from slimschema.types import to_msgspec_type

        # Not all reserved → Enum
        result_type = to_msgspec_type("str | custom")
        assert "Literal" in str(result_type)


class TestTypeAliases:
    """Test type aliases: dict and num."""

    def test_dict_alias_parsing(self):
        """dict should work as an alias for obj."""
        schema = parse_slimschema("metadata: dict")

        assert schema.fields[0].type == "dict"

    def test_dict_alias_validation(self):
        """dict alias should accept objects."""
        schema_str = "metadata: dict"

        # Should accept object
        data, error = to_data('{"metadata": {"key": "value"}}', schema_str)
        assert error is None
        assert data["metadata"] == {"key": "value"}

    def test_num_alias_parsing(self):
        """num should work as an alias for float."""
        schema = parse_slimschema("value: num")

        assert schema.fields[0].type == "num"

    def test_num_alias_validation(self):
        """num alias should accept numbers."""
        schema_str = "value: num"

        # Should accept int
        data, error = to_data('{"value": 42}', schema_str)
        assert error is None
        assert data["value"] == 42

        # Should accept float
        data, error = to_data('{"value": 3.14}', schema_str)
        assert error is None
        assert data["value"] == 3.14


class TestReservedTypeDetection:
    """Test the is_reserved_type() helper function (internal API)."""

    def test_primitives_are_reserved(self):
        """Primitive types should be reserved."""
        from slimschema.types import is_reserved_type

        assert is_reserved_type("str") is True
        assert is_reserved_type("int") is True
        assert is_reserved_type("float") is True
        assert is_reserved_type("bool") is True
        assert is_reserved_type("obj") is True
        assert is_reserved_type("any") is True
        assert is_reserved_type("dict") is True
        assert is_reserved_type("num") is True

    def test_formats_are_reserved(self):
        """Format types should be reserved."""
        from slimschema.types import is_reserved_type

        assert is_reserved_type("email") is True
        assert is_reserved_type("url") is True
        assert is_reserved_type("uuid") is True
        assert is_reserved_type("date") is True
        assert is_reserved_type("datetime") is True

    def test_constraints_are_reserved(self):
        """Constraint patterns should be reserved."""
        from slimschema.types import is_reserved_type

        assert is_reserved_type("1..10") is True
        assert is_reserved_type("0.0..1.0") is True
        assert is_reserved_type("str{3..10}") is True
        assert is_reserved_type("/^[A-Z]+$/") is True
        assert is_reserved_type("list[str]") is True

    def test_literals_are_not_reserved(self):
        """Literal values should not be reserved."""
        from slimschema.types import is_reserved_type

        assert is_reserved_type("active") is False
        assert is_reserved_type("inactive") is False
        assert is_reserved_type("pending") is False
        assert is_reserved_type("foo") is False

    def test_quoted_strings_are_not_reserved(self):
        """Quoted strings should never be reserved."""
        from slimschema.types import is_reserved_type

        assert is_reserved_type('"str"') is False
        assert is_reserved_type("'int'") is False
        assert is_reserved_type('"email"') is False
        assert is_reserved_type('"active"') is False


class TestNativeTypeSyntax:
    """Test native Python type syntax (set, tuple, frozenset)."""

    def test_set_syntax(self):
        """Test set[type] syntax."""
        schema = parse_slimschema("ids: set[int]")

        assert schema.fields[0].name == "ids"
        assert schema.fields[0].type == "set[int]"

    def test_frozenset_syntax(self):
        """Test frozenset[type] syntax."""
        schema = parse_slimschema("constants: frozenset[str]")

        assert schema.fields[0].name == "constants"
        assert schema.fields[0].type == "frozenset[str]"

    def test_tuple_fixed_length(self):
        """Test tuple[type1, type2] syntax."""
        schema = parse_slimschema("coords: tuple[float, float]")

        assert schema.fields[0].name == "coords"
        assert schema.fields[0].type == "tuple[float, float]"

    def test_tuple_three_elements(self):
        """Test tuple with 3 elements."""
        schema = parse_slimschema("rgb: tuple[int, int, int]")

        assert schema.fields[0].name == "rgb"
        assert schema.fields[0].type == "tuple[int, int, int]"

    def test_tuple_variable_length(self):
        """Test tuple[type, ...] syntax."""
        schema = parse_slimschema("path: tuple[int, ...]")

        assert schema.fields[0].name == "path"
        assert schema.fields[0].type == "tuple[int, ...]"

    def test_nested_with_set(self):
        """Test list of sets."""
        schema = parse_slimschema("groups: list[set[int]]")

        assert schema.fields[0].type == "list[set[int]]"
