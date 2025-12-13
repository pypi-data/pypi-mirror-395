"""Tests for type mapping functions."""

import pandas as pd
import polars as pl
import pytest

from cubchoo.errors import UnsupportedTypeError
from cubchoo.type_mappings import (
    get_pandas_dtype_from_polars_type,
    get_polars_type_from_pandas_dtype,
)
from tests.conftest import (
    generate_datetime_types,
    generate_float_types,
    generate_integer_types,
    generate_polars_to_pandas_datetime_types,
    generate_polars_to_pandas_float_types,
    generate_polars_to_pandas_integer_types,
    generate_polars_to_pandas_string_types,
    generate_polars_to_pandas_timedelta_types,
    generate_string_types,
    generate_timedelta_types,
    generate_boolean_types,
)


class TestPandasToPolars:
    """Tests for converting pandas dtypes to Polars types."""

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_integer_types())
    def test_integer_types(self, pandas_dtype, expected_polars_type):
        """Test integer type conversions."""
        assert get_polars_type_from_pandas_dtype(pandas_dtype) == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_float_types())
    def test_float_types(self, pandas_dtype, expected_polars_type):
        """Test float type conversions."""
        assert get_polars_type_from_pandas_dtype(pandas_dtype) == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_string_types())
    def test_string_types(self, pandas_dtype, expected_polars_type):
        """Test string type conversions."""
        assert get_polars_type_from_pandas_dtype(pandas_dtype) == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_boolean_types())
    def test_boolean_types(self, pandas_dtype, expected_polars_type):
        """Test boolean type conversions."""
        assert get_polars_type_from_pandas_dtype(pandas_dtype) == expected_polars_type

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_datetime_types())
    def test_datetime_types(self, pandas_dtype, expected_polars_type):
        """Test datetime type conversions."""
        result = get_polars_type_from_pandas_dtype(pandas_dtype)
        assert isinstance(result, pl.Datetime)
        # Check time unit for non-default cases
        if hasattr(expected_polars_type, "time_unit"):
            assert hasattr(result, "time_unit")
            if hasattr(result, "time_unit") and result.time_unit is not None:
                assert result.time_unit == expected_polars_type.time_unit

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_timedelta_types())
    def test_timedelta_types(self, pandas_dtype, expected_polars_type):
        """Test timedelta type conversions."""
        result = get_polars_type_from_pandas_dtype(pandas_dtype)
        assert isinstance(result, pl.Duration)
        # Check time unit for non-default cases
        if hasattr(expected_polars_type, "time_unit"):
            assert hasattr(result, "time_unit")
            if hasattr(result, "time_unit") and result.time_unit is not None:
                assert result.time_unit == expected_polars_type.time_unit

    def test_categorical_type(self):
        """Test categorical type conversion."""
        assert get_polars_type_from_pandas_dtype("category") == pl.Categorical

    def test_date_type(self):
        """Test date type conversion."""
        result = get_polars_type_from_pandas_dtype("date")
        assert result == pl.Date()

    @pytest.mark.parametrize(
        "pandas_dtype_obj,expected_polars_type",
        [
            (pd.StringDtype(), pl.String),
            (pd.Int64Dtype(), pl.Int64),
            (pd.Float64Dtype(), pl.Float64),
            (pd.Int32Dtype(), pl.Int32),
            (pd.Int16Dtype(), pl.Int16),
            (pd.Int8Dtype(), pl.Int8),
            (pd.UInt64Dtype(), pl.UInt64),
            (pd.UInt32Dtype(), pl.UInt32),
            (pd.UInt16Dtype(), pl.UInt16),
            (pd.UInt8Dtype(), pl.UInt8),
            (pd.Float32Dtype(), pl.Float32),
            (pd.BooleanDtype(), pl.Boolean),
        ],
    )
    def test_pandas_dtype_objects(self, pandas_dtype_obj, expected_polars_type):
        """Test conversion from pandas dtype objects."""
        assert get_polars_type_from_pandas_dtype(pandas_dtype_obj) == expected_polars_type

    def test_categorical_dtype_object(self):
        """Test conversion from pandas CategoricalDtype object."""
        if hasattr(pd, "CategoricalDtype"):
            categorical_dtype = pd.CategoricalDtype()
            assert get_polars_type_from_pandas_dtype(categorical_dtype) == pl.Categorical

    def test_unsupported_type_error(self):
        """Test that unsupported types raise error."""
        with pytest.raises(UnsupportedTypeError):
            get_polars_type_from_pandas_dtype("unsupported_type")

    def test_unsupported_type_error_message(self):
        """Test that error message includes supported types."""
        with pytest.raises(UnsupportedTypeError, match="Unsupported pandas dtype"):
            get_polars_type_from_pandas_dtype("invalid_type")


