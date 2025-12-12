"""Generate LLM prompts with embedded schemas for structured output."""

from .api import to_schema
from .generator import to_yaml


def to_prompt(
    schema,
    *,
    instruction: str | None = None,
    errors: str | None = None,
    xml_tag: str | None = "output",
    fence_language: str | None = "json",
    show_defaults: bool = False,
    show_hidden: bool = False,
) -> str:
    """Generate an LLM prompt with schema for structured output.

    Args:
        schema: Your schema (YAML string, Pydantic model, msgspec Struct, or Schema object)
        instruction: Optional task description (e.g., "Extract product info", "Generate user data")
        errors: Optional error message from previous validation attempt
        xml_tag: XML tag name (default: "output"). Set to None to skip XML wrapper.
        fence_language: Fence language (default: "json"). Set to None to skip fence wrapper.
        show_defaults: Whether to show default values in schema (default: False)
        show_hidden: Whether to show system-managed fields (_prefix) in schema (default: False)

    Returns:
        Complete prompt string ready for LLM

    Examples:
        >>> # Default: <output>```json...```</output> (most robust)
        >>> prompt = to_prompt("name: str\\nage: 18..120")
        >>> print(prompt)
        Follow this schema:
        ```slimschema
        name: str
        age: 18..120
        ```
        <BLANKLINE>
        To generate `JSON`:
        <output>```json
        ```</output>

        >>> # With custom instruction
        >>> prompt = to_prompt("name: str\\nprice: float", instruction="Extract product information.")
        >>> # Instruction appears first, then schema

        >>> # With validation errors for retry
        >>> prompt = to_prompt(schema, errors="Missing required fields: age")
        >>> # Errors shown first

        >>> # Instruction with errors (retry with context)
        >>> prompt = to_prompt(schema, instruction="Fix the validation errors.", errors="Invalid age")
        >>> # Order: instruction, errors, schema

        >>> # Just code fence, no XML tags
        >>> to_prompt(schema, xml_tag=None)

        >>> # Just XML tags, no code fence
        >>> to_prompt(schema, fence_language=None, xml_tag="data")

        >>> # CSV format with custom tag
        >>> to_prompt(schema, xml_tag="data", fence_language="csv")

        >>> # Show defaults (not recommended for LLM prompts)
        >>> to_prompt("age: int = 0", show_defaults=True)

        >>> # Show system-managed fields (not recommended for LLM prompts)
        >>> to_prompt("_id: str = uuid\\nname: str", show_hidden=True)
    """
    # Validate at least one wrapper is provided
    if xml_tag is None and fence_language is None:
        raise ValueError("Must provide at least one of xml_tag or fence_language")

    # Convert schema to YAML format
    schema_ir = to_schema(schema)
    schema_str = to_yaml(schema_ir, show_defaults=show_defaults, show_hidden=show_hidden).strip()

    # Build prompt parts
    parts = []

    # Add instruction if present (first!)
    if instruction:
        parts.append(instruction)
        parts.append("")

    # Add errors if present
    if errors:
        parts.append("Errors found, please correct the output below:")
        parts.append(errors)
        parts.append("")

    # Add schema instruction and schema
    parts.append("Follow this schema:")
    parts.append("```slimschema")
    parts.append(schema_str)
    parts.append("```")
    parts.append("")

    # Add output format instruction
    format_name = fence_language.upper() if fence_language else "OUTPUT"
    parts.append(f"To generate `{format_name}`:")

    # Build the output wrapper
    if xml_tag and fence_language:
        # Both: <output>```json...```</output>
        parts.append(f"<{xml_tag}>```{fence_language}")
        parts.append(f"```</{xml_tag}>")
    elif xml_tag:
        # Just XML: <output>...</output>
        parts.append(f"<{xml_tag}>")
        parts.append(f"</{xml_tag}>")
    elif fence_language:
        # Just fence: ```json...```
        parts.append(f"```{fence_language}")
        parts.append("```")

    return "\n".join(parts)
