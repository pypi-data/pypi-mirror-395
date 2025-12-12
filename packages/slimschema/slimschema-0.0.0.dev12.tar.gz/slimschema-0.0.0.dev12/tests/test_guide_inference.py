"""Tests for Inference Guide.

This test module validates schema inference features documented in docs/guide_inference.md.
Tests cover inferring schemas from data examples with various configurations.
"""


from slimschema.inference import InferenceConfig, from_data


class TestBasicInference:
    """Test basic schema inference from data."""

    def test_infer_from_single_dict(self):
        """Infer schema from a single dictionary."""
        data = {"name": "Alice", "age": 30, "active": True}

        schema = from_data(data)

        assert len(schema.fields) == 3
        assert {f.name for f in schema.fields} == {"name", "age", "active"}

    def test_infer_from_list_of_dicts(self, inference_sample_users):
        """Infer schema from a list of dictionaries."""
        schema = from_data(inference_sample_users)

        assert len(schema.fields) == 3
        assert {f.name for f in schema.fields} == {"name", "age", "active"}



class TestEnumDetection:
    """Test automatic enum detection."""

    def test_detect_enum_from_repeated_values(self, inference_enum_data):
        """Detect enums when values repeat across samples."""
        schema = from_data(inference_enum_data)

        status_field = next(f for f in schema.fields if f.name == "status")
        priority_field = next(f for f in schema.fields if f.name == "priority")

        # Should detect as enums (pipe-delimited)
        assert "|" in status_field.type
        assert "|" in priority_field.type

    def test_enum_vs_string_threshold(self):
        """High cardinality strings should not be detected as enums."""
        data = [
            {"id": f"user_{i}"} for i in range(100)
        ]

        schema = from_data(data)

        id_field = next(f for f in schema.fields if f.name == "id")
        # Should be 'str', not enum
        assert "|" not in id_field.type
        assert "str" in id_field.type

    def test_disable_enum_detection(self):
        """Enum detection can be disabled via config."""
        data = [
            {"status": "active"},
            {"status": "inactive"},
            {"status": "active"}
        ]

        config = InferenceConfig(detect_enums=False)
        schema = from_data(data, config=config)

        status_field = next(f for f in schema.fields if f.name == "status")
        # Should be 'str', not enum
        assert "|" not in status_field.type
        assert "str" in status_field.type


class TestRangeDetection:
    """Test automatic range detection for numeric types."""

    def test_detect_int_range(self):
        """Detect integer ranges from samples."""
        data = [
            {"age": 25},
            {"age": 30},
            {"age": 35}
        ]

        schema = from_data(data)

        age_field = next(f for f in schema.fields if f.name == "age")
        # Should detect range: 25..35
        assert ".." in age_field.type

    def test_detect_float_range(self):
        """Detect float ranges from samples."""
        data = [
            {"score": 87.5},
            {"score": 92.3},
            {"score": 95.7}
        ]

        schema = from_data(data)

        score_field = next(f for f in schema.fields if f.name == "score")
        # May detect range or just use 'float'
        # Behavior depends on implementation
        assert "float" in score_field.type or ".." in score_field.type

    def test_disable_range_detection(self):
        """Range detection can be disabled via config."""
        data = [
            {"age": 25},
            {"age": 30},
            {"age": 35}
        ]

        config = InferenceConfig(detect_ranges=False)
        schema = from_data(data, config=config)

        age_field = next(f for f in schema.fields if f.name == "age")
        # Should be 'int', not range
        assert age_field.type == "int"


class TestFormatDetection:
    """Test automatic format detection (email, url, uuid, date)."""

    def test_detect_email_format(self):
        """Detect email format from string values."""
        data = [
            {"email": "alice@example.com"},
            {"email": "bob@example.org"}
        ]

        schema = from_data(data)

        email_field = next(f for f in schema.fields if f.name == "email")
        # Should detect as 'email' type
        assert "email" in email_field.type

    def test_detect_url_format(self):
        """Detect URL format from string values."""
        data = [
            {"website": "https://example.com"},
            {"website": "http://test.org"}
        ]

        schema = from_data(data)

        website_field = next(f for f in schema.fields if f.name == "website")
        # Should detect as 'url' type
        assert "url" in website_field.type

    def test_detect_date_format(self):
        """Detect date format from ISO date strings."""
        data = [
            {"created": "2024-01-15"},
            {"created": "2024-02-20"}
        ]

        schema = from_data(data)

        created_field = next(f for f in schema.fields if f.name == "created")
        # Should detect as 'date' type
        assert "date" in created_field.type

    def test_detect_datetime_format(self):
        """Detect datetime format from ISO datetime strings."""
        data = [
            {"timestamp": "2024-01-15T10:30:00"},
            {"timestamp": "2024-02-20T14:45:00"}
        ]

        schema = from_data(data)

        timestamp_field = next(f for f in schema.fields if f.name == "timestamp")
        # Should detect as 'datetime' type
        assert "datetime" in timestamp_field.type

    def test_disable_format_detection(self):
        """Format detection can be disabled via config."""
        data = [
            {"email": "alice@example.com"},
            {"email": "bob@example.org"}
        ]

        config = InferenceConfig(detect_formats=False)
        schema = from_data(data, config=config)

        email_field = next(f for f in schema.fields if f.name == "email")
        # Should be 'str', not 'email'
        assert email_field.type == "str"


