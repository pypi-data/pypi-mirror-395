"""PySpark StructType and DataFrame conversions."""

from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from pyspark.sql import DataFrame as SparkDataFrame
    from pyspark.sql import SparkSession
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
        StructField,
        StructType,
        TimestampType,
    )
else:
    SparkSession = None  # type: ignore
    SparkDataFrame = None  # type: ignore
    StructType = None  # type: ignore
    StructField = None  # type: ignore
    StringType = None  # type: ignore
    IntegerType = None  # type: ignore
    LongType = None  # type: ignore
    FloatType = None  # type: ignore
    DoubleType = None  # type: ignore
    BooleanType = None  # type: ignore
    DateType = None  # type: ignore
    TimestampType = None  # type: ignore
    ArrayType = None  # type: ignore
    MapType = None  # type: ignore

from lugia.exceptions import MissingDependencyError
from lugia.utils import (
    is_dataclass,
    is_pydantic_instance,
    is_pydantic_model,
)

try:
    from pyspark.sql import DataFrame as SparkDataFrame
    from pyspark.sql import SparkSession  # noqa: F401
    from pyspark.sql.types import (  # noqa: F401
        ArrayType,
        BooleanType,
        DateType,
        DoubleType,
        FloatType,
        IntegerType,
        LongType,
        MapType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )

    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False


def _check_pyspark():
    """Check if PySpark is available."""
    if not PYSPARK_AVAILABLE:
        raise MissingDependencyError("pyspark", "PySpark conversions")


def to_pyspark(
    source: Any, spark_session: Optional[SparkSession] = None
) -> Union[StructType, SparkDataFrame]:
    """
    Convert a schema or data object to PySpark StructType or DataFrame.

    Args:
        source: Source schema or data
        spark_session: Optional SparkSession (required for DataFrame conversion)

    Returns:
        PySpark StructType or DataFrame
    """
    _check_pyspark()

    # If already PySpark, return as-is
    if isinstance(source, StructType):
        return source
    if isinstance(source, SparkDataFrame):
        return source

    # Handle Pydantic
    if is_pydantic_model(source) or is_pydantic_instance(source):
        return _pydantic_to_pyspark(source, spark_session)

    # Handle dataclass
    if is_dataclass(source):
        return _dataclass_to_pyspark(source, spark_session)

    # Handle list of dicts or instances
    if isinstance(source, list):
        if source and isinstance(source[0], dict):
            if spark_session is None:
                raise ValueError("spark_session is required for DataFrame conversion")
            return _dicts_to_pyspark(source, spark_session)
        elif source and (is_pydantic_instance(source[0]) or is_dataclass(source[0])):
            if spark_session is None:
                raise ValueError("spark_session is required for DataFrame conversion")
            return _instances_to_pyspark(source, spark_session)

    # Handle Polars
    try:
        import polars as pl

        if isinstance(source, pl.DataFrame):
            if spark_session is None:
                raise ValueError("spark_session is required for DataFrame conversion")
            return _polars_to_pyspark(source, spark_session)
        if isinstance(source, pl.Schema):
            return _polars_schema_to_pyspark(source)
    except ImportError:
        pass

    # Handle Pandas
    try:
        import pandas as pd

        if isinstance(source, pd.DataFrame):
            if spark_session is None:
                raise ValueError("spark_session is required for DataFrame conversion")
            return _pandas_to_pyspark(source, spark_session)
    except ImportError:
        pass

    # Handle dict
    if isinstance(source, dict):
        if spark_session is None:
            raise ValueError("spark_session is required for DataFrame conversion")
        return _dicts_to_pyspark([source], spark_session)

    raise ValueError(f"Cannot convert {type(source)} to PySpark")


def _pydantic_to_pyspark(
    source: Any,
    spark_session: Optional[SparkSession] = None,  # type: ignore
) -> Union[StructType, SparkDataFrame]:  # type: ignore
    """Convert Pydantic model or instance to PySpark."""
    try:
        from pydantic import BaseModel
    except ImportError:
        raise MissingDependencyError("pydantic", "Pydantic to PySpark conversion") from None

    if isinstance(source, type) and issubclass(source, BaseModel):
        # Schema only - return StructType
        fields = []
        for field_name, field_info in source.model_fields.items():
            spark_type = _python_type_to_pyspark(field_info.annotation)
            nullable = True  # Pydantic fields can be optional
            fields.append(StructField(field_name, spark_type, nullable=nullable))
        return StructType(fields)
    else:
        # Instance - convert to DataFrame
        if spark_session is None:
            raise ValueError("spark_session is required for DataFrame conversion")
        data = source.model_dump() if hasattr(source, "model_dump") else source.dict()
        return spark_session.createDataFrame([data])  # type: ignore


def _dataclass_to_pyspark(
    source: Any,
    spark_session: Optional[SparkSession] = None,  # type: ignore
) -> Union[StructType, SparkDataFrame]:  # type: ignore
    """Convert dataclass to PySpark."""
    import dataclasses
    from typing import get_type_hints

    if isinstance(source, type):
        # Schema only
        fields = []
        hints = get_type_hints(source)
        for field in dataclasses.fields(source):
            field_type = hints.get(field.name, Any)
            spark_type = _python_type_to_pyspark(field_type)
            nullable = (
                field.default != dataclasses.MISSING or field.default_factory != dataclasses.MISSING
            )
            fields.append(StructField(field.name, spark_type, nullable=nullable))
        return StructType(fields)
    else:
        # Instance
        if spark_session is None:
            raise ValueError("spark_session is required for DataFrame conversion")
        data = dataclasses.asdict(source)
        return spark_session.createDataFrame([data])  # type: ignore


