"""Core conversion functions between PySpark schemas and SQLAlchemy/SQLModel classes."""

import inspect
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase

    try:
        from sqlmodel import SQLModel
    except ImportError:
        SQLModel = Any  # type: ignore

try:
    from pyspark.sql.types import (
        ArrayType,
        BinaryType,
        BooleanType,
        ByteType,
        DataType,
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
        StructField,
        StructType,
        TimestampNTZType,
        TimestampType,
    )
except ImportError:
    raise ImportError("PySpark is required. Install it with: pip install pyspark")

try:
    from sqlalchemy import Column, Table
    from sqlalchemy.orm import DeclarativeBase
except ImportError:
    raise ImportError("SQLAlchemy is required. Install it with: pip install sqlalchemy")

from bulbasaur.errors import SchemaError, UnsupportedTypeError
from bulbasaur.type_mappings import (
    PYSPARK_TO_SQLALCHEMY,
    SQLALCHEMY_TO_PYSPARK,
)

# Check if SQLModel is available
try:
    from sqlmodel import SQLModel

    SQLMODEL_AVAILABLE = True
except ImportError:
    SQLMODEL_AVAILABLE = False


def _validate_pyspark_schema(schema: StructType) -> None:
    """Validate a PySpark schema structure."""
    if not isinstance(schema, StructType):
        raise SchemaError(f"Expected StructType, got {type(schema)}")

    # Check for empty schema
    if not schema.fields:
        raise SchemaError("Schema has no fields. At least one field is required.")

    field_names = [field.name for field in schema.fields]

    # Check for duplicate field names
    if len(field_names) != len(set(field_names)):
        duplicates = [name for name in field_names if field_names.count(name) > 1]
        raise SchemaError(
            f"Duplicate field names found in schema: {set(duplicates)}. "
            "Each field must have a unique name."
        )

    # Check for empty field names
    invalid_names = [
        (i, name) for i, name in enumerate(field_names) if not name or not isinstance(name, str)
    ]
    if invalid_names:
        invalid_list = ", ".join(f"field[{idx}]='{name}'" for idx, name in invalid_names)
        raise SchemaError(
            f"Invalid field names found: {invalid_list}. Field names must be non-empty strings."
        )

    # Check for None types
    for field in schema.fields:
        if field.dataType is None:
            raise SchemaError(
                f"Field '{field.name}' (index {schema.fields.index(field)}) has None type. "
                "All fields must have a valid data type."
            )


def _convert_pyspark_type_to_sqlalchemy(
    pyspark_type: DataType,
    nullable: bool = True,  # noqa: ARG001
) -> Any:
    """Convert a PySpark DataType to a SQLAlchemy type."""
    if isinstance(pyspark_type, StructType):
        raise UnsupportedTypeError(
            "Nested StructType is not directly supported. "
            "Use JSON or String type for nested structures."
        )

    if isinstance(pyspark_type, ArrayType):
        raise UnsupportedTypeError(
            "ArrayType is not directly supported in SQLAlchemy. Consider using JSON or String type."
        )

    if isinstance(pyspark_type, MapType):
        raise UnsupportedTypeError(
            "MapType is not directly supported in SQLAlchemy. Consider using JSON or String type."
        )

    # Map PySpark type to SQLAlchemy type
    if not PYSPARK_TO_SQLALCHEMY:
        raise ImportError("SQLAlchemy is required. Install it with: pip install sqlalchemy")

    # Check DecimalType first (most specific, requires special handling)
    if isinstance(pyspark_type, DecimalType):
        # Handle DecimalType with precision and scale
        # Use None as default to properly handle 0 as a valid value
        precision_attr = getattr(pyspark_type, "precision", None)
        scale_attr = getattr(pyspark_type, "scale", None)
        precision: int = precision_attr if precision_attr is not None else 10
        scale: int = scale_attr if scale_attr is not None else 0
        from sqlalchemy import Numeric

        return Numeric(precision=precision, scale=scale)

    # Check other types
    for pyspark_cls, sqlalchemy_cls in PYSPARK_TO_SQLALCHEMY.items():
        if isinstance(pyspark_type, pyspark_cls):
            # Note: nullable is handled at the Column level, not the type level
            return sqlalchemy_cls()

    raise UnsupportedTypeError(
        f"Unsupported PySpark type: {type(pyspark_type).__name__} ({pyspark_type}). "
        "Supported types include: ByteType, ShortType, IntegerType, LongType, "
        "FloatType, DoubleType, BooleanType, StringType, DateType, TimestampType, "
        "DecimalType, BinaryType. For ArrayType, MapType, and nested StructType, "
        "consider using JSON or String type."
    )


