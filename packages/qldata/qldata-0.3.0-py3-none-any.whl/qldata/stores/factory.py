"""Factory for creating data store instances.

Centralizes store creation logic to avoid duplication across the codebase.
"""

from pathlib import Path
from typing import Literal

from qldata.stores.base.store import DataStore

StoreType = Literal["parquet", "csv", "sqlite", "duckdb"]


class StoreFactory:
    """Factory for creating data store instances.

    Example:
        >>> store = StoreFactory.create("parquet", Path("./data"))
        >>> store = StoreFactory.create_from_config(config)
    """

    @staticmethod
    def create(store_type: StoreType, data_dir: Path) -> DataStore:
        """Create a store instance of the specified type.

        Args:
            store_type: Type of store to create
            data_dir: Base directory for data storage

        Returns:
            Configured DataStore instance

        Raises:
            ValueError: If store_type is not supported

        Example:
            >>> from pathlib import Path
            >>> store = StoreFactory.create("parquet", Path("./data"))
        """
        from qldata.stores.databases.duckdb_store import DuckDBStore
        from qldata.stores.databases.sqlite_store import SQLiteStore
        from qldata.stores.files.csv_store import CSVStore
        from qldata.stores.files.parquet_store import ParquetStore

        stores = {
            "parquet": lambda: ParquetStore(str(data_dir)),
            "csv": lambda: CSVStore(str(data_dir)),
            "sqlite": lambda: SQLiteStore(str(data_dir / "qldata.db")),
            "duckdb": lambda: DuckDBStore(str(data_dir / "qldata.duckdb")),
        }

        if store_type not in stores:
            raise ValueError(
                f"Unknown store type: {store_type}. " f"Supported types: {', '.join(stores.keys())}"
            )

        return stores[store_type]()

    @staticmethod
    def create_from_config(config: "ConfigManager") -> DataStore:  # type: ignore  # noqa: F821
        """Create a store using configuration settings.

        Args:
            config: Configuration manager instance

        Returns:
            DataStore configured from config

        Example:
            >>> from qldata.config import get_config
            >>> config = get_config()
            >>> store = StoreFactory.create_from_config(config)
        """
        return StoreFactory.create(
            store_type=config.get_store_type(),  # type: ignore
            data_dir=config.get_data_dir(),  # type: ignore
        )


__all__ = ["StoreFactory", "StoreType"]
