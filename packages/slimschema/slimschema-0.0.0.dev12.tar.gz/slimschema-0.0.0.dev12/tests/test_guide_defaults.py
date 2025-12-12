"""Tests for default value behavior - corresponds to guide_defaults.md.

This test module covers:
- Default value parsing (literals, functions, factories)
- Schema-aware defaults (range-aware, enum-aware)
- Top-level defaults (field: type = value)
- Nested defaults (recursive application in inline objects)
- Integration with Pydantic and msgspec
- Factory defaults (avoiding mutable default trap)
"""

import json
from datetime import date, datetime

import msgspec
import pytest

from slimschema import (
    DefaultValueError,
    to_data,
    to_msgspec,
    to_prompt,
    to_pydantic,
    to_schema,
    to_yaml,
)
from slimschema.defaults import parse_default_value


class TestDefaultValueParsing:
    """Test parsing of default value expressions."""

    def test_literal_int(self):
        """Integer literals are parsed correctly."""
        value, is_factory = parse_default_value("42")
        assert value == 42
        assert is_factory is False

    def test_literal_float(self):
        """Float literals are parsed correctly."""
        value, is_factory = parse_default_value("3.14")
        assert value == 3.14
        assert is_factory is False

    def test_literal_string(self):
        """String literals are parsed correctly."""
        value, is_factory = parse_default_value('"hello"')
        assert value == "hello"
        assert is_factory is False

    def test_literal_bool_true(self):
        """Boolean true literal."""
        value, is_factory = parse_default_value("True")
        assert value is True
        assert is_factory is False

    def test_literal_bool_false(self):
        """Boolean false literal."""
        value, is_factory = parse_default_value("False")
        assert value is False
        assert is_factory is False

    def test_literal_none(self):
        """None literal."""
        value, is_factory = parse_default_value("None")
        assert value is None
        assert is_factory is False

    def test_yaml_bool_true(self):
        """YAML-style boolean true."""
        value, is_factory = parse_default_value("true")
        assert value is True
        assert is_factory is False

    def test_yaml_bool_false(self):
        """YAML-style boolean false."""
        value, is_factory = parse_default_value("false")
        assert value is False
        assert is_factory is False

    def test_yaml_null(self):
        """YAML-style null."""
        value, is_factory = parse_default_value("null")
        assert value is None
        assert is_factory is False


class TestFactoryDefaults:
    """Factory defaults avoid the mutable default trap."""

    def test_empty_list_is_factory(self):
        """Empty list literal becomes a factory."""
        value, is_factory = parse_default_value("[]")
        assert is_factory is True
        # Each call returns a new list
        list1 = value()
        list2 = value()
        assert list1 == []
        assert list2 == []
        assert list1 is not list2

    def test_empty_dict_is_factory(self):
        """Empty dict literal becomes a factory."""
        value, is_factory = parse_default_value("{}")
        assert is_factory is True
        dict1 = value()
        dict2 = value()
        assert dict1 == {}
        assert dict2 == {}
        assert dict1 is not dict2

    def test_list_function(self):
        """'list' keyword creates factory."""
        value, is_factory = parse_default_value("list")
        assert is_factory is True
        assert callable(value)
        assert value() == []

    def test_dict_function(self):
        """'dict' keyword creates factory."""
        value, is_factory = parse_default_value("dict")
        assert is_factory is True
        assert callable(value)
        assert value() == {}

    def test_set_function(self):
        """'set' keyword creates factory."""
        value, is_factory = parse_default_value("set")
        assert is_factory is True
        assert callable(value)
        assert value() == set()

    def test_now_function(self):
        """'now' creates datetime factory."""
        value, is_factory = parse_default_value("now")
        assert is_factory is True
        result = value()
        assert isinstance(result, datetime)

    def test_today_function(self):
        """'today' creates date factory."""
        value, is_factory = parse_default_value("today")
        assert is_factory is True
        result = value()
        assert isinstance(result, date)

    def test_uuid_function(self):
        """'uuid' creates UUID factory."""
        value, is_factory = parse_default_value("uuid")
        assert is_factory is True
        result = value()
        assert isinstance(result, str)
        assert len(result) == 36  # UUID format

    def test_uuid4_function(self):
        """'uuid4' creates UUID factory."""
        value, is_factory = parse_default_value("uuid4")
        assert is_factory is True
        result = value()
        assert isinstance(result, str)
        assert len(result) == 36


