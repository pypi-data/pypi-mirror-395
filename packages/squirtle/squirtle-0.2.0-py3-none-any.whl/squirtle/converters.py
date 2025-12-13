"""Core conversion functions for squirtle."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, cast

if TYPE_CHECKING:
    import polars as pl
    from polars.datatypes import DataType
    from sqlalchemy import Column
    from sqlalchemy.orm import DeclarativeBase
else:
    try:
        import polars as pl
        from polars.datatypes import DataType
    except ImportError:
        pl = None  # type: ignore[assignment]
        DataType = None  # type: ignore[assignment, misc]

    try:
        from sqlalchemy import Column
        from sqlalchemy.orm import DeclarativeBase
    except ImportError:
        Column = None  # type: ignore[assignment, misc]
        DeclarativeBase = None  # type: ignore[assignment, misc]

from squirtle.errors import SchemaError, UnsupportedTypeError
from squirtle.type_mappings import polars_to_sqlalchemy_type, sqlalchemy_to_polars_type


def to_sqlalchemy_model(
    polars_schema: Union[Dict[str, DataType], "pl.Schema"],
    primary_key: Union[str, List[str]],
    class_name: str = "GeneratedModel",
    base: Optional[Type[DeclarativeBase]] = None,
) -> Type[DeclarativeBase]:
    """
    Convert a Polars schema to a SQLAlchemy model class.

    Args:
        polars_schema: Polars schema (dict[str, DataType] or pl.Schema object)
        primary_key: Field name(s) to use as primary key. Can be a single string or list of strings for composite keys.
        class_name: Name for the generated model class (must be a valid Python identifier)
        base: Base class for the model (optional, defaults to DeclarativeBase)

    Returns:
        SQLAlchemy model class with __tablename__ attribute

    Raises:
        SchemaError: If the schema structure is invalid, class_name is invalid, or primary_key fields don't exist
        UnsupportedTypeError: If a type cannot be converted
        ImportError: If required dependencies are not installed
    """
    if pl is None:
        raise ImportError("polars is required. Install with: pip install polars")
    if DeclarativeBase is None:
        raise ImportError("sqlalchemy is required. Install with: pip install sqlalchemy")

    # Validate class_name is a valid Python identifier
    if not class_name or not class_name.isidentifier():
        raise SchemaError(f"Invalid class name: '{class_name}'. Must be a valid Python identifier.")

    # Convert schema to dict if it's a Schema object
    if hasattr(polars_schema, "items"):
        # It's already a dict-like object
        schema_dict = dict(polars_schema.items())
    elif isinstance(polars_schema, dict):
        schema_dict = polars_schema
    else:
        raise SchemaError(f"Invalid schema type: {type(polars_schema)}")

    # Validate schema
    if not schema_dict:
        raise SchemaError("Schema must contain at least one field")

    # Check for duplicate field names
    field_names = list(schema_dict.keys())
    if len(field_names) != len(set(field_names)):
        raise SchemaError("Schema contains duplicate field names")

    # Validate field names
    for field_name in field_names:
        if not field_name or not isinstance(field_name, str):
            raise SchemaError(f"Invalid field name: {field_name}")

    # Normalize primary_key to a list
    if isinstance(primary_key, str):
        primary_key_fields = [primary_key]
    elif isinstance(primary_key, list):
        primary_key_fields = primary_key
    else:
        raise SchemaError(
            f"primary_key must be a string or list of strings, got {type(primary_key).__name__}"
        )

    # Validate that all primary key fields exist in the schema
    for pk_field in primary_key_fields:
        if not isinstance(pk_field, str):
            raise SchemaError(f"Primary key field must be a string, got {type(pk_field).__name__}")
        if pk_field not in schema_dict:
            raise SchemaError(
                f"Primary key field '{pk_field}' not found in schema. Available fields: {list(schema_dict.keys())}"
            )

    # Use provided base or create default
    if base is None:
        from sqlalchemy.orm import DeclarativeBase as DefaultBase

        class Base(DefaultBase):
            pass

        base = Base

    # Build class attributes
    attrs = {"__tablename__": _to_snake_case(class_name)}

    # Create columns
    for field_name, field_type in schema_dict.items():
        # Check if type is nullable and unwrap if needed
        is_nullable = _is_polars_type_nullable(field_type)
        base_type = _unwrap_polars_nullable(field_type)

        # Convert to SQLAlchemy type
        try:
            sqlalchemy_type = polars_to_sqlalchemy_type(base_type)
        except UnsupportedTypeError as e:
            raise UnsupportedTypeError(f"Field '{field_name}': {e}") from e

        # Determine if this is a primary key
        is_primary_key = field_name in primary_key_fields

        # Create column
        if Column is None:
            raise ImportError("sqlalchemy is required")
        attrs[field_name] = Column(  # type: ignore[assignment]
            sqlalchemy_type, nullable=is_nullable, primary_key=is_primary_key
        )

    # Dynamically create the class
    model_class = type(class_name, (base,), attrs)
    return model_class


def to_polars_schema(model: Union[Type, object]) -> "pl.Schema":
    """
    Convert a SQLAlchemy model class, instance, or SQLModel class to a Polars schema.

    Args:
        model: SQLAlchemy model class/instance or SQLModel class

    Returns:
        Polars Schema object

    Raises:
        SchemaError: If the model structure is invalid
        UnsupportedTypeError: If a type cannot be converted
        ImportError: If required dependencies are not installed
    """
    if pl is None:
        raise ImportError("polars is required. Install with: pip install polars")

    # Get the class if an instance was passed
    if not isinstance(model, type):
        model = type(model)

    # Get the table
    if not hasattr(model, "__table__"):
        raise SchemaError(
            f"Model {model.__name__} does not have a __table__ attribute. "
            "Ensure it's a SQLAlchemy or SQLModel class."
        )

    table = getattr(model, "__table__", None)  # type: ignore[attr-defined]
    if table is None:
        raise SchemaError(f"Model {model.__name__} has no table definition")

    # Build schema dict
    schema_dict = {}

    for column in table.columns:
        column_name = column.name
        column_type = type(column.type)

        # Convert to Polars type
        # Note: Polars schemas don't explicitly track nullability
        try:
            polars_type = sqlalchemy_to_polars_type(column_type)
        except UnsupportedTypeError as e:
            raise UnsupportedTypeError(f"Column '{column_name}': {e}") from e

        # Note: Polars schemas don't explicitly track nullability
        # All columns in Polars DataFrames can be nullable
        # We just use the base type
        schema_dict[column_name] = polars_type

    if not schema_dict:
        raise SchemaError("Model has no columns")

    # Create and return Polars Schema
    return pl.Schema(schema_dict)


def to_sqlmodel_class(
    polars_schema: Union[Dict[str, DataType], "pl.Schema"],
    primary_key: str,
    class_name: str = "GeneratedModel",
) -> Any:  # Return type is Type[SQLModel] but SQLModel may not be available at type-check time
    """
    Convert a Polars schema to a SQLModel class with type annotations.

    Args:
        polars_schema: Polars schema (dict[str, DataType] or pl.Schema object)
        primary_key: Field name to use as primary key (must be a single string)
        class_name: Name for the generated model class (must be a valid Python identifier)

    Returns:
        SQLModel class with type annotations and default values

    Raises:
        SchemaError: If the schema structure is invalid, class_name is invalid, or primary_key field doesn't exist
        UnsupportedTypeError: If a type cannot be converted
        ImportError: If SQLModel is not installed
    """
    try:
        from sqlmodel import Field, SQLModel
    except ImportError:
        raise ImportError(
            "sqlmodel is required for to_sqlmodel_class. "
            "Install with: pip install squirtle[sqlmodel]"
        )

    if pl is None:
        raise ImportError("polars is required. Install with: pip install polars")

    # Validate class_name is a valid Python identifier
    if not class_name or not class_name.isidentifier():
        raise SchemaError(f"Invalid class name: '{class_name}'. Must be a valid Python identifier.")

    # Convert schema to dict if it's a Schema object
    if hasattr(polars_schema, "items"):
        schema_dict = dict(polars_schema.items())
    elif isinstance(polars_schema, dict):
        schema_dict = polars_schema
    else:
        raise SchemaError(f"Invalid schema type: {type(polars_schema)}")

    # Validate schema
    if not schema_dict:
        raise SchemaError("Schema must contain at least one field")

    # Check for duplicate field names
    field_names = list(schema_dict.keys())
    if len(field_names) != len(set(field_names)):
        raise SchemaError("Schema contains duplicate field names")

    # Validate field names
    for field_name in field_names:
        if not field_name or not isinstance(field_name, str):
            raise SchemaError(f"Invalid field name: {field_name}")

    # Validate primary_key parameter
    if not isinstance(primary_key, str):
        raise SchemaError(
            f"primary_key must be a string for SQLModel, got {type(primary_key).__name__}"
        )
    if primary_key not in schema_dict:
        raise SchemaError(
            f"Primary key field '{primary_key}' not found in schema. Available fields: {list(schema_dict.keys())}"
        )

    # Import typing for type annotations
    from typing import Optional

    # Build class attributes
    attrs = {"__tablename__": _to_snake_case(class_name)}

    # Import types for annotations
    from datetime import date, datetime, time
    from decimal import Decimal

    # Create fields with type annotations
    annotations = {}
    for field_name, field_type in schema_dict.items():
        # Check if type is nullable and unwrap if needed
        is_nullable = _is_polars_type_nullable(field_type)
        base_type = _unwrap_polars_nullable(field_type)
        is_primary_key = field_name == primary_key

        # Get Python type annotation
        type_str = str(base_type)

        # Map to actual Python types
        python_type: Any = None
        if type_str in ("Int8", "Int16", "Int32", "Int64", "UInt8", "UInt16", "UInt32", "UInt64"):
            python_type = int
        elif type_str in ("Float32", "Float64"):
            python_type = float
        elif type_str in ("String", "Utf8"):
            python_type = str
        elif type_str in ("Boolean", "Bool"):
            python_type = bool
        elif type_str == "Date":
            python_type = date
        elif type_str.startswith("Datetime") or type_str.startswith("datetime"):
            python_type = datetime
        elif type_str == "Time":
            python_type = time
        elif type_str.startswith("Decimal"):
            python_type = Decimal

        # Build Field definition
        field_kwargs: Dict[str, Any] = {}
        if is_primary_key:
            field_kwargs["primary_key"] = True
        if not is_nullable:
            field_kwargs["nullable"] = False

        # Create annotation
        if python_type is not None:
            if is_nullable:
                annotation_type: Any = Optional[python_type]
            else:
                annotation_type = python_type
        else:
            annotation_type = Any

        # Store annotation
        annotations[field_name] = annotation_type
        # Only pass kwargs if there are any, otherwise use Field() with defaults
        if field_kwargs:
            attrs[field_name] = Field(**field_kwargs)  # type: ignore[call-overload]
        else:
            attrs[field_name] = Field()  # type: ignore[call-overload]

    # Set annotations
    attrs["__annotations__"] = annotations  # type: ignore[assignment]

    # Dynamically create the class
    # Note: This is a simplified version. Full implementation would use
    # proper type annotations and Field() definitions
    model_class = type(class_name, (SQLModel,), attrs)
    return model_class


def _to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _is_polars_type_nullable(polars_type: DataType) -> bool:
    """
    Check if a Polars type is nullable.

    Note: Polars schemas don't explicitly track nullability in the DataType itself.
    All columns in Polars DataFrames can contain nulls regardless of schema type.
    This function defaults to True (nullable) unless we can detect an explicit
    non-nullable marker (which Polars doesn't currently support in schemas).
    """
    if pl is None:
        return True  # Default to nullable if polars not available

    type_str = str(polars_type)
    # Check for Null wrapper - if explicitly wrapped, it's definitely nullable
    if type_str.startswith("Null(") or type_str.startswith("null("):
        return True

    # Check if it's a Null type directly
    if hasattr(pl, "Null") and isinstance(polars_type, pl.Null):
        return True

    # Check for inner attribute (Null wrapper)
    if hasattr(polars_type, "inner"):
        return True

    # Default to nullable since Polars DataFrames can contain nulls
    # even if the schema type doesn't explicitly mark it
    return True


def _unwrap_polars_nullable(polars_type: DataType) -> DataType:
    """Unwrap a nullable Polars type to get the base type."""
    if pl is None:
        return polars_type

    type_str = str(polars_type)

    # Check if it's a Null wrapper
    if type_str.startswith("Null(") or type_str.startswith("null("):
        # Try to get inner type
        if hasattr(polars_type, "inner"):
            return cast(DataType, polars_type.inner)
        # Try to get inner from the type itself
        if hasattr(polars_type, "_inner"):
            return cast(DataType, polars_type._inner)

    # Check if it's a Null type instance
    if hasattr(pl, "Null") and isinstance(polars_type, pl.Null):
        if hasattr(polars_type, "inner"):
            return cast(DataType, polars_type.inner)
        if hasattr(polars_type, "_inner"):
            return cast(DataType, polars_type._inner)

    # Not nullable, return as-is
    return polars_type
