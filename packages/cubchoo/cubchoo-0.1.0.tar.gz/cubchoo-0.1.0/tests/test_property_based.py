"""Property-based tests using hypothesis for schema conversion."""

import string
from typing import Any, Dict

import polars as pl
import pytest
from hypothesis import given, settings, strategies as st

from cubchoo import to_pandas_schema, to_polars_schema
from cubchoo.errors import SchemaError

try:
    import pyarrow as pa

    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False
    pa = None  # type: ignore[assignment, misc]


# ============================================================================
# Hypothesis Strategies for Schema Generation
# ============================================================================


def valid_field_name() -> st.SearchStrategy[str]:
    """Generate valid field names."""
    return st.text(
        alphabet=string.ascii_letters + string.digits + "_-.",
        min_size=1,
        max_size=100,
    )


def pandas_dtype_strategy() -> st.SearchStrategy[str]:
    """Generate valid pandas dtype strings."""
    return st.sampled_from(
        [
            "int8",
            "Int8",
            "int16",
            "Int16",
            "int32",
            "Int32",
            "int64",
            "Int64",
            "uint8",
            "UInt8",
            "uint16",
            "UInt16",
            "uint32",
            "UInt32",
            "uint64",
            "UInt64",
            "float32",
            "Float32",
            "float64",
            "Float64",
            "string",
            "object",
            "str",
            "bool",
            "boolean",
            "category",
            "datetime64[ns]",
            "datetime64[us]",
            "datetime64[ms]",
            "date",
            "timedelta64[ns]",
            "timedelta64[us]",
            "timedelta64[ms]",
        ]
    )


def polars_type_strategy() -> st.SearchStrategy[Any]:
    """Generate valid Polars types."""
    return st.sampled_from(
        [
            pl.Int8,
            pl.Int16,
            pl.Int32,
            pl.Int64,
            pl.UInt8,
            pl.UInt16,
            pl.UInt32,
            pl.UInt64,
            pl.Float32,
            pl.Float64,
            pl.String,
            pl.Utf8,
            pl.Boolean,
            pl.Categorical,
            pl.Date(),
            pl.Datetime(),
            pl.Datetime(time_unit="ns"),
            pl.Datetime(time_unit="us"),
            pl.Datetime(time_unit="ms"),
            pl.Duration(),
            pl.Duration(time_unit="ns"),
            pl.Duration(time_unit="us"),
            pl.Duration(time_unit="ms"),
        ]
    )


def pandas_schema_dict_strategy() -> st.SearchStrategy[Dict[str, str]]:
    """Generate valid pandas schema dictionaries."""
    return st.dictionaries(
        keys=valid_field_name(),
        values=pandas_dtype_strategy(),
        min_size=1,
        max_size=20,
    )


def polars_schema_dict_strategy() -> st.SearchStrategy[Dict[str, Any]]:
    """Generate valid polars schema dictionaries."""
    return st.dictionaries(
        keys=valid_field_name(),
        values=polars_type_strategy(),
        min_size=1,
        max_size=20,
    )


def pyarrow_type_strategy() -> st.SearchStrategy[Any]:
    """Generate valid PyArrow types (if available)."""
    if not PYARROW_AVAILABLE:
        return st.nothing()
    return st.sampled_from(
        [
            pa.int8(),
            pa.int16(),
            pa.int32(),
            pa.int64(),
            pa.uint8(),
            pa.uint16(),
            pa.uint32(),
            pa.uint64(),
            pa.float32(),
            pa.float64(),
            pa.string(),
            pa.bool_(),
            pa.timestamp("ns"),
            pa.timestamp("us"),
            pa.timestamp("ms"),
            pa.date32(),
            pa.date64(),
        ]
    )


def pyarrow_schema_dict_strategy() -> st.SearchStrategy[Dict[str, Any]]:
    """Generate valid PyArrow schema dictionaries (if available)."""
    if not PYARROW_AVAILABLE:
        return st.nothing()
    return st.dictionaries(
        keys=valid_field_name(),
        values=pyarrow_type_strategy(),
        min_size=1,
        max_size=20,
    )


# ============================================================================
# Property-Based Tests
# ============================================================================


