"""Base exception classes."""


class QldataError(Exception):
    """Base exception for all Qldata errors."""

    pass


class ConfigurationError(QldataError):
    """Configuration-related errors."""

    pass
