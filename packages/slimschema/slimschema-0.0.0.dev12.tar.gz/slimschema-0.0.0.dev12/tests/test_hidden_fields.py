"""Tests for system-managed fields feature (@ suffix)."""


from slimschema import Field, Schema, to_data, to_prompt, to_schema, to_yaml


class TestHiddenFieldParsing:
    """Test parsing of system-managed fields with @ suffix."""

    def test_parse_hidden_field(self):
        """Fields ending with @ are parsed as system-managed."""
        schema = to_schema("_id: str")

        assert len(schema.fields) == 1
        assert schema.fields[0].name == "id"
        assert schema.fields[0].hidden is True
        assert schema.fields[0].optional is False

    def test_parse_hidden_with_default(self):
        """Hidden fields can have defaults."""
        schema = to_schema("_id: str = uuid")

        assert schema.fields[0].name == "id"
        assert schema.fields[0].hidden is True
        assert schema.fields[0].default == "uuid"

    def test_parse_hidden_with_comment(self):
        """Hidden fields preserve comments."""
        schema = to_schema("_created: datetime = now  # Auto-generated timestamp")

        assert schema.fields[0].name == "created"
        assert schema.fields[0].hidden is True
        assert schema.fields[0].description == "Auto-generated timestamp"

    def test_parse_mixed_fields(self):
        """Parse schema with regular, optional, and hidden fields."""
        yaml = """
_id: str = uuid
_created: datetime = now
name: str
?email: email
"""
        schema = to_schema(yaml)

        assert len(schema.fields) == 4
        assert schema.fields[0].name == "id"
        assert schema.fields[0].hidden is True
        assert schema.fields[1].name == "created"
        assert schema.fields[1].hidden is True
        assert schema.fields[2].name == "name"
        assert schema.fields[2].hidden is False
        assert schema.fields[2].optional is False
        assert schema.fields[3].name == "email"
        assert schema.fields[3].optional is True
        assert schema.fields[3].hidden is False


class TestHiddenFieldGeneration:
    """Test generation of YAML with hidden fields."""

    def test_generate_with_hidden_shown(self):
        """Hidden fields shown when show_hidden=True."""
        schema = Schema(fields=[
            Field(name="id", type="str", hidden=True, default="uuid"),
            Field(name="name", type="str"),
        ])

        yaml = to_yaml(schema, show_hidden=True)

        assert "_id: str = uuid" in yaml
        assert "name: str" in yaml

    def test_generate_with_hidden_concealed(self):
        """Hidden fields concealed when show_hidden=False."""
        schema = Schema(fields=[
            Field(name="id", type="str", hidden=True, default="uuid"),
            Field(name="name", type="str"),
        ])

        yaml = to_yaml(schema, show_hidden=False)

        assert "id" not in yaml
        assert "name: str" in yaml

    def test_roundtrip_hidden_fields(self):
        """Hidden fields roundtrip correctly."""
        original = """
_id: str = uuid
_created: datetime = now
name: str
"""
        schema1 = to_schema(original)
        yaml = to_yaml(schema1, show_defaults=True, show_hidden=True)
        schema2 = to_schema(yaml)

        assert len(schema2.fields) == 3
        assert schema2.fields[0].name == "id"
        assert schema2.fields[0].hidden is True
        assert schema2.fields[0].default == "uuid"
        assert schema2.fields[1].name == "created"
        assert schema2.fields[1].hidden is True


class TestHiddenFieldsInPrompts:
    """Test hidden fields in LLM prompts."""

    def test_prompt_hides_hidden_fields_by_default(self):
        """Hidden fields not included in prompts by default."""
        yaml = """
_id: str = uuid
_created: datetime = now
name: str
?email: email
"""
        prompt = to_prompt(yaml)

        # Hidden fields should NOT appear in prompt
        assert "id" not in prompt
        assert "created" not in prompt
        # Regular fields should appear
        assert "name: str" in prompt
        assert "?email: email" in prompt

    def test_prompt_shows_hidden_when_requested(self):
        """Hidden fields shown in prompts when show_hidden=True."""
        yaml = """
_id: str = uuid
name: str
"""
        prompt = to_prompt(yaml, show_hidden=True)

        # Hidden field should appear when show_hidden=True
        assert "_id: str" in prompt
        assert "name: str" in prompt

    def test_prompt_hides_defaults_and_hidden(self):
        """Prompts hide both defaults and hidden fields by default."""
        yaml = """
_id: str = uuid
_created: datetime = now
name: str = "Unknown"
age: int = 0
"""
        prompt = to_prompt(yaml)

        # Hidden fields should not appear
        assert "id" not in prompt
        assert "created" not in prompt
        # Regular fields should appear without defaults
        assert "name: str" in prompt
        assert "= " not in prompt.split("slimschema")[1]  # No defaults in schema section


