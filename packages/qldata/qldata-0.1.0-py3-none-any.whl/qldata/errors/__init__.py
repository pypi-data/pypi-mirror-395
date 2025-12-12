"""Error handling package."""

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

__all__ = [
    "QldataError",
    "ConfigurationError",
    "DataError",
    "NoDataFound",
    "InvalidDataFormat",
    "DataValidationError",
    "SourceError",
    "SourceNotAvailable",
    "SourceTimeout",
    "StoreError",
    "StoreWriteError",
    "StoreReadError",
    "ValidationError",
    "PriceValidationError",
    "VolumeValidationError",
    "TimestampValidationError",
]
