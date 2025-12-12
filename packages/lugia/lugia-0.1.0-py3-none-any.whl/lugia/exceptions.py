"""Custom exceptions for lugia."""

from typing import Optional


class LugiaError(Exception):
    """Base exception for all lugia errors."""

    pass


class MissingDependencyError(LugiaError):
    """Raised when a required optional dependency is missing."""

    def __init__(self, dependency: str, feature: Optional[str] = None):
        self.dependency = dependency
        self.feature = feature
        message = f"Missing optional dependency '{dependency}'"
        if feature:
            message += f" required for {feature}"
        message += f". Install it with: pip install lugia[{dependency}]"
        super().__init__(message)


class ConversionError(LugiaError):
    """Raised when a conversion fails."""

    def __init__(self, source_type: str, target_type: str, reason: Optional[str] = None):
        self.source_type = source_type
        self.target_type = target_type
        self.reason = reason
        message = f"Failed to convert from {source_type} to {target_type}"
        if reason:
            message += f": {reason}"
        super().__init__(message)
