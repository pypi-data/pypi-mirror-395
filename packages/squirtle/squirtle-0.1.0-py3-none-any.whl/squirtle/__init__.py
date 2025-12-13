"""Squirtle - Convert between Polars schemas and SQLAlchemy/SQLModel classes."""

__version__ = "0.1.0"

from squirtle.converters import to_polars_schema, to_sqlalchemy_model, to_sqlmodel_class
from squirtle.errors import ConversionError, SchemaError, UnsupportedTypeError

__all__ = [
    "to_polars_schema",
    "to_sqlalchemy_model",
    "to_sqlmodel_class",
    "ConversionError",
    "SchemaError",
    "UnsupportedTypeError",
]