class TestRoundTripProperties:
    """Property-based tests for round-trip conversions."""

    @given(pandas_schema_dict_strategy())
    @settings(max_examples=50, deadline=None)
    def test_pandas_to_polars_to_pandas_round_trip(self, pandas_schema: Dict[str, str]):
        """Test that converting Pandas -> Polars -> Pandas preserves schema."""
        polars_schema = to_polars_schema(pandas_schema)
        converted_back = to_pandas_schema(polars_schema)

        # All original fields should be present
        assert set(converted_back.keys()) == set(pandas_schema.keys())

        # Type preservation (may differ in nullable vs non-nullable)
        for field_name in pandas_schema:
            original_dtype = pandas_schema[field_name]
            converted_dtype = converted_back[field_name]

            # Basic type category should match
            if "int" in original_dtype.lower():
                assert "int" in converted_dtype.lower() or "Int" in converted_dtype
            elif "float" in original_dtype.lower():
                assert "float" in converted_dtype.lower() or "Float" in converted_dtype
            elif original_dtype in ["string", "object", "str"]:
                assert converted_dtype == "string"
            elif original_dtype in ["bool", "boolean"]:
                assert converted_dtype == "boolean"
            elif original_dtype == "category":
                assert converted_dtype == "category"
            elif "datetime" in original_dtype:
                assert "datetime" in converted_dtype
            elif "timedelta" in original_dtype:
                assert "timedelta" in converted_dtype
            elif original_dtype == "date":
                assert converted_dtype == "date"

    @given(polars_schema_dict_strategy())
    @settings(max_examples=50, deadline=None)
    def test_polars_to_pandas_to_polars_round_trip(self, polars_schema: Dict[str, Any]):
        """Test that converting Polars -> Pandas -> Polars preserves schema."""
        pandas_schema = to_pandas_schema(polars_schema)
        converted_back = to_polars_schema(pandas_schema)

        # All original fields should be present
        assert set(converted_back.keys()) == set(polars_schema.keys())

        # Type preservation
        for field_name in polars_schema:
            original_type = polars_schema[field_name]
            converted_type = converted_back[field_name]

            # For simple types, should match exactly
            if isinstance(original_type, type) and not isinstance(
                original_type, (pl.Datetime, pl.Duration)
            ):
                assert converted_type == original_type
            elif isinstance(original_type, pl.Datetime):
                assert isinstance(converted_type, pl.Datetime)
            elif isinstance(original_type, pl.Duration):
                assert isinstance(converted_type, pl.Duration)
            elif isinstance(original_type, pl.Date):
                assert converted_type == pl.Date()

    @given(pyarrow_schema_dict_strategy())
    @settings(max_examples=30, deadline=None)
    def test_pyarrow_round_trip(self, pyarrow_schema: Dict[str, Any]):
        """Test round-trip conversion with PyArrow types."""
        if not PYARROW_AVAILABLE:
            pytest.skip("PyArrow not available")

        # PyArrow -> Polars -> Pandas
        polars_schema = to_polars_schema(pyarrow_schema)
        pandas_schema = to_pandas_schema(polars_schema)

        # All fields should be present
        assert set(pandas_schema.keys()) == set(pyarrow_schema.keys())

        # Pandas -> Polars (round trip)
        polars_schema2 = to_polars_schema(pandas_schema)
        assert set(polars_schema2.keys()) == set(pyarrow_schema.keys())


class TestIdempotencyProperties:
    """Property-based tests for idempotency."""

    @given(pandas_schema_dict_strategy())
    @settings(max_examples=30, deadline=None)
    def test_to_polars_schema_idempotency(self, pandas_schema: Dict[str, str]):
        """Test that converting the same schema twice gives the same result."""
        result1 = to_polars_schema(pandas_schema)
        result2 = to_polars_schema(pandas_schema)

        assert len(result1) == len(result2)
        assert set(result1.keys()) == set(result2.keys())

        for field_name in result1:
            type1 = result1[field_name]
            type2 = result2[field_name]

            if isinstance(type1, pl.Datetime) and isinstance(type2, pl.Datetime):
                assert type1.time_unit == type2.time_unit
            elif isinstance(type1, pl.Duration) and isinstance(type2, pl.Duration):
                assert type1.time_unit == type2.time_unit
            else:
                assert type1 == type2

    @given(polars_schema_dict_strategy())
    @settings(max_examples=30, deadline=None)
    def test_to_pandas_schema_idempotency(self, polars_schema: Dict[str, Any]):
        """Test that converting the same schema twice gives the same result."""
        result1 = to_pandas_schema(polars_schema)
        result2 = to_pandas_schema(polars_schema)

        assert result1 == result2


