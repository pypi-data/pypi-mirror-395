"""Extract and validate structured data from LLM responses.

Supports JSON, CSV, XML, and YAML with multiple tagging strategies:
- XML tags: <output>, <json>, <json_output>, etc.
- Code fences: ```json, ````json, etc.
- Combined: <output>```json...```</output>
- Raw format detection
"""

import csv
import io
import json
import re
from typing import Any

try:
    import xmltodict
    HAS_XMLTODICT = True
except ImportError:
    HAS_XMLTODICT = False

from ruamel.yaml import YAML

from .core import Schema, ValidationResult
from .validate import validate

# Format identifiers (case-insensitive)
FORMATS = ["json", "xml", "csv", "yaml", "yml"]

# Tag name variations: output, format, format_output, output_format
def _tag_patterns(fmt: str) -> list[str]:
    """Generate tag name variations for a format.

    Returns: ['output', 'json', 'json_output', 'output_json', ...]
    """
    patterns = [
        "output",
        fmt,
        f"{fmt}_output",
        f"output_{fmt}",
    ]
    if fmt == "yaml":
        patterns.extend(["yml", "yml_output", "output_yml"])
    return patterns


def _extract_xml_wrapped_fence(text: str) -> tuple[Any, str] | None:
    """Priority 1: Extract from <tag>```format...```</tag> pattern.

    Args:
        text: LLM response text

    Returns:
        (parsed_data, format) or None
    """
    # Try all tag patterns, not just format-specific ones
    all_tags = ["output", "json", "xml", "yaml", "yml", "csv",
                "json_output", "output_json", "xml_output", "output_xml",
                "yaml_output", "output_yaml", "yml_output", "output_yml",
                "csv_output", "output_csv"]

    for tag in all_tags:
        # Match: <tag>```format?...```</tag>
        # Support 3-10 backticks with flexible whitespace
        # The fence label can be any format, not just the tag's format
        pattern = rf"<{tag}>\s*(`{{3,10}})(json|xml|csv|yaml|yml)?\s*(.*?)\s*\1\s*</{tag}>"
        if match := re.search(pattern, text, re.DOTALL | re.IGNORECASE):
            content = match.group(3).strip()
            fence_label = match.group(2)

            # Determine format from fence label (if present) or tag name
            if fence_label:
                detected_fmt = fence_label.lower()
                if detected_fmt == "yml":
                    detected_fmt = "yaml"
            else:
                # Infer from tag name
                for fmt in FORMATS:
                    if fmt in tag.lower():
                        detected_fmt = "yaml" if fmt == "yml" else fmt
                        break
                else:
                    # Generic tag like "output" - try all formats
                    for try_fmt in ["json", "yaml", "xml", "csv"]:
                        parsed = _parse_format(content, try_fmt)
                        if parsed is not None:
                            return parsed, try_fmt
                    continue

            # Parse content
            parsed = _parse_format(content, detected_fmt)
            if parsed is not None:
                return parsed, detected_fmt

    return None


def _extract_fence(text: str) -> tuple[Any, str] | None:
    """Priority 2: Extract from ```format...``` pattern (no XML tags).

    Args:
        text: LLM response text

    Returns:
        (parsed_data, format) or None
    """
    # Match: ```format?\n...\n``` (3-10 backticks)
    # Require newlines to avoid matching inline code like: ```json {...} ```
    # Capture: (backticks)(format?)(content)(same_backticks)
    pattern = r"(`{3,10})(json|xml|csv|yaml|yml)?\s*\n(.*?)\n\s*\1(?:\s|$)"

    for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
        fence_label = match.group(2)
        content = match.group(3).strip()

        # Skip empty content
        if not content:
            continue

        if fence_label:
            # Format explicitly specified
            fmt = fence_label.lower()
            if fmt == "yml":
                fmt = "yaml"
            parsed = _parse_format(content, fmt)
            if parsed is not None:
                return parsed, fmt
        else:
            # Try all formats
            for fmt in FORMATS:
                if fmt == "yml":
                    continue  # Skip yml, use yaml
                parsed = _parse_format(content, fmt)
                if parsed is not None:
                    return parsed, fmt

    return None


