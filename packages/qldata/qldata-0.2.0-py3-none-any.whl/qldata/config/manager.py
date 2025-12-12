# src/qldata/config/manager.py
"""Configuration manager with validation."""

from pathlib import Path
from typing import Any

from qldata.config import defaults
from qldata.errors.base import ConfigurationError


class ConfigManager:
    """Global configuration manager with validation (singleton pattern).

    Provides validated configuration management with proper error handling.
    """

    def __init__(self) -> None:
        """Initialize with default values."""
        self._data_dir: str = str(self._resolve_data_dir(defaults.DEFAULT_DATA_DIR))
        self._store_type: str = defaults.DEFAULT_STORE_TYPE
        self._cache_enabled: bool = defaults.CACHE_ENABLED
        self._cache_max_size: int = defaults.CACHE_MAX_SIZE
        self._validate_enabled: bool = defaults.VALIDATION_ENABLED
        self._source_instance: Any = None
        self._store_instance: Any = None
        self._sync_metadata()

    def set(
        self,
        data_dir: str | None = None,
        store_type: str | None = None,
        cache: bool | None = None,
        cache_size: int | None = None,
        validate: bool | None = None,
    ) -> None:
        """Update configuration values with validation.

        Args:
            data_dir: Directory for data storage
            store_type: Type of store to use (parquet, csv, sqlite, duckdb)
            cache: Enable/disable caching
            cache_size: Maximum cache entries when caching is enabled
            validate: Enable/disable validation

        Raises:
            ConfigurationError: If validation fails
        """
        metadata_dirty = False

        if data_dir is not None:
            resolved = self._validate_data_dir(data_dir)
            self._data_dir = str(resolved)
            # Reset instances when data_dir changes
            self._source_instance = None
            self._store_instance = None
            metadata_dirty = True

        if store_type is not None:
            self._validate_store_type(store_type)
            self._store_type = store_type
            # Reset instances when store_type changes
            self._source_instance = None
            self._store_instance = None
            metadata_dirty = True

        if cache is not None:
            if not isinstance(cache, bool):
                raise ConfigurationError(f"cache must be bool, got {type(cache)}")
            self._cache_enabled = cache
            self._source_instance = None

        if cache_size is not None:
            if not isinstance(cache_size, int) or cache_size <= 0:
                raise ConfigurationError(f"cache_size must be positive int, got {cache_size!r}")
            self._cache_max_size = cache_size
            self._source_instance = None

        if validate is not None:
            if not isinstance(validate, bool):
                raise ConfigurationError(f"validate must be bool, got {type(validate)}")
            self._validate_enabled = validate

        if metadata_dirty:
            self._sync_metadata()

    def _validate_data_dir(self, data_dir: str) -> Path:
        """Validate data directory.

        Args:
            data_dir: Directory path to validate

        Raises:
            ConfigurationError: If validation fails
        """
        if not isinstance(data_dir, str):
            raise ConfigurationError(f"data_dir must be str, got {type(data_dir)}")

        path = self._resolve_data_dir(data_dir)

        # Try to create directory if it doesn't exist and check writability
        try:
            path.mkdir(parents=True, exist_ok=True)
            test_file = path / ".qldata_write_test"
            test_file.write_text("ok")
            test_file.unlink(missing_ok=True)
        except Exception as e:
            raise ConfigurationError(f"Cannot write to data_dir '{path}': {e}") from e

        if not path.is_dir():
            raise ConfigurationError(f"data_dir must be a directory: {path}")

        return path

    @staticmethod
    def _resolve_data_dir(data_dir: str) -> Path:
        """Normalize data directory to an absolute path."""
        return Path(data_dir).expanduser().resolve()

    def _metadata_path(self) -> Path:
        """Location of metadata sidecar file."""
        return self.get_data_dir() / defaults.METADATA_FILENAME

    def _sync_metadata(self) -> None:
        """Metadata sidecar disabled (no-op)."""
        return

    def _validate_store_type(self, store_type: str) -> None:
        """Validate store type.

        Args:
            store_type: Store type to validate

        Raises:
            ConfigurationError: If validation fails
        """
        valid_types = ["parquet", "csv", "sqlite", "duckdb"]

        if not isinstance(store_type, str):
            raise ConfigurationError(f"store_type must be str, got {type(store_type)}")

        if store_type not in valid_types:
            raise ConfigurationError(
                f"Invalid store type '{store_type}'. Must be one of: {valid_types}"
            )

        # Check if dependencies are available
        if store_type == "parquet":
            try:
                import pyarrow  # noqa: F401
            except ImportError as e:
                raise ConfigurationError(
                    "Parquet store requires pyarrow. Install with: pip install pyarrow"
                ) from e

        elif store_type == "duckdb":
            try:
                import duckdb  # noqa: F401
            except ImportError as e:
                raise ConfigurationError(
                    "DuckDB store requires duckdb. Install with: pip install duckdb"
                ) from e

    def get_data_dir(self) -> Path:
        """Get data directory path.

        Returns:
            Path to data directory
        """
        return Path(self._data_dir)

    def get_store_type(self) -> str:
        """Get configured store type.

        Returns:
            Store type string
        """
        return self._store_type

    def is_cache_enabled(self) -> bool:
        """Check if caching is enabled.

        Returns:
            True if caching is enabled
        """
        return self._cache_enabled

    def is_validation_enabled(self) -> bool:
        """Check if validation is enabled.

        Returns:
            True if validation is enabled
        """
        return self._validate_enabled

    def get_default_store(self) -> Any:
        """Get the configured data store.

        Returns:
            DataStore instance

        Raises:
            ConfigurationError: If store creation fails
        """
        if self._store_instance is None:
            self._store_instance = self._create_store()
        return self._store_instance

    def get_default_source(self) -> Any:
        """Get the configured data source.

        Returns:
            DataStore or cached wrapper

        Raises:
            ConfigurationError: If source creation fails
        """
        if self._source_instance is None:
            self._source_instance = self._create_source()
        return self._source_instance

    def _create_store(self) -> Any:
        """Factory method to create store based on config.

        Returns:
            DataStore instance

        Raises:
            ConfigurationError: If store creation fails
        """
        try:
            self._sync_metadata()

            if self._store_type == "parquet":
                from qldata.stores.files.parquet_store import ParquetStore

                return ParquetStore(str(self.get_data_dir()))

            elif self._store_type == "csv":
                from qldata.stores.files.csv_store import CSVStore

                return CSVStore(str(self.get_data_dir()))

            elif self._store_type == "sqlite":
                from qldata.stores.databases.sqlite_store import SQLiteStore

                return SQLiteStore(str(self.get_data_dir() / "qldata.db"))

            elif self._store_type == "duckdb":
                from qldata.stores.databases.duckdb_store import DuckDBStore

                return DuckDBStore(str(self.get_data_dir() / "qldata.duckdb"))

            else:
                raise ConfigurationError(f"Unknown store type: {self._store_type}")

        except ImportError as e:
            raise ConfigurationError(f"Failed to import store '{self._store_type}': {e}") from e
        except Exception as e:
            raise ConfigurationError(f"Failed to create store '{self._store_type}': {e}") from e

    def _create_source(self) -> Any:
        """Factory method to create source based on config.

        Returns store with optional caching wrapper.

        Returns:
            DataStore or cached wrapper

        Raises:
            ConfigurationError: If source creation fails
        """
        try:
            store = self.get_default_store()

            # Wrap with cache if enabled
            if self._cache_enabled:
                from qldata.common import MemoryCache

                return MemoryCache(store, max_size=self._cache_max_size)

            return store

        except Exception as e:
            raise ConfigurationError(f"Failed to create data source: {e}") from e

    def validate_config(self) -> dict[str, Any]:
        """Validate current configuration.

        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Check data directory
        try:
            self._validate_data_dir(self._data_dir)
        except ConfigurationError as e:
            results["valid"] = False
            results["errors"].append(f"Data directory: {e}")

        # Check store type
        try:
            self._validate_store_type(self._store_type)
        except ConfigurationError as e:
            results["valid"] = False
            results["errors"].append(f"Store type: {e}")

        # Check metadata consistency
        try:
            self._sync_metadata()
        except ConfigurationError as e:
            results["valid"] = False
            results["errors"].append(f"Metadata: {e}")

        # Check if store can be created
        try:
            self.get_default_store()
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Store creation: {e}")

        # Check if source can be created
        try:
            self.get_default_source()
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Source creation: {e}")

        return results

    def get_config_dict(self) -> dict[str, Any]:
        """Get current configuration as dictionary.

        Returns:
            Dictionary with current settings
        """
        return {
            "data_dir": self._data_dir,
            "store_type": self._store_type,
            "cache_enabled": self._cache_enabled,
            "cache_size": self._cache_max_size,
            "validate_enabled": self._validate_enabled,
        }

    def __repr__(self) -> str:
        """String representation."""
        config = self.get_config_dict()
        items = [f"{k}={v!r}" for k, v in config.items()]
        return f"ConfigManager({', '.join(items)})"


# Global singleton instance
_config = ConfigManager()


def get_config() -> ConfigManager:
    """Get global configuration instance.

    Returns:
        ConfigManager singleton
    """
    return _config
