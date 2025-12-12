"""Tests for dataset metadata tracking."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

from qldata.models.dataset_metadata import DatasetMetadata
from qldata.models.timeframe import Timeframe
from qldata.stores.files.parquet_store import ParquetStore


class TestDatasetMetadata:
    """Test DatasetMetadata model."""

    def test_metadata_creation(self):
        """Test creating metadata instance."""
        meta = DatasetMetadata(
            symbol="BTCUSDT",
            timeframe=Timeframe.HOUR_1,
            source="binance",
            first_timestamp=datetime(2024, 1, 1),
            last_timestamp=datetime(2024, 12, 31),
            record_count=8760,
            last_updated=datetime.now(),
        )

        assert meta.symbol == "BTCUSDT"
        assert meta.timeframe == Timeframe.HOUR_1
        assert meta.source == "binance"
        assert meta.record_count == 8760

    def test_metadata_serialization(self):
        """Test metadata to_dict and from_dict."""
        meta = DatasetMetadata(
            symbol="ETHUSDT",
            timeframe=Timeframe.DAY_1,
            source="bybit",
            first_timestamp=datetime(2024, 1, 1),
            last_timestamp=datetime(2024, 12, 31),
            record_count=365,
            last_updated=datetime.now(),
            quality_score=0.95,
        )

        # Serialize
        data_dict = meta.to_dict()
        assert data_dict["symbol"] == "ETHUSDT"
        assert data_dict["quality_score"] == 0.95

        # Deserialize
        meta2 = DatasetMetadata.from_dict(data_dict)
        assert meta2.symbol == meta.symbol
        assert meta2.quality_score == meta.quality_score

    def test_is_stale(self):
        """Test staleness checking."""
        # Fresh data
        fresh = DatasetMetadata(
            symbol="TEST",
            timeframe=Timeframe.HOUR_1,
            source="test",
            first_timestamp=datetime.now(),
            last_timestamp=datetime.now(),
            record_count=100,
            last_updated=datetime.now(),
        )
        assert not fresh.is_stale(max_age_hours=24)

        # Stale data
        stale = DatasetMetadata(
            symbol="TEST",
            timeframe=Timeframe.HOUR_1,
            source="test",
            first_timestamp=datetime.now() - timedelta(days=10),
            last_timestamp=datetime.now() - timedelta(days=10),
            record_count=100,
            last_updated=datetime.now() - timedelta(days=10),
        )
        assert stale.is_stale(max_age_hours=24)

    def test_covers_range(self):
        """Test range coverage checking."""
        meta = DatasetMetadata(
            symbol="TEST",
            timeframe=Timeframe.HOUR_1,
            source="test",
            first_timestamp=datetime(2024, 1, 1),
            last_timestamp=datetime(2024, 12, 31),
            record_count=8760,
            last_updated=datetime.now(),
        )

        # Covered range
        assert meta.covers_range(datetime(2024, 6, 1), datetime(2024, 7, 1))

        # Not covered (before start)
        assert not meta.covers_range(datetime(2023, 12, 1), datetime(2024, 1, 15))

        # Not covered (after end)
        assert not meta.covers_range(datetime(2024, 12, 15), datetime(2025, 1, 15))


class TestParquetStoreMetadata:
    """Test metadata tracking in ParquetStore."""

    def test_metadata_written_on_save(self):
        """Test that metadata is automatically written when saving data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ParquetStore(tmpdir)

            # Create test data
            dates = pd.date_range("2024-01-01", periods=100, freq="1h")
            df = pd.DataFrame(
                {
                    "open": 100.0,
                    "high": 101.0,
                    "low": 99.0,
                    "close": 100.5,
                    "volume": 1000.0,
                },
                index=dates,
            )

            # Write data
            store.write_bars("BTCUSDT", df, Timeframe.HOUR_1, source="binance")

            # Metadata should exist
            metadata_file = Path(tmpdir) / ".metadata" / "BTCUSDT_1h.json"
            assert metadata_file.exists()

            # Verify metadata content
            with open(metadata_file) as f:
                meta_dict = json.load(f)

            assert meta_dict["symbol"] == "BTCUSDT"
            assert meta_dict["source"] == "binance"
            assert meta_dict["record_count"] == 100

    def test_read_metadata(self):
        """Test reading metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ParquetStore(tmpdir)

            # Create and write data
            dates = pd.date_range("2024-01-01", periods=50, freq="1D")
            df = pd.DataFrame(
                {
                    "open": 100.0,
                    "high": 100.0,
                    "low": 100.0,
                    "close": 100.0,
                    "volume": 1000.0,
                },
                index=dates,
            )

            store.write_bars("ETHUSDT", df, Timeframe.DAY_1, source="bybit")

            # Read metadata
            meta = store.read_metadata("ETHUSDT", Timeframe.DAY_1)

            assert meta is not None
            assert meta.symbol == "ETHUSDT"
            assert meta.source == "bybit"
            assert meta.record_count == 50
            assert isinstance(meta.first_timestamp, datetime)

    def test_list_metadata(self):
        """Test listing all metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ParquetStore(tmpdir)

            # Write multiple datasets
            for symbol in ["BTC USD", "ETHUSDT", "SOLUSDT"]:
                dates = pd.date_range("2024-01-01", periods=10, freq="1h")
                df = pd.DataFrame(
                    {
                        "open": 1.0,
                        "high": 1.0,
                        "low": 1.0,
                        "close": 1.0,
                        "volume": 1.0,
                    },
                    index=dates,
                )
                store.write_bars(symbol, df, Timeframe.HOUR_1, source="test")

            # List all metadata
            all_meta = store.list_metadata()

            assert len(all_meta) == 3
            symbols = {m.symbol for m in all_meta}
            assert "BTCUSDT" in symbols or "BTC_USD" in symbols  # Symbol sanitization
            assert "ETHUSDT" in symbols
            assert "SOLUSDT" in symbols

    def test_metadata_deleted_with_data(self):
        """Test that metadata is deleted when data is deleted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ParquetStore(tmpdir)

            # Write data
            dates = pd.date_range("2024-01-01", periods=10, freq="1h")
            df = pd.DataFrame(
                {"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0},
                index=dates,
            )
            store.write_bars("TEST", df, Timeframe.HOUR_1, source="test")

            # Verify metadata exists
            assert store.read_metadata("TEST", Timeframe.HOUR_1) is not None

            # Delete data
            store.delete_data("TEST", Timeframe.HOUR_1)

            # Metadata should also be deleted
            assert store.read_metadata("TEST", Timeframe.HOUR_1) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
