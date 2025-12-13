"""Type mappings between Pandas and Polars data types."""

from typing import Any, Union

import pandas as pd
import polars as pl

from cubchoo.errors import UnsupportedTypeError

# Mapping from pandas dtype strings/classes to Polars types
PANDAS_TO_POLARS = {
    # Integer types
    "int8": pl.Int8,
    "Int8": pl.Int8,
    "int16": pl.Int16,
    "Int16": pl.Int16,
    "int32": pl.Int32,
    "Int32": pl.Int32,
    "int64": pl.Int64,
    "Int64": pl.Int64,
    "uint8": pl.UInt8,
    "UInt8": pl.UInt8,
    "uint16": pl.UInt16,
    "UInt16": pl.UInt16,
    "uint32": pl.UInt32,
    "UInt32": pl.UInt32,
    "uint64": pl.UInt64,
    "UInt64": pl.UInt64,
    # Float types
    "float32": pl.Float32,
    "Float32": pl.Float32,
    "float64": pl.Float64,
    "Float64": pl.Float64,
    # String types
    "object": pl.String,
    "string": pl.String,
    "str": pl.String,
    # Boolean types
    "bool": pl.Boolean,
    "boolean": pl.Boolean,
    # Datetime types
    "datetime64[ns]": pl.Datetime(),
    "datetime64[us]": pl.Datetime(time_unit="us"),
    "datetime64[ms]": pl.Datetime(time_unit="ms"),
    "datetime64[s]": pl.Datetime(time_unit="ms"),  # Polars doesn't support 's', use 'ms' as closest
    # Date types
    "date": pl.Date(),
    # Time types
    "timedelta64[ns]": pl.Duration(),
    "timedelta64[us]": pl.Duration(time_unit="us"),
    "timedelta64[ms]": pl.Duration(time_unit="ms"),
    "timedelta64[s]": pl.Duration(
        time_unit="ms"
    ),  # Polars doesn't support 's', use 'ms' as closest
    # Categorical
    "category": pl.Categorical(),
}

# Mapping from Polars types to pandas dtype strings
POLARS_TO_PANDAS = {
    # Integer types
    pl.Int8: "Int8",
    pl.Int16: "Int16",
    pl.Int32: "Int32",
    pl.Int64: "Int64",
    pl.UInt8: "UInt8",
    pl.UInt16: "UInt16",
    pl.UInt32: "UInt32",
    pl.UInt64: "UInt64",
    # Float types
    pl.Float32: "Float32",
    pl.Float64: "Float64",
    # String types
    pl.String: "string",
    pl.Utf8: "string",  # Utf8 is an alias for String
    # Boolean types
    pl.Boolean: "boolean",
    # Datetime types
    pl.Datetime: "datetime64[ns]",
    pl.Date: "date",
    pl.Time: "object",  # Time doesn't have direct pandas equivalent
    pl.Duration: "timedelta64[ns]",
    # Categorical
    pl.Categorical: "category",
    # List types - handled separately
    # Struct types - handled separately
    # Map types - handled separately
}


