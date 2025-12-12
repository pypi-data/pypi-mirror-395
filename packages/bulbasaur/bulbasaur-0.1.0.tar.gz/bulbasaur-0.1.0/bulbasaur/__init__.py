"""
Bulbasaur: Convert between PySpark schemas and SQLAlchemy/SQLModel classes.

Bulbasaur provides bidirectional conversion between PySpark schemas and
SQLAlchemy models, as well as SQLModel classes (optional dependency).
"""

from bulbasaur.converters import (
    to_pyspark_schema,
    to_sqlalchemy_model,
    to_sqlmodel_class,
)
from bulbasaur.errors import (
    BulbasaurError,
    ConversionError,
    SchemaError,
    UnsupportedTypeError,
)

__version__ = "0.1.0"

__all__ = [
    "to_pyspark_schema",
    "to_sqlalchemy_model",
    "to_sqlmodel_class",
    "BulbasaurError",
    "ConversionError",
    "SchemaError",
    "UnsupportedTypeError",
]