class TestTypePreservationProperties:
    """Property-based tests for type preservation."""

    @given(
        field_name=valid_field_name(),
        dtype=pandas_dtype_strategy(),
    )
    @settings(max_examples=100, deadline=None)
    def test_single_field_type_preservation(self, field_name: str, dtype: str):
        """Test that single field type is preserved through conversion."""
        schema = {field_name: dtype}
        polars_schema = to_polars_schema(schema)

        assert field_name in polars_schema
        assert isinstance(polars_schema, pl.Schema)

        pandas_result = to_pandas_schema(polars_schema)
        assert field_name in pandas_result

        # Type category should be preserved
        if "int" in dtype.lower():
            assert "int" in pandas_result[field_name].lower() or "Int" in pandas_result[field_name]
        elif "float" in dtype.lower():
            assert (
                "float" in pandas_result[field_name].lower() or "Float" in pandas_result[field_name]
            )
        elif dtype in ["string", "object", "str"]:
            assert pandas_result[field_name] == "string"
        elif dtype in ["bool", "boolean"]:
            assert pandas_result[field_name] == "boolean"
        elif dtype == "category":
            assert pandas_result[field_name] == "category"

    @given(
        field_name=valid_field_name(),
        polars_type=polars_type_strategy(),
    )
    @settings(max_examples=100, deadline=None)
    def test_polars_type_preservation(self, field_name: str, polars_type: Any):
        """Test that Polars type is preserved through conversion."""
        schema = {field_name: polars_type}
        pandas_schema = to_pandas_schema(schema)

        assert field_name in pandas_schema
        assert isinstance(pandas_schema, dict)

        polars_result = to_polars_schema(pandas_schema)
        assert field_name in polars_result

        # Type should be preserved (may differ in time unit for Datetime/Duration)
        if isinstance(polars_type, pl.Datetime):
            assert isinstance(polars_result[field_name], pl.Datetime)
        elif isinstance(polars_type, pl.Duration):
            assert isinstance(polars_result[field_name], pl.Duration)
        elif isinstance(polars_type, pl.Date):
            assert polars_result[field_name] == pl.Date()
        elif isinstance(polars_type, type):
            assert polars_result[field_name] == polars_type


class TestEdgeCaseProperties:
    """Property-based tests for edge cases."""

    @given(
        field_name=st.text(min_size=1, max_size=1000),
        dtype=pandas_dtype_strategy(),
    )
    @settings(max_examples=20, deadline=None)
    def test_very_long_field_names(self, field_name: str, dtype: str):
        """Test that very long field names work."""
        schema = {field_name: dtype}
        polars_schema = to_polars_schema(schema)

        assert field_name in polars_schema
        assert isinstance(polars_schema, pl.Schema)

    @given(
        field_name=st.text(
            alphabet=string.printable,
            min_size=1,
            max_size=50,
        ),
        dtype=pandas_dtype_strategy(),
    )
    @settings(max_examples=50, deadline=None)
    def test_special_characters_in_field_names(self, field_name: str, dtype: str):
        """Test that special characters in field names work."""
        # Skip if field name contains only whitespace or is empty after stripping
        if not field_name.strip():
            return

        schema = {field_name: dtype}
        try:
            polars_schema = to_polars_schema(schema)
            assert field_name in polars_schema
        except SchemaError:
            # Some special characters may not be valid
            pass

    @given(
        num_fields=st.integers(min_value=1, max_value=100),
        dtype=pandas_dtype_strategy(),
    )
    @settings(max_examples=10, deadline=None)
    def test_large_schemas(self, num_fields: int, dtype: str):
        """Test that large schemas work."""
        schema = {f"field_{i}": dtype for i in range(num_fields)}
        polars_schema = to_polars_schema(schema)

        assert len(polars_schema) == num_fields
        assert isinstance(polars_schema, pl.Schema)

        pandas_result = to_pandas_schema(polars_schema)
        assert len(pandas_result) == num_fields


class TestErrorProperties:
    """Property-based tests for error handling."""

    @given(
        invalid_input=st.one_of(
            st.integers(),
            st.floats(),
            st.booleans(),
            st.lists(st.text()),
            st.tuples(st.text(), st.text()),
        )
    )
    @settings(max_examples=20, deadline=None)
    def test_invalid_input_raises_error(self, invalid_input: Any):
        """Test that invalid input raises SchemaError."""
        # Skip valid inputs
        if isinstance(invalid_input, dict) and invalid_input:
            return
        if isinstance(invalid_input, list) and len(invalid_input) > 0:
            # Check if it's a valid list of tuples
            if all(isinstance(item, tuple) and len(item) == 2 for item in invalid_input):
                return

        with pytest.raises(SchemaError):
            to_polars_schema(invalid_input)  # type: ignore[arg-type]

    @given(
        invalid_input=st.one_of(
            st.integers(),
            st.floats(),
            st.booleans(),
            st.lists(st.text()),
            st.tuples(st.text(), st.text()),
        )
    )
    @settings(max_examples=20, deadline=None)
    def test_invalid_input_to_pandas_raises_error(self, invalid_input: Any):
        """Test that invalid input raises SchemaError for to_pandas_schema."""
        # Skip valid inputs
        if isinstance(invalid_input, dict) and invalid_input:
            return
        if isinstance(invalid_input, list) and len(invalid_input) > 0:
            # Check if it's a valid list of tuples
            if all(isinstance(item, tuple) and len(item) == 2 for item in invalid_input):
                return

        with pytest.raises(SchemaError):
            to_pandas_schema(invalid_input)  # type: ignore[arg-type]
