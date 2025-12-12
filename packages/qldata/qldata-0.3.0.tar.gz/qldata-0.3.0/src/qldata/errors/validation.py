"""Validation-related exceptions."""

from qldata.errors.base import QldataError


class ValidationError(QldataError):
    """Base class for validation errors."""

    pass


class PriceValidationError(ValidationError):
    """Price validation failed."""

    pass


class VolumeValidationError(ValidationError):
    """Volume validation failed."""

    pass


class TimestampValidationError(ValidationError):
    """Timestamp validation failed."""

    pass
