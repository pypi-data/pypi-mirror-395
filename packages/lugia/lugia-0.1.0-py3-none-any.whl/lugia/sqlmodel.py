"""SQLModel model conversions."""

from typing import Any, Optional

from lugia.exceptions import MissingDependencyError
from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
    is_sqlmodel_model,
    is_typeddict,
)

try:
    from sqlmodel import Field, SQLModel, create_engine

    SQLMODEL_AVAILABLE = True
except ImportError:
    SQLMODEL_AVAILABLE = False
    SQLModel = None
    Field = None
    create_engine = None


def _check_sqlmodel():
    """Check if SQLModel is available."""
    if not SQLMODEL_AVAILABLE:
        raise MissingDependencyError("sqlmodel", "SQLModel conversions")


def to_sqlmodel(source: Any) -> type[SQLModel]:
    """
    Convert a schema object to SQLModel model class.

    Args:
        source: Source schema

    Returns:
        SQLModel model class
    """
    _check_sqlmodel()

    # If already SQLModel, return as-is
    if is_sqlmodel_model(source):
        return source

    # Handle Pydantic
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return _pydantic_to_sqlmodel(source)

    # Handle dataclass
    if is_dataclass(source):
        return _dataclass_to_sqlmodel(source)

    # Handle TypedDict
    if is_typeddict(source):
        return _typeddict_to_sqlmodel(source)

    # Handle PySpark
    try:
        from pyspark.sql.types import StructType

        if isinstance(source, StructType):
            return _pyspark_to_sqlmodel(source)
    except ImportError:
        pass

    # Handle Polars
    try:
        import polars as pl

        if isinstance(source, pl.Schema):
            return _polars_to_sqlmodel(source)
    except ImportError:
        pass

    # Handle Pandas
    try:
        import pandas as pd

        if isinstance(source, pd.DataFrame):
            return _pandas_to_sqlmodel(source)
    except ImportError:
        pass

    # Handle SQLAlchemy
    try:
        from sqlalchemy import Table

        if isinstance(source, Table):
            return _sqlalchemy_to_sqlmodel(source)
        if hasattr(source, "__table__"):
            return _sqlalchemy_to_sqlmodel(source.__table__)
    except ImportError:
        pass

    raise ValueError(f"Cannot convert {type(source)} to SQLModel")


def _pydantic_to_sqlmodel(source: Any) -> type[SQLModel]:
    """Convert Pydantic model to SQLModel."""
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to SQLModel conversion") from None

    model = source if isinstance(source, type) and issubclass(source, BaseModel) else type(source)

    # SQLModel is based on Pydantic, so we can create a SQLModel subclass
    # that inherits from the Pydantic model's fields
    annotations = {}
    fields = {}
    for field_name, field_info in model.model_fields.items():
        field_type = field_info.annotation
        default = field_info.default if field_info.default is not ... else None
        annotations[field_name] = field_type
        if default is not None:
            fields[field_name] = Field(default=default)
        else:
            fields[field_name] = Field()

    # Create SQLModel class dynamically with proper annotations
    class_name = f"{model.__name__}SQLModel"
    new_class = type(class_name, (SQLModel,), {**fields, "__annotations__": annotations})
    return new_class


def _dataclass_to_sqlmodel(source: type) -> type[SQLModel]:
    """Convert dataclass to SQLModel."""
    import dataclasses
    from typing import get_type_hints

    hints = get_type_hints(source)
    fields = {}

    for field in dataclasses.fields(source):
        field_type = hints.get(field.name, Any)
        default = field.default if field.default != dataclasses.MISSING else None
        default_factory = (
            field.default_factory if field.default_factory != dataclasses.MISSING else None
        )

        if default_factory is not None:
            fields[field.name] = (field_type, Field(default_factory=default_factory))
        elif default is not None:
            fields[field.name] = (field_type, Field(default=default))
        else:
            fields[field.name] = (field_type, Field())

    class_name = f"{source.__name__}SQLModel"
    return type(class_name, (SQLModel,), fields)


