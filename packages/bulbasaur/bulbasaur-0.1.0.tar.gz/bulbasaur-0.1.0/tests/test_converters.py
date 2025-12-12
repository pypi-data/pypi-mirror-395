"""Tests for converter functions."""

import pytest
from pyspark.sql.types import (
    BooleanType,
    DecimalType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)
from sqlalchemy import Column, Integer, String, Float, Boolean, Numeric
from sqlalchemy.orm import DeclarativeBase

from bulbasaur import to_pyspark_schema, to_sqlalchemy_model
from bulbasaur.errors import SchemaError


class TestToSQLAlchemyModel:
    """Tests for converting PySpark schemas to SQLAlchemy models."""

    def test_simple_schema(self):
        """Test converting a simple PySpark schema."""

        class TestBase(DeclarativeBase):
            pass

        schema = StructType(
            [
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), True),
                StructField("score", DoubleType(), True),
            ]
        )

        model = to_sqlalchemy_model(schema, class_name="Person1", base=TestBase)

        assert hasattr(model, "name")
        assert hasattr(model, "age")
        assert hasattr(model, "score")
        assert model.__tablename__ == "person1"

    def test_with_custom_class_name(self):
        """Test with custom class name."""

        class TestBase(DeclarativeBase):
            pass

        schema = StructType(
            [
                StructField("id", IntegerType(), False),
            ]
        )

        model = to_sqlalchemy_model(schema, class_name="CustomModel1", base=TestBase)
        assert model.__name__ == "CustomModel1"
        assert model.__tablename__ == "custommodel1"

    def test_nullable_fields(self):
        """Test nullable field handling."""

        class TestBase(DeclarativeBase):
            pass

        schema = StructType(
            [
                StructField("required", StringType(), False),
                StructField("optional", StringType(), True),
            ]
        )

        model = to_sqlalchemy_model(schema, class_name="TestModel1", base=TestBase)
        assert model.__table__.columns["required"].nullable is False
        assert model.__table__.columns["optional"].nullable is True

    def test_decimal_type(self):
        """Test DecimalType conversion."""

        class TestBase(DeclarativeBase):
            pass

        schema = StructType(
            [
                StructField("price", DecimalType(10, 2), True),
            ]
        )

        model = to_sqlalchemy_model(schema, class_name="TestModel2", base=TestBase)
        column = model.__table__.columns["price"]
        assert isinstance(column.type, Numeric)
        assert column.type.precision == 10
        assert column.type.scale == 2

    def test_duplicate_field_names(self):
        """Test that duplicate field names raise SchemaError."""
        schema = StructType(
            [
                StructField("name", StringType(), True),
                StructField("name", IntegerType(), True),
            ]
        )

        class TestBase(DeclarativeBase):
            pass

        with pytest.raises(SchemaError, match="Duplicate field names"):
            to_sqlalchemy_model(schema, base=TestBase)

    def test_empty_field_name(self):
        """Test that empty field names raise SchemaError."""
        schema = StructType(
            [
                StructField("", StringType(), True),
            ]
        )

        class TestBase(DeclarativeBase):
            pass

        with pytest.raises(SchemaError, match="non-empty strings"):
            to_sqlalchemy_model(schema, base=TestBase)


class TestToPySparkSchema:
    """Tests for converting SQLAlchemy models to PySpark schemas."""

    def test_simple_model(self):
        """Test converting a simple SQLAlchemy model."""

        class TestBase(DeclarativeBase):
            pass

        class Person(TestBase):
            __tablename__ = "person1"

            name = Column(String, primary_key=True)
            age = Column(Integer)
            score = Column(Float)

        schema = to_pyspark_schema(Person)

        assert len(schema.fields) == 3
        field_names = {field.name for field in schema.fields}
        assert field_names == {"name", "age", "score"}

    def test_field_types(self):
        """Test that field types are correctly converted."""

        class TestBase(DeclarativeBase):
            pass

        class TestModel(TestBase):
            __tablename__ = "test1"

            id = Column(Integer, primary_key=True)
            name = Column(String)
            price = Column(Float)
            active = Column(Boolean)

        schema = to_pyspark_schema(TestModel)

        type_map = {field.name: type(field.dataType) for field in schema.fields}
        assert type_map["id"] == IntegerType
        assert type_map["name"] == StringType
        assert type_map["price"] == DoubleType
        assert type_map["active"] == BooleanType

    def test_nullable_fields(self):
        """Test nullable field handling."""

        class TestBase(DeclarativeBase):
            pass

        class TestModel(TestBase):
            __tablename__ = "test2"

            id = Column(Integer, primary_key=True)
            required = Column(String, nullable=False)
            optional = Column(String, nullable=True)

        schema = to_pyspark_schema(TestModel)

        nullable_map = {field.name: field.nullable for field in schema.fields}
        assert nullable_map["required"] is False
        assert nullable_map["optional"] is True

    def test_numeric_type(self):
        """Test Numeric type conversion."""

        class TestBase(DeclarativeBase):
            pass

        class TestModel(TestBase):
            __tablename__ = "test3"

            id = Column(Integer, primary_key=True)
            price = Column(Numeric(10, 2))

        schema = to_pyspark_schema(TestModel)

        price_field = next(f for f in schema.fields if f.name == "price")
        assert isinstance(price_field.dataType, DecimalType)
        assert price_field.dataType.precision == 10
        assert price_field.dataType.scale == 2


class TestSQLModel:
    """Tests for SQLModel conversions (if available)."""

    def test_sqlmodel_to_pyspark(self):
        """Test converting SQLModel to PySpark schema."""
        try:
            from sqlmodel import SQLModel
        except ImportError:
            pytest.skip("SQLModel not installed")

        from bulbasaur import to_pyspark_schema

        class Person(SQLModel):
            name: str
            age: int
            score: float | None = None

        schema = to_pyspark_schema(Person)

        assert len(schema.fields) == 3
        field_names = {field.name for field in schema.fields}
        assert field_names == {"name", "age", "score"}

        # Check nullable
        nullable_map = {field.name: field.nullable for field in schema.fields}
        assert nullable_map["name"] is False
        assert nullable_map["age"] is False
        assert nullable_map["score"] is True

    def test_pyspark_to_sqlmodel(self):
        """Test converting PySpark schema to SQLModel."""
        try:
            import sqlmodel  # noqa: F401
        except ImportError:
            pytest.skip("SQLModel not installed")

        from bulbasaur import to_sqlmodel_class

        schema = StructType(
            [
                StructField("name", StringType(), False),
                StructField("age", IntegerType(), False),
                StructField("score", DoubleType(), True),
            ]
        )

        Person = to_sqlmodel_class(schema, class_name="Person1")

        assert Person.__name__ == "Person1"
        # Check annotations exist
        annotations = Person.__annotations__
        assert "name" in annotations
        assert "age" in annotations
        assert "score" in annotations
        # Check that fields are accessible (SQLModel creates them from annotations)
        # Create an instance to verify
        person = Person(name="Test", age=30, score=95.5)
        assert person.name == "Test"
        assert person.age == 30
        assert person.score == 95.5
