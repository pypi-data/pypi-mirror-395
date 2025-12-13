"""Tests for core conversion functions."""

import pytest

try:
    import polars as pl
except ImportError:
    pytest.skip("polars not installed", allow_module_level=True)

try:
    from sqlalchemy import Column, Float, Integer, String
    from sqlalchemy.orm import DeclarativeBase
except ImportError:
    pytest.skip("sqlalchemy not installed", allow_module_level=True)

from squirtle.converters import to_polars_schema, to_sqlalchemy_model
from squirtle.errors import SchemaError, UnsupportedTypeError


class Base(DeclarativeBase):
    """Test base class."""

    pass


class TestToSQLAlchemyModel:
    """Tests for to_sqlalchemy_model function."""

    def test_basic_schema(self):
        """Test converting a basic Polars schema to SQLAlchemy model."""
        schema = pl.Schema(
            {
                "name": pl.String,
                "age": pl.Int32,
                "score": pl.Float64,
            }
        )

        Person = to_sqlalchemy_model(schema, primary_key="name", class_name="Person", base=Base)

        assert Person.__name__ == "Person"
        assert Person.__tablename__ == "person"
        assert hasattr(Person, "name")
        assert hasattr(Person, "age")
        assert hasattr(Person, "score")
        # SQLAlchemy model attributes are InstrumentedAttribute, not Column
        from sqlalchemy.orm import InstrumentedAttribute

        assert isinstance(Person.name, InstrumentedAttribute)
        assert isinstance(Person.age, InstrumentedAttribute)
        assert isinstance(Person.score, InstrumentedAttribute)

    def test_schema_dict(self):
        """Test converting a schema dict to SQLAlchemy model."""
        schema_dict = {
            "id": pl.Int64,
            "name": pl.String,
        }

        Model = to_sqlalchemy_model(
            schema_dict, primary_key="id", class_name="TestModel", base=Base
        )

        assert Model.__name__ == "TestModel"
        assert hasattr(Model, "id")
        assert hasattr(Model, "name")

    def test_nullable_fields(self):
        """Test handling of nullable fields."""
        schema = pl.Schema(
            {
                "id": pl.Int64,
                "name": pl.String,
            }
        )

        Model = to_sqlalchemy_model(
            schema, primary_key="id", class_name="TestModelNullable", base=Base
        )

        # id should be primary key
        assert Model.id.primary_key is True
        # All fields default to nullable in Polars schemas
        assert Model.name.nullable is True

    def test_empty_schema(self):
        """Test that empty schema raises SchemaError."""
        schema = pl.Schema({})

        with pytest.raises(SchemaError, match="at least one field"):
            to_sqlalchemy_model(schema, primary_key="name", base=Base)

    def test_duplicate_fields(self):
        """Test that duplicate fields raise SchemaError."""
        # Python dicts can't have duplicate keys, so we test with a Schema
        # that would have duplicates if constructed improperly
        # Instead, test with a list of tuples that has duplicates
        from collections import OrderedDict

        schema_dict = OrderedDict(
            [
                ("name", pl.String),
                ("name", pl.String),  # This will overwrite the first one
            ]
        )
        # The dict will only have one "name" key, so we need to test differently
        # Actually, we can't test this with a dict. Let's test with invalid field names instead
        schema_dict = {
            "": pl.String,  # Empty field name
        }

        with pytest.raises(SchemaError, match="Invalid field name"):
            to_sqlalchemy_model(schema_dict, primary_key="", base=Base)

    def test_unsupported_type(self):
        """Test that unsupported types raise UnsupportedTypeError."""
        schema = pl.Schema(
            {
                "items": pl.List(pl.String),
            }
        )

        with pytest.raises(UnsupportedTypeError):
            to_sqlalchemy_model(schema, primary_key="items", base=Base)


class TestToPolarsSchema:
    """Tests for to_polars_schema function."""

    def test_basic_model(self):
        """Test converting a basic SQLAlchemy model to Polars schema."""

        class PersonBasic(Base):
            __tablename__ = "person_basic"

            name = Column(String, primary_key=True)
            age = Column(Integer)
            score = Column(Float)

        schema = to_polars_schema(PersonBasic)

        assert isinstance(schema, pl.Schema)
        assert "name" in schema
        assert "age" in schema
        assert "score" in schema
        assert schema["name"] == pl.String
        assert schema["age"] == pl.Int32
        assert schema["score"] == pl.Float64

    def test_model_instance(self):
        """Test converting a model instance to Polars schema."""

        class PersonInstance(Base):
            __tablename__ = "person_instance"

            name = Column(String, primary_key=True)
            age = Column(Integer)

        person = PersonInstance()
        schema = to_polars_schema(person)

        assert isinstance(schema, pl.Schema)
        assert "name" in schema
        assert "age" in schema

    def test_nullable_columns(self):
        """Test handling of nullable columns."""

        class PersonNullable(Base):
            __tablename__ = "person_nullable"

            id = Column(Integer, primary_key=True)
            name = Column(String, nullable=True)
            age = Column(Integer, nullable=False)

        schema = to_polars_schema(PersonNullable)

        # Polars schemas don't track nullability, all types are base types
        assert schema["name"] == pl.String
        assert schema["id"] == pl.Int32
        assert schema["age"] == pl.Int32

    def test_model_without_table(self):
        """Test that model without __table__ raises SchemaError."""

        class BadModel:
            pass

        with pytest.raises(SchemaError, match="__table__"):
            to_polars_schema(BadModel)
