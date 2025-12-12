"""SQLAlchemy Table and model conversions."""

from typing import Any, Optional, Union

from lugia.exceptions import MissingDependencyError
from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
    is_sqlalchemy_model,
    is_typeddict,
)

try:
    from sqlalchemy import (
        Boolean,
        Column,
        Date,
        DateTime,
        Float,
        Integer,
        MetaData,
        String,
        Table,
        Text,
        create_engine,
    )
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import DeclarativeBase

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    Table = None  # type: ignore
    Column = None  # type: ignore
    Integer = None  # type: ignore
    String = None  # type: ignore
    Float = None  # type: ignore
    Boolean = None  # type: ignore
    Date = None  # type: ignore
    DateTime = None  # type: ignore
    Text = None  # type: ignore
    MetaData = None  # type: ignore
    create_engine = None  # type: ignore
    declarative_base = None  # type: ignore
    DeclarativeBase = None  # type: ignore


def _check_sqlalchemy():
    """Check if SQLAlchemy is available."""
    if not SQLALCHEMY_AVAILABLE:
        raise MissingDependencyError("sqlalchemy", "SQLAlchemy conversions")


def to_sqlalchemy(
    source: Any,
    table_name: Optional[str] = None,
    metadata: Optional[MetaData] = None,  # type: ignore
) -> Union[Table, type]:  # type: ignore
    """
    Convert a schema object to SQLAlchemy Table or model class.

    Args:
        source: Source schema
        table_name: Optional table name (defaults to source class name)
        metadata: Optional MetaData instance (creates new if not provided)

    Returns:
        SQLAlchemy Table or model class
    """
    _check_sqlalchemy()

    # If already SQLAlchemy, return as-is
    if isinstance(source, Table):
        return source
    if is_sqlalchemy_model(source):
        return source

    # Handle Pydantic
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return _pydantic_to_sqlalchemy(source, table_name, metadata)

    # Handle dataclass
    if is_dataclass(source):
        return _dataclass_to_sqlalchemy(source, table_name, metadata)

    # Handle TypedDict
    if is_typeddict(source):
        return _typeddict_to_sqlalchemy(source, table_name, metadata)

    # Handle PySpark
    try:
        from pyspark.sql.types import StructType

        if isinstance(source, StructType):
            return _pyspark_to_sqlalchemy(source, table_name, metadata)
    except ImportError:
        pass

    # Handle Polars
    try:
        import polars as pl

        if isinstance(source, pl.Schema):
            return _polars_to_sqlalchemy(source, table_name, metadata)
    except ImportError:
        pass

    # Handle Pandas
    try:
        import pandas as pd

        if isinstance(source, pd.DataFrame):
            return _pandas_to_sqlalchemy(source, table_name, metadata)
    except ImportError:
        pass

    raise ValueError(f"Cannot convert {type(source)} to SQLAlchemy")


def _pydantic_to_sqlalchemy(
    source: Any, table_name: str = None, metadata: MetaData = None
) -> Table:
    """Convert Pydantic model to SQLAlchemy Table."""
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to SQLAlchemy conversion") from None

    model = source if isinstance(source, type) and issubclass(source, BaseModel) else type(source)

    if table_name is None:
        table_name = model.__name__.lower()

    if metadata is None:
        metadata = MetaData()

    columns = []
    for field_name, field_info in model.model_fields.items():
        sa_type = _python_type_to_sqlalchemy(field_info.annotation)
        nullable = True  # Default to nullable
        columns.append(Column(field_name, sa_type, nullable=nullable))

    return Table(table_name, metadata, *columns)


def _dataclass_to_sqlalchemy(
    source: type, table_name: str = None, metadata: MetaData = None
) -> Table:
    """Convert dataclass to SQLAlchemy Table."""
    import dataclasses
    from typing import get_type_hints

    if table_name is None:
        table_name = source.__name__.lower()

    if metadata is None:
        metadata = MetaData()

    columns = []
    hints = get_type_hints(source)

    for field in dataclasses.fields(source):
        field_type = hints.get(field.name, Any)
        sa_type = _python_type_to_sqlalchemy(field_type)
        nullable = (
            field.default != dataclasses.MISSING or field.default_factory != dataclasses.MISSING
        )
        columns.append(Column(field.name, sa_type, nullable=nullable))

    return Table(table_name, metadata, *columns)


def _typeddict_to_sqlalchemy(
    td_class: type, table_name: str = None, metadata: MetaData = None
) -> Table:
    """Convert TypedDict to SQLAlchemy Table."""
    from typing import get_type_hints

    if table_name is None:
        table_name = td_class.__name__.lower()

    if metadata is None:
        metadata = MetaData()

    columns = []
    hints = get_type_hints(td_class)

    for name, field_type in hints.items():
        sa_type = _python_type_to_sqlalchemy(field_type)
        nullable = True  # Default to nullable
        columns.append(Column(name, sa_type, nullable=nullable))

    return Table(table_name, metadata, *columns)


