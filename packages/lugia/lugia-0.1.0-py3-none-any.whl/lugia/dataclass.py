"""Python dataclass schema and data conversions."""

import dataclasses
from typing import Any, Optional, Union

from lugia.exceptions import MissingDependencyError
from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
    is_typeddict,
)


def to_dataclass(source: Any) -> Union[type, Any]:
    """
    Convert a schema or data object to Python dataclass.

    Args:
        source: Source schema (class) or data (instance)

    Returns:
        Dataclass class or instance
    """
    # If already a dataclass, return as-is
    if is_dataclass(source):
        return source

    # Handle Pydantic
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return _pydantic_to_dataclass(source)

    # Handle TypedDict
    if is_typeddict(source):
        return _typeddict_to_dataclass(source)

    # Handle PySpark
    try:
        from pyspark.sql.types import StructType

        if isinstance(source, StructType):
            return _pyspark_to_dataclass(source)
    except ImportError:
        pass

    # Handle Polars
    try:
        import polars as pl

        if isinstance(source, pl.Schema):
            return _polars_to_dataclass(source)
        if isinstance(source, pl.DataFrame):
            return _polars_to_dataclass(source.schema)
    except ImportError:
        pass

    # Handle Pandas
    try:
        import pandas as pd

        if isinstance(source, pd.DataFrame):
            return _pandas_to_dataclass(source)
    except ImportError:
        pass

    # Handle SQLModel
    try:
        from sqlmodel import SQLModel

        if isinstance(source, type) and issubclass(source, SQLModel):
            return _pydantic_to_dataclass(source)  # SQLModel is Pydantic-based
    except ImportError:
        pass

    # Handle SQLAlchemy
    try:
        from sqlalchemy import Table

        if isinstance(source, Table):
            return _sqlalchemy_to_dataclass(source)
        if hasattr(source, "__table__"):
            return _sqlalchemy_to_dataclass(source.__table__)
    except ImportError:
        pass

    raise ValueError(f"Cannot convert {type(source)} to dataclass")


def _pydantic_to_dataclass(source: Any) -> Union[type, Any]:
    """Convert Pydantic model to dataclass."""
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to dataclass conversion") from None

    if isinstance(source, type) and issubclass(source, BaseModel):
        # Convert model class
        fields = []
        for field_name, field_info in source.model_fields.items():
            field_type = field_info.annotation
            default = field_info.default if field_info.default is not ... else dataclasses.MISSING
            default_factory = (
                field_info.default_factory
                if hasattr(field_info, "default_factory")
                else dataclasses.MISSING
            )

            if default_factory != dataclasses.MISSING:
                fields.append(
                    (
                        field_name,
                        field_type,
                        dataclasses.field(default_factory=default_factory),
                    )
                )
            elif default != dataclasses.MISSING:
                fields.append((field_name, field_type, default))
            else:
                fields.append((field_name, field_type))

        return dataclasses.make_dataclass(f"{source.__name__}Dataclass", fields)
    else:
        # Convert instance
        dc_class = _pydantic_to_dataclass(type(source))
        return dc_class(**source.model_dump())


def _typeddict_to_dataclass(td_class: type) -> type:
    """Convert TypedDict to dataclass."""
    from typing import get_type_hints

    annotations = get_type_hints(td_class)
    fields = [(name, field_type) for name, field_type in annotations.items()]

    return dataclasses.make_dataclass(f"{td_class.__name__}Dataclass", fields)


def _pyspark_to_dataclass(struct_type) -> type:
    """Convert PySpark StructType to dataclass."""

    fields = []

    for field in struct_type.fields:
        field_type = _pyspark_type_to_python(field.dataType)
        if field.nullable:
            field_type = Optional[field_type]
        fields.append((field.name, field_type))

    return dataclasses.make_dataclass("PysparkDataclass", fields)


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


def _polars_to_dataclass(schema) -> type:
    """Convert Polars Schema to dataclass."""

    fields = []

    for name, dtype in schema.items():
        python_type = _polars_type_to_python(dtype)
        fields.append((name, python_type))

    return dataclasses.make_dataclass("PolarsDataclass", fields)


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


def _pandas_to_dataclass(df) -> type:
    """Convert Pandas DataFrame to dataclass."""

    fields = []

    for col in df.columns:
        dtype = df[col].dtype
        python_type = _pandas_type_to_python(dtype)
        if df[col].isna().any():
            python_type = Optional[python_type]
        fields.append((col, python_type))

    return dataclasses.make_dataclass("PandasDataclass", fields)


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


def _sqlalchemy_to_dataclass(table) -> type:
    """Convert SQLAlchemy Table to dataclass."""

    fields = []

    for column in table.columns:
        python_type = _sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        fields.append((column.name, python_type))

    return dataclasses.make_dataclass(f"{table.name}Dataclass", fields)


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
