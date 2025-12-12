"""Tests for Prompt Generation Guide.

This test module validates prompt generation features documented in docs/guide_llm_workflow.md.
Tests cover to_prompt() functionality and various output format configurations.
"""

import pytest

from slimschema.prompt import to_prompt


class TestBasicPromptGeneration:
    """Test basic prompt generation functionality."""

    def test_basic_prompt_generation(self):
        """Generate a basic prompt with default settings."""
        schema_str = "name: str\nage: 18..120"

        prompt = to_prompt(schema_str)

        assert "Follow this schema:" in prompt
        assert "slimschema" in prompt
        assert "name: str" in prompt
        assert "age: 18..120" in prompt
        assert "<output>" in prompt
        assert "```json" in prompt

    def test_prompt_contains_xml_tags(self):
        """Default prompt includes XML tags."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str)

        assert "<output>" in prompt
        assert "</output>" in prompt

    def test_prompt_contains_code_fence(self):
        """Default prompt includes code fence."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str)

        assert "```json" in prompt
        assert "```" in prompt

    def test_prompt_has_schema_block(self):
        """Prompt includes schema in slimschema fence."""
        schema_str = "username: str{3..20}\nemail: email"

        prompt = to_prompt(schema_str)

        assert "```slimschema" in prompt
        assert "username: str{3..20}" in prompt
        assert "email: email" in prompt


class TestPromptWithErrors:
    """Test prompt generation with validation errors."""

    def test_prompt_with_error_message(self):
        """Prompt includes error message when provided."""
        schema_str = "name: str\nage: int"
        error_msg = "Missing required fields: age"

        prompt = to_prompt(schema_str, errors=error_msg)

        assert "Errors found" in prompt or "correct" in prompt.lower()
        assert error_msg in prompt

    def test_errors_appear_first(self):
        """Error messages appear before schema in prompt."""
        schema_str = "name: str"
        error_msg = "Invalid value"

        prompt = to_prompt(schema_str, errors=error_msg)

        error_pos = prompt.index(error_msg)
        schema_pos = prompt.index("Follow this schema")

        assert error_pos < schema_pos


class TestCustomXmlTags:
    """Test custom XML tag configuration."""

    def test_custom_xml_tag(self):
        """Use custom XML tag name."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str, xml_tag="data")

        assert "<data>" in prompt
        assert "</data>" in prompt
        assert "<output>" not in prompt

    def test_no_xml_tag(self):
        """Disable XML tags by setting to None."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str, xml_tag=None)

        assert "<output>" not in prompt
        assert "</output>" not in prompt
        # Should still have fence
        assert "```json" in prompt

    def test_xml_tag_only_no_fence(self):
        """Use only XML tags without code fence."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str, xml_tag="result", fence_language=None)

        assert "<result>" in prompt
        assert "</result>" in prompt
        assert "```json" not in prompt


class TestCustomFenceLanguage:
    """Test custom code fence language configuration."""

    def test_custom_fence_language(self):
        """Use custom fence language."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str, fence_language="csv")

        assert "```csv" in prompt
        assert "CSV" in prompt  # Format name in instruction

    def test_no_fence_language(self):
        """Disable code fence by setting to None."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str, fence_language=None)

        assert "```json" not in prompt
        # Should still have XML tags
        assert "<output>" in prompt

    def test_fence_only_no_xml(self):
        """Use only code fence without XML tags."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str, xml_tag=None, fence_language="json")

        assert "```json" in prompt
        assert "<output>" not in prompt
        assert "</output>" not in prompt


class TestWrapperRequirement:
    """Test that at least one wrapper is required."""

    def test_requires_at_least_one_wrapper(self):
        """Providing neither xml_tag nor fence_language raises error."""
        schema_str = "name: str"

        with pytest.raises(ValueError, match="Must provide at least one"):
            to_prompt(schema_str, xml_tag=None, fence_language=None)


class TestShowDefaults:
    """Test show_defaults parameter."""

    def test_hide_defaults_by_default(self):
        """Defaults are hidden by default in prompts."""
        schema_str = "count: int = 0\nactive: bool = true"

        prompt = to_prompt(schema_str)

        # Should not show the default values
        assert " = 0" not in prompt or "show_defaults" not in prompt

    def test_show_defaults_when_enabled(self):
        """Defaults are shown when show_defaults=True."""
        schema_str = "count: int = 0\nactive: bool = true"

        prompt = to_prompt(schema_str, show_defaults=True)

        # Should show the default values
        assert "count: int" in prompt or " = 0" in prompt


class TestPromptFromPydantic:
    """Test prompt generation from Pydantic models."""

    def test_prompt_from_pydantic_model(self):
        """Generate prompt from Pydantic model."""
        from pydantic import BaseModel

        class User(BaseModel):
            name: str
            age: int

        prompt = to_prompt(User)

        assert "name: str" in prompt
        assert "age: int" in prompt
        assert "<output>" in prompt


class TestPromptInstructions:
    """Test clarity of prompt instructions."""

    def test_prompt_has_clear_format_instruction(self):
        """Prompt clearly states the output format."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str)

        # Should mention JSON format
        assert "JSON" in prompt.upper()

    def test_custom_format_in_instruction(self):
        """Custom format appears in instruction."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str, fence_language="csv")

        # Should mention CSV format
        assert "CSV" in prompt.upper()


class TestPromptStructure:
    """Test overall structure and organization of prompts."""

    def test_prompt_structure_order(self):
        """Prompt has logical order: errors, schema, output format."""
        schema_str = "name: str"
        error_msg = "Error message"

        prompt = to_prompt(schema_str, errors=error_msg)

        # Find positions
        error_pos = prompt.index(error_msg)
        schema_pos = prompt.index("Follow this schema")
        output_pos = prompt.index("To generate")

        # Verify order
        assert error_pos < schema_pos < output_pos

    def test_prompt_without_errors_structure(self):
        """Prompt without errors has: schema, output format."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str)

        schema_pos = prompt.index("Follow this schema")
        output_pos = prompt.index("To generate")

        assert schema_pos < output_pos

    def test_prompt_line_breaks(self):
        """Prompt has appropriate line breaks for readability."""
        schema_str = "name: str"

        prompt = to_prompt(schema_str)

        # Should have multiple lines
        lines = prompt.split("\n")
        assert len(lines) > 5

    def test_instruction_before_schema(self):
        """Instruction parameter appears before schema."""
        schema_str = "name: str"
        instruction = "Extract user data."

        prompt = to_prompt(schema_str, instruction=instruction)

        instruction_pos = prompt.index(instruction)
        schema_pos = prompt.index("Follow this schema")

        assert instruction_pos < schema_pos

    def test_instruction_with_errors_order(self):
        """With instruction and errors: instruction, errors, schema."""
        schema_str = "name: str"
        instruction = "Fix the errors."
        errors = "Missing field: name"

        prompt = to_prompt(schema_str, instruction=instruction, errors=errors)

        instruction_pos = prompt.index(instruction)
        error_pos = prompt.index(errors)
        schema_pos = prompt.index("Follow this schema")

        assert instruction_pos < error_pos < schema_pos
