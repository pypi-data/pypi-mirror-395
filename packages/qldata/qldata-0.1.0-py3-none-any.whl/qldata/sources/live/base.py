"""Base streaming source interface."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

import pandas as pd


class StreamingSource(ABC):
    """Abstract base class for streaming data sources.

    Streaming sources provide real-time market data via callbacks
    or async iteration.
    """

    @abstractmethod
    def subscribe(
        self, symbols: list[str], callback: Callable[[pd.DataFrame], None], **kwargs: Any
    ) -> None:
        """Subscribe to real-time data for symbols.

        Args:
            symbols: List of symbol tickers
            callback: Function to call with new data
            **kwargs: Source-specific parameters
        """
        pass

    @abstractmethod
    def unsubscribe(self, symbols: list[str] | None = None) -> None:
        """Unsubscribe from symbols.

        Args:
            symbols: Symbols to unsubscribe from (None = all)
        """
        pass

    @abstractmethod
    def start(self) -> None:
        """Start the streaming source."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the streaming source."""
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if source is connected."""
        pass
