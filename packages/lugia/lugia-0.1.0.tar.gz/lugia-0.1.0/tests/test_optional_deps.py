"""Tests for optional dependency handling."""

import pytest

from lugia.exceptions import MissingDependencyError


def test_missing_pydantic_error():
    """Test that missing Pydantic dependency raises informative error."""
    from lugia.pydantic import PYDANTIC_AVAILABLE, MissingDependencyError

    if not PYDANTIC_AVAILABLE:
        with pytest.raises(MissingDependencyError) as exc_info:
            from lugia.pydantic import to_pydantic

            to_pydantic("test")

        assert "pydantic" in str(exc_info.value).lower()
        assert "pip install" in str(exc_info.value).lower()


def test_missing_pandas_error():
    """Test that missing Pandas dependency raises informative error."""
    from lugia.pandas import PANDAS_AVAILABLE

    if not PANDAS_AVAILABLE:
        with pytest.raises(MissingDependencyError) as exc_info:
            from lugia.pandas import to_pandas

            to_pandas("test")

        assert "pandas" in str(exc_info.value).lower()


def test_missing_polars_error():
    """Test that missing Polars dependency raises informative error."""
    from lugia.polars import POLARS_AVAILABLE

    if not POLARS_AVAILABLE:
        with pytest.raises(MissingDependencyError) as exc_info:
            from lugia.polars import to_polars

            to_polars("test")

        assert "polars" in str(exc_info.value).lower()


def test_missing_pyspark_error():
    """Test that missing PySpark dependency raises informative error."""
    from lugia.pyspark import PYSPARK_AVAILABLE

    if not PYSPARK_AVAILABLE:
        with pytest.raises(MissingDependencyError) as exc_info:
            from lugia.pyspark import to_pyspark

            to_pyspark("test")

        assert "pyspark" in str(exc_info.value).lower()


def test_optional_dependency_flags():
    """Test that optional dependency flags are set correctly."""
    from lugia.pandas import PANDAS_AVAILABLE
    from lugia.polars import POLARS_AVAILABLE
    from lugia.pydantic import PYDANTIC_AVAILABLE
    from lugia.pyspark import PYSPARK_AVAILABLE

    # These should be boolean values
    assert isinstance(PYDANTIC_AVAILABLE, bool)
    assert isinstance(PANDAS_AVAILABLE, bool)
    assert isinstance(POLARS_AVAILABLE, bool)
    assert isinstance(PYSPARK_AVAILABLE, bool)
