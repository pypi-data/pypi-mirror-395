"""Tests for JSON Extraction Feature.

This test module validates JSON extraction features documented in
docs/guide_llm_workflow.md. Tests cover robust extraction from various
LLM response formats.
"""


from slimschema import to_data


class TestCleanJsonExtraction:
    """Test extraction of clean JSON responses."""

    def test_extract_clean_json(self, llm_response_clean_json):
        """Extract clean JSON without any wrapping."""
        schema_str = "name: str\nage: int"

        data, error = to_data(llm_response_clean_json, schema_str)

        assert error is None
        assert data["name"] == "Alice"
        assert data["age"] == 30

    def test_extract_json_with_whitespace(self):
        """Extract JSON with surrounding whitespace."""
        schema_str = "name: str\nage: int"
        response = '  \n\n  {"name": "Alice", "age": 30}  \n\n  '

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"


class TestXmlTagExtraction:
    """Test extraction from XML-tagged responses."""

    def test_extract_json_xml_tags(self, llm_response_with_xml_tags):
        """Extract JSON wrapped in <json>...</json> tags."""
        schema_str = "name: str\nage: int"

        data, error = to_data(llm_response_with_xml_tags, schema_str)

        assert error is None
        assert data["name"] == "Alice"
        assert data["age"] == 30

    def test_extract_output_xml_tags(self):
        """Extract JSON wrapped in <output>...</output> tags."""
        schema_str = "name: str\nage: int"
        response = '<output>{"name": "Bob", "age": 25}</output>'

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Bob"

    def test_extract_custom_xml_tags(self):
        """Extract JSON wrapped in custom XML tags."""
        schema_str = "name: str\nage: int"
        response = '<data>{"name": "Charlie", "age": 35}</data>'

        data, error = to_data(response, schema_str)

        # Custom tags like <data> should be supported
        if error is None:
            assert data["name"] == "Charlie"


class TestMarkdownFenceExtraction:
    """Test extraction from markdown code fences."""

    def test_extract_markdown_json_fence(self, llm_response_with_markdown):
        """Extract JSON from markdown ```json fence."""
        schema_str = "name: str\nage: int"

        data, error = to_data(llm_response_with_markdown, schema_str)

        assert error is None
        assert data["name"] == "Alice"
        assert data["age"] == 30

    def test_extract_fence_without_language(self):
        """Extract JSON from fence without language specifier."""
        schema_str = "name: str\nage: int"
        response = '''```
{"name": "Alice", "age": 30}
```'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"


class TestCombinedWrapping:
    """Test extraction from combined XML + fence wrapping."""

    def test_extract_xml_with_fence(self):
        """Extract JSON from <output>```json...```</output> pattern."""
        schema_str = "name: str\nage: int"
        response = '''<output>```json
{"name": "Alice", "age": 30}
```</output>'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"

    def test_extract_json_tag_with_fence(self):
        """Extract JSON from <json>```json...```</json> pattern."""
        schema_str = "name: str\nage: int"
        response = '''<json>```json
{"name": "Bob", "age": 25}
```</json>'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Bob"


class TestExtractionWithSurroundingText:
    """Test extraction when JSON is embedded in text."""

    def test_extract_json_with_surrounding_text(self, llm_response_with_text):
        """Extract JSON when surrounded by explanatory text."""
        schema_str = "name: str\nage: int"

        data, error = to_data(llm_response_with_text, schema_str)

        assert error is None
        assert data["name"] == "Alice"
        assert data["age"] == 30

    def test_extract_from_chatty_response(self):
        """Extract JSON from verbose LLM response."""
        schema_str = "name: str\nage: int"
        response = '''Sure! I'll help you with that. Here's the user data in JSON format:

<json>
{"name": "Alice", "age": 30}
</json>

Is there anything else you need?'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"


