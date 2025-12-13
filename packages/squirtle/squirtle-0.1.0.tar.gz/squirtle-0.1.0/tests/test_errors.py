"""Tests for squirtle error handling."""

import pytest

from squirtle.errors import ConversionError, SchemaError, UnsupportedTypeError


def test_conversion_error():
    """Test ConversionError can be raised and caught."""
    with pytest.raises(ConversionError):
        raise ConversionError("Test error")


def test_schema_error():
    """Test SchemaError can be raised and caught."""
    with pytest.raises(SchemaError):
        raise SchemaError("Invalid schema")

    # SchemaError should be a subclass of ConversionError
    assert issubclass(SchemaError, ConversionError)


def test_unsupported_type_error():
    """Test UnsupportedTypeError can be raised and caught."""
    with pytest.raises(UnsupportedTypeError):
        raise UnsupportedTypeError("Unsupported type")

    # UnsupportedTypeError should be a subclass of ConversionError
    assert issubclass(UnsupportedTypeError, ConversionError)