class TestSchemaAwareDefaults:
    """Defaults can be aware of the field's type constraints."""

    def test_random_with_int_range(self):
        """'random' uses range constraints for int."""
        value, is_factory = parse_default_value("random", field_type="18..65")
        assert is_factory is True
        # Test multiple times to ensure it stays in range
        for _ in range(10):
            result = value()
            assert isinstance(result, int)
            assert 18 <= result <= 65

    def test_random_with_float_range(self):
        """'random' uses range constraints for float."""
        value, is_factory = parse_default_value("random", field_type="-10.5..35.2")
        assert is_factory is True
        for _ in range(10):
            result = value()
            assert isinstance(result, float)
            assert -10.5 <= result <= 35.2

    def test_random_with_enum(self):
        """'random' picks from enum values."""
        value, is_factory = parse_default_value("random", field_type="red | green | blue")
        assert is_factory is True
        for _ in range(10):
            result = value()
            assert result in ["red", "green", "blue"]

    def test_random_with_str_type(self):
        """'random' generates UUID for str type."""
        value, is_factory = parse_default_value("random", field_type="str")
        assert is_factory is True
        result = value()
        assert isinstance(result, str)
        assert len(result) == 36  # UUID length

    def test_random_with_bool_type(self):
        """'random' generates random bool."""
        value, is_factory = parse_default_value("random", field_type="bool")
        assert is_factory is True
        result = value()
        assert isinstance(result, bool)

    def test_randint_function(self):
        """'randint(min, max)' function call."""
        value, is_factory = parse_default_value("randint(1, 100)")
        assert is_factory is True
        result = value()
        assert isinstance(result, int)
        assert 1 <= result <= 100

    def test_uniform_function(self):
        """'uniform(min, max)' function call."""
        value, is_factory = parse_default_value("uniform(0.0, 1.0)")
        assert is_factory is True
        result = value()
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_choice_function(self):
        """'choice([...])' function call."""
        value, is_factory = parse_default_value('choice(["a", "b", "c"])')
        assert is_factory is True
        result = value()
        assert result in ["a", "b", "c"]


class TestDefaultValidation:
    """Invalid defaults should raise errors."""

    def test_invalid_function_raises(self):
        """Disallowed functions raise error."""
        with pytest.raises(DefaultValueError, match="not allowed"):
            parse_default_value("exec('malicious code')")

    def test_invalid_expression_raises(self):
        """Invalid expressions raise error."""
        with pytest.raises(DefaultValueError):
            parse_default_value("1 + 1")  # Not a literal or function

    def test_empty_expression_raises(self):
        """Empty expression raises error."""
        with pytest.raises(DefaultValueError, match="Empty"):
            parse_default_value("")


class TestSchemaParsingWithDefaults:
    """Schema parsing should preserve default values."""

    def test_parse_int_default(self):
        """Int default is preserved."""
        schema = to_schema("age: int = 18")
        assert len(schema.fields) == 1
        field = schema.fields[0]
        assert field.name == "age"
        assert field.type == "int"
        assert field.default == "18"

    def test_parse_string_default(self):
        """String default is preserved."""
        schema = to_schema('name: str = "Unknown"')
        field = schema.fields[0]
        assert field.default == '"Unknown"'

    def test_parse_function_default(self):
        """Function default is preserved."""
        schema = to_schema("created: datetime = now")
        field = schema.fields[0]
        assert field.default == "now"

    def test_parse_multiple_defaults(self):
        """Multiple defaults are preserved."""
        yaml = """
name: str = "Unknown"
age: int = 0
tags: list[str] = list
created: datetime = now
"""
        schema = to_schema(yaml)
        assert len(schema.fields) == 4
        assert schema.fields[0].default == '"Unknown"'
        assert schema.fields[1].default == "0"
        assert schema.fields[2].default == "list"
        assert schema.fields[3].default == "now"

    def test_parse_optional_with_default(self):
        """Optional fields can have defaults."""
        schema = to_schema("?email: str = ''")
        field = schema.fields[0]
        assert field.optional is True
        assert field.default == "''"


