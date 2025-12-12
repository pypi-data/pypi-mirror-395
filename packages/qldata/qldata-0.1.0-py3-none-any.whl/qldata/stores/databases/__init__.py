"""Database stores."""

from qldata.stores.databases.sqlite_store import SQLiteStore

try:
    from qldata.stores.databases.duckdb_store import DuckDBStore

    __all__ = ["SQLiteStore", "DuckDBStore"]
except ImportError:
    __all__ = ["SQLiteStore"]
