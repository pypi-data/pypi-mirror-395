from pathlib import Path
from typing import Literal

from qldata.config import get_config

StoreType = Literal["parquet", "csv", "sqlite", "duckdb"]


def config(
    *,
    data_dir: str | Path | None = None,
    store_type: StoreType | None = None,
    cache: bool | None = None,
    cache_size: int | None = None,
    validate: bool | None = None,
) -> None:
    """Configure global settings with typed parameters.

    Args:
        data_dir: Directory for data storage
        store_type: Storage format ("parquet", "csv", "sqlite", "duckdb")
        cache: Enable/disable caching
        cache_size: Maximum number of items to cache
        validate: Enable/disable data validation

    Examples:
        >>> qd.config(data_dir="./data", store_type="parquet")
        >>> qd.config(cache=True, cache_size=1000)
        >>> qd.config(validate=False)
    """
    cfg = get_config()

    # Build kwargs for set() call
    kwargs = {}

    if data_dir is not None:
        kwargs["data_dir"] = str(data_dir)

    if store_type is not None:
        kwargs["store_type"] = store_type

    if cache is not None:
        kwargs["cache"] = cache

    if cache_size is not None:
        kwargs["cache_size"] = cache_size

    if validate is not None:
        kwargs["validate"] = validate

    cfg.set(**kwargs)


def get_data_dir() -> Path:
    """Get configured data directory.

    Returns:
        Path to data directory
    """
    return get_config().get_data_dir()


def is_cache_enabled() -> bool:
    """Check if caching is enabled.

    Returns:
        True if caching is enabled
    """
    return get_config().is_cache_enabled()


def is_validation_enabled() -> bool:
    """Check if validation is enabled.

    Returns:
        True if validation is enabled
    """
    return get_config().is_validation_enabled()


__all__ = [
    "config",
    "get_data_dir",
    "is_cache_enabled",
    "is_validation_enabled",
]
