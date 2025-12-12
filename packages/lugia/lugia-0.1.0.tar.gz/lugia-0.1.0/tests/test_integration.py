"""Integration tests for cross-format conversions."""

import pytest


def test_pydantic_to_pandas_to_polars():
    """Test conversion chain: Pydantic -> Pandas -> Polars."""
    try:
        import pandas as pd
        import polars as pl
        from pydantic import BaseModel

        from lugia.pandas import to_pandas
        from lugia.polars import to_polars

        class User(BaseModel):
            name: str
            age: int

        user = User(name="John", age=30)

        # Pydantic -> Pandas
        pandas_df = to_pandas(user)
        assert isinstance(pandas_df, pd.DataFrame)

        # Pandas -> Polars
        polars_df = to_polars(pandas_df)
        assert isinstance(polars_df, pl.DataFrame)
        assert len(polars_df) == 1
    except ImportError as e:
        pytest.skip(f"Missing dependency: {e}")


def test_dataclass_to_pydantic_to_pyspark():
    """Test conversion chain: Dataclass -> Pydantic -> PySpark."""
    try:
        import dataclasses

        from pydantic import BaseModel
        from pyspark.sql import SparkSession  # noqa: F401
        from pyspark.sql.types import StructType

        from lugia.pydantic import to_pydantic
        from lugia.pyspark import to_pyspark

        @dataclasses.dataclass
        class User:
            name: str
            age: int

        # Dataclass -> Pydantic
        pydantic_model = to_pydantic(User)
        assert issubclass(pydantic_model, BaseModel)

        # Pydantic -> PySpark
        struct_type = to_pyspark(pydantic_model)
        assert isinstance(struct_type, StructType)
        assert len(struct_type.fields) == 2
    except ImportError as e:
        pytest.skip(f"Missing dependency: {e}")


def test_pandas_to_pydantic_to_dataclass():
    """Test conversion chain: Pandas -> Pydantic -> Dataclass."""
    try:
        import pandas as pd
        from pydantic import BaseModel

        from lugia.dataclass import to_dataclass
        from lugia.pydantic import to_pydantic

        df = pd.DataFrame({"name": ["John", "Jane"], "age": [30, 25]})

        # Pandas -> Pydantic
        pydantic_model = to_pydantic(df)
        assert issubclass(pydantic_model, BaseModel)

        # Pydantic -> Dataclass
        dc_class = to_dataclass(pydantic_model)
        assert dc_class is not None
        assert hasattr(dc_class, "__dataclass_fields__")
    except ImportError as e:
        pytest.skip(f"Missing dependency: {e}")
