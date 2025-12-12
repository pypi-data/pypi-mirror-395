"""DuckDB store for analytical queries."""

from datetime import datetime
from pathlib import Path

import pandas as pd

try:
    import duckdb

    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False

from qldata.models.timeframe import Timeframe
from qldata.stores.base.store import DataStore


class DuckDBStore(DataStore):
    """DuckDB-based data store for fast analytical queries.

    DuckDB is a columnar database optimized for OLAP workloads,
    making it ideal for fast aggregations and analytics.

    Example:
        >>> store = DuckDBStore("./data/market.duckdb")
        >>> store.write_bars("BTCUSDT", bars, Timeframe.HOUR_1)
        >>> data = store.read_bars("BTCUSDT", start, end, Timeframe.HOUR_1)
    """

    def __init__(self, db_path: str | Path) -> None:
        """Initialize DuckDB store.

        Args:
            db_path: Path to DuckDB database file
        """
        if not DUCKDB_AVAILABLE:
            raise ImportError("duckdb package required. Install with: pip install duckdb")

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize connection
        self._conn = duckdb.connect(str(self.db_path))
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema."""
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bars (
                symbol VARCHAR,
                timeframe VARCHAR,
                timestamp TIMESTAMP,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume BIGINT,
                PRIMARY KEY (symbol, timeframe, timestamp)
            )
        """
        )

        # Create index for faster queries
        self._conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_bars_lookup
            ON bars (symbol, timeframe, timestamp)
        """
        )

    def write_bars(
        self,
        symbol: str,
        data: pd.DataFrame,
        timeframe: Timeframe,
    ) -> None:
        """Write bar data to DuckDB.

        Args:
            symbol: Symbol ticker
            data: DataFrame with OHLCV data
            timeframe: Bar timeframe
        """
        if data.empty:
            return

        # Prepare data
        df = data.copy()
        df["symbol"] = symbol
        df["timeframe"] = str(timeframe)
        df = df.reset_index()

        # Required columns
        required = ["timestamp", "open", "high", "low", "close", "volume"]
        df = df[["symbol", "timeframe"] + required]

        # Delete existing data for this symbol/timeframe/date range
        start = df["timestamp"].min()
        end = df["timestamp"].max()

        self._conn.execute(
            """
            DELETE FROM bars
            WHERE symbol = ? AND timeframe = ?
            AND timestamp >= ? AND timestamp <= ?
        """,
            [symbol, str(timeframe), start, end],
        )

        # Insert new data
        self._conn.execute("INSERT INTO bars SELECT * FROM df")

    def read_bars(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
    ) -> pd.DataFrame:
        """Read bar data from DuckDB.

        Args:
            symbol: Symbol ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe

        Returns:
            DataFrame with OHLCV data
        """
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM bars
            WHERE symbol = ?
            AND timeframe = ?
            AND timestamp >= ?
            AND timestamp <= ?
            ORDER BY timestamp
        """

        df = self._conn.execute(query, [symbol, str(timeframe), start, end]).df()

        if not df.empty:
            df = df.set_index("timestamp")

        return df

    def has_data(self, symbol: str, timeframe: Timeframe) -> bool:
        """Check if data exists for symbol/timeframe.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe

        Returns:
            True if data exists
        """
        result = self._conn.execute(
            """
            SELECT COUNT(*) as count
            FROM bars
            WHERE symbol = ? AND timeframe = ?
        """,
            [symbol, str(timeframe)],
        ).fetchone()

        if result is None:
            return False
        return bool(result[0])

    def delete_data(self, symbol: str, timeframe: Timeframe) -> None:
        """Delete all data for symbol/timeframe.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe
        """
        self._conn.execute(
            """
            DELETE FROM bars
            WHERE symbol = ? AND timeframe = ?
        """,
            [symbol, str(timeframe)],
        )

    def query(self, sql: str) -> pd.DataFrame:
        """Execute arbitrary SQL query.

        Args:
            sql: SQL query string

        Returns:
            Query results as DataFrame

        Example:
            >>> df = store.query("SELECT * FROM bars WHERE symbol = 'BTCUSDT' LIMIT 10")
        """
        return self._conn.execute(sql).df()

    def close(self) -> None:
        """Close database connection."""
        self._conn.close()
