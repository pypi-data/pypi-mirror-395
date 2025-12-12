"""Tests for error handling."""

import pytest
from pyspark.sql.types import ArrayType, StringType, StructType, StructField

from bulbasaur import to_sqlalchemy_model
from bulbasaur.errors import SchemaError, UnsupportedTypeError
from sqlalchemy.orm import DeclarativeBase


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_schema_type(self):
        """Test that non-StructType raises SchemaError."""

        class TestBase(DeclarativeBase):
            pass

        with pytest.raises(SchemaError, match="Expected StructType"):
            to_sqlalchemy_model("not a schema", base=TestBase)

    def test_unsupported_array_type(self):
        """Test that ArrayType raises UnsupportedTypeError."""
        schema = StructType(
            [
                StructField("tags", ArrayType(StringType()), True),
            ]
        )

        class TestBase(DeclarativeBase):
            pass

        with pytest.raises(UnsupportedTypeError, match="ArrayType"):
            to_sqlalchemy_model(schema, base=TestBase)

    def test_duplicate_field_names(self):
        """Test that duplicate field names raise SchemaError."""
        schema = StructType(
            [
                StructField("name", StringType(), True),
                StructField("name", StringType(), True),
            ]
        )

        class TestBase(DeclarativeBase):
            pass

        with pytest.raises(SchemaError, match="Duplicate field names"):
            to_sqlalchemy_model(schema, base=TestBase)