def get_polars_type_from_pandas_dtype(dtype: Union[str, type, Any]) -> Union[type, Any]:
    """
    Convert a pandas dtype to a Polars type.

    Args:
        dtype: pandas dtype (string, class, or dtype object)

    Returns:
        Polars type class or instance

    Raises:
        UnsupportedTypeError: If the dtype cannot be converted
    """
    # Handle pandas dtype objects
    if hasattr(dtype, "name"):
        dtype_str = dtype.name
    elif isinstance(dtype, type):
        dtype_str = dtype.__name__
    elif isinstance(dtype, str):
        dtype_str = dtype
    else:
        dtype_str = str(dtype)

    # Check direct mapping
    if dtype_str in PANDAS_TO_POLARS:
        polars_type = PANDAS_TO_POLARS[dtype_str]
        # If it's already an instance (like pl.Datetime(time_unit="us")), return it
        # If it's a class (like pl.Int8), return the class
        return polars_type

    # Handle datetime with timezone
    if "datetime64" in dtype_str:
        # Extract time unit if present
        if "[us]" in dtype_str:
            return pl.Datetime(time_unit="us")
        elif "[ms]" in dtype_str:
            return pl.Datetime(time_unit="ms")
        elif "[s]" in dtype_str:
            # Polars doesn't support 's', use 'ms' as closest
            return pl.Datetime(time_unit="ms")
        else:
            return pl.Datetime()

    # Handle timedelta
    if "timedelta64" in dtype_str:
        if "[us]" in dtype_str:
            return pl.Duration(time_unit="us")
        elif "[ms]" in dtype_str:
            return pl.Duration(time_unit="ms")
        elif "[s]" in dtype_str:
            # Polars doesn't support 's', use 'ms' as closest
            return pl.Duration(time_unit="ms")
        else:
            return pl.Duration()

    # Handle pandas extension dtypes
    if hasattr(pd, "CategoricalDtype") and isinstance(dtype, pd.CategoricalDtype):
        return pl.Categorical

    if hasattr(pd, "StringDtype") and isinstance(dtype, pd.StringDtype):
        return pl.String

    if hasattr(pd, "BooleanDtype") and isinstance(dtype, pd.BooleanDtype):
        return pl.Boolean

    # If we get here, the type is not supported
    supported_types = ", ".join(sorted(set(PANDAS_TO_POLARS.keys())))
    raise UnsupportedTypeError(
        f"Unsupported pandas dtype '{dtype_str}'. "
        f"Supported types include: {supported_types}. "
        f"If you're using a pandas extension dtype, ensure it's properly instantiated."
    )


def get_pandas_dtype_from_polars_type(polars_type: Union[type, Any]) -> str:
    """
    Convert a Polars type to a pandas dtype string.

    Args:
        polars_type: Polars type class or instance

    Returns:
        pandas dtype string

    Raises:
        UnsupportedTypeError: If the type cannot be converted
    """
    # Handle complex types first (they all map to "object" in pandas)
    if isinstance(polars_type, (pl.List, pl.Struct)):
        return "object"

    # Handle Map types (may not be available in all Polars versions)
    try:
        from polars.datatypes import Map  # type: ignore[attr-defined]

        if isinstance(polars_type, Map):
            return "object"
    except ImportError:
        pass

    # Handle parameterized Datetime instances
    if isinstance(polars_type, pl.Datetime):
        time_unit = _get_time_unit(polars_type)
        if time_unit == "us":
            return "datetime64[us]"
        if time_unit == "ms":
            return "datetime64[ms]"
        return "datetime64[ns]"

    # Handle parameterized Duration instances
    if isinstance(polars_type, pl.Duration):
        time_unit = _get_time_unit(polars_type)
        if time_unit == "us":
            return "timedelta64[us]"
        if time_unit == "ms":
            return "timedelta64[ms]"
        return "timedelta64[ns]"

    # Handle type classes directly
    # Note: polars_type may be a class or instance, so we need to check both
    if isinstance(polars_type, type) and polars_type in POLARS_TO_PANDAS:
        return POLARS_TO_PANDAS[polars_type]  # type: ignore[index]

    # Try to get the base type class for instances
    type_class = type(polars_type) if not isinstance(polars_type, type) else polars_type
    if isinstance(type_class, type) and type_class in POLARS_TO_PANDAS:
        return POLARS_TO_PANDAS[type_class]  # type: ignore[index]

    # If we get here, the type is not supported
    supported_types = ", ".join(sorted([str(t) for t in set(POLARS_TO_PANDAS.keys())]))
    raise UnsupportedTypeError(
        f"Unsupported Polars type '{polars_type}' (type: {type(polars_type).__name__}). "
        f"Supported base types include: {supported_types}. "
        f"Complex nested types (List, Struct, Map) are converted to 'object' dtype."
    )


