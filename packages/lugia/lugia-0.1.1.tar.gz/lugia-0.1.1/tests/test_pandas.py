"""Tests for Pandas conversions."""

import pytest


@pytest.fixture
def sample_pandas_df():
    """Create a sample Pandas DataFrame for testing."""
    try:
        import pandas as pd

        return pd.DataFrame(
            {
                "name": ["John", "Jane"],
                "age": [30, 25],
                "email": ["john@example.com", "jane@example.com"],
            }
        )
    except ImportError:
        pytest.skip("Pandas not available")


def test_pandas_to_pydantic(sample_pandas_df):
    """Test converting Pandas DataFrame to Pydantic model."""
    try:
        from pydantic import BaseModel

        from lugia.pydantic import to_pydantic

        pydantic_model = to_pydantic(sample_pandas_df)
        assert pydantic_model is not None
        assert issubclass(pydantic_model, BaseModel)
    except ImportError:
        pytest.skip("Pydantic not available")


def test_pandas_to_dataclass(sample_pandas_df):
    """Test converting Pandas DataFrame to dataclass."""
    from lugia.dataclass import to_dataclass

    dc_class = to_dataclass(sample_pandas_df)
    assert dc_class is not None
    assert hasattr(dc_class, "__dataclass_fields__")
    assert "name" in dc_class.__dataclass_fields__


def test_pandas_to_polars(sample_pandas_df):
    """Test converting Pandas DataFrame to Polars DataFrame."""
    try:
        import polars as pl

        from lugia.polars import to_polars

        polars_df = to_polars(sample_pandas_df)
        assert isinstance(polars_df, pl.DataFrame)
        assert len(polars_df) == 2
        assert "name" in polars_df.columns
    except ImportError:
        pytest.skip("Polars not available")


def test_pandas_to_pyspark(sample_pandas_df, spark_session):
    """Test converting Pandas DataFrame to PySpark DataFrame."""
    try:
        from lugia.pyspark import to_pyspark

        spark_df = to_pyspark(sample_pandas_df, spark_session=spark_session)
        assert spark_df is not None
        assert spark_df.count() == 2
    except ImportError:
        pytest.skip("PySpark not available")


def test_pandas_missing_dependency():
    """Test that missing Pandas dependency raises appropriate error."""
    from lugia.exceptions import MissingDependencyError
    from lugia.pandas import to_pandas

    try:
        import pandas as pd  # noqa: F401

        # If we get here, pandas is available
        assert True
    except ImportError:
        with pytest.raises(MissingDependencyError):
            to_pandas("invalid_source")
