"""Tests for msgspec Integration.

This test module validates msgspec integration features documented in
docs/integration_msgspec.md. Tests cover round-trip conversion between
msgspec Structs and SlimSchema YAML, focusing on high-performance validation.
"""

import pytest

msgspec = pytest.importorskip("msgspec")

from slimschema import to_schema  # noqa: E402


class TestMsgspecToSchema:
    """Test converting msgspec Structs to SlimSchema YAML."""

    def test_basic_struct_to_schema(self):
        """Convert basic msgspec Struct to schema."""

        class User(msgspec.Struct):
            name: str
            age: int

        schema = to_schema(User)

        assert schema.name == "User"
        assert len(schema.fields) == 2
        assert {f.name for f in schema.fields} == {"name", "age"}



class TestMsgspecListFields:
    """Test msgspec Structs with list fields."""

    def test_list_field_to_schema(self):
        """Convert list fields to array syntax."""

        class User(msgspec.Struct):
            name: str
            tags: list[str]

        schema = to_schema(User)

        tags_field = next(f for f in schema.fields if f.name == "tags")
        assert "[" in tags_field.type and "]" in tags_field.type


class TestMsgspecSchemaName:
    """Test schema name preservation."""

    def test_schema_name_from_struct(self):
        """Schema name is taken from Struct class name."""

        class UserAccount(msgspec.Struct):
            name: str

        schema = to_schema(UserAccount)

        assert schema.name == "UserAccount"


class TestMsgspecToYaml:
    """Test YAML generation from msgspec Structs."""

    def test_generate_yaml_from_struct(self):
        """Generate YAML string from msgspec Struct."""

        class User(msgspec.Struct):
            name: str
            age: int

        schema = to_schema(User)
        yaml_str = str(schema)

        assert "# User" in yaml_str or "User" in yaml_str
        assert "name: str" in yaml_str
        assert "age: int" in yaml_str
