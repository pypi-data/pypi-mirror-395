"""Core conversion functions between Pandas and Polars schemas."""

from typing import Any, Dict, List, Tuple, Union

import pandas as pd
import polars as pl

from cubchoo.errors import SchemaError, UnsupportedTypeError
from cubchoo.type_mappings import (
    get_pandas_dtype_from_polars_type,
    get_pandas_dtype_from_pyarrow_type,
    get_polars_type_from_pandas_dtype,
    get_polars_type_from_pyarrow_type,
)


def _is_pyarrow_type(dtype: Any) -> bool:
    """Check if a dtype is a PyArrow DataType."""
    try:
        import pyarrow as pa

        return isinstance(dtype, pa.DataType)
    except ImportError:
        return False


def to_polars_schema(
    pandas_schema: Union[
        Dict[str, Any],
        pd.DataFrame,
        pd.Series,
        List[Tuple[str, Any]],
        Tuple[Tuple[str, Any], ...],
    ],
) -> pl.Schema:
    """
    Convert a Pandas or PyArrow schema to a Polars schema.

    Pandas schemas can be provided as:
    1. Dictionary mapping column names to dtypes: dict[str, dtype]
    2. pandas DataFrame (schema inferred from dtypes)
    3. pandas Series (for single column)

    PyArrow types (pa.DataType) are also supported in dictionaries and lists.
    Install PyArrow with: pip install cubchoo[pyarrow]

    Args:
        pandas_schema: Pandas or PyArrow schema in any supported format

    Returns:
        pl.Schema: Polars Schema object mapping field names to Polars types

    Raises:
        SchemaError: If the schema structure is invalid
        UnsupportedTypeError: If a type cannot be converted

    Example:
        >>> import pandas as pd
        >>> from cubchoo import to_polars_schema
        >>>
        >>> # From dictionary
        >>> schema_dict = {"name": "string", "age": "Int64", "score": "Float64"}
        >>> polars_schema = to_polars_schema(schema_dict)
        >>>
        >>> # From DataFrame
        >>> df = pd.DataFrame({"name": ["Alice"], "age": [30], "score": [95.5]})
        >>> polars_schema = to_polars_schema(df)
        >>>
        >>> # With PyArrow types
        >>> import pyarrow as pa
        >>> schema_with_pa = {"name": pa.string(), "age": pa.int32()}
        >>> polars_schema = to_polars_schema(schema_with_pa)
    """
    # Handle pandas DataFrame
    if isinstance(pandas_schema, pd.DataFrame):
        schema_dict: Dict[str, Any] = {
            str(col): dtype for col, dtype in pandas_schema.dtypes.items()
        }
        return to_polars_schema(schema_dict)

    # Handle pandas Series
    if isinstance(pandas_schema, pd.Series):
        field_name = pandas_schema.name
        if field_name is None or field_name == "":
            raise SchemaError(
                "Cannot convert unnamed pandas Series to Polars schema. "
                "Please provide a name for the Series or use a dictionary format."
            )
        polars_type = get_polars_type_from_pandas_dtype(pandas_schema.dtype)
        return pl.Schema({field_name: polars_type})  # type: ignore[arg-type]

    # Handle dictionary
    if isinstance(pandas_schema, dict):
        _validate_pandas_schema_dict(pandas_schema)
        polars_schema_dict = {}

        for field_name, dtype in pandas_schema.items():
            try:
                if _is_pyarrow_type(dtype):
                    polars_type = get_polars_type_from_pyarrow_type(dtype)
                else:
                    polars_type = get_polars_type_from_pandas_dtype(dtype)
                polars_schema_dict[field_name] = polars_type
            except UnsupportedTypeError as e:
                raise UnsupportedTypeError(
                    f"Failed to convert field '{field_name}' with dtype '{dtype}': {e}"
                ) from e

        return pl.Schema(polars_schema_dict)

    # Handle list of tuples (similar to Polars schema format)
    if isinstance(pandas_schema, (list, tuple)):
        _validate_pandas_schema_list(pandas_schema)
        schema_dict = {}

        for field_name, dtype in pandas_schema:
            try:
                if _is_pyarrow_type(dtype):
                    polars_type = get_polars_type_from_pyarrow_type(dtype)
                else:
                    polars_type = get_polars_type_from_pandas_dtype(dtype)
                schema_dict[field_name] = polars_type
            except UnsupportedTypeError as e:
                raise UnsupportedTypeError(
                    f"Failed to convert field '{field_name}' with dtype '{dtype}': {e}"
                ) from e

        return pl.Schema(schema_dict)

    raise SchemaError(
        f"Invalid pandas schema format: {type(pandas_schema)}. "
        "Expected dict, pandas.DataFrame, pandas.Series, or list of tuples."
    )