def _convert_sqlalchemy_type_to_pyspark(
    sqlalchemy_type: Any,
    nullable: bool = True,  # noqa: ARG001
) -> DataType:
    """Convert a SQLAlchemy type to a PySpark DataType."""
    # Handle TypeDecorator instances
    if hasattr(sqlalchemy_type, "impl"):
        sqlalchemy_type = sqlalchemy_type.impl

    # Get the actual type class
    type_class = type(sqlalchemy_type) if not inspect.isclass(sqlalchemy_type) else sqlalchemy_type

    # Map SQLAlchemy type to PySpark type
    if not SQLALCHEMY_TO_PYSPARK:
        raise ImportError("SQLAlchemy is required. Install it with: pip install sqlalchemy")

    # Check Numeric/DecimalType first (most specific, requires special handling)
    # Only check for Numeric if it's explicitly Numeric (not Float which may inherit from it)
    from sqlalchemy import Numeric, Float

    # Check if it's Numeric (not Float) - Numeric has precision/scale, Float doesn't
    if type_class == Numeric or (
        issubclass(type_class, Numeric)
        and type_class != Float
        and hasattr(sqlalchemy_type, "precision")
    ):
        # Handle Numeric with precision and scale
        # Use None as default to properly handle 0 as a valid value
        precision_attr = getattr(sqlalchemy_type, "precision", None)
        scale_attr = getattr(sqlalchemy_type, "scale", None)
        precision = precision_attr if precision_attr is not None else 10
        scale = scale_attr if scale_attr is not None else 0
        return DecimalType(precision=precision, scale=scale)

    # Check other types
    for sqlalchemy_cls, pyspark_cls in SQLALCHEMY_TO_PYSPARK.items():
        if issubclass(type_class, sqlalchemy_cls) or type_class == sqlalchemy_cls:
            return pyspark_cls()

    raise UnsupportedTypeError(
        f"Unsupported SQLAlchemy type: {type(sqlalchemy_type).__name__} ({sqlalchemy_type}). "
        "Supported types include: SmallInteger, Integer, BigInteger, Float, Boolean, "
        "String, Text, Date, DateTime, Time, Numeric, LargeBinary."
    )


def to_sqlalchemy_model(
    pyspark_schema: StructType,
    class_name: str = "GeneratedModel",
    base: Optional[Type["DeclarativeBase"]] = None,
) -> Type["DeclarativeBase"]:
    """
    Convert a PySpark StructType to a SQLAlchemy model class.

    Args:
        pyspark_schema: PySpark StructType schema
        class_name: Name for the generated model class
        base: Optional base class (defaults to DeclarativeBase)

    Returns:
        SQLAlchemy model class

    Raises:
        SchemaError: If the schema structure is invalid
        UnsupportedTypeError: If a type cannot be converted
    """
    _validate_pyspark_schema(pyspark_schema)

    # Validate class_name
    if not class_name or not isinstance(class_name, str):
        raise SchemaError("class_name must be a non-empty string")
    if not class_name.isidentifier():
        raise SchemaError(
            f"class_name '{class_name}' is not a valid Python identifier. "
            "It must start with a letter or underscore and contain only letters, "
            "digits, and underscores."
        )

    if base is None:
        base = DeclarativeBase

    # Build attributes dictionary for the model class
    attrs: Dict[str, Any] = {
        "__tablename__": class_name.lower(),
    }

    # Convert each field
    has_primary_key = False
    for field in pyspark_schema.fields:
        field_name = field.name
        sqlalchemy_type = _convert_pyspark_type_to_sqlalchemy(
            field.dataType,
            nullable=field.nullable,
        )
        # Check if field name suggests it's a primary key
        is_pk = field_name.lower() in ("id", "pk", "primary_key")
        if is_pk:
            has_primary_key = True
        attrs[field_name] = Column(sqlalchemy_type, nullable=field.nullable, primary_key=is_pk)

    # SQLAlchemy requires at least one primary key
    # If no primary key found, add an auto-incrementing id
    if not has_primary_key:
        from sqlalchemy import Integer

        attrs["id"] = Column(Integer, primary_key=True, autoincrement=True)

    # Create the model class
    model_class = type(class_name, (base,), attrs)

    return model_class


