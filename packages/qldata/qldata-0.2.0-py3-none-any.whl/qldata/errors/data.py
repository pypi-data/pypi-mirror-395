"""Data-related exceptions."""

from qldata.errors.base import QldataError


class DataError(QldataError):
    """Base class for data errors."""

    pass


class NoDataFound(DataError):
    """No data found for the given query."""

    pass


class InvalidDataFormat(DataError):
    """Data format is invalid."""

    pass


class DataValidationError(DataError):
    """Data validation failed."""

    pass