def _extract_xml_tag(text: str) -> tuple[Any, str] | None:
    """Priority 3: Extract from <tag>...</tag> pattern (no fences).

    Args:
        text: LLM response text

    Returns:
        (parsed_data, format) or None
    """
    # Track tags we've already tried to avoid duplicate work
    tried_tags = set()

    for fmt in FORMATS:
        for tag in _tag_patterns(fmt):
            # Skip if we've already tried this tag
            tag_lower = tag.lower()
            if tag_lower in tried_tags:
                continue
            tried_tags.add(tag_lower)

            # Match: <tag>...</tag>
            # But NOT if it contains code fences (already handled in priority 1)
            pattern = rf"<{tag}>(.*?)</{tag}>"
            if match := re.search(pattern, text, re.DOTALL | re.IGNORECASE):
                content = match.group(1).strip()

                # Skip if content contains code fences (would have been caught in priority 1)
                if re.search(r"```", content):
                    continue

                # Determine if this is a format-specific tag or generic 'output' tag
                if tag_lower in ["json", "xml", "csv", "yaml", "yml"]:
                    # Format-specific tag: only try that format
                    actual_fmt = "yaml" if tag_lower == "yml" else tag_lower
                    parsed = _parse_format(content, actual_fmt)
                    if parsed is not None:
                        return parsed, actual_fmt
                    # If parsing fails for a format-specific tag, return None immediately
                    # Do NOT try other formats or continue to other patterns
                    return None
                elif tag_lower == "output":
                    # Generic 'output' tag: try all formats
                    for try_fmt in ["json", "yaml", "xml", "csv"]:
                        parsed = _parse_format(content, try_fmt)
                        if parsed is not None:
                            return parsed, try_fmt
                    # If all formats fail, return None (don't continue to other tags)
                    return None
                elif "_" in tag_lower:
                    # Compound tag like 'json_output' or 'output_json'
                    # Extract the format hint from the tag name
                    format_hint = None
                    for fmt in ["json", "xml", "csv", "yaml", "yml"]:
                        if fmt in tag_lower:
                            format_hint = "yaml" if fmt == "yml" else fmt
                            break

                    if format_hint:
                        # Try the hinted format first
                        parsed = _parse_format(content, format_hint)
                        if parsed is not None:
                            return parsed, format_hint
                        # Then try other formats as fallback
                        for try_fmt in ["json", "yaml", "xml", "csv"]:
                            if try_fmt == format_hint:
                                continue
                            parsed = _parse_format(content, try_fmt)
                            if parsed is not None:
                                return parsed, try_fmt
                    # If all formats fail, return None
                    return None

    return None


def _extract_raw(text: str) -> tuple[Any, str] | None:
    """Priority 4: Try raw format detection (no tags/fences).

    Args:
        text: LLM response text

    Returns:
        (parsed_data, format) or None
    """
    text = text.strip()

    # Try JSON (starts with { or [)
    if text.startswith(("{", "[")):
        parsed = _parse_format(text, "json")
        if parsed is not None:
            return parsed, "json"

    # Try XML (starts with <, but NOT if it's a structured tag like <json>, <output>, etc.)
    if text.startswith("<"):
        # Check if this looks like a structured tag (which should have been caught earlier)
        # Structured tags: <json>, <xml>, <yaml>, <csv>, <output>, <*_output>, <output_*>
        structured_tag_pattern = r"^<(json|xml|yaml|yml|csv|output|[a-z]+_output|output_[a-z]+)>"
        if not re.match(structured_tag_pattern, text, re.IGNORECASE):
            # This looks like actual XML data, not a structured tag
            parsed = _parse_format(text, "xml")
            if parsed is not None:
                return parsed, "xml"

    # Try YAML (has YAML patterns)
    if _looks_like_yaml(text):
        parsed = _parse_format(text, "yaml")
        if parsed is not None:
            return parsed, "yaml"

    # Try CSV (has delimiter patterns)
    if _looks_like_csv(text):
        parsed = _parse_format(text, "csv")
        if parsed is not None:
            return parsed, "csv"

    return None


