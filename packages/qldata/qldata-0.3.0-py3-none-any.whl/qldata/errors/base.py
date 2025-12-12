"""Base exception classes for the qldata library."""


class QldataError(Exception):
    """Base exception for all qldata errors.

    All custom exceptions in the qldata library inherit from this class.
    Catch this to handle any qldata-specific error.

    Example:
        >>> try:
        ...     df = qd.data("BTCUSDT", source="binance").get()
        ... except QldataError as e:
        ...     print(f"qldata error: {e}")
    """

    pass


class ConfigurationError(QldataError):
    """Raised when configuration is invalid or missing.

    Common causes:
    - Invalid store type specified (not one of: parquet, csv, sqlite, duckdb)
    - Data directory not writable or does not exist
    - Missing required dependencies (e.g., pyarrow for parquet)
    - Invalid configuration values (e.g., negative cache size)

    Example:
        >>> qd.config(store_type="invalid")  # Raises ConfigurationError
    """

    pass
