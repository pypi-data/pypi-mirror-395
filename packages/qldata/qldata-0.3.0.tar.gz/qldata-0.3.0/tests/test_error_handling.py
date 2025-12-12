"""Tests for error handling and exception hierarchy."""

import pytest

from qldata.errors import (
    APIError,
    AuthenticationError,
    NetworkError,
    NoDataError,
    RateLimitError,
    ServerError,
)


class TestExceptionHierarchy:
    """Test exception inheritance and relationships."""

    def test_exception_inheritance(self):
        """Verify exception hierarchy is correct."""
        # API errors
        assert issubclass(RateLimitError, APIError)
        assert issubclass(NetworkError, APIError)
        assert issubclass(ServerError, APIError)
        assert issubclass(AuthenticationError, APIError)

        # NoDataError compatibility
        assert NoDataError is not None

    def test_exception_messages(self):
        """Verify exceptions can be created with custom messages."""
        rate_limit = RateLimitError("Rate limit exceeded")
        assert "Rate limit exceeded" in str(rate_limit)

        network_err = NetworkError("Connection timeout")
        assert "Connection timeout" in str(network_err)

    def test_exception_chaining(self):
        """Verify exceptions can be chained properly."""
        original = ValueError("Original error")

        try:
            raise NetworkError("Network failed") from original
        except NetworkError as e:
            assert e.__cause__ == original
            assert isinstance(e.__cause__, ValueError)


class TestAdapterExceptions:
    """Test that adapters raise correct exceptions."""

    @pytest.mark.skip(reason="Requires mock or live API")
    def test_binance_rate_limit_error(self):
        """Test Binance adapter raises RateLimitError on rate limiting."""
        pass

    @pytest.mark.skip(reason="Requires mock or live API")
    def test_bybit_network_error(self):
        """Test Bybit adapter raises NetworkError on network issues."""
        pass


class TestSourceExceptionHandling:
    """Test that sources properly handle and propagate exceptions."""

    @pytest.mark.skip(reason="Requires mock adapter")
    def test_source_reraises_api_errors(self):
        """Verify sources re-raise API errors from adapters."""
        # Mock adapter that raises RateLimitError
        # Verify source re-raises it unchanged

    @pytest.mark.skip(reason="Requires mock adapter")
    def test_source_wraps_unexpected_errors(self):
        """Verify sources wrap unexpected errors in NoDataError."""
        # Mock adapter that raises unexpected exception
        # Verify source wraps it in NoDataError


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
