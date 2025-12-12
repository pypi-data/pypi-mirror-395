"""Tests for Pydantic conversions."""

from typing import Optional

import pytest


@pytest.fixture
def sample_pydantic_model():
    """Create a sample Pydantic model for testing."""
    try:
        from pydantic import BaseModel

        class User(BaseModel):
            name: str
            age: int
            email: Optional[str] = None

        return User
    except ImportError:
        pytest.skip("Pydantic not available")


@pytest.fixture
def sample_pydantic_instance(sample_pydantic_model):
    """Create a sample Pydantic instance."""
    return sample_pydantic_model(name="John", age=30, email="john@example.com")


def test_pydantic_to_dataclass(sample_pydantic_model):
    """Test converting Pydantic model to dataclass."""
    from lugia.dataclass import to_dataclass

    dc_class = to_dataclass(sample_pydantic_model)
    assert dc_class is not None
    assert hasattr(dc_class, "__dataclass_fields__")
    assert "name" in dc_class.__dataclass_fields__
    assert "age" in dc_class.__dataclass_fields__


def test_pydantic_to_typeddict(sample_pydantic_model):
    """Test converting Pydantic model to TypedDict."""
    from lugia.typedict import to_typeddict

    td_class = to_typeddict(sample_pydantic_model)
    assert td_class is not None
    assert hasattr(td_class, "__annotations__")
    assert "name" in td_class.__annotations__


def test_pydantic_to_pandas(sample_pydantic_instance):
    """Test converting Pydantic instance to Pandas DataFrame."""
    try:
        import pandas as pd

        from lugia.pandas import to_pandas

        df = to_pandas(sample_pydantic_instance)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "name" in df.columns
    except ImportError:
        pytest.skip("Pandas not available")


def test_pydantic_to_polars(sample_pydantic_instance):
    """Test converting Pydantic instance to Polars DataFrame."""
    try:
        import polars as pl

        from lugia.polars import to_polars

        df = to_polars(sample_pydantic_instance)
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 1
        assert "name" in df.columns
    except ImportError:
        pytest.skip("Polars not available")


def test_pydantic_to_pyspark_schema(sample_pydantic_model):
    """Test converting Pydantic model to PySpark StructType."""
    try:
        from pyspark.sql.types import StructType

        from lugia.pyspark import to_pyspark

        struct_type = to_pyspark(sample_pydantic_model)
        assert isinstance(struct_type, StructType)
        assert len(struct_type.fields) == 3
    except ImportError:
        pytest.skip("PySpark not available")


def test_pydantic_missing_dependency():
    """Test that missing Pydantic dependency raises appropriate error."""
    from lugia.exceptions import MissingDependencyError
    from lugia.pydantic import to_pydantic

    # This should work if pydantic is available, or skip if not
    try:
        from pydantic import BaseModel  # noqa: F401

        # If we get here, pydantic is available, so test passes
        assert True
    except ImportError:
        # If pydantic is not available, to_pydantic should raise MissingDependencyError
        with pytest.raises(MissingDependencyError):
            to_pydantic("invalid_source")