def to_pyspark_schema(
    model: Union[Type, Any],
) -> StructType:
    """
    Convert a SQLAlchemy model class or instance to a PySpark StructType.

    Args:
        model: SQLAlchemy model class or instance, or SQLModel class

    Returns:
        PySpark StructType schema

    Raises:
        SchemaError: If the model structure is invalid
        UnsupportedTypeError: If a type cannot be converted
    """
    # Handle SQLModel classes
    if SQLMODEL_AVAILABLE:
        try:
            if isinstance(model, type) and issubclass(model, SQLModel):
                return _sqlmodel_to_pyspark(model)
        except (TypeError, AttributeError):
            pass

    # Handle SQLAlchemy declarative models
    if hasattr(model, "__table__"):
        table = getattr(model, "__table__")
    elif isinstance(model, type) and hasattr(model, "__tablename__"):
        # It's a class, get the table
        table = getattr(model, "__table__")
    elif isinstance(model, Table):
        table = model
    else:
        raise SchemaError(
            f"Expected SQLAlchemy model class, instance, or Table object, "
            f"got {type(model).__name__} ({model}). "
            "The model must have a '__table__' attribute or be a Table instance."
        )

    fields = []
    field_names = set()

    for column in table.columns:
        if column.name in field_names:
            raise SchemaError(
                f"Duplicate column name '{column.name}' found in table '{table.name}'. "
                "Each column must have a unique name."
            )
        field_names.add(column.name)

        pyspark_type = _convert_sqlalchemy_type_to_pyspark(
            column.type,
            nullable=column.nullable,
        )

        fields.append(
            StructField(
                name=column.name,
                dataType=pyspark_type,
                nullable=column.nullable,
            )
        )

    return StructType(fields)


def _sqlmodel_to_pyspark(model: Type["SQLModel"]) -> StructType:
    """Convert a SQLModel class to PySpark StructType."""
    if not SQLMODEL_AVAILABLE:
        raise ImportError("SQLModel is not installed. Install it with: pip install sqlmodel")

    fields = []
    field_names = set()

    # Get model annotations (SQLModel uses __annotations__)
    annotations = getattr(model, "__annotations__", {})
    if not annotations:
        raise SchemaError(
            f"Model '{model.__name__}' has no type annotations. "
            "SQLModel classes require type annotations for all fields."
        )

    # Get model_fields if available (SQLModel 0.0.8+)
    model_fields = getattr(model, "model_fields", {})

    for field_name in annotations:
        if field_name in field_names:
            raise SchemaError(
                f"Duplicate field name '{field_name}' found in model '{model.__name__}'. "
                "Each field must have a unique name."
            )
        field_names.add(field_name)

        # Get field type from annotations
        field_type = annotations[field_name]

        # Get field info if available
        field_info = model_fields.get(field_name) if model_fields else None

        # Convert Python type to PySpark type
        pyspark_type = _python_type_to_pyspark(field_type)

        # Determine nullable
        nullable = True
        if field_info:
            # Check if field has a default value (non-nullable)
            if hasattr(field_info, "default") and field_info.default is not ...:
                if field_info.default is not None:
                    nullable = False
            elif hasattr(field_info, "default_factory") and field_info.default_factory is not None:
                nullable = False
        else:
            # Check if type is Optional/Union
            import typing

            if hasattr(typing, "get_origin") and typing.get_origin(field_type) is Union:
                args = typing.get_args(field_type)
                # If None is in the Union, it's nullable
                # If None is not in the Union, it's not nullable
                nullable = type(None) in args

        fields.append(
            StructField(
                name=field_name,
                dataType=pyspark_type,
                nullable=nullable,
            )
        )

    return StructType(fields)


