"""Tests for type mappings between Polars and SQLAlchemy."""

import pytest

try:
    import polars as pl
except ImportError:
    pytest.skip("polars not installed", allow_module_level=True)

try:
    from sqlalchemy import (
        BigInteger,
        Boolean,
        Date,
        DateTime,
        Float,
        Integer,
        Numeric,
        SmallInteger,
        String,
        Time,
    )
except ImportError:
    pytest.skip("sqlalchemy not installed", allow_module_level=True)

from squirtle.errors import UnsupportedTypeError
from squirtle.type_mappings import polars_to_sqlalchemy_type, sqlalchemy_to_polars_type


class TestPolarsToSQLAlchemy:
    """Tests for converting Polars types to SQLAlchemy types."""

    def test_int_types(self):
        """Test integer type conversions."""
        assert polars_to_sqlalchemy_type(pl.Int8) == SmallInteger
        assert polars_to_sqlalchemy_type(pl.Int16) == SmallInteger
        assert polars_to_sqlalchemy_type(pl.Int32) == Integer
        assert polars_to_sqlalchemy_type(pl.Int64) == BigInteger
        assert polars_to_sqlalchemy_type(pl.UInt8) == SmallInteger
        assert polars_to_sqlalchemy_type(pl.UInt16) == SmallInteger
        assert polars_to_sqlalchemy_type(pl.UInt32) == Integer
        assert polars_to_sqlalchemy_type(pl.UInt64) == BigInteger

    def test_float_types(self):
        """Test float type conversions."""
        assert polars_to_sqlalchemy_type(pl.Float32) == Float
        assert polars_to_sqlalchemy_type(pl.Float64) == Float

    def test_string_types(self):
        """Test string type conversions."""
        assert polars_to_sqlalchemy_type(pl.String) == String

    def test_boolean_type(self):
        """Test boolean type conversion."""
        assert polars_to_sqlalchemy_type(pl.Boolean) == Boolean

    def test_date_time_types(self):
        """Test date/time type conversions."""
        assert polars_to_sqlalchemy_type(pl.Date) == Date
        assert polars_to_sqlalchemy_type(pl.Datetime) == DateTime
        assert polars_to_sqlalchemy_type(pl.Time) == Time

    def test_decimal_type(self):
        """Test decimal type conversion."""
        assert polars_to_sqlalchemy_type(pl.Decimal) == Numeric

    def test_unsupported_list_type(self):
        """Test that List types raise UnsupportedTypeError."""
        with pytest.raises(UnsupportedTypeError):
            polars_to_sqlalchemy_type(pl.List(pl.String))

    def test_unsupported_struct_type(self):
        """Test that Struct types raise UnsupportedTypeError."""
        with pytest.raises(UnsupportedTypeError):
            polars_to_sqlalchemy_type(pl.Struct([pl.Field("name", pl.String)]))


class TestSQLAlchemyToPolars:
    """Tests for converting SQLAlchemy types to Polars types."""

    def test_integer_types(self):
        """Test integer type conversions."""
        assert sqlalchemy_to_polars_type(SmallInteger) == pl.Int16
        assert sqlalchemy_to_polars_type(Integer) == pl.Int32
        assert sqlalchemy_to_polars_type(BigInteger) == pl.Int64

    def test_float_types(self):
        """Test float type conversions."""
        assert sqlalchemy_to_polars_type(Float) == pl.Float64

    def test_string_types(self):
        """Test string type conversions."""
        assert sqlalchemy_to_polars_type(String) == pl.String

    def test_boolean_type(self):
        """Test boolean type conversion."""
        assert sqlalchemy_to_polars_type(Boolean) == pl.Boolean

    def test_date_time_types(self):
        """Test date/time type conversions."""
        assert sqlalchemy_to_polars_type(Date) == pl.Date
        assert sqlalchemy_to_polars_type(DateTime) == pl.Datetime
        assert sqlalchemy_to_polars_type(Time) == pl.Time

    def test_numeric_type(self):
        """Test numeric type conversion."""
        assert sqlalchemy_to_polars_type(Numeric) == pl.Decimal
