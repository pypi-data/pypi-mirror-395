"""Type mappings between Polars DataTypes and SQLAlchemy types."""

from typing import TYPE_CHECKING, Any, Dict, Type

if TYPE_CHECKING:
    import polars as pl
    from polars.datatypes import DataType
else:
    try:
        import polars as pl
        from polars.datatypes import DataType
    except ImportError:
        pl = None  # type: ignore[assignment]
        DataType = None  # type: ignore[assignment, misc]

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
    # SQLAlchemy not available
    pass

from squirtle.errors import UnsupportedTypeError


def polars_to_sqlalchemy_type(polars_type: "DataType") -> Type:
    """
    Convert a Polars DataType to a SQLAlchemy type.

    Args:
        polars_type: Polars DataType instance

    Returns:
        SQLAlchemy Column type class

    Raises:
        UnsupportedTypeError: If the Polars type cannot be converted
    """
    if pl is None:
        raise ImportError("polars is required for type conversions")

    # Handle nullable types (wrapped in Null)
    # Check for Null wrapper by examining the type string representation
    if hasattr(polars_type, "inner") and str(polars_type).startswith("Null"):
        polars_type = polars_type.inner

    type_str = str(polars_type)

    # Integer types
    if type_str in ("Int8", "i8"):
        return SmallInteger
    elif type_str in ("Int16", "i16"):
        return SmallInteger
    elif type_str in ("Int32", "i32"):
        return Integer
    elif type_str in ("Int64", "i64"):
        return BigInteger
    elif type_str in ("UInt8", "u8"):
        return SmallInteger
    elif type_str in ("UInt16", "u16"):
        return SmallInteger
    elif type_str in ("UInt32", "u32"):
        return Integer
    elif type_str in ("UInt64", "u64"):
        return BigInteger

    # Float types
    elif type_str in ("Float32", "f32"):
        return Float
    elif type_str in ("Float64", "f64"):
        return Float

    # String types
    elif type_str in ("String", "Utf8", "str"):
        return String

    # Boolean
    elif type_str in ("Boolean", "Bool", "bool"):
        return Boolean

    # Date/Time types
    elif type_str in ("Date", "date"):
        return Date
    elif type_str.startswith("Datetime") or type_str.startswith("datetime"):
        # Handle Datetime with time units like "Datetime('us')"
        return DateTime
    elif type_str in ("Time", "time"):
        return Time

    # Decimal/Numeric
    elif type_str.startswith("Decimal") or type_str.startswith("Decimal("):
        # Extract precision and scale if available
        return Numeric

    # Unsupported types
    elif type_str.startswith("List") or type_str.startswith("Array"):
        raise UnsupportedTypeError(f"List/Array types are not supported: {type_str}")
    elif type_str.startswith("Struct"):
        raise UnsupportedTypeError(f"Struct types are not supported: {type_str}")
    elif type_str.startswith("Map"):
        raise UnsupportedTypeError(f"Map types are not supported: {type_str}")
    else:
        raise UnsupportedTypeError(f"Unsupported Polars type: {type_str}")


def sqlalchemy_to_polars_type(sqlalchemy_type: Type) -> Any:  # type: ignore[return]
    """
    Convert a SQLAlchemy type to a Polars DataType.

    Args:
        sqlalchemy_type: SQLAlchemy Column type class

    Returns:
        Polars DataType instance

    Raises:
        UnsupportedTypeError: If the SQLAlchemy type cannot be converted
    """
    if pl is None:
        raise ImportError("polars is required for type conversions")

    # Get the type name
    type_name = sqlalchemy_type.__name__

    # Integer types
    if type_name == "SmallInteger":
        return pl.Int16
    elif type_name == "Integer":
        return pl.Int32
    elif type_name == "BigInteger":
        return pl.Int64

    # Float types
    elif type_name == "Float":
        return pl.Float64
    elif type_name == "Double":
        return pl.Float64

    # String types
    elif type_name in ("String", "Text", "Unicode", "UnicodeText"):
        return pl.String

    # Boolean
    elif type_name == "Boolean":
        return pl.Boolean

    # Date/Time types
    elif type_name == "Date":
        return pl.Date
    elif type_name == "DateTime":
        return pl.Datetime("us")  # Default to microseconds
    elif type_name == "Time":
        return pl.Time

    # Numeric/Decimal
    elif type_name in ("Numeric", "Decimal"):
        return pl.Decimal

    else:
        raise UnsupportedTypeError(f"Unsupported SQLAlchemy type: {type_name}")


# Mapping dictionaries for reference (populated at runtime)
POLARS_TO_SQLALCHEMY: Dict[str, Type] = {}
SQLALCHEMY_TO_POLARS: Dict[str, Any] = {}

# Initialize dictionaries if imports are available
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

    if pl is not None:
        POLARS_TO_SQLALCHEMY = {
            "Int8": SmallInteger,
            "Int16": SmallInteger,
            "Int32": Integer,
            "Int64": BigInteger,
            "UInt8": SmallInteger,
            "UInt16": SmallInteger,
            "UInt32": Integer,
            "UInt64": BigInteger,
            "Float32": Float,
            "Float64": Float,
            "String": String,
            "Utf8": String,
            "Boolean": Boolean,
            "Bool": Boolean,
            "Date": Date,
            "Datetime": DateTime,
            "Time": Time,
            "Decimal": Numeric,
        }

        SQLALCHEMY_TO_POLARS = {
            "SmallInteger": pl.Int16,
            "Integer": pl.Int32,
            "BigInteger": pl.Int64,
            "Float": pl.Float64,
            "Double": pl.Float64,
            "String": pl.String,
            "Text": pl.String,
            "Boolean": pl.Boolean,
            "Date": pl.Date,
            "DateTime": pl.Datetime,
            "Time": pl.Time,
            "Numeric": pl.Decimal,
            "Decimal": pl.Decimal,
        }
except ImportError:
    pass
