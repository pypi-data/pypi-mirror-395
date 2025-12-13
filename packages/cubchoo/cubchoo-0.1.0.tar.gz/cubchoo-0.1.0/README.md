# Cubchoo

[![PyPI version](https://badge.fury.io/py/cubchoo.svg)](https://badge.fury.io/py/cubchoo)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**C**onvert **U**niversal **B**etween **C**ommon **H**andling of **O**bject **O**rganization

> 🐻 A lightweight Python library for seamless schema conversion between Pandas and Polars

Cubchoo provides simple, bidirectional conversion functions to transform schemas between Pandas and Polars, supporting all data types including nested structures, arrays, and categorical data. Perfect for projects that need to work with both libraries or migrate between them.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Supported Type Mappings](#supported-type-mappings)
- [Advanced Examples](#advanced-examples)
- [Error Handling](#error-handling)
- [Limitations and Notes](#limitations-and-notes)
- [API Reference](#api-reference)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

✨ **Key Features:**

- 🔄 **Bidirectional Conversion**: Convert schemas in both directions (Pandas ↔ Polars)
- 📦 **Multiple Input Formats**: Support for dictionaries, lists, DataFrames, Series, and Schema objects
- 🎯 **Comprehensive Type Support**: All basic types (integers, floats, strings, booleans, datetimes, etc.)
- ✅ **Nullable Types**: Full support for nullable integer and float types (Int64, Float64, etc.)
- 🏷️ **Categorical Data**: Support for categorical data types
- 🛡️ **Error Handling**: Clear error messages with custom exceptions
- ✔️ **Input Validation**: Validates schemas before conversion
- 🚀 **Zero Dependencies**: Only requires pandas and polars (no additional dependencies)
- 🪶 **PyArrow Support**: Optional PyArrow type support (install with `pip install cubchoo[pyarrow]`)

## Installation

### From PyPI

```bash
pip install cubchoo
```

### With PyArrow Support (Optional)

PyArrow support is available as an optional dependency:

```bash
pip install cubchoo[pyarrow]
```

### From Source

```bash
git clone https://github.com/eddiethedean/cubchoo.git
cd cubchoo
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

### All Dependencies

```bash
pip install cubchoo[all]
```

## Requirements

- **Python**: >= 3.8
- **pandas**: >= 1.3.0
- **polars**: >= 0.19.0
- **pyarrow**: >= 10.0.0 (optional, for PyArrow type support)

## Quick Start

Get started with Cubchoo in just a few lines of code!

### Converting Pandas Schema to Polars

Cubchoo supports **multiple Pandas schema formats** - use whichever is most convenient:

```python
import pandas as pd
from cubchoo import to_polars_schema

# Format 1: Dictionary with string dtype names
pandas_schema_dict = {
    "name": "string",
    "age": "Int64",
    "score": "Float64",
    "tags": "object",  # Lists/arrays in pandas are typically object type
}

# Format 2: Dictionary with pandas dtype objects
pandas_schema_dtypes = {
    "name": pd.StringDtype(),
    "age": pd.Int64Dtype(),
    "score": pd.Float64Dtype(),
}

# Format 3: pandas DataFrame (schema inferred from dtypes)
df = pd.DataFrame({
    "name": ["Alice", "Bob"],
    "age": [30, 25],
    "score": [95.5, 87.0],
})

# Format 4: List of tuples
pandas_schema_list = [
    ("name", "string"),
    ("age", "Int64"),
    ("score", "Float64"),
]

# All formats work identically!
polars_schema = to_polars_schema(pandas_schema_dict)
# or: to_polars_schema(pandas_schema_dtypes)
# or: to_polars_schema(df)
# or: to_polars_schema(pandas_schema_list)

print(polars_schema)
# Schema({'name': <class 'polars.datatypes.String'>, 
#         'age': <class 'polars.datatypes.Int64'>, 
#         'score': <class 'polars.datatypes.Float64'>, ...})

# Use directly with Polars DataFrame
import polars as pl
df_polars = pl.DataFrame({}, schema=polars_schema)
```

### Converting Polars Schema to Pandas

```python
import polars as pl
from cubchoo import to_pandas_schema

# Define a Polars schema
polars_schema = pl.Schema({
    "name": pl.String,
    "age": pl.Int32,
    "score": pl.Float64,
    "tags": pl.List(pl.String),
})

# Convert to Pandas schema (returns dict of dtype strings)
pandas_schema = to_pandas_schema(polars_schema)
print(pandas_schema)
# {'name': 'string', 'age': 'Int32', 'score': 'Float64', 'tags': 'object'}

# Use with pandas DataFrame
df = pd.DataFrame({}, dtype=pandas_schema)
```

### Using PyArrow Types (Optional)

With PyArrow support installed, you can use PyArrow types (`pa.DataType`) directly in your schemas:

```python
import pyarrow as pa
from cubchoo import to_polars_schema, to_pandas_schema

# Use PyArrow types in a schema dictionary
schema_with_pa = {
    "name": pa.string(),
    "age": pa.int32(),
    "score": pa.float64(),
}

# Convert PyArrow types to Polars
polars_schema = to_polars_schema(schema_with_pa)

# Convert PyArrow types to Pandas
pandas_schema = to_pandas_schema(schema_with_pa)

# You can also mix Pandas and PyArrow types
mixed_schema = {
    "name": "string",      # Pandas dtype string
    "age": pa.int32(),     # PyArrow type
    "score": "Float64",    # Pandas dtype string
}
polars_schema = to_polars_schema(mixed_schema)
```

**Note**: PyArrow support requires installing with `pip install cubchoo[pyarrow]`.


## Supported Type Mappings

Cubchoo supports comprehensive type mappings between Pandas and Polars. Below are the supported conversions:

### Pandas → Polars

| Pandas Type | Polars Type |
|------------|------------|
| `int8`, `Int8` | `pl.Int8` |
| `int16`, `Int16` | `pl.Int16` |
| `int32`, `Int32` | `pl.Int32` |
| `int64`, `Int64` | `pl.Int64` |
| `uint8`, `UInt8` | `pl.UInt8` |
| `uint16`, `UInt16` | `pl.UInt16` |
| `uint32`, `UInt32` | `pl.UInt32` |
| `uint64`, `UInt64` | `pl.UInt64` |
| `float32`, `Float32` | `pl.Float32` |
| `float64`, `Float64` | `pl.Float64` |
| `object`, `string`, `str` | `pl.String` |
| `bool`, `boolean` | `pl.Boolean` |
| `datetime64[ns]` | `pl.Datetime` |
| `datetime64[us]` | `pl.Datetime(time_unit="us")` |
| `datetime64[ms]` | `pl.Datetime(time_unit="ms")` |
| `datetime64[s]` | `pl.Datetime(time_unit="ms")` * |
| `date` | `pl.Date` |
| `timedelta64[ns]` | `pl.Duration` |
| `timedelta64[us]` | `pl.Duration(time_unit="us")` |
| `timedelta64[ms]` | `pl.Duration(time_unit="ms")` |
| `timedelta64[s]` | `pl.Duration(time_unit="ms")` * |
| `category` | `pl.Categorical` |

\* Note: Polars doesn't support seconds (`s`) time unit, so `datetime64[s]` and `timedelta64[s]` are converted to milliseconds (`ms`) as the closest equivalent.

### Polars → Pandas

| Polars Type | Pandas Type |
|------------|------------|
| `pl.Int8` | `Int8` |
| `pl.Int16` | `Int16` |
| `pl.Int32` | `Int32` |
| `pl.Int64` | `Int64` |
| `pl.UInt8` | `UInt8` |
| `pl.UInt16` | `UInt16` |
| `pl.UInt32` | `UInt32` |
| `pl.UInt64` | `UInt64` |
| `pl.Float32` | `Float32` |
| `pl.Float64` | `Float64` |
| `pl.String`, `pl.Utf8` | `string` |
| `pl.Boolean` | `boolean` |
| `pl.Datetime` | `datetime64[ns]` |
| `pl.Date` | `date` |
| `pl.Duration` | `timedelta64[ns]` |
| `pl.Categorical` | `category` |
| `pl.List(...)` | `object` |
| `pl.Struct(...)` | `object` |
| `pl.Map(...)` | `object` |

## Limitations and Notes

### Complex Types

* **List/Array Types**: Polars `List` types are converted to pandas `object` dtype, as pandas doesn't have native array/list dtypes. The semantic meaning is preserved but the structure information is lost.
* **Struct Types**: Polars `Struct` types are converted to pandas `object` dtype, as pandas doesn't have native struct types.
* **Map Types**: Polars `Map` types are converted to pandas `object` dtype, as pandas doesn't have native map types.

### Datetime Handling

* Pandas `datetime64` types with different time units are converted to Polars `Datetime` with corresponding time units.
* Timezone information in Polars `Datetime` types is not preserved when converting to pandas (pandas uses timezone-naive by default).
* Polars `Time` types are converted to pandas `object` dtype, as pandas doesn't have a native time type.

### Nullability

* **Pandas → Polars**: Nullable types (Int64, Float64, etc.) are properly converted to their Polars equivalents.
* **Polars → Pandas**: All Polars types can contain nulls, so nullable pandas dtypes (Int64, Float64, etc.) are used when appropriate.

### Input Validation

Cubchoo validates schemas before conversion:

* **Duplicate field names**: Raises `SchemaError` if duplicate field names are detected
* **Empty field names**: Raises `SchemaError` if any field name is an empty string
* **Invalid field types**: Raises `SchemaError` if field types are `None`
* **Invalid field name types**: Raises `SchemaError` if field names are not strings

## Advanced Examples

### Working with DataFrames

Easily convert schemas between DataFrames:

```python
import pandas as pd
import polars as pl
from cubchoo import to_polars_schema, to_pandas_schema

# Start with a pandas DataFrame
df_pandas = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [30, 25, 35],
    "score": [95.5, 87.0, 92.3],
})

# Convert schema to Polars
polars_schema = to_polars_schema(df_pandas)

# Create empty Polars DataFrame with same schema
df_polars = pl.DataFrame({}, schema=polars_schema)

# Convert back to pandas schema
pandas_schema = to_pandas_schema(polars_schema)
print(pandas_schema)
# {'name': 'string', 'age': 'Int64', 'score': 'Float64'}
```

### Categorical Data

Handle categorical data seamlessly:

```python
import pandas as pd
import polars as pl
from cubchoo import to_polars_schema, to_pandas_schema

# Pandas categorical
pandas_schema = {"category": "category"}
polars_schema = to_polars_schema(pandas_schema)
assert polars_schema["category"] == pl.Categorical()

# Polars categorical
polars_schema = pl.Schema({"category": pl.Categorical()})
pandas_schema = to_pandas_schema(polars_schema)
assert pandas_schema["category"] == "category"
```

### Series Conversion

Convert single-column schemas from pandas Series:

```python
import pandas as pd
from cubchoo import to_polars_schema

# Named Series
series = pd.Series([1, 2, 3], name="numbers", dtype="Int64")
polars_schema = to_polars_schema(series)
# Returns: Schema({'numbers': <class 'polars.datatypes.Int64'>})
```

### Round-Trip Conversion

Verify schema integrity with round-trip conversions:

```python
import pandas as pd
import polars as pl
from cubchoo import to_polars_schema, to_pandas_schema

# Start with Pandas schema
original = {
    "name": "string",
    "age": "Int64",
    "score": "Float64",
}

# Convert to Polars and back
polars_schema = to_polars_schema(original)
converted_back = to_pandas_schema(polars_schema)

# Verify types match
assert converted_back["name"] == original["name"]
assert converted_back["age"] == original["age"]
assert converted_back["score"] == original["score"]
```

### Datetime with Time Units

Handle different datetime precision:

```python
import pandas as pd
import polars as pl
from cubchoo import to_polars_schema, to_pandas_schema

# Pandas with different time units
pandas_schema = {
    "ns_timestamp": "datetime64[ns]",
    "us_timestamp": "datetime64[us]",
    "ms_timestamp": "datetime64[ms]",
}
polars_schema = to_polars_schema(pandas_schema)

# Polars with time units
polars_schema = {
    "ns": pl.Datetime(time_unit="ns"),
    "us": pl.Datetime(time_unit="us"),
    "ms": pl.Datetime(time_unit="ms"),
}
pandas_schema = to_pandas_schema(polars_schema)
```

## Error Handling

Cubchoo provides clear error messages through custom exceptions. All exceptions inherit from `ConversionError`, so you can catch all conversion errors at once or handle them individually:

```python
from cubchoo import ConversionError, UnsupportedTypeError, SchemaError

# Example 1: Handle specific error types
try:
    schema = to_polars_schema(invalid_schema)
except SchemaError as e:
    print(f"Invalid schema structure: {e}")
    # Handles: duplicate field names, empty field names, invalid field types, etc.
except UnsupportedTypeError as e:
    print(f"Unsupported type: {e}")
    # Handles: types that cannot be converted between Pandas and Polars
except ConversionError as e:
    print(f"General conversion error: {e}")
    # Catches all conversion-related errors (base class)

# Example 2: Catch all conversion errors
try:
    schema = to_polars_schema(invalid_schema)
except ConversionError as e:
    print(f"Conversion failed: {e}")
    # This will catch SchemaError, UnsupportedTypeError, and any future error types
```

## API Reference

### `to_polars_schema(pandas_schema)`

Convert a Pandas schema to a Polars `Schema`.

**Parameters:**

* `pandas_schema`: Pandas schema in any supported format:
  * `dict[str, dtype]`: Dictionary mapping field names to dtypes
  * `pandas.DataFrame`: DataFrame (schema inferred from dtypes)
  * `pandas.Series`: Series (for single column)
  * `list[tuple[str, dtype]]`: List of (field_name, dtype) tuples

**Returns:**

* `polars.Schema`: Polars Schema object mapping field names to Polars types

**Raises:**

* `SchemaError`: If the schema structure is invalid
* `UnsupportedTypeError`: If a type cannot be converted

**Example:**

```python
import pandas as pd
from cubchoo import to_polars_schema

# All formats work:
schema1 = {"name": "string", "age": "Int64"}
schema2 = pd.DataFrame({"name": ["Alice"], "age": [30]})
schema3 = [("name", "string"), ("age", "Int64")]

polars_schema = to_polars_schema(schema1)  # or schema2, or schema3
```

### `to_pandas_schema(polars_schema)`

Convert a Polars `Schema` to a Pandas schema.

**Parameters:**

* `polars_schema`: Polars schema in any supported format:
  * `pl.Schema` object
  * `dict[str, pl.DataType]`: Dictionary mapping field names to types
  * `list[tuple[str, pl.DataType]]`: List of (field_name, type) tuples

**Returns:**

* `dict[str, str]`: Dictionary mapping column names to pandas dtype strings

**Raises:**

* `SchemaError`: If the schema structure is invalid
* `UnsupportedTypeError`: If a type cannot be converted

**Example:**

```python
import polars as pl
from cubchoo import to_pandas_schema

polars_schema = pl.Schema({
    "name": pl.String,
    "age": pl.Int32
})

pandas_schema = to_pandas_schema(polars_schema)
# Returns: {'name': 'string', 'age': 'Int32'}
```

### PyArrow Type Support

Both `to_polars_schema()` and `to_pandas_schema()` support PyArrow types (`pa.DataType`) as input. When PyArrow types are detected in a schema, they are automatically converted to the target format.

**Example:**

```python
import pyarrow as pa
from cubchoo import to_polars_schema, to_pandas_schema

# Schema with PyArrow types
schema = {
    "name": pa.string(),
    "age": pa.int32(),
    "score": pa.float64(),
}

# Convert to Polars
polars_schema = to_polars_schema(schema)

# Convert to Pandas
pandas_schema = to_pandas_schema(schema)
```

**Note**: PyArrow support requires installing with `pip install cubchoo[pyarrow]`.

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/eddiethedean/cubchoo.git
cd cubchoo
```

2. Install in development mode:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cubchoo --cov-report=html

# Run specific test file
pytest tests/test_converters.py
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy cubchoo
```

### Project Structure

```
cubchoo/
├── cubchoo/
│   ├── __init__.py          # Public API
│   ├── converters.py         # Core conversion functions
│   ├── type_mappings.py      # Type mapping dictionaries
│   └── errors.py             # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_converters.py    # Conversion tests
│   └── test_type_mappings.py # Type mapping tests
├── .gitignore
├── LICENSE
├── README.md
├── CHANGELOG.md
└── pyproject.toml            # Package configuration
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Odos Matthews**

- Email: odosmatthews@gmail.com
- GitHub: [@eddiethedean](https://github.com/eddiethedean)

---

Made with ❤️ for the Python data science community

## Contributing

Contributions are welcome and greatly appreciated! 🎉

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Add tests** for new functionality
5. **Ensure all tests pass** (`pytest`)
6. **Ensure code quality** (`ruff format . && ruff check . && mypy cubchoo`)
7. **Commit your changes** (`git commit -m 'Add some amazing feature'`)
8. **Push to the branch** (`git push origin feature/amazing-feature`)
9. **Open a Pull Request**

### Reporting Issues

If you find a bug or have a feature request, please open an issue on [GitHub](https://github.com/eddiethedean/cubchoo/issues).

## Related Projects

- **[charmander](https://github.com/eddiethedean/charmander)** - Convert between Polars and PySpark schemas
- **[poldantic](https://github.com/callum-oakley/poldantic)** - Convert between Pydantic models and Polars schemas

## Inspiration

This project is inspired by [charmander](https://github.com/eddiethedean/charmander), which provides similar functionality for converting between Polars and PySpark schemas.

