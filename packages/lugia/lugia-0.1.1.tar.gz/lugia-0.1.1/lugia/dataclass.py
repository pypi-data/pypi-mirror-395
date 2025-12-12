"""Python dataclass schema and data conversions.

This module provides functions to convert various schema types to Python dataclasses.
"""

import dataclasses
from typing import Any, Optional, Union

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
    is_typeddict,
)


def to_dataclass(source: Any) -> Union[type, Any]:
    """
    Convert a schema or data object to Python dataclass.

    Supports conversion from:
    - Pydantic models and instances
    - TypedDict classes
    - PySpark StructType
    - Polars Schema and DataFrame
    - Pandas DataFrame
    - SQLModel classes (Pydantic-based)
    - SQLAlchemy Table and model classes

    Args:
        source: Source schema (class) or data (instance)

    Returns:
        Dataclass class or instance

    Raises:
        MissingDependencyError: If required dependencies are not installed
        ValueError: If the source type cannot be converted

    Examples:
        >>> import dataclasses
        >>> @dataclasses.dataclass
        ... class User:
        ...     name: str
        ...     age: int
        >>> # Already a dataclass, returns as-is
        >>> to_dataclass(User) is User
        True
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
    """Convert Pydantic model to dataclass.

    Args:
        source: A Pydantic model class or instance

    Returns:
        A dataclass class or instance
    """
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to dataclass conversion") from None

    # Handle Pydantic v1 and v2 compatibility
    def get_fields(model: type[BaseModel]) -> dict[str, Any]:
        if hasattr(model, "model_fields"):
            return model.model_fields  # Pydantic v2
        else:
            return model.__fields__  # Pydantic v1

    def dump_instance(instance: BaseModel) -> dict[str, Any]:
        if hasattr(instance, "model_dump"):
            return instance.model_dump()  # Pydantic v2
        else:
            return instance.dict()  # Pydantic v1

    if isinstance(source, type) and issubclass(source, BaseModel):
        # Convert model class
        fields = []
        model_fields = get_fields(source)
        for field_name, field_info in model_fields.items():
            # Handle both v1 and v2 field info
            if hasattr(field_info, "annotation"):
                field_type = field_info.annotation
            else:
                field_type = field_info.type_  # v1

            if hasattr(field_info, "default"):
                default = (
                    field_info.default if field_info.default is not ... else dataclasses.MISSING
                )
            else:
                default = (
                    field_info.default if field_info.default is not ... else dataclasses.MISSING
                )

            default_factory = (
                field_info.default_factory
                if hasattr(field_info, "default_factory") and field_info.default_factory is not ...
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
        return dc_class(**dump_instance(source))


def _typeddict_to_dataclass(td_class: type) -> type:
    """Convert TypedDict to dataclass.

    Args:
        td_class: A TypedDict class

    Returns:
        A dataclass class
    """
    from typing import get_type_hints

    annotations = get_type_hints(td_class)
    fields = [(name, field_type) for name, field_type in annotations.items()]

    return dataclasses.make_dataclass(f"{td_class.__name__}Dataclass", fields)


def _pyspark_to_dataclass(struct_type) -> type:
    """Convert PySpark StructType to dataclass.

    Args:
        struct_type: A PySpark StructType instance

    Returns:
        A dataclass class
    """
    fields = []

    for field in struct_type.fields:
        field_type = pyspark_type_to_python(field.dataType)
        if field.nullable:
            field_type = Optional[field_type]
        fields.append((field.name, field_type))

    return dataclasses.make_dataclass("PysparkDataclass", fields)


def _polars_to_dataclass(schema) -> type:
    """Convert Polars Schema to dataclass.

    Args:
        schema: A Polars Schema instance

    Returns:
        A dataclass class
    """
    fields = []

    for name, dtype in schema.items():
        python_type = polars_type_to_python(dtype)
        fields.append((name, python_type))

    return dataclasses.make_dataclass("PolarsDataclass", fields)


def _pandas_to_dataclass(df) -> type:
    """Convert Pandas DataFrame to dataclass.

    Args:
        df: A Pandas DataFrame

    Returns:
        A dataclass class
    """
    fields = []

    for col in df.columns:
        dtype = df[col].dtype
        python_type = pandas_type_to_python(dtype)
        if df[col].isna().any():
            python_type = Optional[python_type]
        fields.append((col, python_type))

    return dataclasses.make_dataclass("PandasDataclass", fields)


def _sqlalchemy_to_dataclass(table) -> type:
    """Convert SQLAlchemy Table to dataclass.

    Args:
        table: A SQLAlchemy Table instance

    Returns:
        A dataclass class
    """
    fields = []

    for column in table.columns:
        python_type = sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        fields.append((column.name, python_type))

    return dataclasses.make_dataclass(f"{table.name}Dataclass", fields)
