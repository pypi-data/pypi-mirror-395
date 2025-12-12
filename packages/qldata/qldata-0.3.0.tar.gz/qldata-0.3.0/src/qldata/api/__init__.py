"""Public API package with organized submodules."""

# Core API
from qldata.api.core.unified import UnifiedAPI, current_funding_rate, data

# Configuration
from qldata.api.config.resilience import (
    EXCHANGE_RATE_LIMITS,
    ResilienceConfig,
    get_rate_limit_config,
)
from qldata.api.config.settings import (
    config,
    get_data_dir,
    is_cache_enabled,
    is_validation_enabled,
)

# Reference data
from qldata.api.reference.symbols import (
    get_exchange_info,
    get_symbol_info,
    list_symbols,
)

from qldata.api.queries.multi_symbol import MultiSymbolQuery
from qldata.api.queries.symbol import SymbolQuery

from qldata.api.core.streaming_api import StreamingAPI, stream
from qldata.api.sessions.query import StreamQuery
from qldata.api.sessions.stream import StreamSession

__all__ = [
    # Core
    "data",
    "UnifiedAPI",
    "current_funding_rate",
    # Streaming
    "stream",
    "StreamingAPI",
    "StreamSession",
    "StreamQuery",
    # Queries
    "SymbolQuery",
    "MultiSymbolQuery",
    # Reference
    "get_symbol_info",
    "get_exchange_info",
    "list_symbols",
    # Config
    "config",
    "get_data_dir",
    "is_cache_enabled",
    "is_validation_enabled",
    "ResilienceConfig",
    "get_rate_limit_config",
    "EXCHANGE_RATE_LIMITS",
]
