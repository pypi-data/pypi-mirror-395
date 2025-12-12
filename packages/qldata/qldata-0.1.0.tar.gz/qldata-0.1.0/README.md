# Qldata

**Unified Python interface for historical and live crypto market data.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Qldata standardizes access to Binance, Bybit, and local stores through a fluent query builder, optional data-cleaning pipelines, and production-ready streaming interfaces.

---

## Documentation

| Topic | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Installation, optional dependencies, and the first query. |
| [Data Access](docs/data-access.md) | Query builder reference, batching, and execution modes. |
| [Configuration & Storage](docs/configuration.md) | Runtime config, caches, and store backends. |
| [Transforms & Data Cleaning](docs/transforms.md) | Built-in validation, resampling, and custom pipelines. |
| [Live Streaming](docs/live-streaming.md) | Streams, callbacks, resampling, and troubleshooting. |
| [Operations & Support](docs/contributing.md) | Maintainer-only release workflow, doc syncing, and support channels. |

---

## Quick Start

```bash
pip install qldata
```

```python
import qldata as qd

df = (
    qd.data("BTCUSDT", source="binance", category="spot")
    .last(30)
    .resolution("1h")
    .clean(remove_invalid_prices=True, validate_ohlc=True)
    .get()
)

print(df.tail())
```

Need API keys for authenticated endpoints? Export `BINANCE_API_KEY`, `BINANCE_API_SECRET`, `BYBIT_API_KEY`, and `BYBIT_API_SECRET` before running scripts. The adapters will pick them up automatically.

---

## Highlights

- **Unified query builder** - Express historical requests, local reads, and file loads with consistent chaining (`.between`, `.last`, `.resolution`, `.get`).
- **Multiple sources** - Binance (spot, USD-M, COIN-M), Bybit (spot, linear, inverse, options), plus CSV/Parquet/SQLite/DuckDB stores.
- **Data quality tools** - Validation, duplicate removal, outlier handling, and custom transform pipelines.
- **Streaming API** - Push callbacks or pull-based sessions for live data with client-side resampling.
- **Production configuration** - Cache controls, pluggable storage, structured logging, and testable adapters.

See the [docs](docs/index.md) for deep dives and additional examples.

---

## Publishing Docs to a Public Repo

Planning to keep this codebase private while publishing documentation?

1. Prepare (or clone) your public docs repository, e.g. `../qldata-docs`.
2. Run `python scripts/export_docs.py ../qldata-docs --include-license` from the project root.
3. Commit and push the generated docs repo, then wire it to Read the Docs or another static host (the included `mkdocs.yml` and `docs/requirements.txt` work out of the box with MkDocs + Material).
4. In `pyproject.toml`, point the `Homepage`/`Documentation` URLs at the published site so PyPI displays the correct links.

Repeat the export each time you update docs to keep the public site in sync with the private source.

---

## Operations & Support

Qldata is maintained privately and does not accept external code contributions. Use the public docs repository for questions or bug reports, and see [Operations & Support](docs/contributing.md) for the internal release and documentation-sync workflow.

---

## License

MIT License - see [LICENSE](LICENSE).
