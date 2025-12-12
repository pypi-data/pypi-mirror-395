"""qldata - Modern cryptocurrency trading data library.

## Primary API (use via `import qldata as qd`)

Core data operations:
    - qd.data() - Historical data queries
    - qd.stream() - Live data streaming
    - qd.current_funding_rate() - Quick funding rate access
    - qd.get_symbol_info() - Symbol metadata
    - qd.get_exchange_info() - Exchange information
    - qd.list_symbols() - List available symbols

Example:
    >>> import qldata as qd
    >>> df = qd.data("BTCUSDT", source="binance").last(30).resolution("1h").get()
    >>> stream = qd.stream(["BTCUSDT"], source="binance").resolution("tick").on_data(handler).get()

"""

from ._version import __version__

from .api import (
    StreamingAPI,
    StreamQuery,
    StreamSession,
    UnifiedAPI,
    config,
    current_funding_rate,
    data,
    get_data_dir,
    get_exchange_info,
    get_symbol_info,
    is_cache_enabled,
    is_validation_enabled,
    list_symbols,
    stream,
)
from .api.config import get_config
from .models import (
    Bar,
    FundingRate,
    OpenInterest,
    OrderBook,
    OrderBookLevel,
    SymbolInfo,
    Tick,
    Timeframe,
)
from .monitoring import AlertManager, DataQualityMonitor
from .resilience import HeartbeatMonitor, MessageDeduplicator, ReconnectionManager
from .transforms import (
    TransformPipeline,
    fill_backward,
    fill_forward,
    fill_interpolate,
    remove_duplicates,
    remove_invalid_prices,
    remove_outliers,
    resample,
    resample_bars,
    ticks_to_bars,
)
from .validation.checks import validate_bars

# Note: Advanced imports available as:
# - from qldata.resilience import ReconnectionManager, HeartbeatMonitor, MessageDeduplicator
# - from qldata.adapters import BinanceRestClient, BybitRestClient

__all__ = [
    # Version
    "__version__",
    # Primary API
    "data",
    "stream",
    "current_funding_rate",
    "get_symbol_info",
    "get_exchange_info",
    "list_symbols",
    # Config
    "config",
    "get_config",
    "get_data_dir",
    "is_cache_enabled",
    "is_validation_enabled",
    # Models
    "Bar",
    "Tick",
    "Timeframe",
    "OrderBook",
    "OrderBookLevel",
    "FundingRate",
    "OpenInterest",
    "SymbolInfo",
    # Monitoring (advanced)
    "DataQualityMonitor",
    "AlertManager",
    # Transforms
    "TransformPipeline",
    "fill_forward",
    "fill_backward",
    "fill_interpolate",
    "remove_duplicates",
    "remove_outliers",
    "remove_invalid_prices",
    "resample",
    "resample_bars",
    "ticks_to_bars",
    # Streaming
    "StreamingAPI",
    "StreamQuery",
    "StreamSession",
    # Unified API
    "UnifiedAPI",
    # Resilience (advanced)
    "ReconnectionManager",
    "HeartbeatMonitor",
    "MessageDeduplicator",
]
