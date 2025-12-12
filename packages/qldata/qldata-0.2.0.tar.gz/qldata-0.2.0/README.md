# Data Layer (qldata)

[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/qldata-docs/badge/?version=latest)](https://qldata-docs.readthedocs.io/en/latest/?badge=latest)

**Data Layer** (`qldata`) is a high-performance, production-grade Python library designed for acquiring, storing, transforming, and validating financial market data. It provides a unified interface for interacting with various data sources, including crypto exchanges (Binance, Bybit) and local storage (DuckDB, Parquet).

## 🚀 Key Features

*   **Unified Data Interface**: Seamlessly switch between live exchange feeds and historical data.
*   **High Performance**: Built on `pandas`, `numpy`, and `pyarrow` for efficient data manipulation.
*   **Storage Optimized**: Integrated with `DuckDB` for fast, analytical SQL queries on large datasets.
*   **Exchange Support**: Native adapters for **Binance** and **Bybit** with shared rate limiting and retry logic.
*   **Automatic Chunking**: Transparently handles multi-year historical data requests by auto-splitting into optimal chunks.
*   **Smart Error Handling**: Specific exception types (`RateLimitError`, `NetworkError`, `ServerError`) with automatic retry mechanisms.
*   **Metadata Tracking**: Automatic tracking of dataset freshness, coverage, and quality for smart caching.
*   **Live Streaming**: Robust WebSocket support with automatic reconnection and error handling.
*   **Type Safe**: Fully typed codebase using modern Python type hinting.
*   **Production Ready**: Comprehensive error handling, logging, and retry mechanisms via `tenacity`.

## 🛠️ Installation

Requires Python 3.10+.

```bash
pip install qldata
```

For a minimal install (core data structures only):

```bash
pip install qldata[minimal]
```

For development dependencies:

```bash
pip install qldata[dev]
```

## ⚡ Quick Start

### Fetching Historical Data

The primary entry point for historical data is `qd.data()`.

```python
import qldata as qd

# Fetch last 30 hours of 1-hour klines for BTCUSDT from Binance
df = qd.data("BTCUSDT", source="binance").last(30).resolution("1h").get()
print(df.head())

# Fetch multi-year data - automatically chunked!
# This works seamlessly even for 2+ years of 1-minute data (>1M bars)
df_long = qd.data("BTCUSDT", source="binance").between("2023-01-01", "2025-01-01").resolution("1h").get()
print(f"Fetched {len(df_long)} bars")
```

### Loading from Local Storage

Local stores use the `source="local"` alias and work with naive timestamps for convenience.

```python
import qldata as qd
from qldata.config import get_config

# Point storage to a directory (Parquet by default)
qd.config(data_dir="./data", store_type="parquet")

# Load previously stored bars
local_df = qd.data("BTCUSDT", source="local").resolution("1h").last(48).get()
print(local_df.tail())
```

### Working with Metadata

Check dataset information and freshness:

```python
from qldata.stores.files import ParquetStore

store = ParquetStore("./data")

# List all tracked datasets
for meta in store.list_metadata():
    print(f"{meta.symbol} ({meta.timeframe}): {meta.record_count} bars")
    print(f"  Range: {meta.first_timestamp} to {meta.last_timestamp}")
    print(f"  Stale: {meta.is_stale(max_age_hours=24)}")
```

### Handling Errors

```python
from qldata.errors import RateLimitError, NetworkError

try:
    df = qd.data("BTCUSDT", source="binance").last(100).resolution("1m").get()
except RateLimitError:
    print("Rate limited - automatic retry will handle this")
except NetworkError as e:
    print(f"Network issue: {e}")
```

### Streaming Live Data

For real-time data, use `qd.stream()`.

```python
import qldata as qd
import asyncio

async def handler(msg):
    print(msg)

# Stream live ticks
stream = qd.stream(["BTCUSDT"], source="binance").resolution("tick").on_data(handler).get()

# Note: In a real async application, you would await the stream session
# await stream.start()
```

## 🏗️ Architecture

`qldata` is built with a modular architecture:

*   **Core Models**: Fundamental data structures and types.
*   **Adapters**: Exchange-specific broker adapters (`qldata/adapters/brokers/*.py`) that share rate-limiters/clients.
*   **Stores**: Persistence layer for files/DBs with metadata sidecars and deduplication.
*   **API/Queries**: `qd.data()` / `qd.stream()` builders that route through adapters or local stores.
*   **Resilience/Transforms**: Retry, chunking, validation, and cleaning utilities used by adapters and queries.

## 🤝 Development

This is an internal project. Please follow the guidelines below for development.

1.  **Environment**: Ensure you are using the correct Python version (3.10+).
2.  **Testing**: Run `pytest` before pushing any changes.
3.  **Linting**: Use `ruff` and `black` to maintain code quality.
4.  **Documentation**: Update docstrings and `mkdocs` files when modifying APIs.

See the [Developer Guide](docs/developer-guide/development.md) for more details.
