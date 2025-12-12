"""Tests for PySpark conversions."""

import pytest


@pytest.fixture
def sample_pyspark_schema():
    """Create a sample PySpark StructType for testing."""
    try:
        from pyspark.sql.types import IntegerType, StringType, StructField, StructType

        return StructType(
            [
                StructField("name", StringType(), nullable=False),
                StructField("age", IntegerType(), nullable=False),
                StructField("email", StringType(), nullable=True),
            ]
        )
    except ImportError:
        pytest.skip("PySpark not available")


def test_pyspark_to_pydantic(sample_pyspark_schema):
    """Test converting PySpark StructType to Pydantic model."""
    try:
        from pydantic import BaseModel

        from lugia.pydantic import to_pydantic

        pydantic_model = to_pydantic(sample_pyspark_schema)
        assert pydantic_model is not None
        assert issubclass(pydantic_model, BaseModel)
    except ImportError:
        pytest.skip("Pydantic not available")


def test_pyspark_to_dataclass(sample_pyspark_schema):
    """Test converting PySpark StructType to dataclass."""
    from lugia.dataclass import to_dataclass

    dc_class = to_dataclass(sample_pyspark_schema)
    assert dc_class is not None
    assert hasattr(dc_class, "__dataclass_fields__")
    assert "name" in dc_class.__dataclass_fields__


def test_pyspark_to_polars(sample_pyspark_schema):
    """Test converting PySpark StructType to Polars Schema."""
    try:
        import polars as pl

        from lugia.polars import to_polars

        polars_schema = to_polars(sample_pyspark_schema)
        assert isinstance(polars_schema, pl.Schema)
        assert "name" in polars_schema
    except ImportError:
        pytest.skip("Polars not available")


def test_pyspark_missing_dependency():
    """Test that missing PySpark dependency raises appropriate error."""
    from lugia.exceptions import MissingDependencyError
    from lugia.pyspark import to_pyspark

    try:
        from pyspark.sql.types import StructType  # noqa: F401

        # If we get here, pyspark is available
        assert True
    except ImportError:
        with pytest.raises(MissingDependencyError):
            to_pyspark("invalid_source")
