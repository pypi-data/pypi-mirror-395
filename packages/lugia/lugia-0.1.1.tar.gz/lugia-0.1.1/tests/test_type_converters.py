"""Tests for centralized type converter functions."""

import pytest


def test_pyspark_type_to_python():
    """Test PySpark type to Python type conversion."""
    try:
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

        from lugia.type_converters import pyspark_type_to_python

        assert pyspark_type_to_python(StringType()) is str
        assert pyspark_type_to_python(IntegerType()) is int
        assert pyspark_type_to_python(LongType()) is int
        assert pyspark_type_to_python(FloatType()) is float
        assert pyspark_type_to_python(DoubleType()) is float
        assert pyspark_type_to_python(BooleanType()) is bool
        assert pyspark_type_to_python(DateType()).__name__ == "date"
        assert pyspark_type_to_python(TimestampType()).__name__ == "datetime"
    except ImportError:
        pytest.skip("PySpark not available")


def test_polars_type_to_python():
    """Test Polars type to Python type conversion."""
    try:
        import polars as pl

        from lugia.type_converters import polars_type_to_python

        assert polars_type_to_python(pl.Utf8) is str
        assert polars_type_to_python(pl.String) is str
        assert polars_type_to_python(pl.Int64) is int
        assert polars_type_to_python(pl.Int32) is int
        assert polars_type_to_python(pl.Float64) is float
        assert polars_type_to_python(pl.Float32) is float
        assert polars_type_to_python(pl.Boolean) is bool
        assert polars_type_to_python(pl.Date).__name__ == "date"
        assert polars_type_to_python(pl.Datetime).__name__ == "datetime"
    except ImportError:
        pytest.skip("Polars not available")


def test_pandas_type_to_python():
    """Test Pandas type to Python type conversion."""
    try:
        from typing import Any

        import pandas as pd

        from lugia.type_converters import pandas_type_to_python

        assert pandas_type_to_python("int64") is int
        assert pandas_type_to_python("float64") is float
        assert pandas_type_to_python("bool") is bool
        assert pandas_type_to_python("object") is Any  # Object dtype returns Any
        assert pandas_type_to_python(pd.Int64Dtype()) is int
    except ImportError:
        pytest.skip("Pandas not available")


def test_sqlalchemy_type_to_python():
    """Test SQLAlchemy type to Python type conversion."""
    try:
        from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String

        from lugia.type_converters import sqlalchemy_type_to_python

        assert sqlalchemy_type_to_python(String()) is str
        assert sqlalchemy_type_to_python(Integer()) is int
        assert sqlalchemy_type_to_python(Float()) is float
        assert sqlalchemy_type_to_python(Boolean()) is bool
        assert sqlalchemy_type_to_python(Date()).__name__ == "date"
        assert sqlalchemy_type_to_python(DateTime()).__name__ == "datetime"
    except ImportError:
        pytest.skip("SQLAlchemy not available")


def test_python_type_to_pyspark():
    """Test Python type to PySpark type conversion."""
    try:
        from datetime import date, datetime

        from pyspark.sql.types import (
            BooleanType,
            DateType,
            DoubleType,
            LongType,
            StringType,
            TimestampType,
        )

        from lugia.type_converters import python_type_to_pyspark

        assert isinstance(python_type_to_pyspark(str), StringType)
        assert isinstance(python_type_to_pyspark(int), LongType)
        assert isinstance(python_type_to_pyspark(float), DoubleType)
        assert isinstance(python_type_to_pyspark(bool), BooleanType)
        assert isinstance(python_type_to_pyspark(date), DateType)
        assert isinstance(python_type_to_pyspark(datetime), TimestampType)
    except ImportError:
        pytest.skip("PySpark not available")


def test_python_type_to_polars():
    """Test Python type to Polars type conversion."""
    try:
        from datetime import date, datetime

        import polars as pl

        from lugia.type_converters import python_type_to_polars

        assert python_type_to_polars(str) == pl.Utf8
        assert python_type_to_polars(int) == pl.Int64
        assert python_type_to_polars(float) == pl.Float64
        assert python_type_to_polars(bool) == pl.Boolean
        assert python_type_to_polars(date) == pl.Date
        assert python_type_to_polars(datetime) == pl.Datetime
    except ImportError:
        pytest.skip("Polars not available")


def test_python_type_to_sqlalchemy():
    """Test Python type to SQLAlchemy type conversion."""
    try:
        from datetime import date, datetime

        from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String

        from lugia.type_converters import python_type_to_sqlalchemy

        assert isinstance(python_type_to_sqlalchemy(str), String)
        assert isinstance(python_type_to_sqlalchemy(int), Integer)
        assert isinstance(python_type_to_sqlalchemy(float), Float)
        assert isinstance(python_type_to_sqlalchemy(bool), Boolean)
        assert isinstance(python_type_to_sqlalchemy(date), Date)
        assert isinstance(python_type_to_sqlalchemy(datetime), DateTime)
    except ImportError:
        pytest.skip("SQLAlchemy not available")


def test_python_type_to_pyspark_optional():
    """Test Python Optional type to PySpark conversion."""
    try:
        from typing import Optional

        from pyspark.sql.types import StringType

        from lugia.type_converters import python_type_to_pyspark

        # Optional[str] should convert to StringType (non-None type)
        result = python_type_to_pyspark(Optional[str])
        assert isinstance(result, StringType)
    except ImportError:
        pytest.skip("PySpark not available")


def test_python_type_to_polars_optional():
    """Test Python Optional type to Polars conversion."""
    try:
        from typing import Optional

        import polars as pl

        from lugia.type_converters import python_type_to_polars

        # Optional[str] should convert to pl.Utf8 (non-None type)
        result = python_type_to_polars(Optional[str])
        assert result == pl.Utf8
    except ImportError:
        pytest.skip("Polars not available")


def test_pyspark_type_to_polars():
    """Test PySpark type to Polars type conversion."""
    try:
        import polars as pl
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

        from lugia.type_converters import pyspark_type_to_polars

        assert pyspark_type_to_polars(StringType()) == pl.Utf8
        assert pyspark_type_to_polars(IntegerType()) == pl.Int32
        assert pyspark_type_to_polars(LongType()) == pl.Int64
        assert pyspark_type_to_polars(FloatType()) == pl.Float32
        assert pyspark_type_to_polars(DoubleType()) == pl.Float64
        assert pyspark_type_to_polars(BooleanType()) == pl.Boolean
        assert pyspark_type_to_polars(DateType()) == pl.Date
        assert pyspark_type_to_polars(TimestampType()) == pl.Datetime
    except ImportError:
        pytest.skip("PySpark or Polars not available")
