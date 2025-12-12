"""TypedDict schema conversions."""

from typing import Any, Optional, TypedDict

from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
    is_typeddict,
)


def to_typeddict(source: Any) -> type[TypedDict]:
    """
    Convert a schema object to TypedDict.

    Args:
        source: Source schema (class)

    Returns:
        TypedDict class
    """
    # If already a TypedDict, return as-is
    if is_typeddict(source):
        return source

    # Handle Pydantic
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return _pydantic_to_typeddict(source)

    # Handle dataclass
    if is_dataclass(source):
        return _dataclass_to_typeddict(source)

    # Handle PySpark
    try:
        from pyspark.sql.types import StructType

        if isinstance(source, StructType):
            return _pyspark_to_typeddict(source)
    except ImportError:
        pass

    # Handle Polars
    try:
        import polars as pl

        if isinstance(source, pl.Schema):
            return _polars_to_typeddict(source)
        if isinstance(source, pl.DataFrame):
            return _polars_to_typeddict(source.schema)
    except ImportError:
        pass

    # Handle Pandas
    try:
        import pandas as pd

        if isinstance(source, pd.DataFrame):
            return _pandas_to_typeddict(source)
    except ImportError:
        pass

    # Handle SQLModel
    try:
        from sqlmodel import SQLModel

        if isinstance(source, type) and issubclass(source, SQLModel):
            return _pydantic_to_typeddict(source)  # SQLModel is Pydantic-based
    except ImportError:
        pass

    # Handle SQLAlchemy
    try:
        from sqlalchemy import Table

        if isinstance(source, Table):
            return _sqlalchemy_to_typeddict(source)
        if hasattr(source, "__table__"):
            return _sqlalchemy_to_typeddict(source.__table__)
    except ImportError:
        pass

    raise ValueError(f"Cannot convert {type(source)} to TypedDict")


def _pydantic_to_typeddict(source: Any) -> type[TypedDict]:
    """Convert Pydantic model to TypedDict."""
    try:
        from pydantic import BaseModel
    except ImportError:
        raise ValueError("Pydantic not available") from None

    model = source if isinstance(source, type) and issubclass(source, BaseModel) else type(source)

    annotations = {}
    for field_name, field_info in model.model_fields.items():
        annotations[field_name] = field_info.annotation

    return TypedDict(f"{model.__name__}TypedDict", annotations)


def _dataclass_to_typeddict(dc_class: type) -> type[TypedDict]:
    """Convert dataclass to TypedDict."""
    from typing import get_type_hints

    annotations = get_type_hints(dc_class)
    return TypedDict(f"{dc_class.__name__}TypedDict", annotations)


def _pyspark_to_typeddict(struct_type) -> type[TypedDict]:
    """Convert PySpark StructType to TypedDict."""

    annotations = {}

    for field in struct_type.fields:
        field_type = _pyspark_type_to_python(field.dataType)
        if field.nullable:
            field_type = Optional[field_type]
        annotations[field.name] = field_type

    return TypedDict("PysparkTypedDict", annotations)


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
    else:
        return Any


def _polars_to_typeddict(schema) -> type[TypedDict]:
    """Convert Polars Schema to TypedDict."""

    annotations = {}

    for name, dtype in schema.items():
        python_type = _polars_type_to_python(dtype)
        annotations[name] = python_type

    return TypedDict("PolarsTypedDict", annotations)


def _polars_type_to_python(dtype):
    """Convert Polars dtype to Python type."""
    from typing import Any

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


def _pandas_to_typeddict(df) -> type[TypedDict]:
    """Convert Pandas DataFrame to TypedDict."""

    annotations = {}

    for col in df.columns:
        dtype = df[col].dtype
        python_type = _pandas_type_to_python(dtype)
        if df[col].isna().any():
            python_type = Optional[python_type]
        annotations[col] = python_type

    return TypedDict("PandasTypedDict", annotations)


def _pandas_type_to_python(dtype):
    """Convert Pandas dtype to Python type."""
    from datetime import datetime
    from typing import Any

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


def _sqlalchemy_to_typeddict(table) -> type[TypedDict]:
    """Convert SQLAlchemy Table to TypedDict."""

    annotations = {}

    for column in table.columns:
        python_type = _sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        annotations[column.name] = python_type

    return TypedDict(f"{table.name}TypedDict", annotations)


def _sqlalchemy_type_to_python(sa_type):
    """Convert SQLAlchemy type to Python type."""
    from datetime import date, datetime
    from typing import Any

    from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Text

    try:
        return sa_type.python_type
    except AttributeError:
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
