"""TypedDict schema conversions.

This module provides functions to convert various schema types to TypedDict classes.
"""

from typing import Any, Optional, TypedDict

from lugia.type_converters import (
    pandas_type_to_python,
    polars_type_to_python,
    pyspark_type_to_python,
    sqlalchemy_type_to_python,
)
from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
    is_typeddict,
)


def to_typeddict(source: Any) -> type[TypedDict]:
    """
    Convert a schema object to TypedDict.

    Supports conversion from:
    - Pydantic models and instances
    - Dataclass classes
    - PySpark StructType
    - Polars Schema and DataFrame
    - Pandas DataFrame
    - SQLModel classes (Pydantic-based)
    - SQLAlchemy Table and model classes

    Args:
        source: Source schema (class) or instance

    Returns:
        TypedDict class

    Raises:
        ValueError: If the source type cannot be converted

    Examples:
        >>> from typing import TypedDict
        >>> class User(TypedDict):
        ...     name: str
        ...     age: int
        >>> # Already a TypedDict, returns as-is
        >>> to_typeddict(User) is User
        True
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
    """Convert Pydantic model to TypedDict.

    Args:
        source: A Pydantic model class or instance

    Returns:
        A TypedDict class
    """
    try:
        from pydantic import BaseModel
    except ImportError:
        raise ValueError("Pydantic not available") from None

    model = source if isinstance(source, type) and issubclass(source, BaseModel) else type(source)

    # Handle Pydantic v1 and v2 compatibility
    fields = model.model_fields if hasattr(model, "model_fields") else model.__fields__

    annotations = {}
    for field_name, field_info in fields.items():
        if hasattr(field_info, "annotation"):
            annotations[field_name] = field_info.annotation  # v2
        else:
            annotations[field_name] = field_info.type_  # v1

    return TypedDict(f"{model.__name__}TypedDict", annotations)


def _dataclass_to_typeddict(dc_class: type) -> type[TypedDict]:
    """Convert dataclass to TypedDict.

    Args:
        dc_class: A dataclass class

    Returns:
        A TypedDict class
    """
    from typing import get_type_hints

    annotations = get_type_hints(dc_class)
    return TypedDict(f"{dc_class.__name__}TypedDict", annotations)


def _pyspark_to_typeddict(struct_type) -> type[TypedDict]:
    """Convert PySpark StructType to TypedDict.

    Args:
        struct_type: A PySpark StructType instance

    Returns:
        A TypedDict class
    """
    annotations = {}

    for field in struct_type.fields:
        field_type = pyspark_type_to_python(field.dataType)
        if field.nullable:
            field_type = Optional[field_type]
        annotations[field.name] = field_type

    return TypedDict("PysparkTypedDict", annotations)


def _polars_to_typeddict(schema) -> type[TypedDict]:
    """Convert Polars Schema to TypedDict.

    Args:
        schema: A Polars Schema instance

    Returns:
        A TypedDict class
    """
    annotations = {}

    for name, dtype in schema.items():
        python_type = polars_type_to_python(dtype)
        annotations[name] = python_type

    return TypedDict("PolarsTypedDict", annotations)


def _pandas_to_typeddict(df) -> type[TypedDict]:
    """Convert Pandas DataFrame to TypedDict.

    Args:
        df: A Pandas DataFrame

    Returns:
        A TypedDict class
    """
    annotations = {}

    for col in df.columns:
        dtype = df[col].dtype
        python_type = pandas_type_to_python(dtype)
        if df[col].isna().any():
            python_type = Optional[python_type]
        annotations[col] = python_type

    return TypedDict("PandasTypedDict", annotations)


def _sqlalchemy_to_typeddict(table) -> type[TypedDict]:
    """Convert SQLAlchemy Table to TypedDict.

    Args:
        table: A SQLAlchemy Table instance

    Returns:
        A TypedDict class
    """
    annotations = {}

    for column in table.columns:
        python_type = sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        annotations[column.name] = python_type

    return TypedDict(f"{table.name}TypedDict", annotations)
