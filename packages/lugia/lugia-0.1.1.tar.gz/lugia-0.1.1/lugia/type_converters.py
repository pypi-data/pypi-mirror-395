"""Centralized type conversion utilities for converting between Python types and external library types.

This module provides functions to convert types between Python's type system and
external libraries like PySpark, Polars, Pandas, and SQLAlchemy. These functions
are used by all converter modules to avoid code duplication.
"""

from typing import Any, Optional, Union, get_args, get_origin


def pyspark_type_to_python(spark_type: Any) -> type:
    """Convert PySpark type to Python type.

    Args:
        spark_type: A PySpark DataType instance (e.g., StringType, IntegerType)

    Returns:
        The corresponding Python type (e.g., str, int, float)

    Examples:
        >>> from pyspark.sql.types import StringType, IntegerType
        >>> pyspark_type_to_python(StringType())
        <class 'str'>
        >>> pyspark_type_to_python(IntegerType())
        <class 'int'>
    """
    from datetime import date, datetime
    from typing import Any

    try:
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
            StructType,
            TimestampType,
        )
    except ImportError as e:
        raise ImportError("PySpark is required for PySpark type conversions") from e

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
    elif isinstance(spark_type, ArrayType):
        element_type = pyspark_type_to_python(spark_type.elementType)
        # Construct list type dynamically
        return list[element_type]  # type: ignore[valid-type]
    elif isinstance(spark_type, MapType):
        key_type = pyspark_type_to_python(spark_type.keyType)
        value_type = pyspark_type_to_python(spark_type.valueType)
        return dict[key_type, value_type]  # type: ignore[valid-type]
    elif isinstance(spark_type, StructType):
        # For nested structs, we'd need to create a nested model
        return dict[str, Any]
    else:
        return Any


def polars_type_to_python(dtype: Any) -> type:
    """Convert Polars dtype to Python type.

    Args:
        dtype: A Polars DataType instance (e.g., pl.Utf8, pl.Int64)

    Returns:
        The corresponding Python type (e.g., str, int, float)

    Examples:
        >>> import polars as pl
        >>> polars_type_to_python(pl.Utf8)
        <class 'str'>
        >>> polars_type_to_python(pl.Int64)
        <class 'int'>
    """
    from datetime import date, datetime
    from typing import Any

    try:
        import polars as pl
    except ImportError as e:
        raise ImportError("Polars is required for Polars type conversions") from e

    if dtype == pl.Utf8 or dtype == pl.String:
        return str
    elif dtype == pl.Int64 or dtype == pl.Int32:
        return int
    elif dtype == pl.Float64 or dtype == pl.Float32:
        return float
    elif dtype == pl.Boolean:
        return bool
    elif dtype == pl.Date:
        return date
    elif dtype == pl.Datetime:
        return datetime
    elif isinstance(dtype, pl.List):
        element_type = polars_type_to_python(dtype.inner)
        return list[element_type]  # type: ignore[valid-type]
    elif isinstance(dtype, pl.Struct):
        return dict[str, Any]
    else:
        return Any


def pandas_type_to_python(dtype: Any) -> type:
    """Convert Pandas dtype to Python type.

    Args:
        dtype: A Pandas dtype (e.g., 'int64', 'float64', 'object')

    Returns:
        The corresponding Python type (e.g., int, float, str)

    Examples:
        >>> import pandas as pd
        >>> pandas_type_to_python(pd.Int64Dtype())
        <class 'int'>
        >>> pandas_type_to_python('float64')
        <class 'float'>
    """
    from datetime import datetime
    from typing import Any

    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError("Pandas is required for Pandas type conversions") from e

    if pd.api.types.is_integer_dtype(dtype):
        return int
    elif pd.api.types.is_float_dtype(dtype):
        return float
    elif pd.api.types.is_bool_dtype(dtype):
        return bool
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return datetime
    elif pd.api.types.is_object_dtype(dtype):
        return Any
    else:
        return str


def sqlalchemy_type_to_python(sa_type: Any) -> type:
    """Convert SQLAlchemy type to Python type.

    Args:
        sa_type: A SQLAlchemy TypeEngine instance (e.g., String, Integer)

    Returns:
        The corresponding Python type (e.g., str, int, float)

    Examples:
        >>> from sqlalchemy import String, Integer
        >>> sqlalchemy_type_to_python(String())
        <class 'str'>
        >>> sqlalchemy_type_to_python(Integer())
        <class 'int'>
    """
    from datetime import date, datetime
    from typing import Any

    try:
        from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Text
    except ImportError as e:
        raise ImportError("SQLAlchemy is required for SQLAlchemy type conversions") from e

    # Get the Python type from SQLAlchemy type
    try:
        return sa_type.python_type  # type: ignore[no-any-return]
    except AttributeError:
        # Fallback for types without python_type
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
            return Any  # type: ignore[no-any-return]


