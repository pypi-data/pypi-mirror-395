"""CSV file store implementation (flat files per symbol/timeframe)."""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd

from qldata.common.dataframe.timestamps import TimestampOps
from qldata.common.strings import sanitize_symbol
from qldata.errors.data import NoDataFound
from qldata.errors.store import StoreReadError, StoreWriteError
from qldata.models.timeframe import Timeframe


class CSVStore:
    """Store data in a single CSV file per symbol/timeframe."""

    def __init__(self, base_dir: str) -> None:
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, symbol: str, timeframe: Timeframe) -> Path:
        safe_symbol = sanitize_symbol(symbol)
        return self._base_dir / f"{safe_symbol}_{timeframe}.csv"

    def write_bars(
        self,
        symbol: str,
        data: pd.DataFrame,
        timeframe: Timeframe,
    ) -> None:
        try:
            data = TimestampOps.ensure_datetime_index(data)
            path = self._file_path(symbol, timeframe)

            if path.exists():
                try:
                    existing = pd.read_csv(path, index_col=0, parse_dates=True)
                    existing = TimestampOps.ensure_datetime_index(existing)
                    data = pd.concat([existing, data])
                    data = TimestampOps.remove_duplicate_timestamps(data, keep="last")
                    data = TimestampOps.sort_by_timestamp(data)
                except Exception as read_err:
                    raise StoreWriteError(
                        f"Corrupted CSV file at {path}. Delete or repair the file and retry."
                    ) from read_err

            tmp_path = path.with_suffix(path.suffix + ".tmp")
            data.to_csv(tmp_path)
            os.replace(tmp_path, path)
        except Exception as e:
            raise StoreWriteError(f"Failed to write data for {symbol}: {e}") from e

    def read_bars(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
    ) -> pd.DataFrame:
        try:
            path = self._file_path(symbol, timeframe)
            if not path.exists():
                raise NoDataFound(f"No data found for {symbol} ({timeframe})")

            try:
                data = pd.read_csv(path, index_col=0, parse_dates=True)
                data = TimestampOps.ensure_datetime_index(data)
                data = TimestampOps.filter_date_range(data, start, end)
            except Exception as read_err:
                raise StoreReadError(
                    f"CSV file at {path} may be corrupted. Delete or repair the file and retry."
                ) from read_err

            if data.empty:
                raise NoDataFound(
                    f"No data found for {symbol} ({timeframe}) between {start} and {end}"
                )

            return TimestampOps.sort_by_timestamp(data)
        except NoDataFound:
            raise
        except Exception as e:
            raise StoreReadError(f"Failed to read data for {symbol}: {e}") from e

    def has_data(self, symbol: str, timeframe: Timeframe) -> bool:
        return self._file_path(symbol, timeframe).exists()

    def delete_data(self, symbol: str, timeframe: Timeframe) -> None:
        path = self._file_path(symbol, timeframe)
        if path.exists():
            path.unlink()


__all__ = ["CSVStore"]
