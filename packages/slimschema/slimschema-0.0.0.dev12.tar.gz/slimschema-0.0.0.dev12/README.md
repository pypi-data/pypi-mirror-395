# SlimSchema

**The bridge between LLMs, Python types, and fast validation.**

SlimSchema is a schema language optimized for LLM token efficiency (70% smaller than JSON Schema) that converts seamlessly between **YAML**, **Pydantic**, and **msgspec**.

## Core Features

*   **Token Efficient:** Compressed syntax (`age: 18..120`) saves context window and costs.
*   **Deep Validation:** Recursive validation for nested objects and dictionaries.
*   **Robust Extraction:** extract JSON/XML from noisy LLM markdown.
*   **Universal Bridge:** Convert any format to any format (YAML ↔ Pydantic ↔ msgspec).

## Quick Start

```bash
pip install slimschema
```

### The Magic Example

Define a schema with nested types and defaults, extract data from an LLM response, and get a validated Python object.

```python
from slimschema import to_data, to_pydantic

# 1. Define a compact schema (with nested defaults!)
schema = """
user:
  name: str{3..50}
  role: admin | user | guest = "guest"
  settings:
    theme: str = "dark"
    notifications: bool = true
"""

# 2. Validate LLM output (even if partial)
# Input missing 'settings' -> defaults apply automatically
llm_output = '{"user": {"name": "Alice"}}'
data, error = to_data(llm_output, schema)

print(data)
# {
#   "user": {
#     "name": "Alice",
#     "role": "guest",
#     "settings": {"theme": "dark", "notifications": True}
#   }
# }

# 3. Convert to Pydantic for your app
UserModel = to_pydantic(schema)
instance = UserModel(**data)
print(instance.user.settings.theme) # "dark"
```

## Documentation

**Guides**
*   [Syntax Guide](docs/guide_syntax.md): Primitives, constraints, and inline objects.
*   [Validation Guide](docs/guide_validation.md): How `to_data` validates and reports errors.
*   [Defaults Guide](docs/guide_defaults.md): Handling partial data with scalar and nested defaults.
*   [LLM Workflow](docs/guide_llm_workflow.md): Generating prompts and robust extraction.
*   [Inference Guide](docs/guide_inference.md): Bootstrapping schemas from data.

**Integrations**
*   [Pydantic](docs/integration_pydantic.md): Round-trip conversion and nested models.
*   [msgspec](docs/integration_msgspec.md): High-performance validation structs.

**Advanced**
*   [JSON Patch](docs/feature_json_patch.md): RFC 6902 support.

## API Reference

*   `to_data(response, schema)`: Extract and validate JSON.
*   `to_schema(obj)`: Convert Pydantic/msgspec/YAML to SlimSchema IR.
*   `to_prompt(schema)`: Generate token-optimized prompts.
*   `from_data(data)`: Infer schema from examples.
*   `to_pydantic(schema)`: Generate Pydantic models.
*   `to_msgspec(schema)`: Generate msgspec structs.

## License

MIT
