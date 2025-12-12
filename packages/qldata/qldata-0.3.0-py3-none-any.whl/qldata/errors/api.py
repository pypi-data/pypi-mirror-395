"""API-related exceptions for external service integrations."""

from qldata.errors.base import QldataError


class APIError(QldataError):
    """Base class for external API errors."""

    pass


class RateLimitError(APIError):
    """API rate limit exceeded.

    This indicates that the service is temporarily throttling requests.
    The client should implement exponential backoff and retry.
    """

    pass


class AuthenticationError(APIError):
    """API authentication failed.

    This could be due to invalid credentials, expired tokens,
    or missing API keys.
    """

    pass


class NetworkError(APIError):
    """Network or connectivity error.

    This includes timeout errors, connection failures,
    and transient network issues.
    """

    pass


class ServerError(APIError):
    """External server error (5xx responses).

    The external service is experiencing issues.
    Retry may be appropriate after a delay.
    """

    pass