def python_type_to_pyspark(python_type: Any) -> Any:
    """Convert Python type hint to PySpark type.

    Args:
        python_type: A Python type or type hint (e.g., str, int, Optional[str])

    Returns:
        A PySpark DataType instance (e.g., StringType, IntegerType)

    Examples:
        >>> python_type_to_pyspark(str)
        StringType()
        >>> python_type_to_pyspark(int)
        LongType()
    """
    from datetime import date, datetime

    try:
        from pyspark.sql.types import (
            ArrayType,
            BooleanType,
            DateType,
            DoubleType,
            LongType,
            MapType,
            StringType,
            TimestampType,
        )
    except ImportError as e:
        raise ImportError("PySpark is required for Python to PySpark type conversions") from e

    origin = get_origin(python_type)

    if origin is Optional or (origin is Union and type(None) in get_args(python_type)):
        # Handle Optional types - use the non-None type
        args = get_args(python_type)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return python_type_to_pyspark(non_none_args[0])
        return StringType()

    if origin is list:
        # Handle List types
        args = get_args(python_type)
        if args:
            element_type = python_type_to_pyspark(args[0])
            return ArrayType(element_type)
        return ArrayType(StringType())

    if origin is dict:
        # Handle Dict types
        args = get_args(python_type)
        if len(args) >= 2:
            key_type = python_type_to_pyspark(args[0])
            value_type = python_type_to_pyspark(args[1])
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


def python_type_to_polars(python_type: Any) -> Any:  # type: ignore[no-any-return]
    """Convert Python type hint to Polars type.

    Args:
        python_type: A Python type or type hint (e.g., str, int, Optional[str])

    Returns:
        A Polars DataType instance (e.g., pl.Utf8, pl.Int64)

    Examples:
        >>> python_type_to_polars(str)
        Utf8
        >>> python_type_to_polars(int)
        Int64
    """
    from datetime import date, datetime

    try:
        import polars as pl
    except ImportError as e:
        raise ImportError("Polars is required for Python to Polars type conversions") from e

    origin = get_origin(python_type)

    if origin is Optional or (origin is Union and type(None) in get_args(python_type)):
        # Handle Optional types
        args = get_args(python_type)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return python_type_to_polars(non_none_args[0])
        return pl.Utf8

    if origin is list:
        # Handle List types
        args = get_args(python_type)
        if args:
            element_type = python_type_to_polars(args[0])
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


def python_type_to_sqlalchemy(python_type: Any) -> Any:  # type: ignore[no-any-return]
    """Convert Python type hint to SQLAlchemy type.

    Args:
        python_type: A Python type or type hint (e.g., str, int, Optional[str])

    Returns:
        A SQLAlchemy TypeEngine instance (e.g., String, Integer)

    Examples:
        >>> python_type_to_sqlalchemy(str)
        String()
        >>> python_type_to_sqlalchemy(int)
        Integer()
    """
    from datetime import date, datetime

    try:
        from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String
    except ImportError as e:
        raise ImportError("SQLAlchemy is required for Python to SQLAlchemy type conversions") from e

    origin = get_origin(python_type)

    if origin is Optional or (origin is Union and type(None) in get_args(python_type)):
        # Handle Optional types
        args = get_args(python_type)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return python_type_to_sqlalchemy(non_none_args[0])
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


def pyspark_type_to_polars(spark_type: Any) -> Any:  # type: ignore[no-any-return]
    """Convert PySpark type to Polars type.

    Args:
        spark_type: A PySpark DataType instance

    Returns:
        A Polars DataType instance

    Examples:
        >>> from pyspark.sql.types import StringType, IntegerType
        >>> pyspark_type_to_polars(StringType())
        Utf8
        >>> pyspark_type_to_polars(IntegerType())
        Int32
    """
    try:
        import polars as pl
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
    except ImportError as e:
        raise ImportError(f"Required library not available: {e}") from e

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
        element_type = pyspark_type_to_polars(spark_type.elementType)
        return pl.List(element_type)
    else:
        return pl.Utf8  # Default