class TestPolarsToPandas:
    """Tests for converting Polars types to pandas dtypes."""

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_integer_types()
    )
    def test_integer_types(self, polars_type, expected_pandas_dtype):
        """Test integer type conversions."""
        assert get_pandas_dtype_from_polars_type(polars_type) == expected_pandas_dtype

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_float_types()
    )
    def test_float_types(self, polars_type, expected_pandas_dtype):
        """Test float type conversions."""
        assert get_pandas_dtype_from_polars_type(polars_type) == expected_pandas_dtype

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_string_types()
    )
    def test_string_types(self, polars_type, expected_pandas_dtype):
        """Test string type conversions."""
        assert get_pandas_dtype_from_polars_type(polars_type) == expected_pandas_dtype

    def test_boolean_types(self):
        """Test boolean type conversions."""
        assert get_pandas_dtype_from_polars_type(pl.Boolean) == "boolean"

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_datetime_types()
    )
    def test_datetime_types(self, polars_type, expected_pandas_dtype):
        """Test datetime type conversions."""
        assert get_pandas_dtype_from_polars_type(polars_type) == expected_pandas_dtype

    @pytest.mark.parametrize(
        "polars_type,expected_pandas_dtype", generate_polars_to_pandas_timedelta_types()
    )
    def test_timedelta_types(self, polars_type, expected_pandas_dtype):
        """Test timedelta type conversions."""
        assert get_pandas_dtype_from_polars_type(polars_type) == expected_pandas_dtype

    def test_categorical_type(self):
        """Test categorical type conversion."""
        assert get_pandas_dtype_from_polars_type(pl.Categorical) == "category"

    def test_time_type(self):
        """Test Time type conversion (maps to object)."""
        assert get_pandas_dtype_from_polars_type(pl.Time) == "object"

    @pytest.mark.parametrize(
        "list_type",
        [
            pl.List(pl.String),
            pl.List(pl.Int32),
            pl.List(pl.Float64),
            pl.List(pl.List(pl.String)),
            pl.List(pl.List(pl.Int32)),
        ],
    )
    def test_list_types(self, list_type):
        """Test list type conversions (converted to object)."""
        assert get_pandas_dtype_from_polars_type(list_type) == "object"

    def test_struct_types(self):
        """Test struct type conversions (converted to object)."""
        struct_type = pl.Struct(
            [
                pl.Field("name", pl.String),
                pl.Field("age", pl.Int32),
            ]
        )
        assert get_pandas_dtype_from_polars_type(struct_type) == "object"

    def test_nested_struct_types(self):
        """Test nested struct type conversions."""
        nested_struct = pl.Struct(
            [
                pl.Field("outer", pl.Struct([pl.Field("inner", pl.String)])),
            ]
        )
        assert get_pandas_dtype_from_polars_type(nested_struct) == "object"

    def test_map_types(self):
        """Test Map type conversions (converted to object)."""
        try:
            from polars.datatypes import Map  # type: ignore[attr-defined]

            map_type = Map(pl.String, pl.Int32)
            assert get_pandas_dtype_from_polars_type(map_type) == "object"
        except ImportError:
            pytest.skip("Map type not available in this Polars version")

    def test_unsupported_type_error(self):
        """Test that unsupported types raise error."""

        # Create a mock unsupported type
        class UnsupportedType:
            pass

        with pytest.raises(UnsupportedTypeError):
            get_pandas_dtype_from_polars_type(UnsupportedType())

    def test_unsupported_type_error_message(self):
        """Test that error message is informative."""

        class UnsupportedType:
            pass

        with pytest.raises(UnsupportedTypeError, match="Unsupported"):
            get_pandas_dtype_from_polars_type(UnsupportedType())


class TestTypeMappingRoundTrip:
    """Tests for round-trip type conversions."""

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_integer_types())
    def test_integer_round_trip(self, pandas_dtype, expected_polars_type):
        """Test round-trip conversion for integer types."""
        polars_type = get_polars_type_from_pandas_dtype(pandas_dtype)
        pandas_result = get_pandas_dtype_from_polars_type(polars_type)
        # Note: round-trip may not be exact due to nullable vs non-nullable
        assert pandas_result in [
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
        polars_type = get_polars_type_from_pandas_dtype(pandas_dtype)
        pandas_result = get_pandas_dtype_from_polars_type(polars_type)
        assert pandas_result in ["Float32", "Float64"]

    @pytest.mark.parametrize("pandas_dtype,expected_polars_type", generate_string_types())
    def test_string_round_trip(self, pandas_dtype, expected_polars_type):
        """Test round-trip conversion for string types."""
        polars_type = get_polars_type_from_pandas_dtype(pandas_dtype)
        pandas_result = get_pandas_dtype_from_polars_type(polars_type)
        assert pandas_result == "string"

    def test_categorical_round_trip(self):
        """Test round-trip conversion for categorical type."""
        polars_type = get_polars_type_from_pandas_dtype("category")
        pandas_result = get_pandas_dtype_from_polars_type(polars_type)
        assert pandas_result == "category"
