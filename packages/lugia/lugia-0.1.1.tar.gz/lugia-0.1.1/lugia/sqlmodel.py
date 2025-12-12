"""SQLModel model conversions.

This module provides functions to convert various schema types to SQLModel classes.
SQLModel is a library that combines SQLAlchemy and Pydantic.
"""

from typing import Any, Optional

from lugia.exceptions import MissingDependencyError
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

    Supports conversion from:
    - Pydantic models and instances
    - Dataclass classes
    - TypedDict classes
    - PySpark StructType
    - Polars Schema
    - Pandas DataFrame
    - SQLAlchemy Table and model classes

    Args:
        source: Source schema (class) or instance

    Returns:
        SQLModel model class

    Raises:
        MissingDependencyError: If SQLModel is not installed
        ValueError: If the source type cannot be converted

    Examples:
        >>> from sqlmodel import SQLModel
        >>> class User(SQLModel):
        ...     name: str
        ...     age: int
        >>> # Already SQLModel, returns as-is
        >>> to_sqlmodel(User) is User
        True
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
    """Convert Pydantic model to SQLModel.

    Args:
        source: A Pydantic model class or instance

    Returns:
        A SQLModel class
    """
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to SQLModel conversion") from None

    model = source if isinstance(source, type) and issubclass(source, BaseModel) else type(source)

    # Handle Pydantic v1 and v2 compatibility
    model_fields = model.model_fields if hasattr(model, "model_fields") else model.__fields__

    # SQLModel is based on Pydantic, so we can create a SQLModel subclass
    # that inherits from the Pydantic model's fields
    annotations = {}
    fields = {}
    for field_name, field_info in model_fields.items():
        # Handle both v1 and v2 field info
        if hasattr(field_info, "annotation"):
            field_type = field_info.annotation  # v2
        else:
            field_type = field_info.type_  # v1

        if hasattr(field_info, "default"):
            default = field_info.default if field_info.default is not ... else None
        else:
            default = None

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
    """Convert dataclass to SQLModel.

    Args:
        source: A dataclass class

    Returns:
        A SQLModel class
    """
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
    """Convert TypedDict to SQLModel.

    Args:
        td_class: A TypedDict class

    Returns:
        A SQLModel class
    """
    from typing import get_type_hints

    hints = get_type_hints(td_class)
    fields = {}

    for name, field_type in hints.items():
        fields[name] = (field_type, Field())

    class_name = f"{td_class.__name__}SQLModel"
    return type(class_name, (SQLModel,), fields)


def _pyspark_to_sqlmodel(struct_type) -> type[SQLModel]:
    """Convert PySpark StructType to SQLModel.

    Args:
        struct_type: A PySpark StructType instance

    Returns:
        A SQLModel class
    """
    fields = {}

    for field in struct_type.fields:
        field_type = pyspark_type_to_python(field.dataType)
        if field.nullable:
            field_type = Optional[field_type]
        fields[field.name] = (field_type, Field())

    return type("PysparkSQLModel", (SQLModel,), fields)


def _polars_to_sqlmodel(schema) -> type[SQLModel]:
    """Convert Polars Schema to SQLModel.

    Args:
        schema: A Polars Schema instance

    Returns:
        A SQLModel class
    """
    fields = {}

    for name, dtype in schema.items():
        python_type = polars_type_to_python(dtype)
        fields[name] = (python_type, Field())

    return type("PolarsSQLModel", (SQLModel,), fields)


def _pandas_to_sqlmodel(df) -> type[SQLModel]:
    """Convert Pandas DataFrame to SQLModel.

    Args:
        df: A Pandas DataFrame

    Returns:
        A SQLModel class
    """
    fields = {}

    for col in df.columns:
        dtype = df[col].dtype
        python_type = pandas_type_to_python(dtype)
        if df[col].isna().any():
            python_type = Optional[python_type]
        fields[col] = (python_type, Field())

    return type("PandasSQLModel", (SQLModel,), fields)


def _sqlalchemy_to_sqlmodel(table) -> type[SQLModel]:
    """Convert SQLAlchemy Table to SQLModel.

    Args:
        table: A SQLAlchemy Table instance

    Returns:
        A SQLModel class
    """
    fields = {}

    for column in table.columns:
        python_type = sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        fields[column.name] = (python_type, Field())

    return type(f"{table.name}SQLModel", (SQLModel,), fields)


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
