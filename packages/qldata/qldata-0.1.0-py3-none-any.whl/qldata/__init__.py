"""Top-level public API for qldata.

This module exposes a stable, user-friendly surface:

    import qldata as qd

    qd.config(...)
    df = qd.data("BTCUSDT", source="binance", category="spot").last(30).resolution("1h").get()
"""

from .api.config import (
    config,
    get_data_dir,
    get_config,
    is_cache_enabled,
    is_validation_enabled,
)
from .api.unified import UnifiedAPI, data
from .api.streaming import StreamingAPI, StreamQuery, StreamSession, stream
from .models import (
    AssetType,
    Bar,
    Exchange,
    Quote,
    Symbol,
    Tick,
    Timeframe,
)
from .transforms import (
    TransformPipeline,
    fill_backward,
    fill_forward,
    fill_interpolate,
    remove_duplicates,
    remove_outliers,
    resample,
    resample_bars,
    ticks_to_bars,
)
from .validation.checks import validate_bars

__all__ = [
    # Config
    "config",
    "get_data_dir",
    "get_config",
    "is_cache_enabled",
    "is_validation_enabled",
    # Unified data API
    "data",
    "UnifiedAPI",
    "stream",
    "StreamingAPI",
    "StreamQuery",
    "StreamSession",
    # Models
    "Timeframe",
    "AssetType",
    "Exchange",
    "Symbol",
    "Tick",
    "Bar",
    "Quote",
    # Transforms
    "TransformPipeline",
    "remove_duplicates",
    "remove_outliers",
    "resample_bars",
    "resample",
    "ticks_to_bars",
    "fill_forward",
    "fill_backward",
    "fill_interpolate",
    # Validation
    "validate_bars",
]
