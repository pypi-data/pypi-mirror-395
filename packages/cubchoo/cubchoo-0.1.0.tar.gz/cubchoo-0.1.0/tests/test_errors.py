"""Comprehensive tests for error messages and error handling."""

import pandas as pd
import pytest

from cubchoo import to_pandas_schema, to_polars_schema
from cubchoo.errors import ConversionError, SchemaError, UnsupportedTypeError
from cubchoo.type_mappings import (
    get_pandas_dtype_from_polars_type,
    get_polars_type_from_pandas_dtype,
)


class TestSchemaErrorMessages:
    """Tests for SchemaError messages."""

    def test_empty_schema_error_message(self):
        """Test that empty schema error message is informative."""
        with pytest.raises(SchemaError, match="cannot be empty"):
            to_polars_schema({})

        with pytest.raises(SchemaError, match="cannot be empty"):
            to_pandas_schema({})

    def test_duplicate_field_names_error_message(self):
        """Test that duplicate field names error includes field names."""
        schema = [
            ("name", "string"),
            ("name", "Int64"),
        ]
        with pytest.raises(SchemaError, match="Duplicate field names"):
            to_polars_schema(schema)

        with pytest.raises(SchemaError, match="Duplicate field names"):
            to_pandas_schema(schema)

    def test_empty_field_name_error_message(self):
        """Test that empty field name error is informative."""
        schema = {"": "string"}
        with pytest.raises(SchemaError, match="Empty or invalid field names"):
            to_polars_schema(schema)

        with pytest.raises(SchemaError, match="Empty or invalid field names"):
            to_pandas_schema(schema)

    def test_none_dtype_error_message(self):
        """Test that None dtype error includes field name."""
        schema = {"field_name": None}
        with pytest.raises(SchemaError, match="has None dtype"):
            to_polars_schema(schema)

        schema = {"field_name": None}
        with pytest.raises(SchemaError, match="has None type"):
            to_pandas_schema(schema)

    def test_invalid_format_error_message(self):
        """Test that invalid format error is informative."""
        with pytest.raises(SchemaError, match="Invalid"):
            to_polars_schema("invalid")  # type: ignore[arg-type]

        with pytest.raises(SchemaError, match="Invalid"):
            to_pandas_schema("invalid")  # type: ignore[arg-type]

    def test_unnamed_series_error_message(self):
        """Test that unnamed Series error is informative."""
        series = pd.Series([1, 2, 3], dtype="Int64")
        with pytest.raises(SchemaError, match="unnamed pandas Series"):
            to_polars_schema(series)

    def test_malformed_tuple_error_message(self):
        """Test that malformed tuple error is informative."""
        schema = [("name",)]  # Wrong length
        with pytest.raises(SchemaError, match="Invalid"):
            to_polars_schema(schema)  # type: ignore[arg-type]

    def test_invalid_field_name_type_error(self):
        """Test error for invalid field name types."""
        schema = {123: "string"}  # type: ignore[dict-item]
        with pytest.raises(SchemaError, match="Empty or invalid field names"):
            to_polars_schema(schema)

    def test_error_includes_field_name(self):
        """Test that errors include the problematic field name."""
        schema = {
            "valid_field": "string",
            "invalid_field": None,
        }
        with pytest.raises(SchemaError, match="invalid_field"):
            to_polars_schema(schema)


class TestUnsupportedTypeErrorMessages:
    """Tests for UnsupportedTypeError messages."""

    def test_unsupported_pandas_dtype_error_message(self):
        """Test that unsupported pandas dtype error includes the type."""
        with pytest.raises(UnsupportedTypeError, match="Unsupported pandas dtype"):
            get_polars_type_from_pandas_dtype("unsupported_type")

    def test_unsupported_type_error_includes_supported_types(self):
        """Test that error message includes supported types."""
        with pytest.raises(UnsupportedTypeError, match="Supported types include"):
            get_polars_type_from_pandas_dtype("invalid_type")

    def test_unsupported_polars_type_error_message(self):
        """Test that unsupported Polars type error is informative."""

        class UnsupportedType:
            pass

        with pytest.raises(UnsupportedTypeError, match="Unsupported"):
            get_pandas_dtype_from_polars_type(UnsupportedType())

    def test_unsupported_type_in_schema_error(self):
        """Test that unsupported type in schema includes field name."""
        schema = {
            "valid_field": "string",
            "invalid_field": "unsupported_type",
        }
        with pytest.raises(UnsupportedTypeError, match="invalid_field"):
            to_polars_schema(schema)