def to_pandas_schema(
    polars_schema: Union[
        pl.Schema,
        Dict[str, Any],
        List[Tuple[str, Any]],
        Tuple[Tuple[str, Any], ...],
    ],
) -> Dict[str, str]:
    """
    Convert a Polars or PyArrow schema to a Pandas schema.

    Polars schemas can be provided as:
    1. pl.Schema object
    2. Dictionary mapping field names to Polars types: dict[str, pl.DataType]
    3. List of tuples: list[tuple[str, pl.DataType]]

    PyArrow types (pa.DataType) are also supported in dictionaries and lists.
    Install PyArrow with: pip install cubchoo[pyarrow]

    Args:
        polars_schema: Polars or PyArrow schema in any supported format

    Returns:
        dict[str, str]: Dictionary mapping column names to pandas dtype strings

    Raises:
        SchemaError: If the schema structure is invalid
        UnsupportedTypeError: If a type cannot be converted

    Example:
        >>> import polars as pl
        >>> from cubchoo import to_pandas_schema
        >>>
        >>> # From pl.Schema
        >>> polars_schema = pl.Schema({
        ...     "name": pl.String,
        ...     "age": pl.Int32,
        ...     "score": pl.Float64,
        ... })
        >>> pandas_schema = to_pandas_schema(polars_schema)
        >>> # Returns: {"name": "string", "age": "Int32", "score": "Float64"}
        >>>
        >>> # With PyArrow types
        >>> import pyarrow as pa
        >>> schema_with_pa = {"name": pa.string(), "age": pa.int32()}
        >>> pandas_schema = to_pandas_schema(schema_with_pa)
    """
    # Handle pl.Schema object
    if isinstance(polars_schema, pl.Schema):
        schema_dict_polars: Dict[str, Any] = dict(polars_schema)
        return to_pandas_schema(schema_dict_polars)

    # Handle dictionary
    if isinstance(polars_schema, dict):
        _validate_polars_schema_dict(polars_schema)
        pandas_schema_dict: Dict[str, str] = {}

        for field_name, polars_type in polars_schema.items():
            try:
                if _is_pyarrow_type(polars_type):
                    pandas_dtype = get_pandas_dtype_from_pyarrow_type(polars_type)
                else:
                    pandas_dtype = get_pandas_dtype_from_polars_type(polars_type)
                pandas_schema_dict[field_name] = pandas_dtype
            except UnsupportedTypeError as e:
                raise UnsupportedTypeError(
                    f"Failed to convert field '{field_name}' with type '{polars_type}': {e}"
                ) from e

        return pandas_schema_dict

    # Handle list of tuples
    if isinstance(polars_schema, (list, tuple)):
        _validate_polars_schema_list(polars_schema)
        schema_dict: Dict[str, str] = {}

        for field_name, polars_type in polars_schema:
            try:
                if _is_pyarrow_type(polars_type):
                    pandas_dtype = get_pandas_dtype_from_pyarrow_type(polars_type)
                else:
                    pandas_dtype = get_pandas_dtype_from_polars_type(polars_type)
                schema_dict[field_name] = pandas_dtype
            except UnsupportedTypeError as e:
                raise UnsupportedTypeError(
                    f"Failed to convert field '{field_name}' with type '{polars_type}': {e}"
                ) from e

        return schema_dict

    raise SchemaError(
        f"Invalid Polars schema format: {type(polars_schema)}. "
        "Expected pl.Schema, dict, or list of tuples."
    )


