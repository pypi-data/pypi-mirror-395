"""Tests for user-friendly error handling."""

import pytest

from slimschema import SchemaParseError, parse_slimschema, to_data


class TestSchemaParseErrors:
    """Test that schema parsing errors are user-friendly."""

    def test_old_array_syntax_without_quotes(self):
        """Old [type] syntax without quotes gives helpful error."""
        with pytest.raises(SchemaParseError) as exc_info:
            parse_slimschema("tags: [str]")

        error_msg = str(exc_info.value)
        assert "list[type]" in error_msg
        assert "[type]" in error_msg
        assert "Line 1" in error_msg

    def test_unclosed_inline_object(self):
        """Unclosed braces in inline object give helpful error."""
        with pytest.raises(SchemaParseError) as exc_info:
            parse_slimschema("settings: {theme:str")

        error_msg = str(exc_info.value)
        assert "Unclosed braces" in error_msg or "inline object" in error_msg

    def test_tab_indentation(self):
        """Tab characters give helpful error."""
        with pytest.raises(SchemaParseError) as exc_info:
            parse_slimschema("user:\n\tname: str")

        error_msg = str(exc_info.value)
        assert "tab" in error_msg.lower()
        assert "spaces" in error_msg.lower()

    def test_missing_colon(self):
        """Missing colon gives helpful error."""
        with pytest.raises(SchemaParseError) as exc_info:
            parse_slimschema("name str")

        error_msg = str(exc_info.value)
        assert "colon" in error_msg.lower() or "name: type" in error_msg.lower()

    def test_duplicate_field_names(self):
        """Duplicate field names give helpful error."""
        with pytest.raises(SchemaParseError) as exc_info:
            parse_slimschema("name: str\nname: int")

        error_msg = str(exc_info.value)
        assert "duplicate" in error_msg.lower()

    def test_old_array_syntax_in_nested_context(self):
        """Old array syntax in nested objects detected."""
        # This should fail with a helpful message
        with pytest.raises(SchemaParseError) as exc_info:
            parse_slimschema("items: [int]")

        error_msg = str(exc_info.value)
        assert "list[" in error_msg

    def test_valid_schemas_still_work(self):
        """Valid schemas are not affected by error detection."""
        # These should all parse successfully
        schemas = [
            "name: str",
            "age: 18..120",
            "tags: list[str]",
            'items: "[str]"',  # Quoted old syntax is valid
            "settings: {theme:str, lang:str}",
            "coords: tuple[float, float]",
            "ids: set[int]",
        ]

        for schema_str in schemas:
            schema = parse_slimschema(schema_str)
            assert len(schema.fields) >= 1


class TestErrorMessagesInToData:
    """Test that to_data() shows friendly schema errors."""

    def test_schema_error_in_to_data(self):
        """to_data() wraps schema parse errors nicely."""
        data, error = to_data('{"tags": ["a"]}', "tags: [str]")

        assert data is None
        assert error is not None
        assert "list[type]" in error
        assert "Invalid schema:" in error

    def test_validation_errors_still_work(self):
        """Validation errors are separate from schema errors."""
        data, error = to_data('{"age": 5}', "age: 18..120")

        assert data is None
        assert error is not None
        # Should be a validation error, not a schema parse error
        assert "Invalid schema:" not in error
        assert "18" in error  # Should mention the constraint


class TestQuotedOldSyntaxStillWorks:
    """Test that quoted old syntax is still valid (for backwards compat)."""

    def test_quoted_array_syntax_works(self):
        """Quoted [type] syntax is valid."""
        schema = parse_slimschema('tags: "[str]"')
        assert len(schema.fields) == 1
        assert schema.fields[0].name == "tags"

    def test_quoted_array_with_default(self):
        """Quoted [type] with default works."""
        schema = parse_slimschema('tags: "[str] = []"')
        assert schema.fields[0].default == "[]"


class TestEdgeCases:
    """Test edge cases in error detection."""

    def test_array_in_default_not_flagged(self):
        """Arrays in default values should not trigger error."""
        # This has [type] but it's in a default value, so should be fine
        # Actually, this might still fail because of YAML parsing, but let's see
        schema = parse_slimschema('tags: list[str] = []')
        assert len(schema.fields) == 1

    def test_array_pattern_in_regex_not_flagged(self):
        """Regex patterns with [] should not trigger false positives."""
        # This has [] but it's a regex pattern
        schema = parse_slimschema('code: /^[A-Z]+$/')
        assert len(schema.fields) == 1

    def test_multiline_error_shows_correct_line(self):
        """Error on second line shows correct line number."""
        with pytest.raises(SchemaParseError) as exc_info:
            parse_slimschema("name: str\ntags: [int]")

        error_msg = str(exc_info.value)
        assert "Line 2" in error_msg