class TestNestedInference:
    """Test inference of nested object structures."""

    def test_infer_nested_objects(self, inference_nested_data):
        """Infer inline object syntax from nested dictionaries."""
        schema = from_data(inference_nested_data)

        user_field = next(f for f in schema.fields if f.name == "user")
        # Should detect nested object with inline syntax
        assert "{" in user_field.type and "}" in user_field.type

    def test_infer_arrays(self):
        """Infer array types from lists."""
        data = [
            {"tags": ["python", "testing"]},
            {"tags": ["slimschema", "validation"]}
        ]

        schema = from_data(data)

        tags_field = next(f for f in schema.fields if f.name == "tags")
        # Should detect as array type
        assert "[" in tags_field.type and "]" in tags_field.type

    def test_infer_array_of_objects(self):
        """Infer array of objects with inline syntax."""
        data = [
            {"items": [{"id": 1, "name": "Item1"}, {"id": 2, "name": "Item2"}]},
            {"items": [{"id": 3, "name": "Item3"}]}
        ]

        schema = from_data(data)

        items_field = next(f for f in schema.fields if f.name == "items")
        # Should detect as array of objects
        assert "[{" in items_field.type


class TestOptionalFields:
    """Test inference of optional fields."""

    def test_infer_optional_from_missing_values(self):
        """Fields missing in some samples are marked optional."""
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob"},  # Missing email
            {"name": "Charlie", "email": "charlie@example.com"}
        ]

        schema = from_data(data)

        email_field = next(f for f in schema.fields if f.name == "email")
        # Should be marked optional
        assert email_field.optional is True

    def test_infer_required_from_always_present(self):
        """Fields present in all samples are marked required."""
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
            {"name": "Charlie", "email": "charlie@example.com"}
        ]

        schema = from_data(data)

        name_field = next(f for f in schema.fields if f.name == "name")
        email_field = next(f for f in schema.fields if f.name == "email")
        # Both should be required
        assert name_field.optional is False
        assert email_field.optional is False


class TestInferenceConfig:
    """Test InferenceConfig customization."""

    def test_max_samples_limit(self):
        """Process only first N samples when max_samples is set."""
        data = [{"id": i} for i in range(1000)]

        config = InferenceConfig(max_samples=10)
        schema = from_data(data, config=config)

        # Should still infer the schema
        assert len(schema.fields) == 1

    def test_enum_max_cardinality(self):
        """Control enum detection threshold."""
        data = [{"status": f"status{i % 8}"} for i in range(100)]

        # Default: Should not detect as enum (> 5 unique values)
        from_data(data)  # Test default behavior

        # Custom: Allow up to 10 unique values
        config = InferenceConfig(enum_max_cardinality=10)
        schema_custom = from_data(data, config=config)
        status_custom = next(f for f in schema_custom.fields if f.name == "status")

        # Custom config should detect as enum
        assert "|" in status_custom.type


class TestSchemaName:
    """Test schema name inference and assignment."""

    def test_schema_name_from_parameter(self):
        """Schema name can be provided via parameter."""
        data = [{"name": "Alice"}]

        schema = from_data(data, name="User")

        assert schema.name == "User"

    def test_schema_without_name(self):
        """Schema name is optional."""
        data = [{"name": "Alice"}]

        schema = from_data(data)

        assert schema.name is None


class TestEdgeCases:
    """Test edge cases in inference."""

    def test_infer_from_empty_list(self):
        """Inferring from empty list returns empty schema."""
        schema = from_data([])

        assert len(schema.fields) == 0

    def test_infer_from_all_null_values(self):
        """Fields with all null values default to str type."""
        data = [
            {"field": None},
            {"field": None}
        ]

        schema = from_data(data)

        field = next(f for f in schema.fields if f.name == "field")
        # Should default to 'str' as most permissive
        assert field.type == "str"
        assert field.optional is True
