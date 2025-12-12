"""Tests for dataclass conversions."""

import dataclasses
from typing import Optional

import pytest


@pytest.fixture
def sample_dataclass():
    """Create a sample dataclass for testing."""

    @dataclasses.dataclass
    class User:
        name: str
        age: int
        email: Optional[str] = None

    return User


@pytest.fixture
def sample_dataclass_instance(sample_dataclass):
    """Create a sample dataclass instance."""
    return sample_dataclass(name="John", age=30, email="john@example.com")


def test_dataclass_to_pydantic(sample_dataclass):
    """Test converting dataclass to Pydantic model."""
    try:
        from pydantic import BaseModel

        from lugia.pydantic import to_pydantic

        pydantic_model = to_pydantic(sample_dataclass)
        assert pydantic_model is not None
        assert issubclass(pydantic_model, BaseModel)
    except ImportError:
        pytest.skip("Pydantic not available")


def test_dataclass_to_typeddict(sample_dataclass):
    """Test converting dataclass to TypedDict."""
    from lugia.typedict import to_typeddict

    td_class = to_typeddict(sample_dataclass)
    assert td_class is not None
    assert hasattr(td_class, "__annotations__")
    assert "name" in td_class.__annotations__


def test_dataclass_to_pandas(sample_dataclass_instance):
    """Test converting dataclass instance to Pandas DataFrame."""
    try:
        import pandas as pd

        from lugia.pandas import to_pandas

        df = to_pandas(sample_dataclass_instance)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "name" in df.columns
    except ImportError:
        pytest.skip("Pandas not available")


def test_dataclass_to_polars(sample_dataclass_instance):
    """Test converting dataclass instance to Polars DataFrame."""
    try:
        import polars as pl

        from lugia.polars import to_polars

        df = to_polars(sample_dataclass_instance)
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 1
        assert "name" in df.columns
    except ImportError:
        pytest.skip("Polars not available")


def test_dataclass_to_pyspark_schema(sample_dataclass):
    """Test converting dataclass to PySpark StructType."""
    try:
        from pyspark.sql.types import StructType

        from lugia.pyspark import to_pyspark

        struct_type = to_pyspark(sample_dataclass)
        assert isinstance(struct_type, StructType)
        assert len(struct_type.fields) == 3
    except ImportError:
        pytest.skip("PySpark not available")
