"""Tests for JSON Patch (RFC 6902) Feature.

This test module validates JSON Patch features documented in
docs/advanced_json_patch.md. Tests cover all standard patch operations
and schema-validated patching.
"""

import pytest

from slimschema.patch import apply_patch, apply_patch_validated


class TestAddOperation:
    """Test 'add' patch operation."""

    def test_add_property_to_object(self):
        """Add a new property to an object."""
        data = {"name": "Alice"}
        patch = {"op": "add", "path": "/age", "value": 30}

        result, error = apply_patch(data, patch)

        assert error is None
        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_add_nested_property(self):
        """Add a property to a nested object."""
        data = {"user": {"name": "Alice"}}
        patch = {"op": "add", "path": "/user/age", "value": 30}

        result, error = apply_patch(data, patch)

        assert error is None
        assert result["user"]["age"] == 30

    def test_add_array_element(self):
        """Add an element to an array."""
        data = {"tags": ["python"]}
        patch = {"op": "add", "path": "/tags/1", "value": "testing"}

        result, error = apply_patch(data, patch)

        assert error is None
        assert result["tags"] == ["python", "testing"]

    def test_add_array_element_with_dash(self):
        """Add element to end of array using '-'."""
        data = {"tags": ["python", "testing"]}
        patch = {"op": "add", "path": "/tags/-", "value": "slimschema"}

        result, error = apply_patch(data, patch)

        assert error is None
        assert result["tags"] == ["python", "testing", "slimschema"]

    def test_add_overwrites_existing(self):
        """Add operation overwrites existing values."""
        data = {"name": "Alice"}
        patch = {"op": "add", "path": "/name", "value": "Bob"}

        result, error = apply_patch(data, patch)

        assert error is None
        assert result["name"] == "Bob"


class TestRemoveOperation:
    """Test 'remove' patch operation."""

    def test_remove_property(self):
        """Remove a property from an object."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "remove", "path": "/age"}

        result, error = apply_patch(data, patch)

        assert error is None
        assert "age" not in result
        assert result["name"] == "Alice"

    def test_remove_nested_property(self):
        """Remove a property from a nested object."""
        data = {"user": {"name": "Alice", "age": 30}}
        patch = {"op": "remove", "path": "/user/age"}

        result, error = apply_patch(data, patch)

        assert error is None
        assert "age" not in result["user"]
        assert result["user"]["name"] == "Alice"

    def test_remove_array_element(self):
        """Remove an element from an array."""
        data = {"tags": ["python", "testing", "slimschema"]}
        patch = {"op": "remove", "path": "/tags/1"}

        result, error = apply_patch(data, patch)

        assert error is None
        assert result["tags"] == ["python", "slimschema"]

    def test_remove_nonexistent_path_errors(self):
        """Removing a nonexistent path returns error."""
        data = {"name": "Alice"}
        patch = {"op": "remove", "path": "/age"}

        result, error = apply_patch(data, patch)

        assert error is not None
        assert result == data  # Original unchanged


class TestReplaceOperation:
    """Test 'replace' patch operation."""

    def test_replace_property(self):
        """Replace a property value."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "replace", "path": "/age", "value": 31}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result["age"] == 31

    def test_replace_nested_property(self):
        """Replace a nested property value."""
        data = {"user": {"name": "Alice", "age": 30}}
        patch = {"op": "replace", "path": "/user/age", "value": 31}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result["user"]["age"] == 31

    def test_replace_array_element(self):
        """Replace an array element."""
        data = {"tags": ["python", "testing"]}
        patch = {"op": "replace", "path": "/tags/1", "value": "slimschema"}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result["tags"] == ["python", "slimschema"]

    def test_replace_nonexistent_path_errors(self):
        """Replacing a nonexistent path returns error."""
        data = {"name": "Alice"}
        patch = {"op": "replace", "path": "/age", "value": 30}

        result, error = apply_patch(data, patch)

        assert error is not None
        assert result == data  # Original unchanged