class TestYamlGenerationWithDefaults:
    """YAML generation should preserve or hide defaults as requested."""

    def test_generate_with_defaults_shown(self):
        """Defaults shown when show_defaults=True."""
        schema = to_schema("age: int = 18")
        yaml = to_yaml(schema, show_defaults=True)
        assert "age: int = 18" in yaml

    def test_generate_with_defaults_hidden(self):
        """Defaults hidden when show_defaults=False."""
        schema = to_schema("age: int = 18")
        yaml = to_yaml(schema, show_defaults=False)
        assert yaml == "age: int"

    def test_roundtrip_preserves_defaults(self):
        """Parse -> generate -> parse preserves defaults."""
        original = "name: str = 'test'\nage: int = 0"
        schema1 = to_schema(original)
        yaml = to_yaml(schema1, show_defaults=True)
        schema2 = to_schema(yaml)

        assert len(schema2.fields) == 2
        assert schema2.fields[0].default == "'test'"
        assert schema2.fields[1].default == "0"


class TestPromptGenerationWithDefaults:
    """Prompts should hide defaults by default (save tokens)."""

    def test_prompt_hides_defaults_by_default(self):
        """Defaults not shown in prompt by default."""
        prompt = to_prompt("age: int = 18")
        assert "= 18" not in prompt
        assert "age: int" in prompt

    def test_prompt_shows_defaults_when_requested(self):
        """Defaults shown when show_defaults=True."""
        prompt = to_prompt("age: int = 18", show_defaults=True)
        assert "age: int = 18" in prompt


class TestTopLevelDefaults:
    """Top-level field defaults are applied during validation."""

    def test_apply_int_default(self):
        """Int defaults applied to missing fields."""
        schema = "name: str\nage: int = 18"
        data, error = to_data('{"name": "Alice"}', schema)

        assert error is None
        assert data["name"] == "Alice"
        assert data["age"] == 18

    def test_apply_string_default(self):
        """String defaults applied."""
        schema = 'status: str = "pending"'
        data, error = to_data("{}", schema)

        assert error is None
        assert data["status"] == "pending"

    def test_apply_list_default(self):
        """List defaults applied."""
        schema = 'tags: list[str] = list'
        data, error = to_data("{}", schema)

        assert error is None
        assert data["tags"] == []

    def test_apply_dict_default(self):
        """Dict defaults applied."""
        schema = "metadata: obj = dict"
        data, error = to_data("{}", schema)

        assert error is None
        assert data["metadata"] == {}

    def test_apply_datetime_default(self):
        """Datetime defaults applied."""
        schema = "created: datetime = now"
        data, error = to_data("{}", schema)

        assert error is None
        assert isinstance(data["created"], str)  # Datetime is serialized

    def test_apply_uuid_default(self):
        """UUID defaults applied."""
        schema = "id: str = uuid"
        data, error = to_data("{}", schema)

        assert error is None
        assert isinstance(data["id"], str)
        assert len(data["id"]) == 36

    def test_apply_yaml_bool_defaults(self):
        """YAML boolean literals work as defaults."""
        schema = "active: bool = true\ndeleted: bool = false"
        data, error = to_data("{}", schema)

        assert error is None
        assert data["active"] is True
        assert data["deleted"] is False

    def test_provided_value_overrides_default(self):
        """Provided values override defaults."""
        schema = "age: int = 18"
        data, error = to_data('{"age": 25}', schema)

        assert error is None
        assert data["age"] == 25  # Not 18

    def test_multiple_defaults_applied(self):
        """Multiple defaults applied together."""
        schema = """
name: str = "Unknown"
age: int = 0
tags: list[str] = list
"""
        data, error = to_data("{}", schema)

        assert error is None
        assert data["name"] == "Unknown"
        assert data["age"] == 0
        assert data["tags"] == []


