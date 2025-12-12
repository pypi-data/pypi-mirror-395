"""Polars DataFrame and Schema conversions."""

from typing import Any, Optional, Union

from lugia.exceptions import MissingDependencyError
from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
)

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None  # type: ignore


def _check_polars():
    """Check if Polars is available."""
    if not POLARS_AVAILABLE:
        raise MissingDependencyError("polars", "Polars conversions")


def to_polars(source: Any) -> Union[pl.DataFrame, pl.Schema]:
    """
    Convert a schema or data object to Polars DataFrame or Schema.

    Args:
        source: Source schema or data

    Returns:
        Polars DataFrame or Schema
    """
    _check_polars()

    # If already Polars, return as-is
    if isinstance(source, pl.DataFrame):
        return source
    if isinstance(source, pl.Schema):
        return source

    # Handle Pydantic
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return _pydantic_to_polars(source)

    # Handle dataclass
    if is_dataclass(source):
        return _dataclass_to_polars(source)

    # Handle list of dicts or instances
    if isinstance(source, list):
        if source and isinstance(source[0], dict):
            return pl.DataFrame(source)
        elif source and (is_pydantic_instance(source[0]) or is_dataclass(source[0])):
            return _instances_to_polars(source)

    # Handle PySpark
    try:
        from pyspark.sql import DataFrame as SparkDataFrame
        from pyspark.sql.types import StructType

        if isinstance(source, SparkDataFrame):
            return _pyspark_to_polars(source)
        if isinstance(source, StructType):
            return _pyspark_schema_to_polars(source)
    except ImportError:
        pass

    # Handle Pandas
    try:
        import pandas as pd

        if isinstance(source, pd.DataFrame):
            return _pandas_to_polars(source)
    except ImportError:
        pass

    # Handle dict
    if isinstance(source, dict):
        return pl.DataFrame([source])

    raise ValueError(f"Cannot convert {type(source)} to Polars")


def _pydantic_to_polars(source: Any) -> Union[pl.DataFrame, pl.Schema]:
    """Convert Pydantic model or instance to Polars."""
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to Polars conversion") from None

    if isinstance(source, type) and issubclass(source, BaseModel):
        # Schema only - return Schema
        schema_dict = {}
        for field_name, field_info in source.model_fields.items():
            polars_type = _python_type_to_polars(field_info.annotation)
            schema_dict[field_name] = polars_type
        return pl.Schema(schema_dict)
    else:
        # Instance - convert to dict and create DataFrame
        data = source.model_dump() if hasattr(source, "model_dump") else source.dict()
        return pl.DataFrame([data])


def _dataclass_to_polars(source: Any) -> Union[pl.DataFrame, pl.Schema]:
    """Convert dataclass to Polars."""
    import dataclasses
    from typing import get_type_hints

    if isinstance(source, type):
        # Schema only
        schema_dict = {}
        hints = get_type_hints(source)
        for field in dataclasses.fields(source):
            field_type = hints.get(field.name, Any)
            polars_type = _python_type_to_polars(field_type)
            schema_dict[field.name] = polars_type
        return pl.Schema(schema_dict)
    else:
        # Instance
        data = dataclasses.asdict(source)
        return pl.DataFrame([data])


def _instances_to_polars(instances: list[Any]) -> pl.DataFrame:
    """Convert list of instances to Polars DataFrame."""
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
    return pl.DataFrame(rows)


def _pyspark_to_polars(spark_df) -> pl.DataFrame:
    """Convert PySpark DataFrame to Polars DataFrame."""
    try:
        from pyspark.sql import DataFrame as SparkDataFrame  # noqa: F401
    except ImportError:
        raise MissingDependencyError("pyspark", "PySpark to Polars conversion") from None

    # Convert to Pandas first, then to Polars
    pandas_df = spark_df.toPandas()
    return pl.from_pandas(pandas_df)


def _pyspark_schema_to_polars(struct_type) -> pl.Schema:
    """Convert PySpark StructType to Polars Schema."""
    schema_dict = {}
    for field in struct_type.fields:
        polars_type = _pyspark_type_to_polars(field.dataType)
        schema_dict[field.name] = polars_type
    return pl.Schema(schema_dict)


def _pyspark_type_to_polars(spark_type):
    """Convert PySpark type to Polars type."""
    from pyspark.sql.types import (
        ArrayType,
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
        return pl.Utf8
    elif isinstance(spark_type, IntegerType):
        return pl.Int32
    elif isinstance(spark_type, LongType):
        return pl.Int64
    elif isinstance(spark_type, FloatType):
        return pl.Float32
    elif isinstance(spark_type, DoubleType):
        return pl.Float64
    elif isinstance(spark_type, BooleanType):
        return pl.Boolean
    elif isinstance(spark_type, DateType):
        return pl.Date
    elif isinstance(spark_type, TimestampType):
        return pl.Datetime
    elif isinstance(spark_type, ArrayType):
        element_type = _pyspark_type_to_polars(spark_type.elementType)
        return pl.List(element_type)
    else:
        return pl.Utf8  # Default to string


def _pandas_to_polars(pandas_df) -> pl.DataFrame:
    """Convert Pandas DataFrame to Polars DataFrame."""
    try:
        import pandas as pd  # noqa: F401
    except ImportError:
        raise MissingDependencyError("pandas", "Pandas to Polars conversion") from None

    return pl.from_pandas(pandas_df)


def _python_type_to_polars(python_type) -> pl.DataType:
    """Convert Python type hint to Polars type."""
    from datetime import date, datetime
    from typing import Union, get_args, get_origin

    origin = get_origin(python_type)

    if origin is Optional or (origin is Union and type(None) in get_args(python_type)):
        # Handle Optional types
        args = get_args(python_type)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return _python_type_to_polars(non_none_args[0])
        return pl.Utf8

    if origin is list:
        # Handle List types
        args = get_args(python_type)
        if args:
            element_type = _python_type_to_polars(args[0])
            return pl.List(element_type)
        return pl.List(pl.Utf8)

    # Handle base types
    if python_type is str:
        return pl.Utf8
    elif python_type is int:
        return pl.Int64
    elif python_type is float:
        return pl.Float64
    elif python_type is bool:
        return pl.Boolean
    elif python_type is date:
        return pl.Date
    elif python_type is datetime:
        return pl.Datetime
    else:
        return pl.Utf8  # Default to string


def from_polars(polars_obj: Union[pl.DataFrame, pl.Schema], target_type: str = "pydantic") -> Any:
    """
    Convert Polars DataFrame or Schema to another schema type.

    Args:
        polars_obj: Polars DataFrame or Schema
        target_type: Target schema type ('pydantic', 'dataclass', 'typedict', etc.)

    Returns:
        Converted schema or data
    """
    _check_polars()

    if target_type == "pydantic":
        from lugia.pydantic import to_pydantic

        return to_pydantic(polars_obj)
    elif target_type == "dataclass":
        from lugia.dataclass import to_dataclass

        return to_dataclass(polars_obj)
    elif target_type == "typedict":
        from lugia.typedict import to_typeddict

        return to_typeddict(polars_obj)
    elif target_type == "pandas":
        from lugia.pandas import to_pandas

        return to_pandas(polars_obj)
    elif target_type == "pyspark":
        from lugia.pyspark import to_pyspark

        return to_pyspark(polars_obj)
    else:
        raise ValueError(f"Unsupported target type: {target_type}")