class TestErrorContext:
    """Tests for error context and chaining."""

    def test_error_preserves_original_exception(self):
        """Test that errors preserve original exception context."""
        schema = {
            "field": "unsupported_type",
        }
        with pytest.raises(UnsupportedTypeError) as exc_info:
            to_polars_schema(schema)

        # Error should include field name
        assert "field" in str(exc_info.value) or "Failed to convert field" in str(exc_info.value)

    def test_nested_error_messages(self):
        """Test that nested errors provide context."""
        schema = {
            "field1": "string",
            "field2": "unsupported_type",
            "field3": "Int64",
        }
        with pytest.raises(UnsupportedTypeError) as exc_info:
            to_polars_schema(schema)

        # Should mention field2
        error_msg = str(exc_info.value)
        assert "field2" in error_msg or "Failed to convert field" in error_msg


class TestErrorTypes:
    """Tests for different error types."""

    def test_schema_error_type(self):
        """Test that SchemaError is raised for schema issues."""
        with pytest.raises(SchemaError):
            to_polars_schema({})

        assert isinstance(SchemaError("test"), Exception)

    def test_unsupported_type_error_type(self):
        """Test that UnsupportedTypeError is raised for type issues."""
        with pytest.raises(UnsupportedTypeError):
            get_polars_type_from_pandas_dtype("invalid")

        assert isinstance(UnsupportedTypeError("test"), Exception)

    def test_conversion_error_type(self):
        """Test that ConversionError exists and is a valid exception."""
        # ConversionError may not be used directly, but should exist
        assert issubclass(ConversionError, Exception)


class TestErrorEdgeCases:
    """Tests for error edge cases."""

    def test_multiple_errors_in_schema(self):
        """Test schema with multiple errors (should report first one)."""
        schema = {
            "": "string",  # Empty field name
            "field": None,  # None dtype
        }
        # Should catch one of the errors
        with pytest.raises(SchemaError):
            to_polars_schema(schema)

    def test_error_with_special_characters_in_field_name(self):
        """Test error message with special characters in field name."""
        schema = {
            "field-with-special-chars!@#": "unsupported_type",
        }
        with pytest.raises(UnsupportedTypeError) as exc_info:
            to_polars_schema(schema)

        error_msg = str(exc_info.value)
        # Should handle special characters in error message
        assert "field" in error_msg or "Failed to convert" in error_msg

    def test_error_with_very_long_field_name(self):
        """Test error message with very long field name."""
        long_name = "a" * 1000
        schema = {long_name: "unsupported_type"}
        with pytest.raises(UnsupportedTypeError) as exc_info:
            to_polars_schema(schema)

        error_msg = str(exc_info.value)
        # Should handle long field names
        assert len(error_msg) > 0

    def test_error_with_unicode_field_name(self):
        """Test error message with unicode field name."""
        schema = {
            "field_中文": "unsupported_type",
        }
        with pytest.raises(UnsupportedTypeError) as exc_info:
            to_polars_schema(schema)

        error_msg = str(exc_info.value)
        # Should handle unicode in error message
        assert "field" in error_msg or "Failed to convert" in error_msg


class TestErrorRecovery:
    """Tests for error recovery scenarios."""

    def test_partial_schema_conversion(self):
        """Test that one error doesn't prevent seeing other errors."""
        # This test ensures error reporting is clear
        schema = {
            "valid1": "string",
            "invalid": "unsupported_type",
            "valid2": "Int64",
        }
        # Should raise error for invalid field
        with pytest.raises(UnsupportedTypeError):
            to_polars_schema(schema)

    def test_error_message_clarity(self):
        """Test that error messages are clear and actionable."""
        schema = {"field": "invalid_type"}
        with pytest.raises(UnsupportedTypeError) as exc_info:
            to_polars_schema(schema)

        error_msg = str(exc_info.value)
        # Error should be informative
        assert len(error_msg) > 20  # Should have some detail
        assert (
            "field" in error_msg or "Failed to convert" in error_msg or "Unsupported" in error_msg
        )
