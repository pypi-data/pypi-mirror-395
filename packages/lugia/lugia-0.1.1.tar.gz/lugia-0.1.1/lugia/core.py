"""Core conversion utilities and type detection."""

from typing import Any, Optional

from lugia.exceptions import ConversionError
from lugia.utils import (
    get_type_name,
    is_dataclass,
    is_sqlalchemy_model,
    is_typeddict,
)


def detect_type(obj: Any) -> str:
    """
    Detect the type of a schema or data object.

    This function attempts to identify the type of a given object by checking
    against known schema types. It supports both class types and instances.

    Args:
        obj: The object to detect the type of (can be a class or instance)

    Returns:
        A string representing the detected type. One of: 'pydantic', 'dataclass',
        'typedict', 'pyspark', 'polars', 'pandas', 'sqlmodel', 'sqlalchemy', 'unknown'

    Examples:
        >>> from pydantic import BaseModel
        >>> class User(BaseModel):
        ...     name: str
        >>> detect_type(User)
        'pydantic'
        >>> detect_type(User(name="John"))
        'pydantic'
    """
    # Check for Pydantic
    try:
        from pydantic import BaseModel

        if isinstance(obj, type) and issubclass(obj, BaseModel):
            return "pydantic"
        if isinstance(obj, BaseModel):
            return "pydantic"
    except (ImportError, TypeError):
        pass

    # Check for SQLModel
    try:
        from sqlmodel import SQLModel

        if isinstance(obj, type) and issubclass(obj, SQLModel):
            return "sqlmodel"
    except (ImportError, TypeError):
        pass

    # Check for SQLAlchemy
    if is_sqlalchemy_model(obj):
        return "sqlalchemy"

    # Check for dataclass
    if is_dataclass(obj):
        return "dataclass"

    # Check for TypedDict
    if is_typeddict(obj):
        return "typedict"

    # Check for PySpark
    try:
        from pyspark.sql.types import StructType

        if isinstance(obj, StructType):
            return "pyspark"
        from pyspark.sql import DataFrame as SparkDataFrame

        if isinstance(obj, SparkDataFrame):
            return "pyspark"
    except ImportError:
        pass

    # Check for Polars
    try:
        import polars as pl

        if isinstance(obj, pl.DataFrame):
            return "polars"
        if isinstance(obj, pl.Schema):
            return "polars"
    except ImportError:
        pass

    # Check for Pandas
    try:
        import pandas as pd

        if isinstance(obj, pd.DataFrame):
            return "pandas"
        if isinstance(obj, pd.Series):
            return "pandas"
    except ImportError:
        pass

    return "unknown"


def convert(source: Any, target: Optional[str] = None, target_type: Optional[type] = None) -> Any:
    """
    Convert a schema or data object to another format.

    This is the unified conversion function that automatically detects the source
    type and converts it to the specified target format. Either 'target' or
    'target_type' must be provided.

    Args:
        source: The source schema or data to convert
        target: Target format name (e.g., 'pyspark', 'polars', 'pydantic', 'dataclass')
        target_type: Target type class (alternative to target string)

    Returns:
        Converted schema or data object

    Raises:
        ConversionError: If the source type cannot be detected or conversion fails
        ValueError: If neither 'target' nor 'target_type' is provided

    Examples:
        >>> from pydantic import BaseModel
        >>> class User(BaseModel):
        ...     name: str
        ...     age: int
        >>> # Convert to dataclass
        >>> UserDC = convert(User, target="dataclass")
        >>> # Convert back to Pydantic
        >>> UserPydantic = convert(UserDC, target="pydantic")
    """
    source_type = detect_type(source)

    if source_type == "unknown":
        raise ConversionError(
            get_type_name(source),
            target or get_type_name(target_type) if target_type else "unknown",
            "Could not detect source type",
        )

    # Determine target type
    if target_type:
        target = detect_type(target_type)
    elif not target:
        raise ValueError("Either 'target' or 'target_type' must be provided")

    # Import and call appropriate converter
    if target == "pyspark":
        from lugia.pyspark import to_pyspark

        return to_pyspark(source)
    elif target == "polars":
        from lugia.polars import to_polars

        return to_polars(source)
    elif target == "pandas":
        from lugia.pandas import to_pandas

        return to_pandas(source)
    elif target == "pydantic":
        from lugia.pydantic import to_pydantic

        return to_pydantic(source)
    elif target == "dataclass":
        from lugia.dataclass import to_dataclass

        return to_dataclass(source)
    elif target == "typedict":
        from lugia.typedict import to_typeddict

        return to_typeddict(source)
    elif target == "sqlmodel":
        from lugia.sqlmodel import to_sqlmodel

        return to_sqlmodel(source)
    elif target == "sqlalchemy":
        from lugia.sqlalchemy import to_sqlalchemy

        return to_sqlalchemy(source)
    else:
        raise ConversionError(source_type, target, f"Unsupported target type: {target}")
