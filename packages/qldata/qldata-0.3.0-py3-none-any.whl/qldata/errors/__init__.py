"""Error handling package."""

from qldata.errors.api import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    ServerError,
)
from qldata.errors.base import ConfigurationError, QldataError
from qldata.errors.data import DataError, DataValidationError, InvalidDataFormat, NoDataFound
from qldata.errors.source import SourceError, SourceNotAvailable, SourceTimeout
from qldata.errors.store import StoreError, StoreReadError, StoreWriteError
from qldata.errors.validation import (
    PriceValidationError,
    TimestampValidationError,
    ValidationError,
    VolumeValidationError,
)

# Backward compatibility alias
NoDataError = NoDataFound

__all__ = [
    "QldataError",
    "ConfigurationError",
    # Data errors
    "DataError",
    "NoDataFound",
    "NoDataError",  # Alias
    "InvalidDataFormat",
    "DataValidationError",
    # API errors
    "APIError",
    "RateLimitError",
    "AuthenticationError",
    "NetworkError",
    "ServerError",
    # Source errors
    "SourceError",
    "SourceNotAvailable",
    "SourceTimeout",
    # Store errors
    "StoreError",
    "StoreWriteError",
    "StoreReadError",
    # Validation errors
    "ValidationError",
    "PriceValidationError",
    "VolumeValidationError",
    "TimestampValidationError",
]