class TestNestedDefaults:
    """CRITICAL: Defaults in inline objects must be applied recursively."""

    def test_nested_scalar_defaults(self):
        """Scalar defaults in nested objects are applied."""
        yaml = """
config:
  timeout: int = 30
  retries: int = 3
"""
        data, error = to_data('{"config": {}}', yaml)
        assert error is None
        assert data["config"]["timeout"] == 30
        assert data["config"]["retries"] == 3

    def test_nested_defaults_with_partial_data(self):
        """Some nested values provided, others use defaults."""
        yaml = """
config:
  timeout: int = 30
  retries: int = 3
"""
        data, error = to_data('{"config": {"timeout": 60}}', yaml)
        assert error is None
        assert data["config"]["timeout"] == 60  # Provided
        assert data["config"]["retries"] == 3   # Default

    def test_nested_factory_defaults(self):
        """Factory defaults in nested objects work correctly."""
        yaml = """
config:
  tags: list[str] = list
  metadata: obj = dict
"""
        data, error = to_data('{"config": {}}', yaml)
        assert error is None
        assert data["config"]["tags"] == []
        assert data["config"]["metadata"] == {}

    def test_nested_regex_with_defaults(self):
        """Regex fields with defaults in nested objects."""
        yaml = """
state:
  secret: /^[A-Z]{3}$/ = "DEF"
"""
        data, error = to_data('{"state": {}}', yaml)
        assert error is None
        assert data["state"]["secret"] == "DEF"

    def test_complex_nested_defaults_scenario(self):
        """Complex real-world nested defaults scenario."""
        yaml = """
workflow_:
  board: /^[A-Z-]{4,9}$/ = "U-REPLACE"
  count: int = 6
  guesses: list[/^[A-Z]$/] = list
guesser:
evaluator:
  secret: /^[A-Z]{4,9}$/ = "UNDEFINED"
  tracking: dict{/^[1-9]$/, /^[A-Z-]$/} = dict
"""
        profiles = ["guesser", "evaluator", "workflow_"]
        default = {name: {} for name in profiles}

        data, error = to_data(json.dumps(default), yaml)
        assert error is None
        assert data["workflow_"]["board"] == "U-REPLACE"
        assert data["workflow_"]["count"] == 6
        assert data["workflow_"]["guesses"] == []
        assert data["evaluator"]["secret"] == "UNDEFINED"
        assert data["evaluator"]["tracking"] == {}