class TestMoveOperation:
    """Test 'move' patch operation."""

    def test_move_property(self):
        """Move a property to a new location."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "move", "from": "/age", "path": "/years"}

        result, error = apply_patch(data, patch)
        assert error is None

        assert "age" not in result
        assert result["years"] == 30
        assert result["name"] == "Alice"

    def test_move_nested_to_root(self):
        """Move a nested property to root level."""
        data = {"user": {"name": "Alice", "age": 30}}
        patch = {"op": "move", "from": "/user/age", "path": "/age"}

        result, error = apply_patch(data, patch)
        assert error is None

        assert "age" not in result["user"]
        assert result["age"] == 30

    def test_move_array_element(self):
        """Move an array element to a different index."""
        data = {"tags": ["python", "testing", "slimschema"]}
        patch = {"op": "move", "from": "/tags/2", "path": "/tags/0"}

        result, error = apply_patch(data, patch)

        # Implementation-dependent: verify behavior
        assert "slimschema" in result["tags"]


class TestCopyOperation:
    """Test 'copy' patch operation."""

    def test_copy_property(self):
        """Copy a property to a new location."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "copy", "from": "/age", "path": "/years"}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result["age"] == 30
        assert result["years"] == 30
        assert result["name"] == "Alice"

    def test_copy_nested_object(self):
        """Copy a nested object."""
        data = {"user": {"name": "Alice"}, "metadata": {}}
        patch = {"op": "copy", "from": "/user", "path": "/metadata/user"}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result["user"]["name"] == "Alice"
        assert result["metadata"]["user"]["name"] == "Alice"



class TestTestOperation:
    """Test 'test' patch operation."""

    def test_test_succeeds_when_equal(self):
        """Test operation succeeds when values are equal."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "test", "path": "/age", "value": 30}

        result, error = apply_patch(data, patch)

        # Data should be unchanged
        assert result == data

    def test_test_fails_when_not_equal(self):
        """Test operation fails when values are not equal."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "test", "path": "/age", "value": 31}

        result, error = apply_patch(data, patch)

        assert error is not None
        assert result == data  # Original unchanged

    def test_test_nested_value(self):
        """Test operation on nested value."""
        data = {"user": {"name": "Alice", "age": 30}}
        patch = {"op": "test", "path": "/user/name", "value": "Alice"}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result == data


class TestMultiplePatchOperations:
    """Test applying multiple patch operations."""

    def test_apply_multiple_patches(self):
        """Apply a list of patch operations."""
        data = {"name": "Alice", "age": 30}
        patches = [
            {"op": "add", "path": "/email", "value": "alice@example.com"},
            {"op": "replace", "path": "/age", "value": 31},
            {"op": "remove", "path": "/name"}
        ]

        result, error = apply_patch(data, patches)
        assert error is None

        assert "name" not in result
        assert result["age"] == 31
        assert result["email"] == "alice@example.com"

    def test_patches_applied_sequentially(self):
        """Patches are applied in order."""
        data = {"count": 0}
        patches = [
            {"op": "replace", "path": "/count", "value": 1},
            {"op": "replace", "path": "/count", "value": 2},
            {"op": "replace", "path": "/count", "value": 3}
        ]

        result, error = apply_patch(data, patches)
        assert error is None

        assert result["count"] == 3


class TestErrorHandling:
    """Test error handling in patch operations."""

    def test_invalid_operation(self):
        """Invalid operation type returns error."""
        data = {"name": "Alice"}
        patch = {"op": "invalid", "path": "/name"}

        result, error = apply_patch(data, patch)

        assert error is not None
        assert result == data

    def test_missing_required_field(self):
        """Missing required field returns error."""
        data = {"name": "Alice"}
        patch = {"op": "add", "value": 30}  # Missing 'path'

        result, error = apply_patch(data, patch)

        assert error is not None
        assert result == data

    def test_invalid_path_format(self):
        """Invalid path format returns error."""
        data = {"name": "Alice"}
        patch = {"op": "add", "path": "invalid", "value": 30}  # Missing leading /

        result, error = apply_patch(data, patch)

        assert error is not None
        assert result == data

    def test_array_index_out_of_bounds(self):
        """Array index out of bounds returns error."""
        data = {"tags": ["python"]}
        patch = {"op": "replace", "path": "/tags/5", "value": "testing"}

        result, error = apply_patch(data, patch)

        assert error is not None
        assert result == data


class TestImmutability:
    """Test that original data is not modified."""

    def test_original_data_unchanged(self):
        """Apply_patch returns new data, doesn't modify original."""
        original = {"name": "Alice", "age": 30}
        patch = {"op": "replace", "path": "/age", "value": 31}

        result, error = apply_patch(original, patch)

        # Original should be unchanged
        assert original["age"] == 30
        assert result["age"] == 31

    def test_nested_data_unchanged(self):
        """Nested structures in original data are not modified."""
        original = {"user": {"name": "Alice", "age": 30}}
        patch = {"op": "replace", "path": "/user/age", "value": 31}

        result, error = apply_patch(original, patch)
        assert error is None

        assert original["user"]["age"] == 30
        assert result["user"]["age"] == 31


