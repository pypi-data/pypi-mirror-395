"""Source-related exceptions."""

from qldata.errors.base import QldataError


class SourceError(QldataError):
    """Base class for data source errors."""

    pass


class SourceNotAvailable(SourceError):
    """Data source is not available."""

    pass


class SourceTimeout(SourceError):
    """Data source request timed out."""

    pass