def _get_time_unit(time_type: Union[pl.Datetime, pl.Duration]) -> str:
    """
    Extract time_unit from a Datetime or Duration instance.

    Args:
        time_type: pl.Datetime or pl.Duration instance

    Returns:
        Time unit string ("ns", "us", or "ms"), defaulting to "ns"
    """
    try:
        return time_type.time_unit
    except (AttributeError, TypeError):
        return "ns"


def get_polars_type_from_pyarrow_type(pyarrow_type: Any) -> Union[type, Any]:
    """
    Convert a PyArrow type to a Polars type.

    Args:
        pyarrow_type: PyArrow type instance

    Returns:
        Polars type class or instance

    Raises:
        UnsupportedTypeError: If the type cannot be converted
        ImportError: If pyarrow is not installed
    """
    try:
        import pyarrow as pa  # noqa: F401
    except ImportError:
        raise ImportError(
            "PyArrow is required for PyArrow type support. "
            "Install it with: pip install cubchoo[pyarrow]"
        )

    if not isinstance(pyarrow_type, pa.DataType):
        raise UnsupportedTypeError(f"Expected PyArrow DataType, got {type(pyarrow_type)}")

    # Integer types
    if pa.types.is_int8(pyarrow_type):
        return pl.Int8
    if pa.types.is_int16(pyarrow_type):
        return pl.Int16
    if pa.types.is_int32(pyarrow_type):
        return pl.Int32
    if pa.types.is_int64(pyarrow_type):
        return pl.Int64
    if pa.types.is_uint8(pyarrow_type):
        return pl.UInt8
    if pa.types.is_uint16(pyarrow_type):
        return pl.UInt16
    if pa.types.is_uint32(pyarrow_type):
        return pl.UInt32
    if pa.types.is_uint64(pyarrow_type):
        return pl.UInt64

    # Float types
    if pa.types.is_float32(pyarrow_type):
        return pl.Float32
    if pa.types.is_float64(pyarrow_type):
        return pl.Float64

    # String types
    if pa.types.is_string(pyarrow_type) or pa.types.is_large_string(pyarrow_type):
        return pl.String
    if pa.types.is_binary(pyarrow_type) or pa.types.is_large_binary(pyarrow_type):
        return pl.String  # Binary maps to String in Polars

    # Boolean types
    if pa.types.is_boolean(pyarrow_type):
        return pl.Boolean

    # Date and time types
    if pa.types.is_date32(pyarrow_type) or pa.types.is_date64(pyarrow_type):
        return pl.Date()
    if pa.types.is_timestamp(pyarrow_type):
        # Extract time unit from PyArrow timestamp
        unit = pyarrow_type.unit if hasattr(pyarrow_type, "unit") else "ns"
        if unit == "us":
            return pl.Datetime(time_unit="us")
        if unit == "ms":
            return pl.Datetime(time_unit="ms")
        if unit == "s":
            return pl.Datetime(time_unit="ms")  # Polars doesn't support 's', use 'ms'
        return pl.Datetime()  # Default to ns
    if pa.types.is_time32(pyarrow_type) or pa.types.is_time64(pyarrow_type):
        return pl.Time
    if pa.types.is_duration(pyarrow_type):
        unit = pyarrow_type.unit if hasattr(pyarrow_type, "unit") else "ns"
        if unit == "us":
            return pl.Duration(time_unit="us")
        if unit == "ms":
            return pl.Duration(time_unit="ms")
        if unit == "s":
            return pl.Duration(time_unit="ms")  # Polars doesn't support 's', use 'ms'
        return pl.Duration()

    # List types
    if pa.types.is_list(pyarrow_type) or pa.types.is_large_list(pyarrow_type):
        # For nested types, we'll convert to object in pandas, so return List
        inner_type = pyarrow_type.value_type if hasattr(pyarrow_type, "value_type") else None
        if inner_type:
            inner_polars = get_polars_type_from_pyarrow_type(inner_type)
            return pl.List(inner_polars)
        return pl.List(pl.String)  # Default to List of String

    # Struct types
    if pa.types.is_struct(pyarrow_type):
        return pl.Struct([])  # Complex structs map to object in pandas

    # Dictionary (categorical)
    if pa.types.is_dictionary(pyarrow_type):
        return pl.Categorical()

    # If we get here, the type is not supported
    raise UnsupportedTypeError(
        f"Unsupported PyArrow type: {pyarrow_type}. "
        "Supported types include: integers, floats, strings, booleans, dates, timestamps, lists, structs, dictionaries."
    )


