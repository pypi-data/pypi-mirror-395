"""Comprehensive integration tests for squirtle."""

import pytest

try:
    import polars as pl
except ImportError:
    pytest.skip("polars not installed", allow_module_level=True)

try:
    from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String  # noqa: F401
    from sqlalchemy.orm import DeclarativeBase
except ImportError:
    pytest.skip("sqlalchemy not installed", allow_module_level=True)

from squirtle.converters import to_polars_schema, to_sqlalchemy_model


class Base(DeclarativeBase):
    """Test base class."""

    pass


class TestRoundTrip:
    """Tests for round-trip conversions."""

    def test_round_trip_basic(self):
        """Test round-trip conversion with basic types."""
        original_schema = pl.Schema(
            {
                "name": pl.String,
                "age": pl.Int32,
                "score": pl.Float64,
            }
        )

        # Convert to SQLAlchemy
        Model = to_sqlalchemy_model(
            original_schema, primary_key="name", class_name="Person", base=Base
        )

        # Convert back to Polars
        converted_schema = to_polars_schema(Model)

        # Verify fields exist
        assert len(converted_schema) == len(original_schema)
        assert "name" in converted_schema
        assert "age" in converted_schema
        assert "score" in converted_schema

    def test_round_trip_with_nullable(self):
        """Test round-trip conversion with nullable fields."""
        original_schema = pl.Schema(
            {
                "id": pl.Int64,
                "name": pl.String,
                "age": pl.Int32,
            }
        )

        Model = to_sqlalchemy_model(
            original_schema, primary_key="id", class_name="PersonNullable", base=Base
        )
        converted_schema = to_polars_schema(Model)

        assert len(converted_schema) == len(original_schema)
        # Verify fields exist (Polars doesn't track nullability in schemas)
        assert "name" in converted_schema
        assert converted_schema["name"] == pl.String

    def test_round_trip_all_types(self):
        """Test round-trip conversion with various types."""
        original_schema = pl.Schema(
            {
                "id": pl.Int64,
                "name": pl.String,
                "age": pl.Int32,
                "score": pl.Float64,
                "active": pl.Boolean,
                "birth_date": pl.Date,
                "created_at": pl.Datetime("us"),  # Datetime needs time unit
            }
        )

        Model = to_sqlalchemy_model(
            original_schema, primary_key="id", class_name="PersonAllTypes", base=Base
        )
        converted_schema = to_polars_schema(Model)

        assert len(converted_schema) == len(original_schema)
        for field_name in original_schema.keys():
            assert field_name in converted_schema


class TestComplexScenarios:
    """Tests for complex scenarios."""

    def test_multiple_models(self):
        """Test creating multiple models from different schemas."""
        schema1 = pl.Schema({"id": pl.Int64, "name": pl.String})
        schema2 = pl.Schema({"id": pl.Int64, "email": pl.String})

        Model1 = to_sqlalchemy_model(schema1, primary_key="id", class_name="User", base=Base)
        Model2 = to_sqlalchemy_model(schema2, primary_key="id", class_name="Contact", base=Base)

        assert Model1.__name__ == "User"
        assert Model2.__name__ == "Contact"
        assert Model1.__tablename__ == "user"
        assert Model2.__tablename__ == "contact"

    def test_custom_base_class(self):
        """Test using a custom base class."""

        class CustomBase(DeclarativeBase):
            pass

        schema = pl.Schema({"id": pl.Int64, "name": pl.String})
        Model = to_sqlalchemy_model(schema, primary_key="id", class_name="Test", base=CustomBase)

        assert issubclass(Model, CustomBase)

    def test_table_name_generation(self):
        """Test that table names are generated correctly."""
        schema = pl.Schema({"id": pl.Int64})

        Model1 = to_sqlalchemy_model(schema, primary_key="id", class_name="PersonTable", base=Base)
        Model2 = to_sqlalchemy_model(
            schema, primary_key="id", class_name="UserProfileTable", base=Base
        )

        assert Model1.__tablename__ == "person_table"
        assert Model2.__tablename__ == "user_profile_table"