def _pyspark_to_sqlalchemy(struct_type, table_name: str = None, metadata: MetaData = None) -> Table:
    """Convert PySpark StructType to SQLAlchemy Table."""

    if table_name is None:
        table_name = "pyspark_table"

    if metadata is None:
        metadata = MetaData()

    columns = []
    for field in struct_type.fields:
        sa_type = _pyspark_type_to_sqlalchemy(field.dataType)
        columns.append(Column(field.name, sa_type, nullable=field.nullable))

    return Table(table_name, metadata, *columns)


def _pyspark_type_to_sqlalchemy(spark_type):
    """Convert PySpark type to SQLAlchemy type."""
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
        return String()
    elif isinstance(spark_type, (IntegerType, LongType)):
        return Integer()
    elif isinstance(spark_type, (FloatType, DoubleType)):
        return Float()
    elif isinstance(spark_type, BooleanType):
        return Boolean()
    elif isinstance(spark_type, DateType):
        return Date()
    elif isinstance(spark_type, TimestampType):
        return DateTime()
    else:
        return String()  # Default


def _polars_to_sqlalchemy(schema, table_name: str = None, metadata: MetaData = None) -> Table:
    """Convert Polars Schema to SQLAlchemy Table."""

    if table_name is None:
        table_name = "polars_table"

    if metadata is None:
        metadata = MetaData()

    columns = []
    for name, dtype in schema.items():
        sa_type = _polars_type_to_sqlalchemy(dtype)
        columns.append(Column(name, sa_type, nullable=True))

    return Table(table_name, metadata, *columns)


def _polars_type_to_sqlalchemy(dtype):
    """Convert Polars type to SQLAlchemy type."""
    import polars as pl

    if dtype == pl.Utf8 or dtype == pl.String:
        return String()
    elif dtype == pl.Int64 or dtype == pl.Int32:
        return Integer()
    elif dtype == pl.Float64 or dtype == pl.Float32:
        return Float()
    elif dtype == pl.Boolean:
        return Boolean()
    elif dtype == pl.Date:
        return Date()
    elif dtype == pl.Datetime:
        return DateTime()
    else:
        return String()  # Default


def _pandas_to_sqlalchemy(df, table_name: str = None, metadata: MetaData = None) -> Table:
    """Convert Pandas DataFrame to SQLAlchemy Table."""

    if table_name is None:
        table_name = "pandas_table"

    if metadata is None:
        metadata = MetaData()

    columns = []
    for col in df.columns:
        dtype = df[col].dtype
        sa_type = _pandas_type_to_sqlalchemy(dtype)
        nullable = df[col].isna().any()
        columns.append(Column(col, sa_type, nullable=nullable))

    return Table(table_name, metadata, *columns)


def _pandas_type_to_sqlalchemy(dtype):
    """Convert Pandas dtype to SQLAlchemy type."""
    import pandas as pd

    if pd.api.types.is_integer_dtype(dtype):
        return Integer()
    elif pd.api.types.is_float_dtype(dtype):
        return Float()
    elif pd.api.types.is_bool_dtype(dtype):
        return Boolean()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return DateTime()
    else:
        return String()  # Default


def _python_type_to_sqlalchemy(python_type) -> Any:
    """Convert Python type hint to SQLAlchemy type."""
    from datetime import date, datetime
    from typing import Union, get_args, get_origin

    origin = get_origin(python_type)

    if origin is Optional or (origin is Union and type(None) in get_args(python_type)):
        # Handle Optional types
        args = get_args(python_type)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return _python_type_to_sqlalchemy(non_none_args[0])
        return String()

    # Handle base types
    if python_type is str:
        return String()
    elif python_type is int:
        return Integer()
    elif python_type is float:
        return Float()
    elif python_type is bool:
        return Boolean()
    elif python_type is date:
        return Date()
    elif python_type is datetime:
        return DateTime()
    else:
        return String()  # Default


def from_sqlalchemy(sa_obj: Union[Table, type], target_type: str = "pydantic") -> Any:
    """
    Convert SQLAlchemy Table or model to another schema type.

    Args:
        sa_obj: SQLAlchemy Table or model class
        target_type: Target schema type ('pydantic', 'dataclass', 'typedict', etc.)

    Returns:
        Converted schema
    """
    _check_sqlalchemy()

    if target_type == "pydantic":
        from lugia.pydantic import to_pydantic

        return to_pydantic(sa_obj)
    elif target_type == "dataclass":
        from lugia.dataclass import to_dataclass

        return to_dataclass(sa_obj)
    elif target_type == "typedict":
        from lugia.typedict import to_typeddict

        return to_typeddict(sa_obj)
    elif target_type == "pandas":
        from lugia.pandas import to_pandas

        return to_pandas(sa_obj)
    elif target_type == "polars":
        from lugia.polars import to_polars

        return to_polars(sa_obj)
    elif target_type == "pyspark":
        from lugia.pyspark import to_pyspark

        return to_pyspark(sa_obj)
    else:
        raise ValueError(f"Unsupported target type: {target_type}")
