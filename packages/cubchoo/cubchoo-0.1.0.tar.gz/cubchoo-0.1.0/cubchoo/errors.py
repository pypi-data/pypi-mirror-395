"""Custom exceptions for cubchoo schema conversion."""


class ConversionError(Exception):
    """Base exception for all conversion errors."""

    pass


class SchemaError(ConversionError):
    """Raised when a schema structure is invalid."""

    pass


class UnsupportedTypeError(ConversionError):
    """Raised when a type cannot be converted between Pandas and Polars."""

    pass