def _validate_pandas_schema_dict(schema_dict: Dict[str, Any]) -> None:
    """Validate a pandas schema dictionary."""
    if not isinstance(schema_dict, dict):
        raise SchemaError(f"Expected dict, got {type(schema_dict)}")

    if not schema_dict:
        raise SchemaError("Schema dictionary cannot be empty")

    field_names = list(schema_dict.keys())

    # Check for duplicate field names
    if len(field_names) != len(set(field_names)):
        duplicates = [name for name in field_names if field_names.count(name) > 1]
        raise SchemaError(f"Duplicate field names found: {set(duplicates)}")

    # Check for empty field names
    empty_names = [name for name in field_names if not name or not isinstance(name, str)]
    if empty_names:
        raise SchemaError(f"Empty or invalid field names found: {empty_names}")

    # Check for None dtypes
    for field_name, dtype in schema_dict.items():
        if dtype is None:
            raise SchemaError(f"Field '{field_name}' has None dtype")


def _validate_pandas_schema_list(
    schema_list: Union[List[Tuple[str, Any]], Tuple[Tuple[str, Any], ...]],
) -> None:
    """Validate a pandas schema list of tuples."""
    if not isinstance(schema_list, (list, tuple)):
        raise SchemaError(
            f"Invalid schema format: {type(schema_list)}. "
            "Expected iterable of (field_name, dtype) tuples."
        )

    if not schema_list:
        raise SchemaError("Schema list cannot be empty")

    field_names = []

    for idx, item in enumerate(schema_list):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise SchemaError(
                f"Invalid schema format: {type(schema_list)}. "
                f"Expected iterable of (field_name, dtype) tuples. "
                f"Item at index {idx} is not a tuple: {item}"
            )

        field_name, dtype = item

        if not isinstance(field_name, str):
            raise SchemaError(
                f"Invalid field name type at index {idx}: {type(field_name)}. "
                "Field names must be strings."
            )

        if not field_name:
            raise SchemaError(f"Empty field name at index {idx}")

        if dtype is None:
            raise SchemaError(f"Field '{field_name}' at index {idx} has None dtype")

        field_names.append(field_name)

    # Check for duplicate field names
    if len(field_names) != len(set(field_names)):
        duplicates = [name for name in field_names if field_names.count(name) > 1]
        raise SchemaError(f"Duplicate field names found: {set(duplicates)}")


def _validate_polars_schema_dict(schema_dict: Dict[str, Any]) -> None:
    """Validate a Polars schema dictionary."""
    if not isinstance(schema_dict, dict):
        raise SchemaError(f"Expected dict, got {type(schema_dict)}")

    if not schema_dict:
        raise SchemaError("Schema dictionary cannot be empty")

    field_names = list(schema_dict.keys())

    # Check for duplicate field names
    if len(field_names) != len(set(field_names)):
        duplicates = [name for name in field_names if field_names.count(name) > 1]
        raise SchemaError(f"Duplicate field names found: {set(duplicates)}")

    # Check for empty field names
    empty_names = [name for name in field_names if not name or not isinstance(name, str)]
    if empty_names:
        raise SchemaError(f"Empty or invalid field names found: {empty_names}")

    # Check for None types
    for field_name, polars_type in schema_dict.items():
        if polars_type is None:
            raise SchemaError(f"Field '{field_name}' has None type")


def _validate_polars_schema_list(
    schema_list: Union[List[Tuple[str, Any]], Tuple[Tuple[str, Any], ...]],
) -> None:
    """Validate a Polars schema list of tuples."""
    if not isinstance(schema_list, (list, tuple)):
        raise SchemaError(
            f"Invalid schema format: {type(schema_list)}. "
            "Expected iterable of (field_name, type) tuples."
        )

    if not schema_list:
        raise SchemaError("Schema list cannot be empty")

    field_names = []

    for idx, item in enumerate(schema_list):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise SchemaError(
                f"Invalid schema format: {type(schema_list)}. "
                f"Expected iterable of (field_name, type) tuples. "
                f"Item at index {idx} is not a tuple: {item}"
            )

        field_name, polars_type = item

        if not isinstance(field_name, str):
            raise SchemaError(
                f"Invalid field name type at index {idx}: {type(field_name)}. "
                "Field names must be strings."
            )

        if not field_name:
            raise SchemaError(f"Empty field name at index {idx}")

        if polars_type is None:
            raise SchemaError(f"Field '{field_name}' at index {idx} has None type")

        field_names.append(field_name)

    # Check for duplicate field names
    if len(field_names) != len(set(field_names)):
        duplicates = [name for name in field_names if field_names.count(name) > 1]
        raise SchemaError(f"Duplicate field names found: {set(duplicates)}")