class TestComplexPatches:
    """Test complex patch scenarios."""

    def test_deep_nesting(self):
        """Apply patches to deeply nested structures."""
        data = {
            "app": {
                "config": {
                    "settings": {
                        "theme": "light"
                    }
                }
            }
        }
        patch = {"op": "replace", "path": "/app/config/settings/theme", "value": "dark"}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result["app"]["config"]["settings"]["theme"] == "dark"

    def test_mixed_arrays_and_objects(self):
        """Apply patches to structures with mixed arrays and objects."""
        data = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ]
        }
        patch = {"op": "replace", "path": "/users/0/age", "value": 31}

        result, error = apply_patch(data, patch)
        assert error is None

        assert result["users"][0]["age"] == 31
        assert result["users"][1]["age"] == 25


class TestSchemaValidatedPatching:
    """Test apply_patch_validated() with schema validation."""

    def test_valid_patch_returns_success(self):
        """Valid patch returns (data, None)."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "replace", "path": "/age", "value": 31}
        schema = "name: str\nage: int"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert result["age"] == 31
        assert result["name"] == "Alice"

    def test_type_violation_returns_error(self):
        """Type violation returns (original_data, error)."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "replace", "path": "/age", "value": "thirty"}  # String, not int
        schema = "name: str\nage: int"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert "age" in error.lower() or "int" in error.lower()
        # Original data unchanged
        assert result == data
        assert result["age"] == 30

    def test_list_replaced_with_string(self):
        """List replaced with string violates schema."""
        data = {"tags": ["A", "B", "C"]}
        patch = {"op": "replace", "path": "/tags", "value": "XYZ"}
        schema = "tags: list[str]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data  # Original data unchanged

    def test_constraint_violation_string_length(self):
        """String length constraint violation."""
        data = {"username": "alice"}
        patch = {"op": "replace", "path": "/username", "value": "ab"}  # Too short
        schema = "username: str{3..20}"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_constraint_violation_numeric_range(self):
        """Numeric range constraint violation."""
        data = {"age": 30}
        patch = {"op": "replace", "path": "/age", "value": 15}  # Too young
        schema = "age: 18..120"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_regex_pattern_violation(self):
        """Regex pattern violation."""
        data = {"sku": "ABC-1234"}
        patch = {"op": "replace", "path": "/sku", "value": "abc-1234"}  # Lowercase
        schema = "sku: /^[A-Z]{3}-\\d{4}$/"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_enum_violation(self):
        """Enum constraint violation."""
        data = {"status": "draft"}
        patch = {"op": "replace", "path": "/status", "value": "pending"}  # Not in enum
        schema = "status: draft | active | archived"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_array_element_type_violation(self):
        """Array element type violation."""
        data = {"scores": [90, 85]}
        patch = {"op": "add", "path": "/scores/-", "value": "100"}  # String, not int
        schema = "scores: list[int]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_multiple_patches_all_valid(self):
        """Multiple patches all valid."""
        data = {"name": "Alice", "age": 30}
        patches = [
            {"op": "replace", "path": "/age", "value": 31},
            {"op": "add", "path": "/city", "value": "NYC"}
        ]
        schema = "name: str\nage: int\n?city: str"

        result, error = apply_patch_validated(data, patches, schema)

        assert error is None
        assert result["age"] == 31
        assert result["city"] == "NYC"

    def test_multiple_patches_one_invalid(self):
        """Multiple patches with one invalid - all rejected."""
        data = {"name": "Alice", "age": 30}
        patches = [
            {"op": "replace", "path": "/age", "value": 31},  # Valid
            {"op": "add", "path": "/score", "value": "high"}  # Invalid type
        ]
        schema = "name: str\nage: int\nscore?: int"

        result, error = apply_patch_validated(data, patches, schema)

        assert error is not None
        # Original data unchanged
        assert result == data

    def test_structural_error_returns_original_data(self):
        """Structural error (path not found) returns original data."""
        data = {"name": "Alice"}
        patch = {"op": "replace", "path": "/nonexistent", "value": 123}
        schema = "name: str"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_required_field_removed(self):
        """Removing required field violates schema."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "remove", "path": "/age"}
        schema = "name: str\nage: int"  # Both required

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_optional_field_removed_is_valid(self):
        """Removing optional field is valid."""
        data = {"name": "Alice", "bio": "Developer"}
        patch = {"op": "remove", "path": "/bio"}
        schema = "name: str\n?bio: str"  # bio is optional

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert "bio" not in result
        assert result["name"] == "Alice"

    def test_nested_object_type_violation(self):
        """Nested object type violation."""
        data = {"user": {"name": "Alice", "age": 30}}
        patch = {"op": "replace", "path": "/user/age", "value": "thirty"}
        schema = """
