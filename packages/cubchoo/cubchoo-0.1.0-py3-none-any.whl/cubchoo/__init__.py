"""
Cubchoo - Convert between Pandas and Polars schemas.

Cubchoo provides simple, bidirectional conversion functions to transform
schemas between Pandas and Polars, supporting all data types including
nested structures, arrays, and categorical data.
"""

from cubchoo.converters import (
    to_pandas_schema,
    to_polars_schema,
)
from cubchoo.errors import (
    ConversionError,
    SchemaError,
    UnsupportedTypeError,
)

__version__ = "0.1.0"
__all__ = [
    "to_pandas_schema",
    "to_polars_schema",
    "ConversionError",
    "SchemaError",
    "UnsupportedTypeError",
]
