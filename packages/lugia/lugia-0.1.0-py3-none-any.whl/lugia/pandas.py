"""Pandas DataFrame and Series conversions."""

from typing import Any, Union

from lugia.exceptions import MissingDependencyError
from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
    is_typeddict,
)

try:
    import numpy as np
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None  # type: ignore
    np = None  # type: ignore


def _check_pandas():
    """Check if Pandas is available."""
    if not PANDAS_AVAILABLE:
        raise MissingDependencyError("pandas", "Pandas conversions")


def to_pandas(source: Any) -> Union[pd.DataFrame, pd.Series]:
    """
    Convert a schema or data object to Pandas DataFrame or Series.

    Args:
        source: Source schema or data

    Returns:
        Pandas DataFrame or Series
    """
    _check_pandas()

    # If already Pandas, return as-is
    if isinstance(source, (pd.DataFrame, pd.Series)):
        return source

    # Handle Pydantic
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return _pydantic_to_pandas(source)

    # Handle dataclass
    if is_dataclass(source):
        return _dataclass_to_pandas(source)

    # Handle TypedDict
    if is_typeddict(source):
        return _typeddict_to_pandas(source)

    # Handle list of dicts or instances
    if isinstance(source, list):
        if source and isinstance(source[0], dict):
            return pd.DataFrame(source)
        elif source and (is_pydantic_instance(source[0]) or is_dataclass(source[0])):
            return _instances_to_pandas(source)

    # Handle PySpark
    try:
        from pyspark.sql import DataFrame as SparkDataFrame

        if isinstance(source, SparkDataFrame):
            return _pyspark_to_pandas(source)
    except ImportError:
        pass

    # Handle Polars
    try:
        import polars as pl

        if isinstance(source, pl.DataFrame):
            return _polars_to_pandas(source)
    except ImportError:
        pass

    # Handle dict
    if isinstance(source, dict):
        return pd.DataFrame([source])

    raise ValueError(f"Cannot convert {type(source)} to Pandas")


def _pydantic_to_pandas(source: Any) -> pd.DataFrame:
    """Convert Pydantic model or instance to Pandas DataFrame."""
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to Pandas conversion") from None

    if isinstance(source, type) and issubclass(source, BaseModel):
        # Schema only - return empty DataFrame with correct columns
        fields = list(source.model_fields.keys())
        return pd.DataFrame(columns=fields)
    else:
        # Instance - convert to dict and create DataFrame
        data = source.model_dump() if hasattr(source, "model_dump") else source.dict()
        return pd.DataFrame([data])


def _dataclass_to_pandas(source: Any) -> pd.DataFrame:
    """Convert dataclass to Pandas DataFrame."""
    import dataclasses

    if isinstance(source, type):
        # Schema only
        fields = [f.name for f in dataclasses.fields(source)]
        return pd.DataFrame(columns=fields)
    else:
        # Instance
        data = dataclasses.asdict(source)
        return pd.DataFrame([data])


def _typeddict_to_pandas(td_class: type) -> pd.DataFrame:
    """Convert TypedDict to Pandas DataFrame."""
    from typing import get_type_hints

    if isinstance(td_class, type):
        # Schema only - return empty DataFrame with correct columns
        hints = get_type_hints(td_class)
        fields = list(hints.keys())
        return pd.DataFrame(columns=fields)
    else:
        # Instance (dict)
        return pd.DataFrame([td_class])


def _instances_to_pandas(instances: list[Any]) -> pd.DataFrame:
    """Convert list of instances to Pandas DataFrame."""
    rows = []
    for instance in instances:
        if is_pydantic_instance(instance):
            rows.append(
                instance.model_dump() if hasattr(instance, "model_dump") else instance.dict()
            )
        elif is_dataclass(instance):
            import dataclasses

            rows.append(dataclasses.asdict(instance))
        else:
            rows.append(instance.__dict__)
    return pd.DataFrame(rows)


def _pyspark_to_pandas(spark_df) -> pd.DataFrame:
    """Convert PySpark DataFrame to Pandas DataFrame."""
    try:
        from pyspark.sql import DataFrame as SparkDataFrame  # noqa: F401
    except ImportError:
        raise MissingDependencyError("pyspark", "PySpark to Pandas conversion") from None

    return spark_df.toPandas()


def _polars_to_pandas(polars_df) -> pd.DataFrame:
    """Convert Polars DataFrame to Pandas DataFrame."""
    try:
        import polars as pl  # noqa: F401
    except ImportError:
        raise MissingDependencyError("polars", "Polars to Pandas conversion") from None

    return polars_df.to_pandas()


def from_pandas(df: pd.DataFrame, target_type: str = "pydantic") -> Any:
    """
    Convert Pandas DataFrame to another schema type.

    Args:
        df: Pandas DataFrame
        target_type: Target schema type ('pydantic', 'dataclass', 'typedict', etc.)

    Returns:
        Converted schema or data
    """
    _check_pandas()

    if target_type == "pydantic":
        from lugia.pydantic import to_pydantic

        return to_pydantic(df)
    elif target_type == "dataclass":
        from lugia.dataclass import to_dataclass

        return to_dataclass(df)
    elif target_type == "typedict":
        from lugia.typedict import to_typeddict

        return to_typeddict(df)
    elif target_type == "polars":
        from lugia.polars import to_polars

        return to_polars(df)
    elif target_type == "pyspark":
        from lugia.pyspark import to_pyspark

        return to_pyspark(df)
    else:
        raise ValueError(f"Unsupported target type: {target_type}")
