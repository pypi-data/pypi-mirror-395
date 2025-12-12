"""Shared query helper functions and utilities."""

import inspect
from threading import Lock

from qldata.adapters.brokers.base import BaseBrokerAdapter

_ADAPTER_CACHE: dict[tuple[str, str | None], BaseBrokerAdapter] = {}
_ADAPTER_CACHE_LOCK = Lock()


def _get_adapter(source: str, category: str | None) -> BaseBrokerAdapter:
    """Create or reuse broker adapters to avoid rebuilding clients each call."""
    if source == "binance":
        from qldata.adapters.brokers.binance import BinanceAdapter

        adapter_cls = BinanceAdapter
    elif source == "bybit":
        from qldata.adapters.brokers.bybit import BybitAdapter

        adapter_cls = BybitAdapter
    else:
        raise ValueError(f"Unknown source: {source}")

    key = (source, category)
    with _ADAPTER_CACHE_LOCK:
        cached = _ADAPTER_CACHE.get(key)
        if cached and inspect.isclass(adapter_cls) and isinstance(cached, adapter_cls):
            return cached

    # Instantiate adapter (support mocks that may not be proper classes)
    try:
        adapter: BaseBrokerAdapter = adapter_cls(category=category) if category else adapter_cls()
    except TypeError:
        adapter = adapter_cls()  # type: ignore[assignment]

    with _ADAPTER_CACHE_LOCK:
        _ADAPTER_CACHE[key] = adapter
        return adapter