def get_pandas_dtype_from_pyarrow_type(pyarrow_type: Any) -> str:
    """
    Convert a PyArrow type to a pandas dtype string.

    Args:
        pyarrow_type: PyArrow type instance

    Returns:
        pandas dtype string

    Raises:
        UnsupportedTypeError: If the type cannot be converted
        ImportError: If pyarrow is not installed
    """
    try:
        import pyarrow as pa  # noqa: F401
    except ImportError:
        raise ImportError(
            "PyArrow is required for PyArrow type support. "
            "Install it with: pip install cubchoo[pyarrow]"
        )

    if not isinstance(pyarrow_type, pa.DataType):
        raise UnsupportedTypeError(f"Expected PyArrow DataType, got {type(pyarrow_type)}")

    # Integer types
    if pa.types.is_int8(pyarrow_type):
        return "Int8"
    if pa.types.is_int16(pyarrow_type):
        return "Int16"
    if pa.types.is_int32(pyarrow_type):
        return "Int32"
    if pa.types.is_int64(pyarrow_type):
        return "Int64"
    if pa.types.is_uint8(pyarrow_type):
        return "UInt8"
    if pa.types.is_uint16(pyarrow_type):
        return "UInt16"
    if pa.types.is_uint32(pyarrow_type):
        return "UInt32"
    if pa.types.is_uint64(pyarrow_type):
        return "UInt64"

    # Float types
    if pa.types.is_float32(pyarrow_type):
        return "Float32"
    if pa.types.is_float64(pyarrow_type):
        return "Float64"

    # String types
    if pa.types.is_string(pyarrow_type) or pa.types.is_large_string(pyarrow_type):
        return "string"
    if pa.types.is_binary(pyarrow_type) or pa.types.is_large_binary(pyarrow_type):
        return "object"  # Binary maps to object in pandas

    # Boolean types
    if pa.types.is_boolean(pyarrow_type):
        return "boolean"

    # Date and time types
    if pa.types.is_date32(pyarrow_type) or pa.types.is_date64(pyarrow_type):
        return "date"
    if pa.types.is_timestamp(pyarrow_type):
        unit = pyarrow_type.unit if hasattr(pyarrow_type, "unit") else "ns"
        if unit == "us":
            return "datetime64[us]"
        if unit == "ms":
            return "datetime64[ms]"
        if unit == "s":
            return "datetime64[s]"
        return "datetime64[ns]"
    if pa.types.is_time32(pyarrow_type) or pa.types.is_time64(pyarrow_type):
        return "object"  # Time doesn't have direct pandas equivalent
    if pa.types.is_duration(pyarrow_type):
        unit = pyarrow_type.unit if hasattr(pyarrow_type, "unit") else "ns"
        if unit == "us":
            return "timedelta64[us]"
        if unit == "ms":
            return "timedelta64[ms]"
        if unit == "s":
            return "timedelta64[s]"
        return "timedelta64[ns]"

    # List types
    if pa.types.is_list(pyarrow_type) or pa.types.is_large_list(pyarrow_type):
        return "object"  # Lists map to object in pandas

    # Struct types
    if pa.types.is_struct(pyarrow_type):
        return "object"  # Structs map to object in pandas

    # Dictionary (categorical)
    if pa.types.is_dictionary(pyarrow_type):
        return "category"

    # If we get here, the type is not supported
    raise UnsupportedTypeError(
        f"Unsupported PyArrow type: {pyarrow_type}. "
        "Supported types include: integers, floats, strings, booleans, dates, timestamps, lists, structs, dictionaries."
    )


