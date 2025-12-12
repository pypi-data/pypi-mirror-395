"""
Lugia - Universal schema converter for Python data types.

Lugia provides bidirectional conversions between popular data schema types
including PySpark, Polars, Pandas, Pydantic, dataclass, TypedDict, SQLModel,
and SQLAlchemy. All dependencies are optional for maximum flexibility.
"""

__version__ = "0.1.0"
__author__ = "Odos Matthews"
__email__ = "odosmatthews@gmail.com"

import contextlib

from lugia.core import convert, detect_type
from lugia.exceptions import ConversionError, MissingDependencyError

# Import conversion functions (they handle optional dependencies internally)
with contextlib.suppress(ImportError):
    from lugia.pydantic import to_pydantic

with contextlib.suppress(ImportError):
    from lugia.dataclass import to_dataclass

with contextlib.suppress(ImportError):
    from lugia.typedict import to_typeddict

with contextlib.suppress(ImportError):
    from lugia.pandas import from_pandas, to_pandas

with contextlib.suppress(ImportError):
    from lugia.polars import from_polars, to_polars

with contextlib.suppress(ImportError):
    from lugia.pyspark import from_pyspark, to_pyspark

with contextlib.suppress(ImportError):
    from lugia.sqlalchemy import from_sqlalchemy, to_sqlalchemy

with contextlib.suppress(ImportError):
    from lugia.sqlmodel import from_sqlmodel, to_sqlmodel

__all__ = [
    "convert",
    "detect_type",
    "ConversionError",
    "MissingDependencyError",
    # Conversion functions
    "to_pydantic",
    "to_dataclass",
    "to_typeddict",
    "to_pandas",
    "from_pandas",
    "to_polars",
    "from_polars",
    "to_pyspark",
    "from_pyspark",
    "to_sqlalchemy",
    "from_sqlalchemy",
    "to_sqlmodel",
    "from_sqlmodel",
]
