"""Pydantic schema and data conversions."""

from typing import Any, Optional, Union

from lugia.exceptions import MissingDependencyError
from lugia.utils import (
    get_annotations,
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
    is_typeddict,
)

try:
    from pydantic import BaseModel, create_model
    from pydantic.fields import FieldInfo

    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseModel = None  # type: ignore
    create_model = None  # type: ignore
    FieldInfo = None  # type: ignore


def _check_pydantic():
    """Check if Pydantic is available."""
    if not PYDANTIC_AVAILABLE:
        raise MissingDependencyError("pydantic", "Pydantic conversions")


def to_pydantic(source: Any) -> Union[type[BaseModel], BaseModel]:
    """
    Convert a schema or data object to Pydantic.

    Args:
        source: Source schema (class) or data (instance)

    Returns:
        Pydantic model class or instance
    """
    _check_pydantic()

    # If already Pydantic, return as-is
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return source

    # Handle dataclass
    if is_dataclass(source):
        return _dataclass_to_pydantic(source)

    # Handle TypedDict
    if is_typeddict(source):
        return _typeddict_to_pydantic(source)

    # Handle PySpark
    try:
        from pyspark.sql.types import StructType

        if isinstance(source, StructType):
            return _pyspark_to_pydantic(source)
    except ImportError:
        pass

    # Handle Polars
    try:
        import polars as pl

        if isinstance(source, pl.Schema):
            return _polars_to_pydantic(source)
        if isinstance(source, pl.DataFrame):
            return _polars_to_pydantic(source.schema)
    except ImportError:
        pass

    # Handle Pandas
    try:
        import pandas as pd

        if isinstance(source, pd.DataFrame):
            return _pandas_to_pydantic(source)
    except ImportError:
        pass

    # Handle SQLModel
    try:
        from sqlmodel import SQLModel

        if isinstance(source, type) and issubclass(source, SQLModel):
            return source  # SQLModel is already a Pydantic model
    except ImportError:
        pass

    # Handle SQLAlchemy
    try:
        from sqlalchemy import Column, Table  # noqa: F401

        if isinstance(source, Table):
            return _sqlalchemy_to_pydantic(source)
        if hasattr(source, "__table__"):
            return _sqlalchemy_to_pydantic(source.__table__)
    except ImportError:
        pass

    raise ValueError(f"Cannot convert {type(source)} to Pydantic")


def _dataclass_to_pydantic(dc_class: type) -> type[BaseModel]:
    """Convert a dataclass to Pydantic model."""
    import dataclasses

    fields = {}
    annotations = get_annotations(dc_class)

    for field in dataclasses.fields(dc_class):
        field_type = annotations.get(field.name, Any)
        default = field.default if field.default != dataclasses.MISSING else ...
        default_factory = (
            field.default_factory if field.default_factory != dataclasses.MISSING else None
        )

        if default_factory is not None:
            fields[field.name] = (
                field_type,
                FieldInfo(default_factory=default_factory),
            )
        elif default != ...:
            fields[field.name] = (field_type, default)
        else:
            fields[field.name] = (field_type, ...)

    return create_model(f"{dc_class.__name__}Model", **fields)


def _typeddict_to_pydantic(td_class: type) -> type[BaseModel]:
    """Convert a TypedDict to Pydantic model."""
    annotations = get_annotations(td_class)
    fields = {}

    for name, field_type in annotations.items():
        # Check if field is required (TypedDict doesn't have a simple way to check this)
        # We'll assume all fields are required unless they're Optional
        fields[name] = (field_type, ...)

    return create_model(f"{td_class.__name__}Model", **fields)


def _pyspark_to_pydantic(struct_type) -> type[BaseModel]:
    """Convert PySpark StructType to Pydantic model."""

    fields = {}

    for field in struct_type.fields:
        field_type = _pyspark_type_to_python(field.dataType)
        fields[field.name] = (
            field_type,
            ... if not field.nullable else Optional[field_type],
        )

    return create_model("PysparkModel", **fields)


