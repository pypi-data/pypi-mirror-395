"""SQLite database store implementation."""

import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

from qldata.errors.data import NoDataFound
from qldata.errors.store import StoreReadError, StoreWriteError
from qldata.models.timeframe import Timeframe
from qldata.stores.base.store import DataStore


class SQLiteStore(DataStore):
    """Store data in SQLite database."""

    def __init__(self, db_path: str) -> None:
        """Initialize SQLite store.

        Args:
            db_path: Path to SQLite database file
        """
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS bars (
                    symbol TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    PRIMARY KEY (symbol, timeframe, timestamp)
                )
                """
            )

            # Create indexes for common queries
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_bars_symbol_timeframe
                ON bars (symbol, timeframe)
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_bars_timestamp
                ON bars (timestamp)
                """
            )

    def write_bars(
        self,
        symbol: str,
        data: pd.DataFrame,
        timeframe: Timeframe,
    ) -> None:
        """Write bar data to SQLite database.

        Args:
            symbol: Symbol ticker
            data: DataFrame with OHLCV data (indexed by timestamp)
            timeframe: Bar timeframe
        """
        try:
            # Prepare data for insert
            data_copy = data.copy()
            data_copy["symbol"] = symbol
            data_copy["timeframe"] = str(timeframe)
            data_copy = data_copy.reset_index()

            # Write to database (replace on conflict)
            with sqlite3.connect(self._db_path) as conn:
                # Remove any overlapping rows to avoid PK conflicts and duplicate data
                start = data_copy["timestamp"].min()
                end = data_copy["timestamp"].max()
                conn.execute(
                    """
                    DELETE FROM bars
                    WHERE symbol = ?
                      AND timeframe = ?
                      AND timestamp >= ?
                      AND timestamp <= ?
                    """,
                    (symbol, str(timeframe), start, end),
                )

                data_copy.to_sql(
                    "bars",
                    conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                )

        except Exception as e:
            raise StoreWriteError(f"Failed to write data for {symbol}: {e}") from e

    def read_bars(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
    ) -> pd.DataFrame:
        """Read bar data from SQLite database.

        Args:
            symbol: Symbol ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe

        Returns:
            DataFrame with OHLCV data
        """
        try:
            query = """
                SELECT timestamp, open, high, low, close, volume
                FROM bars
                WHERE symbol = ?
                  AND timeframe = ?
                  AND timestamp >= ?
                  AND timestamp <= ?
                ORDER BY timestamp
            """

            with sqlite3.connect(self._db_path) as conn:
                data = pd.read_sql_query(
                    query,
                    conn,
                    params=(symbol, str(timeframe), start, end),
                    parse_dates=["timestamp"],
                )

            if data.empty:
                raise NoDataFound(
                    f"No data found for {symbol} ({timeframe}) between {start} and {end}"
                )

            data.set_index("timestamp", inplace=True)
            return data

        except NoDataFound:
            raise
        except Exception as e:
            raise StoreReadError(f"Failed to read data for {symbol}: {e}") from e

    def has_data(self, symbol: str, timeframe: Timeframe) -> bool:
        """Check if store has data for symbol/timeframe.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe

        Returns:
            True if data exists
        """
        query = """
            SELECT COUNT(*) as count
            FROM bars
            WHERE symbol = ? AND timeframe = ?
        """

        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(query, (symbol, str(timeframe)))
            count = int(cursor.fetchone()[0])

        return count > 0

    def delete_data(self, symbol: str, timeframe: Timeframe) -> None:
        """Delete all data for symbol/timeframe.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe
        """
        query = "DELETE FROM bars WHERE symbol = ? AND timeframe = ?"

        with sqlite3.connect(self._db_path) as conn:
            conn.execute(query, (symbol, str(timeframe)))