def _parse_format(content: str, fmt: str) -> Any:
    """Parse content as a specific format.

    Args:
        content: Text to parse
        fmt: Format ('json', 'csv', 'xml', 'yaml')

    Returns:
        Parsed data or None if parsing fails
    """
    # Let individual parse functions handle their own errors
    if fmt == "json":
        return _parse_json(content)
    elif fmt == "csv":
        return _parse_csv(content)
    elif fmt == "xml":
        return _parse_xml(content)
    elif fmt in ("yaml", "yml"):
        return _parse_yaml(content)

    return None


def _parse_json(content: str) -> dict | list | None:
    """Parse JSON content.

    Handles:
    - Standard JSON: {"key": "value"}
    - JSON arrays: [1, 2, 3]
    - JSONL/JSON-ND with commas: {"a":1}, {"b":2}
    - JSONL/JSON-ND without commas (newline-delimited)

    Args:
        content: JSON string

    Returns:
        Parsed dict/list or None
    """
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try wrapping in array brackets (for comma-separated objects)
    try:
        return json.loads(f"[{content}]")
    except json.JSONDecodeError:
        pass

    # Try JSONL/JSON-ND (newline-delimited, no commas)
    try:
        lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        if len(lines) > 1:
            # Multiple lines - try parsing each as JSON
            objects = []
            for line in lines:
                try:
                    obj = json.loads(line)
                    objects.append(obj)
                except json.JSONDecodeError:
                    # If any line fails, this isn't valid JSONL
                    return None
            # All lines parsed successfully
            return objects if objects else None
    except (ValueError, IndexError):
        # Catch only expected errors from split/strip operations
        pass

    return None


def _parse_csv(content: str) -> list[dict] | None:
    """Parse CSV content using csv.Sniffer for dialect detection.

    Args:
        content: CSV string

    Returns:
        List of dicts or None
    """
    # Use Sniffer to detect delimiter
    sample = content[:1024]  # Use first 1KB for sniffing
    sniffer = csv.Sniffer()

    try:
        # Provide possible delimiters to help Sniffer
        dialect = sniffer.sniff(sample, delimiters=',;\t|')
    except csv.Error:
        # Fallback to default dialect
        dialect = csv.excel

    # Always try with headers first (more common case)
    # csv.DictReader will handle it gracefully even if first row isn't headers
    try:
        reader = csv.DictReader(io.StringIO(content), dialect=dialect)
        rows = list(reader)

        # Heuristic: if we got valid dict rows, check if keys look like headers (non-numeric)
        # Valid headers should have at least one non-numeric, non-empty key
        if rows and rows[0]:
            keys = list(rows[0].keys())
            # If any key is a proper string (not just digits), assume we have headers
            if any(key and not key.strip().isdigit() for key in keys):
                return rows if rows else None
    except (csv.Error, ValueError, StopIteration):
        # Specific errors from CSV parsing
        pass

    # Fallback: try without headers
    try:
        reader = csv.reader(io.StringIO(content), dialect=dialect)
        rows = [dict(enumerate(row)) for row in reader]
        return rows if rows else None
    except (csv.Error, ValueError, StopIteration):
        # Specific errors from CSV parsing
        pass

    return None


