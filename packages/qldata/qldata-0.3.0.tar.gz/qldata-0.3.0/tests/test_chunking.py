"""Tests for automatic chunking in adapters."""

from datetime import datetime, timedelta

import pandas as pd
import pytest

from qldata.models.timeframe import Timeframe


class TestChunking:
    """Test automatic chunking for large date ranges."""

    def test_calculate_chunks(self):
        """Test chunk calculation logic."""
        from qldata.adapters.brokers.base import BaseBrokerAdapter

        # Create a dummy adapter instance
        class DummyAdapter(BaseBrokerAdapter):
            INTERVAL_MAP = {Timeframe.MIN_1: "1m"}
            MAX_BARS_PER_REQUEST = 1000

            def _fetch_data(self, symbol, start, end, interval, **kwargs):
                # Return empty DataFrame for testing
                return pd.DataFrame()

        adapter = DummyAdapter()

        # Test chunking calculation
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)  # 1 day = 1440 minutes > 1000 bars

        chunks = adapter._calculate_chunks(start, end, Timeframe.MIN_1)

        # Should split into at least 2 chunks
        assert len(chunks) >= 2

        # Verify chunks cover the full range
        assert chunks[0][0] == start
        assert chunks[-1][1] == end

        # Verify no gaps
        for i in range(len(chunks) - 1):
            assert chunks[i][1] == chunks[i + 1][0]

    def test_no_chunking_for_small_ranges(self):
        """Test that small ranges don't get chunked."""
        from qldata.adapters.brokers.base import BaseBrokerAdapter

        class DummyAdapter(BaseBrokerAdapter):
            INTERVAL_MAP = {Timeframe.HOUR_1: "1h"}
            MAX_BARS_PER_REQUEST = 1000

            def _fetch_data(self, symbol, start, end, interval, **kwargs):
                idx = pd.date_range(start, end, freq="1h")
                return pd.DataFrame({"close": range(len(idx))}, index=idx)

        adapter = DummyAdapter()

        start = datetime(2024, 1, 1)
        end = start + timedelta(hours=100)  # 100 bars < 1000

        # This should NOT trigger chunking
        df = adapter.get_bars("TEST", start, end, Timeframe.HOUR_1)

        # Should have fetched data directly
        assert not df.empty

    @pytest.mark.skip(reason="Requires live API or complex mocking")
    def test_large_range_chunking_integration(self):
        """Integration test for large range chunking."""
        pass


class TestDeduplication:
    """Test deduplication in chunked responses."""

    def test_overlapping_chunks_deduplicated(self):
        """Ensure overlapping data from chunks is deduplicated."""
        from qldata.adapters.brokers.base import BaseBrokerAdapter

        class TestAdapter(BaseBrokerAdapter):
            INTERVAL_MAP = {Timeframe.MIN_1: "1m"}
            MAX_BARS_PER_REQUEST = 100

            def _fetch_data(self, symbol, start, end, interval, **kwargs):
                # Simulate overlapping data
                idx = pd.date_range(start, end, freq="1min")
                return pd.DataFrame(
                    {"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 100.0},
                    index=idx,
                )

        adapter = TestAdapter()

        start = datetime(2024, 1, 1)
        end = start + timedelta(hours=3)  # 180 bars, will chunk

        df = adapter.get_bars("TEST", start, end, Timeframe.MIN_1)

        # Check no duplicates in index
        assert df.index.is_unique


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
