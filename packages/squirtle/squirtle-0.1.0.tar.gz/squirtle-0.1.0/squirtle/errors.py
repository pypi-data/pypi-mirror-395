"""Custom exceptions for squirtle."""


class ConversionError(Exception):
    """Base exception for conversion errors."""

    pass


class SchemaError(ConversionError):
    """Raised when a schema structure is invalid."""

    pass


class UnsupportedTypeError(ConversionError):
    """Raised when a type cannot be converted."""

    pass
