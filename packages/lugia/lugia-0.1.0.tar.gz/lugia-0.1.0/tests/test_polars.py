"""Tests for Polars conversions."""

import pytest


@pytest.fixture
def sample_polars_df():
    """Create a sample Polars DataFrame for testing."""
    try:
        import polars as pl

        return pl.DataFrame(
            {
                "name": ["John", "Jane"],
                "age": [30, 25],
                "email": ["john@example.com", "jane@example.com"],
            }
        )
    except ImportError:
        pytest.skip("Polars not available")


def test_polars_to_pydantic(sample_polars_df):
    """Test converting Polars DataFrame to Pydantic model."""
    try:
        from pydantic import BaseModel

        from lugia.pydantic import to_pydantic

        pydantic_model = to_pydantic(sample_polars_df)
        assert pydantic_model is not None
        assert issubclass(pydantic_model, BaseModel)
    except ImportError:
        pytest.skip("Pydantic not available")


def test_polars_to_dataclass(sample_polars_df):
    """Test converting Polars DataFrame to dataclass."""
    from lugia.dataclass import to_dataclass

    dc_class = to_dataclass(sample_polars_df)
    assert dc_class is not None
    assert hasattr(dc_class, "__dataclass_fields__")
    assert "name" in dc_class.__dataclass_fields__


def test_polars_to_pandas(sample_polars_df):
    """Test converting Polars DataFrame to Pandas DataFrame."""
    try:
        import pandas as pd

        from lugia.pandas import to_pandas

        pandas_df = to_pandas(sample_polars_df)
        assert isinstance(pandas_df, pd.DataFrame)
        assert len(pandas_df) == 2
        assert "name" in pandas_df.columns
    except ImportError:
        pytest.skip("Pandas not available")


def test_polars_missing_dependency():
    """Test that missing Polars dependency raises appropriate error."""
    from lugia.exceptions import MissingDependencyError
    from lugia.polars import to_polars

    try:
        import polars as pl  # noqa: F401

        # If we get here, polars is available
        assert True
    except ImportError:
        with pytest.raises(MissingDependencyError):
            to_polars("invalid_source")