def _parse_xml(content: str) -> dict | None:
    """Parse XML content to dict.

    Args:
        content: XML string

    Returns:
        Parsed dict or None
    """
    if not HAS_XMLTODICT:
        # Fallback: try basic XML parsing with xml.etree
        import xml.etree.ElementTree as ET

        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            return None

        # Simple conversion: element to dict
        def elem_to_dict(elem):
            result = {}
            if elem.text and elem.text.strip():
                result['_text'] = elem.text.strip()
            for child in elem:
                child_data = elem_to_dict(child)
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = child_data
            result.update(elem.attrib)
            return result

        return {root.tag: elem_to_dict(root)}

    try:
        return xmltodict.parse(content)
    except Exception:
        # xmltodict can raise various exceptions during parsing
        # Catch all since we're at a library boundary
        return None


def _parse_yaml(content: str) -> Any:
    """Parse YAML content using ruamel.yaml (supports comments).

    Args:
        content: YAML string

    Returns:
        Parsed data or None
    """
    try:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.default_flow_style = False
        return yaml.load(content)
    except Exception:
        # ruamel.yaml can raise various exceptions during parsing
        # Catch all since we're at a library boundary
        return None


def _looks_like_yaml(text: str) -> bool:
    """Heuristic: does text look like YAML?

    Args:
        text: Text to check

    Returns:
        True if text has YAML-like patterns
    """
    # Check for YAML patterns: key: value, - list items, etc.
    patterns = [
        r"^\s*\w+:\s*",  # key: value
        r"^\s*-\s+\w+",  # - list item
        r"^\s*#",  # # comment
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.MULTILINE):
            return True

    return False


def _looks_like_csv(text: str) -> bool:
    """Heuristic: does text look like CSV?

    Args:
        text: Text to check

    Returns:
        True if text has CSV-like patterns
    """
    # Check for CSV patterns: consistent delimiters, multiple lines
    lines = text.strip().split('\n')

    if len(lines) < 2:
        return False

    # Check if most lines have the same number of delimiters
    for delimiter in [',', ';', '\t', '|']:
        counts = [line.count(delimiter) for line in lines[:10]]  # Check first 10 lines
        if counts and len(set(counts)) == 1 and counts[0] > 0:
            return True

    return False


def extract_structured_data(text: str, expected_format: str | None = None) -> tuple[Any, str] | None:
    """Extract structured data from LLM response.

    Tries in priority order:
    1. XML tag wrapping fence: <output>```json...```</output>
    2. Fence alone: ```json...```
    3. XML tag alone: <json>...</json>
    4. Raw format detection

    Args:
        text: LLM response text
        expected_format: Optional hint for format ('json', 'csv', 'xml', 'yaml')

    Returns:
        (parsed_data, format) or None if extraction failed
    """
    # Priority 1: XML wrapped fence
    result = _extract_xml_wrapped_fence(text)
    if result:
        return result

    # Priority 2: Fence alone
    result = _extract_fence(text)
    if result:
        return result

    # Priority 3: XML tag alone
    result = _extract_xml_tag(text)
    if result:
        return result

    # Priority 4: Raw detection
    result = _extract_raw(text)
    if result:
        return result

    return None


def extract_json(text: str) -> dict | list | None:
    """Extract JSON from LLM response text.

    Maintained for backward compatibility.

    Args:
        text: LLM response text

    Returns:
        Parsed JSON dict/list or None
    """
    result = extract_structured_data(text, expected_format="json")
    if result and result[1] == "json":
        return result[0]
    return None


def validate_response(response: str, schema: Schema) -> ValidationResult:
    """Extract JSON from LLM response and validate against schema.

    Args:
        response: LLM response text
        schema: Schema IR

    Returns:
        ValidationResult
    """
    from .errors import ValidationError

    data = extract_json(response)

    if data is None:
        errors = ValidationError()
        errors.add("$", ValidationError.FORMAT, "No valid JSON found in response")
        return ValidationResult(
            valid=False, data=None, errors=errors, schema=schema
        )

    return validate(data, schema)