def _python_type_to_pyspark(python_type: Any) -> DataType:
    """Convert a Python type annotation to PySpark DataType."""
    import typing

    # Handle Union types (including Optional)
    if hasattr(typing, "get_origin"):
        origin = typing.get_origin(python_type)
        if origin is Union:
            args = typing.get_args(python_type)
            # Filter out None types
            non_none_types = [arg for arg in args if arg is not type(None)]
            if non_none_types:
                # Use the first non-None type (most common case for Optional)
                # For complex Unions, this is a reasonable default
                return _python_type_to_pyspark(non_none_types[0])
            # If all types are None, default to StringType
            return StringType()

    # Map Python types to PySpark types
    type_mapping = {
        int: IntegerType(),
        float: DoubleType(),
        bool: BooleanType(),
        str: StringType(),
        bytes: BinaryType(),
    }

    # Check direct type match
    if python_type in type_mapping:
        return type_mapping[python_type]

    # Check if it's a SQLAlchemy type
    try:
        from sqlalchemy.types import TypeEngine

        if inspect.isclass(python_type) and issubclass(python_type, TypeEngine):
            return _convert_sqlalchemy_type_to_pyspark(python_type())
    except (TypeError, AttributeError):
        pass

    # Default to StringType for unknown types
    return StringType()


def to_sqlmodel_class(
    pyspark_schema: StructType,
    class_name: str = "GeneratedModel",
) -> Type["SQLModel"]:
    """
    Convert a PySpark StructType to a SQLModel class.

    Args:
        pyspark_schema: PySpark StructType schema
        class_name: Name for the generated model class

    Returns:
        SQLModel class

    Raises:
        SchemaError: If the schema structure is invalid
        UnsupportedTypeError: If a type cannot be converted
        ImportError: If SQLModel is not installed
    """
    if not SQLMODEL_AVAILABLE:
        raise ImportError("SQLModel is not installed. Install it with: pip install sqlmodel")

    _validate_pyspark_schema(pyspark_schema)

    # Validate class_name
    if not class_name or not isinstance(class_name, str):
        raise SchemaError("class_name must be a non-empty string")
    if not class_name.isidentifier():
        raise SchemaError(
            f"class_name '{class_name}' is not a valid Python identifier. "
            "It must start with a letter or underscore and contain only letters, "
            "digits, and underscores."
        )

    # Build annotations dictionary
    annotations: Dict[str, Any] = {}
    # Store field defaults for SQLModel
    field_defaults: Dict[str, Any] = {}

    # Convert each field
    for field in pyspark_schema.fields:
        field_name = field.name
        python_type = _pyspark_type_to_python(field.dataType)

        # Make type Optional if nullable
        if field.nullable:
            from typing import Optional

            python_type = Optional[python_type]  # type: ignore[assignment]
            # For nullable fields, set default to None
            field_defaults[field_name] = None

        annotations[field_name] = python_type

    # Create the SQLModel class
    namespace = {
        "__annotations__": annotations,
        **field_defaults,
    }

    model_class = type(class_name, (SQLModel,), namespace)

    return model_class


def _pyspark_type_to_python(pyspark_type: DataType) -> Type:
    """Convert a PySpark DataType to a Python type annotation."""
    type_mapping = {
        ByteType: int,
        ShortType: int,
        IntegerType: int,
        LongType: int,
        FloatType: float,
        DoubleType: float,
        BooleanType: bool,
        StringType: str,
        DateType: str,  # Date as string in Python
        TimestampType: str,  # Timestamp as string in Python
        TimestampNTZType: str,
        DecimalType: float,  # Decimal as float in Python
        BinaryType: bytes,
        NullType: str,
    }

    for pyspark_cls, python_type in type_mapping.items():
        if isinstance(pyspark_type, pyspark_cls):
            return python_type

    # Default to str for unknown types
    return str
