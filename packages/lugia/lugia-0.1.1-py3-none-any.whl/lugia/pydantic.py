"""Pydantic schema and data conversions.

This module provides functions to convert various schema types to Pydantic models.
It supports both Pydantic v1 and v2 with automatic compatibility detection.
"""

from typing import Any, Optional, Union

from lugia.exceptions import MissingDependencyError
from lugia.type_converters import (
    pandas_type_to_python,
    polars_type_to_python,
    pyspark_type_to_python,
    sqlalchemy_type_to_python,
)
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
    PYDANTIC_V2 = False
    try:
        # Check if Pydantic v2 is available
        import pydantic

        # Check for v2 indicators without triggering deprecation warnings
        # Pydantic v2 has a v1 compatibility module
        if hasattr(pydantic, "v1"):
            PYDANTIC_V2 = True
        else:
            # Check version number if available
            if hasattr(pydantic, "__version__"):
                version = pydantic.__version__
                PYDANTIC_V2 = version.startswith("2.")
            else:
                # Fallback: create a test model and check for model_fields
                # This avoids accessing __fields__ directly
                test_model = type("_TestModel", (BaseModel,), {})
                PYDANTIC_V2 = hasattr(test_model, "model_fields")
    except Exception:
        pass
except ImportError:
    PYDANTIC_AVAILABLE = False
    PYDANTIC_V2 = False
    BaseModel = None  # type: ignore
    create_model = None  # type: ignore
    FieldInfo = None  # type: ignore


def _check_pydantic():
    """Check if Pydantic is available."""
    if not PYDANTIC_AVAILABLE:
        raise MissingDependencyError("pydantic", "Pydantic conversions")


def _get_pydantic_fields(model: type[BaseModel]) -> dict[str, Any]:
    """Get model fields in a way compatible with both Pydantic v1 and v2.

    Args:
        model: A Pydantic BaseModel class

    Returns:
        Dictionary of field names to field info objects
    """
    if PYDANTIC_V2:
        return model.model_fields  # type: ignore
    else:
        return model.__fields__  # type: ignore


def _pydantic_dump(instance: BaseModel) -> dict[str, Any]:
    """Dump a Pydantic instance to dict in a way compatible with both v1 and v2.

    Args:
        instance: A Pydantic model instance

    Returns:
        Dictionary representation of the instance
    """
    if PYDANTIC_V2:
        return instance.model_dump()
    else:
        return instance.dict()


def to_pydantic(source: Any) -> Union[type[BaseModel], BaseModel]:
    """
    Convert a schema or data object to Pydantic.

    Supports conversion from:
    - Dataclass classes and instances
    - TypedDict classes
    - PySpark StructType
    - Polars Schema and DataFrame
    - Pandas DataFrame
    - SQLModel classes (already Pydantic-based)
    - SQLAlchemy Table and model classes

    Args:
        source: Source schema (class) or data (instance)

    Returns:
        Pydantic model class or instance

    Raises:
        MissingDependencyError: If Pydantic is not installed
        ValueError: If the source type cannot be converted

    Examples:
        >>> from pydantic import BaseModel
        >>> class User(BaseModel):
        ...     name: str
        ...     age: int
        >>> # Already Pydantic, returns as-is
        >>> to_pydantic(User) is User
        True
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
    """Convert a dataclass to Pydantic model.

    Args:
        dc_class: A dataclass class

    Returns:
        A Pydantic model class
    """
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
    """Convert a TypedDict to Pydantic model.

    Args:
        td_class: A TypedDict class

    Returns:
        A Pydantic model class

    Note:
        All TypedDict fields are treated as required unless they are Optional.
    """
    annotations = get_annotations(td_class)
    fields = {}

    for name, field_type in annotations.items():
        # Check if field is required (TypedDict doesn't have a simple way to check this)
        # We'll assume all fields are required unless they're Optional
        fields[name] = (field_type, ...)

    return create_model(f"{td_class.__name__}Model", **fields)


def _pyspark_to_pydantic(struct_type) -> type[BaseModel]:
    """Convert PySpark StructType to Pydantic model.

    Args:
        struct_type: A PySpark StructType instance

    Returns:
        A Pydantic model class
    """
    fields = {}

    for field in struct_type.fields:
        field_type = pyspark_type_to_python(field.dataType)
        fields[field.name] = (
            field_type,
            ... if not field.nullable else Optional[field_type],
        )

    return create_model("PysparkModel", **fields)


def _polars_to_pydantic(schema) -> type[BaseModel]:
    """Convert Polars Schema to Pydantic model.

    Args:
        schema: A Polars Schema instance

    Returns:
        A Pydantic model class
    """
    fields = {}

    for name, dtype in schema.items():
        python_type = polars_type_to_python(dtype)
        fields[name] = (python_type, ...)

    return create_model("PolarsModel", **fields)


def _pandas_to_pydantic(df) -> type[BaseModel]:
    """Convert Pandas DataFrame to Pydantic model.

    Args:
        df: A Pandas DataFrame

    Returns:
        A Pydantic model class
    """
    from typing import Optional

    fields = {}

    for col in df.columns:
        dtype = df[col].dtype
        python_type = pandas_type_to_python(dtype)
        # Check for nullable columns
        if df[col].isna().any():
            python_type = Optional[python_type]
        fields[col] = (python_type, ...)

    return create_model("PandasModel", **fields)


def _sqlalchemy_to_pydantic(table) -> type[BaseModel]:
    """Convert SQLAlchemy Table to Pydantic model.

    Args:
        table: A SQLAlchemy Table instance

    Returns:
        A Pydantic model class
    """
    from typing import Optional

    fields = {}

    for column in table.columns:
        python_type = sqlalchemy_type_to_python(column.type)
        if column.nullable:
            python_type = Optional[python_type]
        fields[column.name] = (python_type, ...)

    return create_model(f"{table.name}Model", **fields)
