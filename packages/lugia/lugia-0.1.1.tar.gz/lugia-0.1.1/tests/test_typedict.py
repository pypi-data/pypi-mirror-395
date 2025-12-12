"""Tests for TypedDict conversions."""

from typing import Optional, TypedDict

import pytest


@pytest.fixture
def sample_typeddict():
    """Create a sample TypedDict for testing."""

    class User(TypedDict):
        name: str
        age: int
        email: Optional[str]

    return User


def test_typeddict_to_pydantic(sample_typeddict):
    """Test converting TypedDict to Pydantic model."""
    try:
        from pydantic import BaseModel

        from lugia.pydantic import to_pydantic

        pydantic_model = to_pydantic(sample_typeddict)
        assert pydantic_model is not None
        assert issubclass(pydantic_model, BaseModel)
    except ImportError:
        pytest.skip("Pydantic not available")


def test_typeddict_to_dataclass(sample_typeddict):
    """Test converting TypedDict to dataclass."""
    from lugia.dataclass import to_dataclass

    dc_class = to_dataclass(sample_typeddict)
    assert dc_class is not None
    assert hasattr(dc_class, "__dataclass_fields__")
    assert "name" in dc_class.__dataclass_fields__


def test_typeddict_to_pandas(sample_typeddict):
    """Test converting TypedDict to Pandas DataFrame schema."""
    try:
        import pandas as pd

        from lugia.pandas import to_pandas

        # TypedDict is a schema, so we get an empty DataFrame
        df = to_pandas(sample_typeddict)
        assert isinstance(df, pd.DataFrame)
        assert "name" in df.columns
    except ImportError:
        pytest.skip("Pandas not available")
