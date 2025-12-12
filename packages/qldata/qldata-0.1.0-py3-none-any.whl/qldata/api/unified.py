"""Unified API entry point."""

from typing import Any

from qldata.api.symbol_query import MultiSymbolQuery, SymbolQuery
from qldata.config import get_config
from qldata.config.manager import ConfigManager


class UnifiedAPI:
    """Single entry point for all data operations."""

    def __call__(
        self,
        symbols: str | list[str],
        *,
        source: str | None = None,
        category: str | None = None,
        config: ConfigManager | None = None,
        **kwargs: Any,
    ) -> SymbolQuery | MultiSymbolQuery:
        """Start a data query.

        Args:
            symbols: Single symbol or list of symbols
            source: Broker ("binance", "bybit"), storage ("local"), or file path
            category: Market category for brokers
            config: Optional ConfigManager to inject (defaults to global)
            **kwargs: Additional options (e.g., data_dir, store_type)
        """
        if source is None:
            raise ValueError(
                "source is required. Use brokers ('binance','bybit'), storage ('local'), "
                "or a file path (csv/parquet)."
            )

        is_file = self._is_file_path(source)

        # Validate category only for broker sources
        if category and source in {"binance", "bybit"}:
            self._validate_category(source, category)

        cfg = config or get_config()

        if isinstance(symbols, str):
            query = SymbolQuery(symbols, config=cfg)
            query.from_source(source, category=category, **kwargs)
            return query

        if isinstance(symbols, list):
            if is_file:
                raise ValueError("Cannot load multiple symbols from a single file path")
            query = MultiSymbolQuery(symbols, config=cfg)
            query.from_source(source, category=category, **kwargs)
            return query

        raise TypeError(f"symbols must be str or list, got {type(symbols).__name__}")

    @staticmethod
    def _is_file_path(source: str) -> bool:
        """Check if source looks like a file path."""
        from pathlib import Path

        return any(source.endswith(ext) for ext in [".csv", ".parquet", ".pq"]) or Path(source).expanduser().resolve().exists()

    def _validate_category(self, source: str, category: str) -> None:
        """Validate category for a given source."""
        valid: dict[str, set[str]] = {
            "binance": {"spot", "usdm", "coinm", "option"},
            "bybit": {"spot", "linear", "inverse", "option"},
        }
        allowed = valid.get(source)
        if allowed is None:
            raise ValueError(f"Unknown source: {source}")
        if allowed and category not in allowed:
            raise ValueError(f"Invalid category '{category}' for source '{source}'. Allowed: {sorted(allowed)}")
        if not allowed and category is not None:
            raise ValueError(f"Source '{source}' does not support category selection")


# Singleton instance
data = UnifiedAPI()


__all__ = ["data", "UnifiedAPI"]