def get_pyarrow_type_from_polars_type(polars_type: Union[type, Any]) -> Any:
    """
    Convert a Polars type to a PyArrow type.

    Args:
        polars_type: Polars type class or instance

    Returns:
        PyArrow DataType instance

    Raises:
        UnsupportedTypeError: If the type cannot be converted
        ImportError: If pyarrow is not installed
    """
    try:
        import pyarrow as pa  # noqa: F401
    except ImportError:
        raise ImportError(
            "PyArrow is required for PyArrow type support. "
            "Install it with: pip install cubchoo[pyarrow]"
        )

    # Handle instances first (Datetime, Duration, List, Struct)
    if isinstance(polars_type, pl.Datetime):
        time_unit = _get_time_unit(polars_type)
        if time_unit == "us":
            return pa.timestamp("us")
        if time_unit == "ms":
            return pa.timestamp("ms")
        if time_unit == "s":
            return pa.timestamp("s")
        return pa.timestamp("ns")

    if isinstance(polars_type, pl.Duration):
        time_unit = _get_time_unit(polars_type)
        if time_unit == "us":
            return pa.duration("us")
        if time_unit == "ms":
            return pa.duration("ms")
        if time_unit == "s":
            return pa.duration("s")
        return pa.duration("ns")

    if isinstance(polars_type, pl.List):
        inner_type = polars_type.inner if hasattr(polars_type, "inner") else pl.String
        inner_pa = get_pyarrow_type_from_polars_type(inner_type)
        return pa.list_(inner_pa)

    if isinstance(polars_type, pl.Struct):
        # Convert struct fields to PyArrow fields
        fields = []
        if hasattr(polars_type, "fields"):
            for field in polars_type.fields:
                pa_type = get_pyarrow_type_from_polars_type(field.dtype)
                fields.append(pa.field(field.name, pa_type))
        return pa.struct(fields) if fields else pa.struct([])

    # Handle type classes
    # Integer types
    if polars_type == pl.Int8:
        return pa.int8()
    if polars_type == pl.Int16:
        return pa.int16()
    if polars_type == pl.Int32:
        return pa.int32()
    if polars_type == pl.Int64:
        return pa.int64()
    if polars_type == pl.UInt8:
        return pa.uint8()
    if polars_type == pl.UInt16:
        return pa.uint16()
    if polars_type == pl.UInt32:
        return pa.uint32()
    if polars_type == pl.UInt64:
        return pa.uint64()

    # Float types
    if polars_type == pl.Float32:
        return pa.float32()
    if polars_type == pl.Float64:
        return pa.float64()

    # String types
    if polars_type in (pl.String, pl.Utf8):
        return pa.string()

    # Boolean types
    if polars_type == pl.Boolean:
        return pa.bool_()

    # Date and time types
    if polars_type == pl.Date:
        return pa.date32()
    if polars_type == pl.Time:
        return pa.time64("ns")

    # Categorical
    if polars_type == pl.Categorical:
        return pa.dictionary(pa.int32(), pa.string())

    # If we get here, the type is not supported
    raise UnsupportedTypeError(
        f"Unsupported Polars type: {polars_type}. Cannot convert to PyArrow type."
    )


def get_pyarrow_type_from_pandas_dtype(dtype: Union[str, type, Any]) -> Any:
    """
    Convert a pandas dtype to a PyArrow type.

    Args:
        dtype: pandas dtype (string, class, or dtype object)

    Returns:
        PyArrow DataType instance

    Raises:
        UnsupportedTypeError: If the type cannot be converted
        ImportError: If pyarrow is not installed
    """
    try:
        import pyarrow as pa  # noqa: F401
    except ImportError:
        raise ImportError(
            "PyArrow is required for PyArrow type support. "
            "Install it with: pip install cubchoo[pyarrow]"
        )

    # First convert to Polars, then to PyArrow
    polars_type = get_polars_type_from_pandas_dtype(dtype)
    return get_pyarrow_type_from_polars_type(polars_type)