def _instances_to_pyspark(
    instances: list[Any],
    spark_session: SparkSession,  # type: ignore
) -> SparkDataFrame:  # type: ignore
    """Convert list of instances to PySpark DataFrame."""
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
    return spark_session.createDataFrame(rows)  # type: ignore


def _dicts_to_pyspark(dicts: list[dict], spark_session: SparkSession) -> SparkDataFrame:  # type: ignore
    """Convert list of dicts to PySpark DataFrame."""
    return spark_session.createDataFrame(dicts)  # type: ignore


def _polars_to_pyspark(polars_df: Any, spark_session: SparkSession) -> SparkDataFrame:  # type: ignore
    """Convert Polars DataFrame to PySpark DataFrame."""
    try:
        import polars as pl  # noqa: F401
    except ImportError:
        raise MissingDependencyError("polars", "Polars to PySpark conversion") from None

    # Convert to Pandas first, then to PySpark
    pandas_df = polars_df.to_pandas()
    return spark_session.createDataFrame(pandas_df)  # type: ignore


def _polars_schema_to_pyspark(schema: Any) -> StructType:  # type: ignore
    """Convert Polars Schema to PySpark StructType."""
    fields = []
    for name, dtype in schema.items():
        spark_type = _polars_type_to_pyspark(dtype)
        fields.append(StructField(name, spark_type, nullable=True))
    return StructType(fields)


def _polars_type_to_pyspark(dtype: Any) -> Any:
    """Convert Polars type to PySpark type."""
    import polars as pl

    if dtype == pl.Utf8 or dtype == pl.String:
        return StringType()
    elif dtype == pl.Int64:
        return LongType()
    elif dtype == pl.Int32:
        return IntegerType()
    elif dtype == pl.Float64:
        return DoubleType()
    elif dtype == pl.Float32:
        return FloatType()
    elif dtype == pl.Boolean:
        return BooleanType()
    elif dtype == pl.Date:
        return DateType()
    elif dtype == pl.Datetime:
        return TimestampType()
    elif isinstance(dtype, pl.List):
        element_type = _polars_type_to_pyspark(dtype.inner)
        return ArrayType(element_type)
    else:
        return StringType()  # Default


def _pandas_to_pyspark(pandas_df: Any, spark_session: SparkSession) -> SparkDataFrame:  # type: ignore
    """Convert Pandas DataFrame to PySpark DataFrame."""
    try:
        import pandas as pd  # noqa: F401
    except ImportError:
        raise MissingDependencyError("pandas", "Pandas to PySpark conversion") from None

    # Convert pandas DataFrame to list of dicts to avoid compatibility issues
    # with PySpark 3.2.0 and pandas 2.x (iteritems() removed)
    data = pandas_df.to_dict("records")
    return spark_session.createDataFrame(data)  # type: ignore


def _python_type_to_pyspark(python_type: Any) -> Any:
    """Convert Python type hint to PySpark type."""
    from datetime import date, datetime
    from typing import Union, get_args, get_origin

    origin = get_origin(python_type)

    if origin is Optional or (origin is Union and type(None) in get_args(python_type)):
        # Handle Optional types - use the non-None type
        args = get_args(python_type)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return _python_type_to_pyspark(non_none_args[0])
        return StringType()

    if origin is list:
        # Handle List types
        args = get_args(python_type)
        if args:
            element_type = _python_type_to_pyspark(args[0])
            return ArrayType(element_type)
        return ArrayType(StringType())

    if origin is dict:
        # Handle Dict types
        args = get_args(python_type)
        if len(args) >= 2:
            key_type = _python_type_to_pyspark(args[0])
            value_type = _python_type_to_pyspark(args[1])
            return MapType(key_type, value_type)
        return MapType(StringType(), StringType())

    # Handle base types
    if python_type is str:
        return StringType()
    elif python_type is int:
        return LongType()
    elif python_type is float:
        return DoubleType()
    elif python_type is bool:
        return BooleanType()
    elif python_type is date:
        return DateType()
    elif python_type is datetime:
        return TimestampType()
    else:
        return StringType()  # Default to string


def from_pyspark(
    pyspark_obj: Union[StructType, SparkDataFrame], target_type: str = "pydantic"
) -> Any:
    """
    Convert PySpark StructType or DataFrame to another schema type.

    Args:
        pyspark_obj: PySpark StructType or DataFrame
        target_type: Target schema type ('pydantic', 'dataclass', 'typedict', etc.)

    Returns:
        Converted schema or data
    """
    _check_pyspark()

    if target_type == "pydantic":
        from lugia.pydantic import to_pydantic

        return to_pydantic(pyspark_obj)
    elif target_type == "dataclass":
        from lugia.dataclass import to_dataclass

        return to_dataclass(pyspark_obj)
    elif target_type == "typedict":
        from lugia.typedict import to_typeddict

        return to_typeddict(pyspark_obj)
    elif target_type == "pandas":
        from lugia.pandas import to_pandas

        return to_pandas(pyspark_obj)
    elif target_type == "polars":
        from lugia.polars import to_polars

        return to_polars(pyspark_obj)
    else:
        raise ValueError(f"Unsupported target type: {target_type}")
