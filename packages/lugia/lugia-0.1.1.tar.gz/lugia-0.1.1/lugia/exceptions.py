"""Custom exceptions for lugia."""

from typing import Optional


class LugiaError(Exception):
    """Base exception for all lugia errors."""

    pass


class MissingDependencyError(LugiaError):
    """Raised when a required optional dependency is missing.

    This error is raised when a conversion requires an optional dependency that
    is not installed. It provides clear instructions on how to install the
    missing dependency.

    Attributes:
        dependency: The name of the missing dependency
        feature: Optional description of the feature that requires the dependency

    Examples:
        >>> raise MissingDependencyError("pandas", "Pandas conversions")
        Traceback (most recent call last):
        ...
        MissingDependencyError: Missing optional dependency 'pandas' required for Pandas conversions. Install it with: pip install lugia[pandas]
    """

    def __init__(self, dependency: str, feature: Optional[str] = None):
        self.dependency = dependency
        self.feature = feature
        message = f"Missing optional dependency '{dependency}'"
        if feature:
            message += f" required for {feature}"
        message += f". Install it with: pip install lugia[{dependency}]"
        super().__init__(message)


class ConversionError(LugiaError):
    """Raised when a conversion fails.

    This error is raised when a conversion between schema types cannot be completed.
    It includes information about the source and target types, and optionally a
    reason for the failure.

    Attributes:
        source_type: The type of the source object that failed to convert
        target_type: The target type that was attempted
        reason: Optional reason for the conversion failure

    Examples:
        >>> raise ConversionError("pydantic", "dataclass", "Missing required field")
        Traceback (most recent call last):
        ...
        ConversionError: Failed to convert from pydantic to dataclass: Missing required field
    """

    def __init__(self, source_type: str, target_type: str, reason: Optional[str] = None):
        self.source_type = source_type
        self.target_type = target_type
        self.reason = reason
        message = f"Failed to convert from {source_type} to {target_type}"
        if reason:
            message += f": {reason}"
        super().__init__(message)
