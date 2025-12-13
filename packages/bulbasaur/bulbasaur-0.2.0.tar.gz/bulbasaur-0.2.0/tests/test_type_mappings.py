"""Tests for type mappings."""

from pyspark.sql.types import (
    BooleanType,
    DateType,
    DoubleType,
    IntegerType,
    LongType,
    ShortType,
    StringType,
    TimestampType,
)

from bulbasaur.type_mappings import (
    PYSPARK_TO_SQLALCHEMY,
    SQLALCHEMY_TO_PYSPARK,
)


class TestTypeMappings:
    """Tests for type mapping dictionaries."""

    def test_pyspark_to_sqlalchemy_mappings_exist(self):
        """Test that PySpark to SQLAlchemy mappings are defined."""
        assert len(PYSPARK_TO_SQLALCHEMY) > 0

    def test_sqlalchemy_to_pyspark_mappings_exist(self):
        """Test that SQLAlchemy to PySpark mappings are defined."""
        assert len(SQLALCHEMY_TO_PYSPARK) > 0

    def test_common_types_mapped(self):
        """Test that common types are mapped."""
        assert ShortType in PYSPARK_TO_SQLALCHEMY
        assert IntegerType in PYSPARK_TO_SQLALCHEMY
        assert LongType in PYSPARK_TO_SQLALCHEMY
        assert DoubleType in PYSPARK_TO_SQLALCHEMY
        assert StringType in PYSPARK_TO_SQLALCHEMY
        assert BooleanType in PYSPARK_TO_SQLALCHEMY
        assert DateType in PYSPARK_TO_SQLALCHEMY
        assert TimestampType in PYSPARK_TO_SQLALCHEMY
