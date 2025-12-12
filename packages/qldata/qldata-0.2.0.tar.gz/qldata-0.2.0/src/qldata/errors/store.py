"""Store-related exceptions."""

from qldata.errors.base import QldataError


class StoreError(QldataError):
    """Base class for data store errors."""

    pass


class StoreWriteError(StoreError):
    """Failed to write data to store."""

    pass


class StoreReadError(StoreError):
    """Failed to read data from store."""

    pass
