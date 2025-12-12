"""Default configuration values."""

# Data storage
DEFAULT_DATA_DIR = "./data"
DEFAULT_STORE_TYPE = "parquet"  # parquet, csv, sqlite
DATA_VERSION = "1.0.0"
METADATA_FILENAME = ".qldata_meta.json"

# Validation
VALIDATION_ENABLED = False

# Caching
CACHE_ENABLED = True
CACHE_MAX_SIZE = 1000  # Number of items to cache

# Logging
LOG_LEVEL = "INFO"
