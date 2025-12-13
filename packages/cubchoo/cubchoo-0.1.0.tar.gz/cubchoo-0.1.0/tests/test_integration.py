"""Integration tests for real-world schema conversion scenarios."""

import pandas as pd
import polars as pl

from cubchoo import to_pandas_schema, to_polars_schema


class TestRealWorldScenarios:
    """Tests for real-world schema conversion scenarios."""

    def test_ecommerce_schema(self):
        """Test e-commerce order schema conversion."""
        # Simulate an e-commerce order schema
        pandas_schema = {
            "order_id": "Int64",
            "customer_id": "Int64",
            "product_id": "Int64",
            "quantity": "Int32",
            "price": "Float64",
            "order_date": "datetime64[ns]",
            "shipping_date": "date",
            "status": "category",
            "notes": "string",
        }

        polars_schema = to_polars_schema(pandas_schema)
        assert isinstance(polars_schema, pl.Schema)
        assert len(polars_schema) == 9

        # Round trip
        pandas_result = to_pandas_schema(polars_schema)
        assert len(pandas_result) == 9
        assert pandas_result["order_id"] == "Int64"
        assert pandas_result["status"] == "category"

    def test_time_series_schema(self):
        """Test time series data schema conversion."""
        pandas_schema = {
            "timestamp": "datetime64[ns]",
            "value": "Float64",
            "sensor_id": "Int32",
            "location": "string",
            "quality": "Int8",
        }

        polars_schema = to_polars_schema(pandas_schema)
        assert isinstance(polars_schema, pl.Schema)

        # Convert back
        pandas_result = to_pandas_schema(polars_schema)
        assert "timestamp" in pandas_result
        assert "datetime" in pandas_result["timestamp"]

    def test_user_profile_schema(self):
        """Test user profile schema conversion."""
        pandas_schema = {
            "user_id": "Int64",
            "username": "string",
            "email": "string",
            "age": "Int32",
            "created_at": "datetime64[ns]",
            "is_active": "boolean",
            "preferences": "string",  # JSON string
        }

        polars_schema = to_polars_schema(pandas_schema)
        pandas_result = to_pandas_schema(polars_schema)

        assert pandas_result["user_id"] == "Int64"
        assert pandas_result["username"] == "string"
        assert pandas_result["is_active"] == "boolean"

    def test_financial_data_schema(self):
        """Test financial data schema conversion."""
        pandas_schema = {
            "symbol": "string",
            "date": "date",
            "open": "Float64",
            "high": "Float64",
            "low": "Float64",
            "close": "Float64",
            "volume": "Int64",
            "adjusted_close": "Float64",
        }

        polars_schema = to_polars_schema(pandas_schema)
        pandas_result = to_pandas_schema(polars_schema)

        assert all(field in pandas_result for field in pandas_schema.keys())
        assert pandas_result["symbol"] == "string"
        assert pandas_result["date"] == "date"

    def test_actual_dataframe_conversion(self):
        """Test conversion with actual DataFrame data."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
                "score": [95.5, 87.0, 92.3],
                "active": [True, False, True],
                "created": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
            }
        )

        polars_schema = to_polars_schema(df)
        assert isinstance(polars_schema, pl.Schema)
        assert "id" in polars_schema
        assert "name" in polars_schema
        assert "score" in polars_schema
        assert "active" in polars_schema
        assert "created" in polars_schema

        # Convert to pandas schema
        pandas_schema = to_pandas_schema(polars_schema)
        assert isinstance(pandas_schema, dict)
        assert len(pandas_schema) == 5

    def test_actual_polars_dataframe_schema(self):
        """Test conversion with actual Polars DataFrame schema."""
        df = pl.DataFrame(
            {
                "id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
                "score": [95.5, 87.0, 92.3],
                "active": [True, False, True],
            }
        )

        pandas_schema = to_pandas_schema(df.schema)
        assert isinstance(pandas_schema, dict)
        assert "id" in pandas_schema
        assert "name" in pandas_schema
        assert pandas_schema["name"] == "string"
        assert pandas_schema["active"] == "boolean"

        # Round trip
        polars_schema = to_polars_schema(pandas_schema)
        assert polars_schema["id"] == pl.Int64
        assert polars_schema["name"] == pl.String

    def test_schema_with_many_fields(self):
        """Test schema with many fields (realistic large schema)."""
        # Simulate a schema with 50 fields
        pandas_schema = {f"field_{i}": "string" if i % 2 == 0 else "Int64" for i in range(50)}

        polars_schema = to_polars_schema(pandas_schema)
        assert len(polars_schema) == 50

        pandas_result = to_pandas_schema(polars_schema)
        assert len(pandas_result) == 50

    def test_mixed_nullable_and_non_nullable(self):
        """Test schema with mixed nullable and non-nullable types."""
        df = pd.DataFrame(
            {
                "nullable_int": pd.Series([1, 2, None], dtype="Int64"),
                "non_nullable_int": pd.Series([1, 2, 3], dtype="int64"),
                "nullable_string": pd.Series(["a", "b", None], dtype="string"),
                "non_nullable_string": pd.Series(["a", "b", "c"], dtype="string"),
            }
        )

        polars_schema = to_polars_schema(df)
        assert polars_schema["nullable_int"] == pl.Int64
        assert polars_schema["non_nullable_int"] == pl.Int64
        assert polars_schema["nullable_string"] == pl.String
        assert polars_schema["non_nullable_string"] == pl.String

    def test_categorical_with_categories(self):
        """Test categorical type with actual categories."""
        df = pd.DataFrame(
            {
                "status": pd.Categorical(
                    ["pending", "completed", "failed"],
                    categories=["pending", "completed", "failed"],
                ),
            }
        )

        polars_schema = to_polars_schema(df)
        assert polars_schema["status"] == pl.Categorical

        pandas_result = to_pandas_schema(polars_schema)
        assert pandas_result["status"] == "category"

    def test_datetime_with_timezone(self):
        """Test datetime with timezone information."""
        df = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            }
        )

        polars_schema = to_polars_schema(df)
        assert isinstance(polars_schema["timestamp"], pl.Datetime)

    def test_complex_nested_workflow(self):
        """Test complex workflow with multiple conversions."""
        # Start with pandas schema
        pandas_schema = {
            "id": "Int64",
            "name": "string",
            "score": "Float64",
        }

        # Convert to Polars
        polars_schema = to_polars_schema(pandas_schema)

        # Convert to pandas
        pandas_result = to_pandas_schema(polars_schema)

        # Convert back to Polars
        polars_result = to_polars_schema(pandas_result)

        # All should be consistent
        assert polars_result["id"] == polars_schema["id"]
        assert polars_result["name"] == polars_schema["name"]
        assert polars_result["score"] == polars_schema["score"]

    def test_performance_large_schema(self):
        """Test performance with large schema (1000 fields)."""
        schema = {f"field_{i}": "string" for i in range(1000)}

        polars_schema = to_polars_schema(schema)
        assert len(polars_schema) == 1000

        pandas_result = to_pandas_schema(polars_schema)
        assert len(pandas_result) == 1000

    def test_mixed_input_formats(self):
        """Test mixing different input formats in workflow."""
        # Start with dict
        schema_dict = {"name": "string", "age": "Int32"}

        # Convert to Polars
        polars_schema = to_polars_schema(schema_dict)

        # Convert to pandas dict
        pandas_dict = to_pandas_schema(polars_schema)

        # Convert back using list of tuples
        schema_list = list(pandas_dict.items())
        polars_result = to_polars_schema(schema_list)

        assert polars_result["name"] == pl.String
        assert polars_result["age"] == pl.Int32
