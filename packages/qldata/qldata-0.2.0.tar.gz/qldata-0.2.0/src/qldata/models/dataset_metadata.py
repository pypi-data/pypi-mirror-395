"""Dataset metadata model for tracking stored data."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from qldata.models.timeframe import Timeframe


@dataclass
class DatasetMetadata:
    """Metadata about a stored dataset.

    Tracks important information about currently stored data to enable:
    - Smart cache invalidation
    - Data quality monitoring
    - Usage analytics
    - Dataset discovery

    Attributes:
        symbol: Trading symbol/ticker
        timeframe: Bar timeframe
        source: Data source name (e.g., "binance", "bybit")
        first_timestamp: Earliest timestamp in dataset
        last_timestamp: Latest timestamp in dataset
        record_count: Total number of records
        last_updated: When this dataset was last written
        quality_score: Optional data quality score (0.0-1.0)
        checksum: Optional data checksum for integrity verification
    """

    symbol: str
    timeframe: Timeframe
    source: str
    first_timestamp: datetime
    last_timestamp: datetime
    record_count: int
    last_updated: datetime
    quality_score: float | None = None
    checksum: str | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary with all fields serialized to JSON-compatible types
        """
        d = asdict(self)
        d["timeframe"] = str(self.timeframe)
        d["first_timestamp"] = self.first_timestamp.isoformat()
        d["last_timestamp"] = self.last_timestamp.isoformat()
        d["last_updated"] = self.last_updated.isoformat()
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "DatasetMetadata":
        """Create from dictionary.

        Args:
            data: Dictionary with metadata fields

        Returns:
            DatasetMetadata instance
        """
        data = data.copy()
        data["timeframe"] = Timeframe.from_string(data["timeframe"])
        data["first_timestamp"] = datetime.fromisoformat(data["first_timestamp"])
        data["last_timestamp"] = datetime.fromisoformat(data["last_timestamp"])
        data["last_updated"] = datetime.fromisoformat(data["last_updated"])
        return cls(**data)

    def is_stale(self, max_age_hours: int = 24) -> bool:
        """Check if dataset is stale and should be refreshed.

        Args:
            max_age_hours: Maximum age in hours before considering stale

        Returns:
            True if data is older than max_age_hours
        """
        # Compare using a consistent timezone to avoid naive/aware errors
        now = datetime.now(self.last_updated.tzinfo) if self.last_updated.tzinfo else datetime.now(
            timezone.utc
        )
        age = now - (
            self.last_updated if self.last_updated.tzinfo else self.last_updated.replace(tzinfo=timezone.utc)
        )
        return age.total_seconds() > (max_age_hours * 3600)

    def covers_range(self, start: datetime, end: datetime) -> bool:
        """Check if dataset covers a requested time range.

        Args:
            start: Requested start time
            end: Requested end time

        Returns:
            True if dataset fully covers the requested range
        """
        return self.first_timestamp <= start and self.last_timestamp >= end
