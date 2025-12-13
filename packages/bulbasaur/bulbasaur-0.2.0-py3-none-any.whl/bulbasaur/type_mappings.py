"""Type mappings between PySpark and SQLAlchemy types."""

from typing import Any, Dict

# Initialize as empty dicts, will be populated if dependencies are available
PYSPARK_TO_SQLALCHEMY: Dict[Any, Any] = {}
SQLALCHEMY_TO_PYSPARK: Dict[Any, Any] = {}
PYSPARK_TYPE_NAMES: Dict[str, Any] = {}
SQLALCHEMY_TYPE_NAMES: Dict[str, Any] = {}

try:
    from pyspark.sql.types import (
        ArrayType,
        BinaryType,
        BooleanType,
        ByteType,
        DateType,
        DecimalType,
        DoubleType,
        FloatType,
        IntegerType,
        LongType,
        MapType,
        NullType,
        ShortType,
        StringType,
        StructType,
        TimestampNTZType,
        TimestampType,
    )

    PYSPARK_TYPE_NAMES = {
        "ByteType": ByteType,
        "ShortType": ShortType,
        "IntegerType": IntegerType,
        "LongType": LongType,
        "FloatType": FloatType,
        "DoubleType": DoubleType,
        "BooleanType": BooleanType,
        "StringType": StringType,
        "DateType": DateType,
        "TimestampType": TimestampType,
        "TimestampNTZType": TimestampNTZType,
        "DecimalType": DecimalType,
        "BinaryType": BinaryType,
        "NullType": NullType,
        "ArrayType": ArrayType,
        "MapType": MapType,
        "StructType": StructType,
    }
except ImportError:
    # Allow import even if PySpark is not installed
    pass

try:
    from sqlalchemy import (
        BigInteger,
        Boolean,
        Date,
        DateTime,
        Float,
        Integer,
        LargeBinary,
        Numeric,
        SmallInteger,
        String,
        Text,
        Time,
    )
    from sqlalchemy.dialects.postgresql import (
        JSON,
        JSONB,
        UUID as PG_UUID,
    )
    from sqlalchemy.types import Enum as SA_Enum

    # Try to import Interval (may not be available in all SQLAlchemy versions)
    try:
        from sqlalchemy import Interval
    except ImportError:
        Interval = None  # type: ignore[assignment,misc]

    SQLALCHEMY_TYPE_NAMES = {
        "SmallInteger": SmallInteger,
        "Integer": Integer,
        "BigInteger": BigInteger,
        "Float": Float,
        "Boolean": Boolean,
        "String": String,
        "Text": Text,
        "Date": Date,
        "DateTime": DateTime,
        "Time": Time,
        "Numeric": Numeric,
        "LargeBinary": LargeBinary,
        "JSON": JSON,
        "JSONB": JSONB,
        "Enum": SA_Enum,
        "UUID": PG_UUID,
    }
    if Interval is not None:
        SQLALCHEMY_TYPE_NAMES["Interval"] = Interval
except ImportError:
    # Allow import even if SQLAlchemy is not installed
    JSON = None  # type: ignore[assignment,misc]
    JSONB = None  # type: ignore[assignment,misc]
    PG_UUID = None  # type: ignore[assignment,misc]
    SA_Enum = None  # type: ignore[assignment,misc]
    Interval = None  # type: ignore[assignment,misc]


# Populate mappings if both dependencies are available
if "ByteType" in globals() and "SmallInteger" in globals():
    # PySpark to SQLAlchemy type mappings
    PYSPARK_TO_SQLALCHEMY = {
        ByteType: SmallInteger,
        ShortType: SmallInteger,
        IntegerType: Integer,
        LongType: BigInteger,
        FloatType: Float,
        DoubleType: Float,  # SQLAlchemy Float maps to DOUBLE
        BooleanType: Boolean,
        StringType: String,
        DateType: Date,
        TimestampType: DateTime,
        TimestampNTZType: DateTime,
        DecimalType: Numeric,
        BinaryType: LargeBinary,
        NullType: String,  # Fallback to String for NullType
    }

    # SQLAlchemy to PySpark type mappings
    SQLALCHEMY_TO_PYSPARK = {
        SmallInteger: ShortType,
        Integer: IntegerType,
        BigInteger: LongType,
        Float: DoubleType,  # SQLAlchemy Float is typically DOUBLE
        Boolean: BooleanType,
        String: StringType,
        Text: StringType,  # Text maps to StringType
        Date: DateType,
        DateTime: TimestampType,
        Time: TimestampType,  # Time maps to TimestampType
        Numeric: DecimalType,
        LargeBinary: BinaryType,
    }

    # Add optional SQLAlchemy types if available
    if JSON is not None:
        SQLALCHEMY_TO_PYSPARK[JSON] = StringType  # JSON maps to StringType
    if JSONB is not None:
        SQLALCHEMY_TO_PYSPARK[JSONB] = StringType  # JSONB maps to StringType
    if SA_Enum is not None:
        SQLALCHEMY_TO_PYSPARK[SA_Enum] = StringType  # Enum maps to StringType
    if PG_UUID is not None:
        SQLALCHEMY_TO_PYSPARK[PG_UUID] = StringType  # UUID maps to StringType
    if Interval is not None:
        SQLALCHEMY_TO_PYSPARK[Interval] = StringType  # Interval maps to StringType