class TestHiddenFieldsWithValidation:
    """Test validation behavior with hidden fields."""

    def test_hidden_fields_applied_as_defaults(self):
        """Hidden fields with defaults are applied during validation."""
        yaml = """
_id: str = "auto-id-123"
name: str
"""
        data, error = to_data('{"name": "Alice"}', yaml)

        assert error is None
        assert data["id"] == "auto-id-123"
        assert data["name"] == "Alice"

    def test_hidden_fields_can_be_overridden(self):
        """Hidden fields can be provided in input (not truly hidden from backend)."""
        yaml = """
_id: str = "auto-id"
name: str
"""
        data, error = to_data('{"id": "custom-id", "name": "Bob"}', yaml)

        assert error is None
        assert data["id"] == "custom-id"
        assert data["name"] == "Bob"

    def test_validation_with_hidden_and_optional(self):
        """Mix of hidden, optional, and required fields validates correctly."""
        yaml = """
_id: str = "generated"
_created: datetime = "2025-01-01T00:00:00"
name: str
?tags: list[str]
"""
        # Valid with just required field
        data, error = to_data('{"name": "Test"}', yaml)
        assert error is None
        assert data["id"] == "generated"
        assert data["created"] == "2025-01-01T00:00:00"
        assert data["name"] == "Test"
        assert "tags" not in data  # Optional field not provided

        # Valid with all fields
        data, error = to_data('{"name": "Test", "tags": ["a", "b"]}', yaml)
        assert error is None
        assert data["tags"] == ["a", "b"]


class TestDualMarkers:
    """Test fields with both optional and hidden markers."""

    def test_parse_dual_markers_underscore_first(self):
        """Parse _?field as both hidden and optional."""
        schema = to_schema("_?last_login: datetime")

        assert len(schema.fields) == 1
        assert schema.fields[0].name == "last_login"
        assert schema.fields[0].optional is True
        assert schema.fields[0].hidden is True

    def test_parse_dual_markers_question_first(self):
        """Parse ?_field as both hidden and optional (order shouldn't matter)."""
        schema = to_schema("?_cached_value: str")

        assert len(schema.fields) == 1
        assert schema.fields[0].name == "cached_value"
        assert schema.fields[0].optional is True
        assert schema.fields[0].hidden is True

    def test_generate_dual_markers(self):
        """Generate _?field when both flags are set."""
        schema = to_schema("_?version: int")
        yaml = to_yaml(schema)

        assert "_?version: int" in yaml

    def test_dual_markers_with_default(self):
        """Dual markers work with default values."""
        yaml = "_?metadata: obj = dict"
        schema = to_schema(yaml)

        assert schema.fields[0].name == "metadata"
        assert schema.fields[0].optional is True
        assert schema.fields[0].hidden is True
        assert schema.fields[0].default == "dict"

    def test_dual_markers_roundtrip(self):
        """Dual markers roundtrip correctly."""
        original = """
_?last_login: datetime
name: str
_created: datetime = now
?bio: str
"""
        schema = to_schema(original)
        regenerated = to_yaml(schema)

        # Parse regenerated YAML and verify
        schema2 = to_schema(regenerated)
        assert len(schema2.fields) == 4

        last_login = next(f for f in schema2.fields if f.name == "last_login")
        assert last_login.optional is True
        assert last_login.hidden is True

    def test_dual_markers_validation(self):
        """Validation works with dual markers - field is optional but system-managed."""
        yaml = """
_?cached_result: str
name: str
"""
        # Valid without the optional hidden field
        data, error = to_data('{"name": "Test"}', yaml)
        assert error is None
        assert data["name"] == "Test"
        assert "cached_result" not in data

        # System can add it later (simulated by providing it)
        data, error = to_data('{"name": "Test", "cached_result": "value"}', yaml)
        assert error is None
        assert data["cached_result"] == "value"

    def test_dual_markers_hidden_from_prompt(self):
        """Dual marker fields are hidden from prompts by default."""
        yaml = """
_?last_activity: datetime
name: str
"""
        from slimschema import to_prompt

        prompt = to_prompt(yaml)
        assert "last_activity" not in prompt
        assert "name: str" in prompt

        # But shown when show_hidden=True
        prompt_with_hidden = to_prompt(yaml, show_hidden=True)
        assert "_?last_activity: datetime" in prompt_with_hidden

    def test_dual_markers_with_comment(self):
        """Comments work with dual markers."""
        schema = to_schema("_?version: int  # Optional system tracking")

        assert schema.fields[0].name == "version"
        assert schema.fields[0].optional is True
        assert schema.fields[0].hidden is True
        assert schema.fields[0].description == "Optional system tracking"