class TestPydanticIntegrationWithDefaults:
    """Pydantic models should respect defaults."""

    def test_pydantic_int_default(self):
        """Pydantic model applies int default."""
        model = to_pydantic("name: str\nage: int = 18")
        instance = model(name="Alice")

        assert instance.name == "Alice"
        assert instance.age == 18

    def test_pydantic_string_default(self):
        """Pydantic model applies string default."""
        model = to_pydantic('status: str = "pending"')
        instance = model()

        assert instance.status == "pending"

    def test_pydantic_list_default_no_mutable_trap(self):
        """Pydantic list defaults avoid mutable default trap."""
        model = to_pydantic('tags: list[str] = list')
        instance1 = model()
        instance2 = model()

        # Verify no mutable default trap
        instance1.tags.append("test")
        assert len(instance1.tags) == 1
        assert len(instance2.tags) == 0

    def test_pydantic_dict_default_no_mutable_trap(self):
        """Pydantic dict defaults avoid mutable default trap."""
        model = to_pydantic("metadata: obj = dict")
        instance1 = model()
        instance2 = model()

        instance1.metadata["key"] = "value"
        assert "key" in instance1.metadata
        assert "key" not in instance2.metadata

    def test_pydantic_now_default(self):
        """Pydantic model applies datetime.now default."""
        model = to_pydantic("created: datetime = now")
        instance = model()

        assert isinstance(instance.created, datetime)

    def test_pydantic_uuid_default(self):
        """Pydantic model applies UUID default."""
        model = to_pydantic("id: str = uuid")
        instance = model()

        assert isinstance(instance.id, str)
        assert len(instance.id) == 36

    def test_pydantic_range_aware_random(self):
        """Pydantic models use range-aware random."""
        model = to_pydantic("age: 18..65 = random")
        instance = model()

        assert isinstance(instance.age, int)
        assert 18 <= instance.age <= 65

    def test_pydantic_enum_aware_random(self):
        """Pydantic models use enum-aware random."""
        model = to_pydantic("color: red | green | blue = random")
        instance = model()

        assert instance.color in ["red", "green", "blue"]

    def test_pydantic_nested_defaults(self):
        """Pydantic models apply nested defaults correctly."""
        yaml = """
config:
  timeout: int = 30
  retries: int = 3
"""
        model = to_pydantic(yaml)
        instance = model(config={})

        assert instance.config.timeout == 30
        assert instance.config.retries == 3

    def test_pydantic_complex_nested_defaults(self):
        """Pydantic models match to_data behavior for nested defaults."""
        yaml = """
workflow_:
  board: /^[A-Z-]{4,9}$/ = "U-REPLACE"
  count: int = 6
  guesses: list[/^[A-Z]$/] = list
guesser:
evaluator:
  secret: /^[A-Z]{4,9}$/ = "UNDEFINED"
  tracking: dict{/^[1-9]$/, /^[A-Z-]$/} = dict
"""
        profiles = ["guesser", "evaluator", "workflow_"]
        default = {name: {} for name in profiles}

        # to_data result
        state, error = to_data(json.dumps(default), yaml)
        assert error is None

        # Pydantic result
        model = to_pydantic(yaml)
        instance = model(**default)
        dumped = instance.model_dump()

        # Should match exactly
        assert dumped == state


