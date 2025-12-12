"""Utility functions for type checking and validation."""

from typing import Any, get_args, get_origin


def is_dataclass(obj: Any) -> bool:
    """Check if an object is a dataclass."""
    try:
        import dataclasses

        return dataclasses.is_dataclass(obj)
    except ImportError:
        return False


def is_typeddict(obj: Any) -> bool:
    """Check if an object is a TypedDict."""
    try:
        from typing import TypedDict  # noqa: F401

        return isinstance(obj, type) and issubclass(obj, dict) and hasattr(obj, "__annotations__")
    except (ImportError, TypeError):
        return False


def is_pydantic_model(obj: Any) -> bool:
    """Check if an object is a Pydantic model."""
    try:
        from pydantic import BaseModel

        return isinstance(obj, type) and issubclass(obj, BaseModel)
    except (ImportError, TypeError):
        return False


def is_pydantic_instance(obj: Any) -> bool:
    """Check if an object is a Pydantic model instance."""
    try:
        from pydantic import BaseModel

        return isinstance(obj, BaseModel)
    except ImportError:
        return False


def is_sqlmodel_model(obj: Any) -> bool:
    """Check if an object is a SQLModel model."""
    try:
        from sqlmodel import SQLModel

        return isinstance(obj, type) and issubclass(obj, SQLModel)
    except (ImportError, TypeError):
        return False


def is_sqlalchemy_model(obj: Any) -> bool:
    """Check if an object is a SQLAlchemy model."""
    try:
        from sqlalchemy.ext.declarative import DeclarativeMeta

        return isinstance(obj, type) and issubclass(obj, DeclarativeMeta)
    except (ImportError, TypeError, AttributeError):
        # SQLAlchemy 2.0+ uses different base
        try:
            from sqlalchemy.orm import DeclarativeBase

            return isinstance(obj, type) and issubclass(obj, DeclarativeBase)
        except (ImportError, TypeError):
            return False


def get_type_name(obj: Any) -> str:
    """Get a human-readable type name for an object."""
    if isinstance(obj, type):
        return obj.__name__
    return type(obj).__name__


def get_annotations(obj: Any) -> dict[Any, Any]:
    """Get type annotations from a class or function."""
    if isinstance(obj, type):
        return getattr(obj, "__annotations__", {})  # type: ignore[no-any-return]
    elif hasattr(obj, "__annotations__"):
        return obj.__annotations__  # type: ignore[no-any-return]
    return {}


def normalize_type_hint(hint: Any) -> Any:
    """Normalize type hints for comparison."""
    origin = get_origin(hint)
    if origin is not None:
        args = get_args(hint)
        return (origin, tuple(normalize_type_hint(arg) for arg in args))
    return hint