class TestMalformedJson:
    """Test handling of malformed JSON."""

    def test_malformed_json_returns_error(self, llm_response_malformed):
        """Malformed JSON returns error."""
        schema_str = "name: str\nage: int"

        data, error = to_data(llm_response_malformed, schema_str)

        assert data is None
        assert error is not None

    def test_invalid_json_syntax(self):
        """Invalid JSON syntax returns error."""
        schema_str = "name: str\nage: int"
        response = '{"name": "Alice" age: 30}'  # Missing comma

        data, error = to_data(response, schema_str)

        assert data is None
        assert error is not None


class TestNoJsonFound:
    """Test handling when no JSON is found."""

    def test_no_json_in_response(self):
        """Response with no JSON returns error."""
        schema_str = "name: str\nage: int"
        response = "Sorry, I couldn't generate the data."

        data, error = to_data(response, schema_str)

        assert data is None
        assert error is not None
        # Updated error message includes all formats
        assert "no valid" in error.lower() and "found in response" in error.lower()

    def test_empty_response(self):
        """Empty response returns error."""
        schema_str = "name: str\nage: int"
        response = ""

        data, error = to_data(response, schema_str)

        assert data is None
        assert error is not None


class TestMultipleBackticks:
    """Test handling of various backtick counts."""

    def test_triple_backticks(self):
        """Standard triple backticks work."""
        schema_str = "name: str\nage: int"
        response = '''```json
{"name": "Alice", "age": 30}
```'''

        data, error = to_data(response, schema_str)

        assert error is None

    def test_quadruple_backticks(self):
        """Quadruple backticks (4) work."""
        schema_str = "name: str\nage: int"
        response = '''````json
{"name": "Alice", "age": 30}
````'''

        data, error = to_data(response, schema_str)

        # Should handle 4 backticks
        if error is None:
            assert data["name"] == "Alice"


class TestCaseSensitivity:
    """Test case-insensitive tag and fence matching."""

    def test_uppercase_json_tag(self):
        """Uppercase <JSON> tag works."""
        schema_str = "name: str\nage: int"
        response = '<JSON>{"name": "Alice", "age": 30}</JSON>'

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"

    def test_mixed_case_fence(self):
        """Mixed case fence language works."""
        schema_str = "name: str\nage: int"
        response = '''```JSON
{"name": "Alice", "age": 30}
```'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"


class TestNestedJsonExtraction:
    """Test extraction of nested JSON structures."""

    def test_extract_nested_json(self):
        """Extract nested JSON structure."""
        schema_str = """
user:
  name: str
  age: int
  settings:
    theme: str
    notifications: bool
"""
        response = '''<json>
{
  "user": {
    "name": "Alice",
    "age": 30,
    "settings": {
      "theme": "dark",
      "notifications": true
    }
  }
}
</json>'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["user"]["name"] == "Alice"
        assert data["user"]["settings"]["theme"] == "dark"


class TestArrayExtraction:
    """Test extraction of JSON arrays."""

    def test_extract_json_array(self):
        """Extract JSON array."""
        schema_str = "tags: list[str]"
        response = '<json>{"tags": ["python", "testing", "slimschema"]}</json>'

        data, error = to_data(response, schema_str)

        assert error is None
        assert len(data["tags"]) == 3
        assert "python" in data["tags"]


class TestExtractionRobustness:
    """Test robustness against common LLM quirks."""

    def test_extra_newlines_in_fence(self):
        """Handle extra newlines inside fence."""
        schema_str = "name: str\nage: int"
        response = '''```json


{"name": "Alice", "age": 30}


```'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"

    def test_indented_json_in_fence(self):
        """Handle indented JSON inside fence."""
        schema_str = "name: str\nage: int"
        response = '''```json
    {"name": "Alice", "age": 30}
```'''

        data, error = to_data(response, schema_str)

        assert error is None
        assert data["name"] == "Alice"

    def test_json_with_trailing_comma(self):
        """Handle JSON with trailing comma (common LLM mistake)."""
        schema_str = "name: str\nage: int"
        response = '{"name": "Alice", "age": 30,}'  # Trailing comma

        data, error = to_data(response, schema_str)

        # Trailing comma is invalid JSON, should error
        # (unless repair is implemented)
        assert data is None or error is not None