class TestMsgspecIntegrationWithDefaults:
    """msgspec Structs should respect defaults."""

    def test_msgspec_int_default(self):
        """msgspec Struct applies int default."""
        struct = to_msgspec("name: str\nage: int = 18")
        instance = msgspec.convert({"name": "Alice"}, type=struct)

        assert instance.name == "Alice"
        assert instance.age == 18

    def test_msgspec_string_default(self):
        """msgspec Struct applies string default."""
        struct = to_msgspec('status: str = "pending"')
        instance = msgspec.convert({}, type=struct)

        assert instance.status == "pending"

    def test_msgspec_list_default(self):
        """msgspec Struct applies list default."""
        struct = to_msgspec('tags: list[str] = list')
        instance = msgspec.convert({}, type=struct)

        assert instance.tags == []

    def test_msgspec_dict_default(self):
        """msgspec Struct applies dict default."""
        struct = to_msgspec("metadata: obj = dict")
        instance = msgspec.convert({}, type=struct)

        assert instance.metadata == {}

    def test_msgspec_now_default(self):
        """msgspec Struct applies datetime.now default."""
        struct = to_msgspec("created: datetime = now")
        instance = msgspec.convert({}, type=struct)

        # datetime defaults are converted to ISO string for msgspec
        assert isinstance(instance.created, str)
        datetime.fromisoformat(instance.created)  # Verify valid ISO format

    def test_msgspec_today_default(self):
        """msgspec Struct applies date.today default."""
        struct = to_msgspec("birthday: date = today")
        instance = msgspec.convert({}, type=struct)

        # date defaults are converted to ISO string for msgspec
        assert isinstance(instance.birthday, str)
        date.fromisoformat(instance.birthday)  # Verify valid ISO format

    def test_msgspec_uuid_default(self):
        """msgspec Struct applies UUID default."""
        struct = to_msgspec("id: str = uuid")
        instance = msgspec.convert({}, type=struct)

        assert isinstance(instance.id, str)
        assert len(instance.id) == 36

    def test_msgspec_range_aware_random(self):
        """msgspec Structs use range-aware random."""
        struct = to_msgspec("age: 18..65 = random")
        instance = msgspec.convert({}, type=struct)

        assert isinstance(instance.age, int)
        assert 18 <= instance.age <= 65

    def test_msgspec_enum_aware_random(self):
        """msgspec Structs use enum-aware random."""
        struct = to_msgspec("status: active | inactive = random")
        instance = msgspec.convert({}, type=struct)

        assert instance.status in ["active", "inactive"]

    def test_msgspec_nested_defaults(self):
        """msgspec Structs apply nested defaults correctly."""
        yaml = """
config:
  timeout: int = 30
  retries: int = 3
"""
        struct = to_msgspec(yaml)
        instance = msgspec.convert({"config": {}}, type=struct)

        assert instance.config.timeout == 30
        assert instance.config.retries == 3

    def test_msgspec_complex_nested_defaults(self):
        """msgspec Structs match to_data behavior for nested defaults."""
        yaml = """
workflow_:
  board: /^[A-Z-]{4,9}$/ = "U-REPLACE"
  count: int = 6
  guesses: list[/^[A-Z]$/] = list
guesser:
evaluator:
  secret: /^[A-Z]{4,9}$/ = "UNDEFINED"
  tracking: dict{/^[1-9]$/, /^[A-Z-]$/} = dict
"""
        profiles = ["guesser", "evaluator", "workflow_"]
        default = {name: {} for name in profiles}

        # to_data result
        state, error = to_data(json.dumps(default), yaml)
        assert error is None

        # msgspec result
        struct = to_msgspec(yaml)
        instance = msgspec.convert(default, type=struct)
        builtins = msgspec.to_builtins(instance)

        # Should match exactly
        assert builtins == state


class TestSchemaAwareDefaultsInValidation:
    """Schema-aware defaults work in to_data validation."""

    def test_range_aware_random_int(self):
        """Random uses range constraints from schema."""
        schema = "age: 18..65 = random"
        data, error = to_data("{}", schema)

        assert error is None
        assert isinstance(data["age"], int)
        assert 18 <= data["age"] <= 65

    def test_range_aware_random_float(self):
        """Random uses float range constraints."""
        schema = "temperature: -10.5..35.2 = random"
        data, error = to_data("{}", schema)

        assert error is None
        assert isinstance(data["temperature"], (int, float))
        assert -10.5 <= data["temperature"] <= 35.2

    def test_enum_aware_random(self):
        """Random picks from enum values."""
        schema = "pick: red | green | blue = random"

        # Test multiple times to ensure it's always valid
        for _ in range(10):
            data, error = to_data("{}", schema)
            assert error is None
            assert data["pick"] in ["red", "green", "blue"]

    def test_explicit_enum_default(self):
        """Explicit enum value as default."""
        schema = 'status: active | inactive | pending = "active"'
        data, error = to_data("{}", schema)

        assert error is None
        assert data["status"] == "active"

    def test_multiple_schema_aware_defaults(self):
        """Multiple fields with schema-aware defaults."""
        schema = """
name: str
age: 18..65 = random
status: active | inactive | pending = random
score: 0.0..100.0 = random
"""
        data, error = to_data('{"name": "Alice"}', schema)

        assert error is None
        assert data["name"] == "Alice"
        assert 18 <= data["age"] <= 65
        assert data["status"] in ["active", "inactive", "pending"]
        assert 0.0 <= data["score"] <= 100.0