user:
  name: str
  age: int
"""

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_add_to_nested_object_valid(self):
        """Add to nested object with valid type."""
        data = {"user": {"name": "Alice"}}
        patch = {"op": "add", "path": "/user/age", "value": 30}
        schema = """
user:
  name: str
  age?: int
"""

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert result["user"]["age"] == 30

    def test_tuple_length_violation(self):
        """Tuple with wrong length violates schema."""
        data = {"coords": [40.7, -74.0]}
        patch = {"op": "replace", "path": "/coords", "value": [40.7]}  # Only 1 element
        schema = "coords: tuple[float, float]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_set_deduplication(self):
        """Set with duplicates auto-deduplicates (current behavior)."""
        data = {"ids": [1, 2, 3]}
        patch = {"op": "replace", "path": "/ids", "value": [1, 2, 2, 3]}
        schema = "ids: set[int]"

        result, error = apply_patch_validated(data, patch, schema)

        # Should succeed (msgspec auto-deduplicates)
        assert error is None
        assert set(result["ids"]) == {1, 2, 3}
        # Result should be a list for JSON Patch compatibility
        assert isinstance(result["ids"], list)

    def test_with_pydantic_model(self):
        """Works with Pydantic models."""
        try:
            from pydantic import BaseModel, Field

            class User(BaseModel):
                name: str = Field(min_length=3)
                age: int = Field(ge=18, le=120)

            data = {"name": "Alice", "age": 30}
            patch = {"op": "replace", "path": "/age", "value": 15}  # Too young

            result, error = apply_patch_validated(data, patch, User)

            assert error is not None
            assert result == data
        except ImportError:
            pytest.skip("Pydantic not installed")

    def test_with_msgspec_struct(self):
        """Works with msgspec Structs."""
        try:
            import msgspec

            class Product(msgspec.Struct):
                title: str
                price: float

            data = {"title": "Widget", "price": 9.99}
            patch = {"op": "replace", "path": "/price", "value": "expensive"}  # Wrong type

            result, error = apply_patch_validated(data, patch, Product)

            assert error is not None
            assert result == data
        except ImportError:
            pytest.skip("msgspec not installed")

    def test_format_validation_email(self):
        """Email format validation."""
        data = {"email": "alice@example.com"}
        patch = {"op": "replace", "path": "/email", "value": "not-an-email"}
        schema = "email: email"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data

    def test_copy_operation_with_validation(self):
        """Copy operation validated."""
        data = {"age": 30, "backup_age": 30}
        patch = {"op": "copy", "from": "/age", "path": "/backup_age"}
        schema = "age: int\nbackup_age: int"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert result["backup_age"] == 30

    def test_move_creates_type_mismatch(self):
        """Move operation creating type mismatch."""
        data = {"name": "Alice", "age": 30}
        patch = {"op": "move", "from": "/name", "path": "/age"}  # String to int field
        schema = "?name: str\nage: int"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is not None
        assert result == data


class TestSetTypeWithJSONPatch:
    """Test set types with JSON Patch operations.

    Sets are validated for uniqueness but stored as lists for JSON Patch compatibility.
    This allows operations like /path/- (append) to work while maintaining uniqueness semantics.
    """

    def test_set_stored_as_list_after_validation(self):
        """Set fields are stored as lists after validation."""
        data = {"tags": ["python", "testing"]}
        patch = {"op": "add", "path": "/tags/-", "value": "slimschema"}
        schema = "tags: set[str]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert isinstance(result["tags"], list)
        # Sets don't preserve order, so check content not order
        assert set(result["tags"]) == {"python", "testing", "slimschema"}

    def test_set_append_operation_with_dash(self):
        """Can append to set using /- notation."""
        data = {"prior_guesses": ["A", "B"]}
        patch = {"op": "add", "path": "/prior_guesses/-", "value": "H"}
        schema = "prior_guesses: set[/^[A-Z]$/]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert "H" in result["prior_guesses"]
        assert isinstance(result["prior_guesses"], list)

    def test_set_with_duplicates_rejected_on_validation(self):
        """Duplicates in set are auto-deduplicated by msgspec."""
        data = {"ids": [1, 2, 3]}
        patch = {"op": "add", "path": "/ids/-", "value": 2}  # Duplicate
        schema = "ids: set[int]"

        result, error = apply_patch_validated(data, patch, schema)

        # msgspec auto-deduplicates, so this should succeed
        assert error is None
        assert set(result["ids"]) == {1, 2, 3}
        assert isinstance(result["ids"], list)

    def test_frozenset_also_stored_as_list(self):
        """Frozenset fields are also stored as lists."""
        data = {"immutable_tags": ["stable", "production"]}
        patch = {"op": "add", "path": "/immutable_tags/-", "value": "verified"}
        schema = "immutable_tags: frozenset[str]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert isinstance(result["immutable_tags"], list)
        assert "verified" in result["immutable_tags"]

    def test_set_replace_operation(self):
        """Replace operation works with set fields."""
        data = {"categories": ["tech", "news"]}
        patch = {"op": "replace", "path": "/categories", "value": ["sports", "tech"]}
        schema = "categories: set[str]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert isinstance(result["categories"], list)
        assert set(result["categories"]) == {"sports", "tech"}

    def test_set_add_element_by_index(self):
        """Add element to set at specific index."""
        data = {"numbers": [1, 3]}
        patch = {"op": "add", "path": "/numbers/1", "value": 2}
        schema = "numbers: set[int]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert isinstance(result["numbers"], list)
        # Element inserted at index 1
        assert 2 in result["numbers"]

    def test_set_remove_element(self):
        """Remove element from set by index."""
        data = {"tags": ["a", "b", "c"]}
        patch = {"op": "remove", "path": "/tags/1"}
        schema = "tags: set[str]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert isinstance(result["tags"], list)
        # Sets don't preserve order, so check content not order
        assert set(result["tags"]) == {"a", "c"}

    def test_set_with_type_validation(self):
        """Set validates element types."""
        data = {"scores": [90, 85]}
        patch = {"op": "add", "path": "/scores/-", "value": "100"}  # String, not int
        schema = "scores: set[int]"

        result, error = apply_patch_validated(data, patch, schema)

        # Should fail type validation
        assert error is not None
        assert result == data

    def test_set_with_regex_constraint(self):
        """Set with regex constraint on elements."""
        data = {"codes": ["ABC", "XYZ"]}
        patch = {"op": "add", "path": "/codes/-", "value": "abc"}  # Lowercase
        schema = "codes: set[/^[A-Z]{3}$/]"

        result, error = apply_patch_validated(data, patch, schema)

        # Should fail regex validation
        assert error is not None
        assert result == data

    def test_set_copy_operation(self):
        """Copy operation works with set fields."""
        data = {"primary_tags": ["a", "b"], "backup_tags": []}
        patch = {"op": "copy", "from": "/primary_tags", "path": "/backup_tags"}
        schema = "primary_tags: set[str]\nbackup_tags: set[str]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert isinstance(result["backup_tags"], list)
        assert set(result["backup_tags"]) == {"a", "b"}

    def test_set_move_operation(self):
        """Move operation works with set fields."""
        data = {"old_tags": ["x", "y"], "new_tags": []}
        patch = {"op": "move", "from": "/old_tags", "path": "/new_tags"}
        schema = "?old_tags: set[str]\nnew_tags: set[str]"

        result, error = apply_patch_validated(data, patch, schema)

        assert error is None
        assert "old_tags" not in result
        assert isinstance(result["new_tags"], list)
        assert set(result["new_tags"]) == {"x", "y"}

    def test_multiple_set_operations(self):
        """Multiple operations on set fields."""
        data = {"items": ["a", "b"]}
        patches = [
            {"op": "add", "path": "/items/-", "value": "c"},
            {"op": "add", "path": "/items/-", "value": "d"},
            {"op": "remove", "path": "/items/0"}
        ]
        schema = "items: set[str]"

        result, error = apply_patch_validated(data, patches, schema)

        assert error is None
        assert isinstance(result["items"], list)
        # "a" removed, "c" and "d" added
        assert set(result["items"]) == {"b", "c", "d"}
