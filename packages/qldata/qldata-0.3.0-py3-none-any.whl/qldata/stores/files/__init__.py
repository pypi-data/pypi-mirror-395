"""File-based stores."""

from qldata.stores.files.csv_store import CSVStore
from qldata.stores.files.parquet_store import ParquetStore

__all__ = [
    "ParquetStore",
    "CSVStore",
]