def _typeddict_to_sqlmodel(td_class: type) -> type[SQLModel]:
    """Convert TypedDict to SQLModel."""
    from typing import get_type_hints

    hints = get_type_hints(td_class)
    fields = {}

    for name, field_type in hints.items():
        fields[name] = (field_type, Field())

    class_name = f"{td_class.__name__}SQLModel"
    return type(class_name, (SQLModel,), fields)


def _pyspark_to_sqlmodel(struct_type) -> type[SQLModel]:
    """Convert PySpark StructType to SQLModel."""

    fields = {}

    for field in struct_type.fields:
        field_type = _pyspark_type_to_python(field.dataType)
        if field.nullable:
            field_type = Optional[field_type]
        fields[field.name] = (field_type, Field())

    return type("PysparkSQLModel", (SQLModel,), fields)


def _pyspark_type_to_python(spark_type):
    """Convert PySpark type to Python type."""
    from datetime import date, datetime
    from typing import Any

    from pyspark.sql.types import (
        BooleanType,
        DateType,
        DoubleType,
        FloatType,
        IntegerType,
        LongType,
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
    else:
        return Any


def _polars_to_sqlmodel(schema) -> type[SQLModel]:
    """Convert Polars Schema to SQLModel."""

    fields = {}

    for name, dtype in schema.items():
        python_type = _polars_type_to_python(dtype)
        fields[name] = (python_type, Field())

    return type("PolarsSQLModel", (SQLModel,), fields)


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
    else:
        return Any


def _pandas_to_sqlmodel(df) -> type[SQLModel]:
    """Convert Pandas DataFrame to SQLModel."""

    fields = {}

    for col in df.columns:
        dtype = df[col].dtype
        python_type = _pandas_type_to_python(dtype)
        if df[col].isna().any():
            python_type = Optional[python_type]
        fields[col] = (python_type, Field())

    return type("PandasSQLModel", (SQLModel,), fields)


def _pandas_type_to_python(dtype):
    """Convert Pandas dtype to Python type."""
    from typing import Any

    import pandas as pd

    if pd.api.types.is_integer_dtype(dtype):
        return int
    elif pd.api.types.is_float_dtype(dtype):
        return float
    elif pd.api.types.is_bool_dtype(dtype):
        return bool
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        from datetime import datetime

        return datetime
    elif pd.api.types.is_object_dtype(dtype):
        return Any
    else:
        return str


def _sqlalchemy_to_sqlmodel(table) -> type[SQLModel]:
    """Convert SQLAlchemy Table to SQLModel."""

    fields = {}

    for column in table.columns:
        python_type = _sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        fields[column.name] = (python_type, Field())

    return type(f"{table.name}SQLModel", (SQLModel,), fields)


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


def from_sqlmodel(sqlmodel_class: type[SQLModel], target_type: str = "pydantic") -> Any:
    """
    Convert SQLModel model to another schema type.

    Args:
        sqlmodel_class: SQLModel model class
        target_type: Target schema type ('pydantic', 'dataclass', 'typedict', etc.)

    Returns:
        Converted schema
    """
    _check_sqlmodel()

    if target_type == "pydantic":
        from lugia.pydantic import to_pydantic

        return to_pydantic(sqlmodel_class)
    elif target_type == "dataclass":
        from lugia.dataclass import to_dataclass

        return to_dataclass(sqlmodel_class)
    elif target_type == "typedict":
        from lugia.typedict import to_typeddict

        return to_typeddict(sqlmodel_class)
    elif target_type == "pandas":
        from lugia.pandas import to_pandas

        return to_pandas(sqlmodel_class)
    elif target_type == "polars":
        from lugia.polars import to_polars

        return to_polars(sqlmodel_class)
    elif target_type == "pyspark":
        from lugia.pyspark import to_pyspark

        return to_pyspark(sqlmodel_class)
    elif target_type == "sqlalchemy":
        from lugia.sqlalchemy import to_sqlalchemy

        return to_sqlalchemy(sqlmodel_class)
    else:
        raise ValueError(f"Unsupported target type: {target_type}")