def _pyspark_type_to_python(spark_type):
    """Convert PySpark type to Python type."""
    from datetime import date, datetime
    from typing import Any

    from pyspark.sql.types import (
        ArrayType,
        BooleanType,
        DateType,
        DoubleType,
        FloatType,
        IntegerType,
        LongType,
        MapType,
        StringType,
        StructType,
        TimestampType,
    )

    if isinstance(spark_type, StringType):
        return str
    elif isinstance(spark_type, (IntegerType, LongType)):
        return int
    elif isinstance(spark_type, (FloatType, DoubleType)):
        return float
    elif isinstance(spark_type, BooleanType):
        return bool
    elif isinstance(spark_type, DateType):
        return date
    elif isinstance(spark_type, TimestampType):
        return datetime
    elif isinstance(spark_type, ArrayType):
        element_type = _pyspark_type_to_python(spark_type.elementType)
        return list[element_type]
    elif isinstance(spark_type, MapType):
        key_type = _pyspark_type_to_python(spark_type.keyType)
        value_type = _pyspark_type_to_python(spark_type.valueType)
        return dict[key_type, value_type]
    elif isinstance(spark_type, StructType):
        # For nested structs, we'd need to create a nested model
        return dict[str, Any]
    else:
        return Any


def _polars_to_pydantic(schema) -> type[BaseModel]:
    """Convert Polars Schema to Pydantic model."""

    fields = {}

    for name, dtype in schema.items():
        python_type = _polars_type_to_python(dtype)
        fields[name] = (python_type, ...)

    return create_model("PolarsModel", **fields)


def _polars_type_to_python(dtype):
    """Convert Polars dtype to Python type."""
    import polars as pl

    if dtype == pl.Utf8 or dtype == pl.String:
        return str
    elif dtype == pl.Int64 or dtype == pl.Int32:
        return int
    elif dtype == pl.Float64 or dtype == pl.Float32:
        return float
    elif dtype == pl.Boolean:
        return bool
    elif dtype == pl.Date:
        from datetime import date

        return date
    elif dtype == pl.Datetime:
        from datetime import datetime

        return datetime
    elif isinstance(dtype, pl.List):
        element_type = _polars_type_to_python(dtype.inner)
        return list[element_type]
    elif isinstance(dtype, pl.Struct):
        return dict[str, Any]
    else:
        return Any


def _pandas_to_pydantic(df) -> type[BaseModel]:
    """Convert Pandas DataFrame to Pydantic model."""
    from typing import Optional

    fields = {}

    for col in df.columns:
        dtype = df[col].dtype
        python_type = _pandas_type_to_python(dtype)
        # Check for nullable columns
        if df[col].isna().any():
            python_type = Optional[python_type]
        fields[col] = (python_type, ...)

    return create_model("PandasModel", **fields)


def _pandas_type_to_python(dtype):
    """Convert Pandas dtype to Python type."""
    from datetime import datetime

    import pandas as pd

    if pd.api.types.is_integer_dtype(dtype):
        return int
    elif pd.api.types.is_float_dtype(dtype):
        return float
    elif pd.api.types.is_bool_dtype(dtype):
        return bool
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return datetime
    elif pd.api.types.is_object_dtype(dtype):
        return Any
    else:
        return str


def _sqlalchemy_to_pydantic(table) -> type[BaseModel]:
    """Convert SQLAlchemy Table to Pydantic model."""
    from typing import Optional

    fields = {}

    for column in table.columns:
        python_type = _sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        fields[column.name] = (python_type, ...)

    return create_model(f"{table.name}Model", **fields)


def _sqlalchemy_type_to_python(sa_type):
    """Convert SQLAlchemy type to Python type."""
    from datetime import date, datetime

    from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Text

    # Get the Python type from SQLAlchemy type
    try:
        return sa_type.python_type
    except AttributeError:
        # Fallback for types without python_type
        if isinstance(sa_type, (String, Text)):
            return str
        elif isinstance(sa_type, Integer):
            return int
        elif isinstance(sa_type, Float):
            return float
        elif isinstance(sa_type, Boolean):
            return bool
        elif isinstance(sa_type, Date):
            return date
        elif isinstance(sa_type, DateTime):
            return datetime
        else:
            return Any
