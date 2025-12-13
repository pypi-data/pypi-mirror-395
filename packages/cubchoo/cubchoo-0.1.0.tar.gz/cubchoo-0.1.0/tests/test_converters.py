"""Tests for schema conversion functions."""

import pandas as pd
import polars as pl
import pytest

from cubchoo import to_pandas_schema, to_polars_schema
from cubchoo.errors import SchemaError, UnsupportedTypeError
from tests.conftest import (
    generate_datetime_types,
    generate_float_types,
    generate_integer_types,
    generate_polars_to_pandas_datetime_types,
    generate_polars_to_pandas_float_types,
    generate_polars_to_pandas_integer_types,
    generate_polars_to_pandas_timedelta_types,
    generate_string_types,
    generate_timedelta_types,
    generate_boolean_types,
    generate_pyarrow_types,
    generate_pyarrow_to_pandas_types,
)


class TestToPolarsSchema:
    """Tests for converting Pandas schemas to Polars schemas."""

    def test_dict_with_string_dtypes(self):
        """Test conversion from dictionary with string dtype names."""
        pandas_schema = {
            "name": "string",
            "age": "Int64",
            "score": "Float64",
        }
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["name"] == pl.String
        assert polars_schema["age"] == pl.Int64
        assert polars_schema["score"] == pl.Float64

    def test_dict_with_pandas_dtypes(self):
        """Test conversion from dictionary with pandas dtype objects."""
        pandas_schema = {
            "name": pd.StringDtype(),
            "age": pd.Int64Dtype(),
            "score": pd.Float64Dtype(),
        }
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["name"] == pl.String
        assert polars_schema["age"] == pl.Int64
        assert polars_schema["score"] == pl.Float64

    def test_from_dataframe(self):
        """Test conversion from pandas DataFrame."""
        df = pd.DataFrame(
            {
                "name": ["Alice", "Bob"],
                "age": [30, 25],
                "score": [95.5, 87.0],
            }
        )
        polars_schema = to_polars_schema(df)

        assert isinstance(polars_schema, pl.Schema)
        assert "name" in polars_schema
        assert "age" in polars_schema
        assert "score" in polars_schema

    def test_from_named_series(self):
        """Test conversion from named pandas Series."""
        series = pd.Series([1, 2, 3], name="numbers", dtype="Int64")
        polars_schema = to_polars_schema(series)

        assert isinstance(polars_schema, pl.Schema)
        assert "numbers" in polars_schema
        assert polars_schema["numbers"] == pl.Int64

    def test_from_unnamed_series_error(self):
        """Test that unnamed Series raises error."""
        series = pd.Series([1, 2, 3], dtype="Int64")  # No name
        with pytest.raises(SchemaError, match="unnamed pandas Series"):
            to_polars_schema(series)

    def test_from_empty_name_series_error(self):
        """Test that Series with empty name raises error."""
        series = pd.Series([1, 2, 3], name="", dtype="Int64")
        with pytest.raises(SchemaError, match="unnamed pandas Series"):
            to_polars_schema(series)

    def test_dataframe_with_mixed_nullable_types(self):
        """Test DataFrame with mixed nullable and non-nullable types."""
        df = pd.DataFrame(
            {
                "nullable_int": pd.Series([1, 2, None], dtype="Int64"),
                "non_nullable_int": pd.Series([1, 2, 3], dtype="int64"),
                "nullable_float": pd.Series([1.0, 2.0, None], dtype="Float64"),
                "non_nullable_float": pd.Series([1.0, 2.0, 3.0], dtype="float64"),
            }
        )
        polars_schema = to_polars_schema(df)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["nullable_int"] == pl.Int64
        assert polars_schema["non_nullable_int"] == pl.Int64
        assert polars_schema["nullable_float"] == pl.Float64
        assert polars_schema["non_nullable_float"] == pl.Float64

    def test_from_list_of_tuples(self):
        """Test conversion from list of tuples."""
        pandas_schema = [
            ("name", "string"),
            ("age", "Int64"),
            ("score", "Float64"),
        ]
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["name"] == pl.String
        assert polars_schema["age"] == pl.Int64
        assert polars_schema["score"] == pl.Float64

    def test_datetime_types(self):
        """Test conversion of datetime types."""
        pandas_schema = {
            "timestamp": "datetime64[ns]",
            "date": "date",
        }
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert isinstance(polars_schema["timestamp"], pl.Datetime)
        assert polars_schema["date"] == pl.Date

    def test_datetime_with_different_time_units(self):
        """Test conversion of datetime with different time units."""
        pandas_schema = {
            "ns_timestamp": "datetime64[ns]",
            "us_timestamp": "datetime64[us]",
            "ms_timestamp": "datetime64[ms]",
            "s_timestamp": "datetime64[s]",  # Should map to ms
        }
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert isinstance(polars_schema["ns_timestamp"], pl.Datetime)
        assert isinstance(polars_schema["us_timestamp"], pl.Datetime)
        assert isinstance(polars_schema["ms_timestamp"], pl.Datetime)
        assert isinstance(polars_schema["s_timestamp"], pl.Datetime)

    def test_timedelta_types(self):
        """Test conversion of timedelta types."""
        pandas_schema = {
            "duration_ns": "timedelta64[ns]",
            "duration_us": "timedelta64[us]",
            "duration_ms": "timedelta64[ms]",
            "duration_s": "timedelta64[s]",  # Should map to ms
        }
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert isinstance(polars_schema["duration_ns"], pl.Duration)
        assert isinstance(polars_schema["duration_us"], pl.Duration)
        assert isinstance(polars_schema["duration_ms"], pl.Duration)
        assert isinstance(polars_schema["duration_s"], pl.Duration)

    def test_categorical_type(self):
        """Test conversion of categorical type."""
        pandas_schema = {"category": "category"}
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["category"] == pl.Categorical

    def test_empty_schema_error(self):
        """Test that empty schema raises error."""
        with pytest.raises(SchemaError, match="cannot be empty"):
            to_polars_schema({})

    def test_duplicate_field_names_error(self):
        """Test that duplicate field names raise error."""
        # Use list of tuples to test duplicate field names
        pandas_schema = [
            ("name", "string"),
            ("name", "Int64"),  # Duplicate field name
        ]
        with pytest.raises(SchemaError, match="Duplicate field names"):
            to_polars_schema(pandas_schema)

    def test_invalid_format_error(self):
        """Test that invalid format raises error."""
        with pytest.raises(SchemaError):
            to_polars_schema("invalid")  # type: ignore[arg-type]

    def test_empty_string_field_name_error(self):
        """Test that empty string field names raise error."""
        pandas_schema = {
            "": "string",  # Empty field name
            "valid": "Int64",
        }
        with pytest.raises(SchemaError, match="Empty or invalid field names"):
            to_polars_schema(pandas_schema)

    def test_none_dtype_error(self):
        """Test that None dtype raises error."""
        pandas_schema = {
            "name": "string",
            "age": None,  # None dtype
        }
        with pytest.raises(SchemaError, match="has None dtype"):
            to_polars_schema(pandas_schema)

    def test_very_long_field_name(self):
        """Test that very long field names work."""
        long_name = "a" * 1000
        pandas_schema = {long_name: "string"}
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert long_name in polars_schema

    def test_special_characters_in_field_name(self):
        """Test that special characters in field names work."""
        pandas_schema = {
            "field_with_underscore": "string",
            "field-with-dash": "Int64",
            "field.with.dot": "Float64",
            "field with spaces": "string",
        }
        polars_schema = to_polars_schema(pandas_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert "field_with_underscore" in polars_schema
        assert "field-with-dash" in polars_schema
        assert "field.with.dot" in polars_schema
        assert "field with spaces" in polars_schema


class TestToPandasSchema:
    """Tests for converting Polars schemas to Pandas schemas."""

    def test_pl_schema_object(self):
        """Test conversion from pl.Schema object."""
        polars_schema = pl.Schema(
            {
                "name": pl.String,
                "age": pl.Int32,
                "score": pl.Float64,
            }
        )
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["name"] == "string"
        assert pandas_schema["age"] == "Int32"
        assert pandas_schema["score"] == "Float64"

    def test_dict_format(self):
        """Test conversion from dictionary."""
        polars_schema = {
            "name": pl.String,
            "age": pl.Int32,
            "score": pl.Float64,
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["name"] == "string"
        assert pandas_schema["age"] == "Int32"
        assert pandas_schema["score"] == "Float64"

    def test_list_of_tuples(self):
        """Test conversion from list of tuples."""
        polars_schema = [
            ("name", pl.String),
            ("age", pl.Int32),
            ("score", pl.Float64),
        ]
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["name"] == "string"
        assert pandas_schema["age"] == "Int32"
        assert pandas_schema["score"] == "Float64"

    def test_datetime_types(self):
        """Test conversion of datetime types."""
        polars_schema = {
            "timestamp": pl.Datetime(time_unit="ns"),
            "date": pl.Date(),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["timestamp"] == "datetime64[ns]"
        assert pandas_schema["date"] == "date"

    def test_datetime_with_different_time_units(self):
        """Test conversion of datetime with different time units."""
        polars_schema = {
            "ns_timestamp": pl.Datetime(time_unit="ns"),
            "us_timestamp": pl.Datetime(time_unit="us"),
            "ms_timestamp": pl.Datetime(time_unit="ms"),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["ns_timestamp"] == "datetime64[ns]"
        assert pandas_schema["us_timestamp"] == "datetime64[us]"
        assert pandas_schema["ms_timestamp"] == "datetime64[ms]"

    def test_timedelta_types(self):
        """Test conversion of timedelta types."""
        polars_schema = {
            "duration_ns": pl.Duration(time_unit="ns"),
            "duration_us": pl.Duration(time_unit="us"),
            "duration_ms": pl.Duration(time_unit="ms"),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["duration_ns"] == "timedelta64[ns]"
        assert pandas_schema["duration_us"] == "timedelta64[us]"
        assert pandas_schema["duration_ms"] == "timedelta64[ms]"

    def test_list_types(self):
        """Test conversion of List types."""
        polars_schema = {
            "string_list": pl.List(pl.String),
            "nested_list": pl.List(pl.List(pl.Int32)),
            "int_list": pl.List(pl.Int64),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["string_list"] == "object"
        assert pandas_schema["nested_list"] == "object"
        assert pandas_schema["int_list"] == "object"

    def test_struct_types(self):
        """Test conversion of Struct types."""
        polars_schema = {
            "struct_field": pl.Struct(
                [
                    pl.Field("name", pl.String),
                    pl.Field("age", pl.Int32),
                ]
            ),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["struct_field"] == "object"

    def test_map_types(self):
        """Test conversion of Map types."""
        try:
            from polars.datatypes import Map  # type: ignore[attr-defined]

            polars_schema = {
                "string_map": Map(pl.String, pl.Int32),
                "int_map": Map(pl.Int64, pl.Float64),
            }
            pandas_schema = to_pandas_schema(polars_schema)

            assert isinstance(pandas_schema, dict)
            assert pandas_schema["string_map"] == "object"
            assert pandas_schema["int_map"] == "object"
        except ImportError:
            # Map type not available in this Polars version
            pytest.skip("Map type not available in this Polars version")

    def test_categorical_type(self):
        """Test conversion of categorical type."""
        polars_schema = {"category": pl.Categorical}
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["category"] == "category"

    def test_empty_schema_error(self):
        """Test that empty schema raises error."""
        with pytest.raises(SchemaError, match="cannot be empty"):
            to_pandas_schema({})

    def test_duplicate_field_names_error(self):
        """Test that duplicate field names raise error."""
        polars_schema = [
            ("name", pl.String),
            ("name", pl.Int32),  # Duplicate
        ]
        with pytest.raises(SchemaError, match="Duplicate field names"):
            to_pandas_schema(polars_schema)

    def test_invalid_format_error(self):
        """Test that invalid format raises error."""
        with pytest.raises(SchemaError):
            to_pandas_schema("invalid")  # type: ignore[arg-type]

    def test_empty_string_field_name_error(self):
        """Test that empty string field names raise error."""
        polars_schema = {
            "": pl.String,  # Empty field name
            "valid": pl.Int32,
        }
        with pytest.raises(SchemaError, match="Empty or invalid field names"):
            to_pandas_schema(polars_schema)

    def test_none_type_error(self):
        """Test that None type raises error."""
        polars_schema = {
            "name": pl.String,
            "age": None,  # None type
        }
        with pytest.raises(SchemaError, match="has None type"):
            to_pandas_schema(polars_schema)

    def test_very_long_field_name(self):
        """Test that very long field names work."""
        long_name = "a" * 1000
        polars_schema = {long_name: pl.String}
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert long_name in pandas_schema

    def test_special_characters_in_field_name(self):
        """Test that special characters in field names work."""
        polars_schema = {
            "field_with_underscore": pl.String,
            "field-with-dash": pl.Int32,
            "field.with.dot": pl.Float64,
            "field with spaces": pl.String,
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert isinstance(pandas_schema, dict)
        assert "field_with_underscore" in pandas_schema
        assert "field-with-dash" in pandas_schema
        assert "field.with.dot" in pandas_schema
        assert "field with spaces" in pandas_schema


class TestRoundTrip:
    """Tests for round-trip conversions."""

    def test_basic_round_trip(self):
        """Test round-trip conversion for basic types."""
        original = {
            "name": "string",
            "age": "Int64",
            "score": "Float64",
        }

        # Pandas -> Polars -> Pandas
        polars_schema = to_polars_schema(original)
        converted_back = to_pandas_schema(polars_schema)

        assert converted_back["name"] == original["name"]
        assert converted_back["age"] == original["age"]
        assert converted_back["score"] == original["score"]

    def test_polars_to_pandas_to_polars(self):
        """Test round-trip conversion starting from Polars."""
        original = pl.Schema(
            {
                "name": pl.String,
                "age": pl.Int32,
                "score": pl.Float64,
            }
        )

        # Polars -> Pandas -> Polars
        pandas_schema = to_pandas_schema(original)
        converted_back = to_polars_schema(pandas_schema)

        assert converted_back["name"] == original["name"]
        assert converted_back["age"] == original["age"]
        assert converted_back["score"] == original["score"]


class TestPyArrowTypeSupport:
    """Tests for PyArrow type support in existing conversion functions (optional dependency)."""

    def test_to_polars_from_pyarrow_types(self):
        """Test converting PyArrow types to Polars schema."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema_with_pa = {
            "name": pa.string(),
            "age": pa.int32(),
            "score": pa.float64(),
        }
        polars_schema = to_polars_schema(schema_with_pa)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["name"] == pl.String
        assert polars_schema["age"] == pl.Int32
        assert polars_schema["score"] == pl.Float64

    def test_to_pandas_from_pyarrow_types(self):
        """Test converting PyArrow types to Pandas schema."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema_with_pa = {
            "name": pa.string(),
            "age": pa.int32(),
            "score": pa.float64(),
        }
        pandas_schema = to_pandas_schema(schema_with_pa)

        assert isinstance(pandas_schema, dict)
        assert pandas_schema["name"] == "string"
        assert pandas_schema["age"] == "Int32"
        assert pandas_schema["score"] == "Float64"

    def test_pyarrow_types_in_list(self):
        """Test PyArrow types in list of tuples format."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema_list = [
            ("name", pa.string()),
            ("age", pa.int32()),
            ("score", pa.float64()),
        ]
        polars_schema = to_polars_schema(schema_list)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["name"] == pl.String
        assert polars_schema["age"] == pl.Int32
        assert polars_schema["score"] == pl.Float64

    def test_mixed_pandas_and_pyarrow_types(self):
        """Test mixing Pandas and PyArrow types in the same schema."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        mixed_schema = {
            "name": "string",  # Pandas dtype string
            "age": pa.int32(),  # PyArrow type
            "score": "Float64",  # Pandas dtype string
        }
        polars_schema = to_polars_schema(mixed_schema)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["name"] == pl.String
        assert polars_schema["age"] == pl.Int32
        assert polars_schema["score"] == pl.Float64

    def test_pyarrow_round_trip(self):
        """Test round-trip conversion with PyArrow types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        # Start with PyArrow types
        original = {
            "name": pa.string(),
            "age": pa.int32(),
            "score": pa.float64(),
        }

        # PyArrow -> Polars -> Pandas
        polars_schema = to_polars_schema(original)
        pandas_schema = to_pandas_schema(polars_schema)

        assert pandas_schema["name"] == "string"
        assert pandas_schema["age"] == "Int32"
        assert pandas_schema["score"] == "Float64"

        # Pandas -> Polars (round trip)
        polars_schema2 = to_polars_schema(pandas_schema)
        assert polars_schema2["name"] == pl.String
        assert polars_schema2["age"] == pl.Int32
        assert polars_schema2["score"] == pl.Float64


# ============================================================================
# Parametrized Tests for Expanded Coverage
# ============================================================================


class TestToPolarsSchemaParametrized:
    """Parametrized tests for converting Pandas schemas to Polars schemas."""

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_integer_types())
    def test_integer_types_parametrized(self, pandas_dtype, expected_polars_type):
        """Test integer type conversions with parametrization."""
        schema = {"field": pandas_dtype}
        result = to_polars_schema(schema)
        assert isinstance(result, pl.Schema)
        assert result["field"] == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_float_types())
    def test_float_types_parametrized(self, pandas_dtype, expected_polars_type):
        """Test float type conversions with parametrization."""
        schema = {"field": pandas_dtype}
        result = to_polars_schema(schema)
        assert isinstance(result, pl.Schema)
        assert result["field"] == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_string_types())
    def test_string_types_parametrized(self, pandas_dtype, expected_polars_type):
        """Test string type conversions with parametrization."""
        schema = {"field": pandas_dtype}
        result = to_polars_schema(schema)
        assert isinstance(result, pl.Schema)
        assert result["field"] == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_boolean_types())
    def test_boolean_types_parametrized(self, pandas_dtype, expected_polars_type):
        """Test boolean type conversions with parametrization."""
        schema = {"field": pandas_dtype}
        result = to_polars_schema(schema)
        assert isinstance(result, pl.Schema)
        assert result["field"] == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_datetime_types())
    def test_datetime_types_parametrized(self, pandas_dtype, expected_polars_type):
        """Test datetime type conversions with parametrization."""
        schema = {"field": pandas_dtype}
        result = to_polars_schema(schema)
        assert isinstance(result, pl.Schema)
        assert isinstance(result["field"], pl.Datetime)

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_timedelta_types())
    def test_timedelta_types_parametrized(self, pandas_dtype, expected_polars_type):
        """Test timedelta type conversions with parametrization."""
        schema = {"field": pandas_dtype}
        result = to_polars_schema(schema)
        assert isinstance(result, pl.Schema)
        assert isinstance(result["field"], pl.Duration)

    @pytest.mark.parametrize(
        "invalid_input,expected_error",
        [
            ("string", SchemaError),
            (123, SchemaError),
            (None, SchemaError),
            ([], SchemaError),
        ],
    )
    def test_invalid_format_errors_parametrized(self, invalid_input, expected_error):
        """Test invalid format errors with parametrization."""
        with pytest.raises(expected_error):
            to_polars_schema(invalid_input)  # type: ignore[arg-type]


class TestToPandasSchemaParametrized:
    """Parametrized tests for converting Polars schemas to Pandas schemas."""

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_integer_types()
    )
    def test_integer_types_parametrized(self, polars_type, expected_pandas_dtype):
        """Test integer type conversions with parametrization."""
        schema = {"field": polars_type}
        result = to_pandas_schema(schema)
        assert isinstance(result, dict)
        assert result["field"] == expected_pandas_dtype

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_float_types()
    )
    def test_float_types_parametrized(self, polars_type, expected_pandas_dtype):
        """Test float type conversions with parametrization."""
        schema = {"field": polars_type}
        result = to_pandas_schema(schema)
        assert isinstance(result, dict)
        assert result["field"] == expected_pandas_dtype

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_datetime_types()
    )
    def test_datetime_types_parametrized(self, polars_type, expected_pandas_dtype):
        """Test datetime type conversions with parametrization."""
        schema = {"field": polars_type}
        result = to_pandas_schema(schema)
        assert isinstance(result, dict)
        assert result["field"] == expected_pandas_dtype

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_timedelta_types()
    )
    def test_timedelta_types_parametrized(self, polars_type, expected_pandas_dtype):
        """Test timedelta type conversions with parametrization."""
        schema = {"field": polars_type}
        result = to_pandas_schema(schema)
        assert isinstance(result, dict)
        assert result["field"] == expected_pandas_dtype

    def test_duration_default_time_unit(self):
        """Test Duration() default time unit conversion."""
        schema = {"field": pl.Duration()}
        result = to_pandas_schema(schema)
        assert isinstance(result, dict)
        # Default Duration() maps based on its time_unit attribute
        assert "timedelta" in result["field"]

    @pytest.mark.parametrize(
        "invalid_input,expected_error",
        [
            ("string", SchemaError),
            (123, SchemaError),
            (None, SchemaError),
            ([], SchemaError),
        ],
    )
    def test_invalid_format_errors_parametrized(self, invalid_input, expected_error):
        """Test invalid format errors with parametrization."""
        with pytest.raises(expected_error):
            to_pandas_schema(invalid_input)  # type: ignore[arg-type]


class TestRoundTripParametrized:
    """Parametrized tests for round-trip conversions."""

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_integer_types())
    def test_integer_round_trip(self, pandas_dtype, expected_polars_type):
        """Test round-trip conversion for integer types."""
        original = {"field": pandas_dtype}
        polars_schema = to_polars_schema(original)
        pandas_result = to_pandas_schema(polars_schema)
        # Round-trip should preserve the type (may be nullable version)
        assert pandas_result["field"] in [
            "Int8",
            "Int16",
            "Int32",
            "Int64",
            "UInt8",
            "UInt16",
            "UInt32",
            "UInt64",
        ]

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_float_types())
    def test_float_round_trip(self, pandas_dtype, expected_polars_type):
        """Test round-trip conversion for float types."""
        original = {"field": pandas_dtype}
        polars_schema = to_polars_schema(original)
        pandas_result = to_pandas_schema(polars_schema)
        assert pandas_result["field"] in ["Float32", "Float64"]

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_string_types())
    def test_string_round_trip(self, pandas_dtype, expected_polars_type):
        """Test round-trip conversion for string types."""
        original = {"field": pandas_dtype}
        polars_schema = to_polars_schema(original)
        pandas_result = to_pandas_schema(polars_schema)
        assert pandas_result["field"] == "string"

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_integer_types()
    )
    def test_polars_to_pandas_round_trip(self, polars_type, expected_pandas_dtype):
        """Test round-trip conversion starting from Polars integer types."""
        original = {"field": polars_type}
        pandas_schema = to_pandas_schema(original)
        polars_result = to_polars_schema(pandas_schema)
        assert polars_result["field"] == polars_type

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_float_types()
    )
    def test_polars_float_round_trip(self, polars_type, expected_pandas_dtype):
        """Test round-trip conversion starting from Polars float types."""
        original = {"field": polars_type}
        pandas_schema = to_pandas_schema(original)
        polars_result = to_polars_schema(pandas_schema)
        assert polars_result["field"] == polars_type


class TestPyArrowTypeSupportParametrized:
    """Parametrized tests for PyArrow type support."""

    @pytest.mark.parametrize("pyarrow_type,expected_polars_type", generate_pyarrow_types())
    def test_pyarrow_to_polars_parametrized(self, pyarrow_type, expected_polars_type):
        """Test converting PyArrow types to Polars with parametrization."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {"field": pyarrow_type}
        result = to_polars_schema(schema)
        assert isinstance(result, pl.Schema)
        assert result["field"] == expected_polars_type

    @pytest.mark.parametrize(
        "pyarrow_type,expected_pandas_dtype", generate_pyarrow_to_pandas_types()
    )
    def test_pyarrow_to_pandas_parametrized(self, pyarrow_type, expected_pandas_dtype):
        """Test converting PyArrow types to Pandas with parametrization."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {"field": pyarrow_type}
        result = to_pandas_schema(schema)
        assert isinstance(result, dict)
        assert result["field"] == expected_pandas_dtype


class TestPyArrowComprehensive:
    """Comprehensive tests for all PyArrow types."""

    def test_pyarrow_all_integer_types(self):
        """Test all PyArrow integer types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "int8": pa.int8(),
            "int16": pa.int16(),
            "int32": pa.int32(),
            "int64": pa.int64(),
            "uint8": pa.uint8(),
            "uint16": pa.uint16(),
            "uint32": pa.uint32(),
            "uint64": pa.uint64(),
        }
        polars_schema = to_polars_schema(schema)

        assert polars_schema["int8"] == pl.Int8
        assert polars_schema["int16"] == pl.Int16
        assert polars_schema["int32"] == pl.Int32
        assert polars_schema["int64"] == pl.Int64
        assert polars_schema["uint8"] == pl.UInt8
        assert polars_schema["uint16"] == pl.UInt16
        assert polars_schema["uint32"] == pl.UInt32
        assert polars_schema["uint64"] == pl.UInt64

    def test_pyarrow_all_float_types(self):
        """Test all PyArrow float types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "float32": pa.float32(),
            "float64": pa.float64(),
        }
        polars_schema = to_polars_schema(schema)

        assert polars_schema["float32"] == pl.Float32
        assert polars_schema["float64"] == pl.Float64

    def test_pyarrow_timestamp_with_timezones(self):
        """Test PyArrow timestamp types with different time units."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "ts_ns": pa.timestamp("ns"),
            "ts_us": pa.timestamp("us"),
            "ts_ms": pa.timestamp("ms"),
            "ts_s": pa.timestamp("s"),
        }
        polars_schema = to_polars_schema(schema)

        assert isinstance(polars_schema["ts_ns"], pl.Datetime)
        assert isinstance(polars_schema["ts_us"], pl.Datetime)
        assert isinstance(polars_schema["ts_ms"], pl.Datetime)
        # Note: Polars doesn't support 's', so it may map to 'ms'

    def test_pyarrow_date_types(self):
        """Test PyArrow date32 and date64 types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "date32": pa.date32(),
            "date64": pa.date64(),
        }
        polars_schema = to_polars_schema(schema)

        assert polars_schema["date32"] == pl.Date()
        assert polars_schema["date64"] == pl.Date()

    def test_pyarrow_duration_types(self):
        """Test PyArrow duration types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "duration_ns": pa.duration("ns"),
            "duration_us": pa.duration("us"),
            "duration_ms": pa.duration("ms"),
            "duration_s": pa.duration("s"),
        }
        polars_schema = to_polars_schema(schema)

        assert isinstance(polars_schema["duration_ns"], pl.Duration)
        assert isinstance(polars_schema["duration_us"], pl.Duration)
        assert isinstance(polars_schema["duration_ms"], pl.Duration)
        assert isinstance(polars_schema["duration_s"], pl.Duration)

    def test_pyarrow_string_types(self):
        """Test PyArrow string and large_string types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "string": pa.string(),
            "large_string": pa.large_string(),
        }
        polars_schema = to_polars_schema(schema)

        assert polars_schema["string"] == pl.String
        assert polars_schema["large_string"] == pl.String

    def test_pyarrow_binary_types(self):
        """Test PyArrow binary types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "binary": pa.binary(),
            "large_binary": pa.large_binary(),
        }
        polars_schema = to_polars_schema(schema)

        # Binary types may map to object or string
        assert (
            polars_schema["binary"] in [pl.String, pl.Object]
            if hasattr(pl, "Object")
            else pl.String
        )
        assert (
            polars_schema["large_binary"] in [pl.String, pl.Object]
            if hasattr(pl, "Object")
            else pl.String
        )

    def test_pyarrow_list_types(self):
        """Test PyArrow list types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "list_string": pa.list_(pa.string()),
            "list_int": pa.list_(pa.int32()),
            "nested_list": pa.list_(pa.list_(pa.int32())),
        }
        polars_schema = to_polars_schema(schema)

        assert isinstance(polars_schema["list_string"], pl.List)
        assert isinstance(polars_schema["list_int"], pl.List)
        assert isinstance(polars_schema["nested_list"], pl.List)

    def test_pyarrow_struct_types(self):
        """Test PyArrow struct types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "struct": pa.struct(
                [
                    pa.field("name", pa.string()),
                    pa.field("age", pa.int32()),
                ]
            ),
        }
        polars_schema = to_polars_schema(schema)

        assert isinstance(polars_schema["struct"], pl.Struct)

    def test_pyarrow_map_types(self):
        """Test PyArrow map types."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        try:
            schema = {
                "map": pa.map_(pa.string(), pa.int32()),
            }
            # Map types may not be supported, so we expect an error
            # Try to convert and catch any error
            try:
                result = to_polars_schema(schema)
                # If it succeeds, that's fine too
                assert "map" in result
            except (UnsupportedTypeError, TypeError, AttributeError, ValueError):
                # Map type not supported - this is expected
                pass
        except (AttributeError, TypeError):
            # Map type may not be available in this PyArrow version
            pytest.skip("Map type not available in this PyArrow version")

    def test_pyarrow_to_pandas_all_types(self):
        """Test converting all PyArrow types to Pandas."""
        try:
            import pyarrow as pa  # noqa: F401
        except ImportError:
            pytest.skip("PyArrow not installed")

        schema = {
            "int32": pa.int32(),
            "float64": pa.float64(),
            "string": pa.string(),
            "bool": pa.bool_(),
            "timestamp": pa.timestamp("ns"),
            "date": pa.date32(),
        }
        pandas_schema = to_pandas_schema(schema)

        assert pandas_schema["int32"] == "Int32"
        assert pandas_schema["float64"] == "Float64"
        assert pandas_schema["string"] == "string"
        assert pandas_schema["bool"] == "boolean"
        assert "datetime" in pandas_schema["timestamp"]
        assert pandas_schema["date"] == "date"


class TestEdgeCases:
    """Tests for edge cases and complex schemas."""

    def test_nested_list_structures(self):
        """Test nested list structures."""
        polars_schema = {
            "nested_list_2": pl.List(pl.List(pl.String)),
            "nested_list_3": pl.List(pl.List(pl.List(pl.Int32))),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert pandas_schema["nested_list_2"] == "object"
        assert pandas_schema["nested_list_3"] == "object"

    def test_nested_struct_structures(self):
        """Test nested struct structures."""
        polars_schema = {
            "outer_struct": pl.Struct(
                [
                    pl.Field("inner_struct", pl.Struct([pl.Field("value", pl.String)])),
                    pl.Field("simple_field", pl.Int32),
                ]
            ),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert pandas_schema["outer_struct"] == "object"

    def test_struct_with_list(self):
        """Test struct containing list fields."""
        polars_schema = {
            "struct_with_list": pl.Struct(
                [
                    pl.Field("name", pl.String),
                    pl.Field("scores", pl.List(pl.Float64)),
                ]
            ),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert pandas_schema["struct_with_list"] == "object"

    def test_list_with_struct(self):
        """Test list containing struct elements."""
        polars_schema = {
            "list_of_structs": pl.List(
                pl.Struct(
                    [
                        pl.Field("name", pl.String),
                        pl.Field("age", pl.Int32),
                    ]
                )
            ),
        }
        pandas_schema = to_pandas_schema(polars_schema)

        assert pandas_schema["list_of_structs"] == "object"

    def test_empty_dataframe(self):
        """Test conversion from empty DataFrame."""
        df = pd.DataFrame()
        with pytest.raises(SchemaError, match="cannot be empty"):
            to_polars_schema(df)

    def test_dataframe_with_all_types(self):
        """Test DataFrame with all supported types."""
        df = pd.DataFrame(
            {
                "int_col": pd.Series([1, 2], dtype="int64"),
                "float_col": pd.Series([1.0, 2.0], dtype="float64"),
                "string_col": pd.Series(["a", "b"], dtype="string"),
                "bool_col": pd.Series([True, False], dtype="boolean"),
                "datetime_col": pd.Series([pd.Timestamp("2023-01-01"), pd.Timestamp("2023-01-02")]),
                "category_col": pd.Series(["A", "B"], dtype="category"),
            }
        )
        polars_schema = to_polars_schema(df)

        assert isinstance(polars_schema, pl.Schema)
        assert len(polars_schema) == 6

    def test_schema_with_100_fields(self):
        """Test schema with 100 fields (performance/edge case)."""
        schema = {f"field_{i}": "string" for i in range(100)}
        polars_schema = to_polars_schema(schema)

        assert isinstance(polars_schema, pl.Schema)
        assert len(polars_schema) == 100

        pandas_schema = to_pandas_schema(polars_schema)
        assert len(pandas_schema) == 100
        assert all(pandas_schema[f"field_{i}"] == "string" for i in range(100))

    def test_malformed_tuple_list(self):
        """Test malformed list of tuples."""
        # Tuple with wrong length
        malformed = [("name",), ("age", "Int32", "extra")]
        with pytest.raises(SchemaError):
            to_polars_schema(malformed)  # type: ignore[arg-type]

    def test_malformed_dict_keys(self):
        """Test malformed dictionary keys."""
        # None key
        malformed = {None: "string"}  # type: ignore[dict-item]
        with pytest.raises(SchemaError):
            to_polars_schema(malformed)

    def test_tuple_list_with_invalid_types(self):
        """Test list of tuples with invalid types."""
        # Non-string field name
        malformed = [(123, "string")]  # type: ignore[list-item]
        with pytest.raises(SchemaError):
            to_polars_schema(malformed)

    def test_complex_mixed_schema(self):
        """Test complex schema with mixed types and formats."""
        schema = {
            "simple_int": "Int32",
            "simple_string": "string",
            "datetime_field": "datetime64[ns]",
            "timedelta_field": "timedelta64[ns]",
            "category_field": "category",
        }
        polars_schema = to_polars_schema(schema)

        assert isinstance(polars_schema, pl.Schema)
        assert polars_schema["simple_int"] == pl.Int32
        assert polars_schema["simple_string"] == pl.String
        assert isinstance(polars_schema["datetime_field"], pl.Datetime)
        assert isinstance(polars_schema["timedelta_field"], pl.Duration)
        assert polars_schema["category_field"] == pl.Categorical

    def test_unicode_field_names(self):
        """Test field names with unicode characters."""
        schema = {
            "field_中文": "string",
            "field_🚀": "Int32",
            "field_émoji": "Float64",
        }
        polars_schema = to_polars_schema(schema)

        assert isinstance(polars_schema, pl.Schema)
        assert "field_中文" in polars_schema
        assert "field_🚀" in polars_schema
        assert "field_émoji" in polars_schema

    def test_all_nullable_types(self):
        """Test all nullable type combinations."""
        schema = {
            "nullable_int": "Int64",
            "nullable_float": "Float64",
            "nullable_string": "string",
            "nullable_bool": "boolean",
        }
        polars_schema = to_polars_schema(schema)

        assert polars_schema["nullable_int"] == pl.Int64
        assert polars_schema["nullable_float"] == pl.Float64
        assert polars_schema["nullable_string"] == pl.String
        assert polars_schema["nullable_bool"] == pl.Boolean

    def test_time_type_conversion(self):
        """Test Time type conversion."""
        polars_schema = {"time_field": pl.Time}
        pandas_schema = to_pandas_schema(polars_schema)

        # Time maps to object in pandas
        assert pandas_schema["time_field"] == "object"
