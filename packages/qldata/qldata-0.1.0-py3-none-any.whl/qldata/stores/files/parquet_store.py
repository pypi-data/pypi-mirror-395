"""Parquet file store implementation (flat files per symbol/timeframe)."""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from qldata.common.dataframe.timestamps import TimestampOps
from qldata.common.logger import get_logger
from qldata.common.strings import sanitize_symbol
from qldata.errors.data import NoDataFound
from qldata.errors.store import StoreReadError, StoreWriteError
from qldata.models.timeframe import Timeframe

logger = get_logger(__name__)


class ParquetStore:
    """Store data in a single Parquet file per symbol/timeframe."""

    def __init__(self, base_dir: str) -> None:
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, symbol: str, timeframe: Timeframe) -> Path:
        safe_symbol = sanitize_symbol(symbol)
        return self._base_dir / f"{safe_symbol}_{timeframe}.parquet"

    def write_bars(
        self,
        symbol: str,
        data: pd.DataFrame,
        timeframe: Timeframe,
    ) -> None:
        try:
            logger.info(f"Writing {len(data)} bars for {symbol} ({timeframe})")
            data = TimestampOps.ensure_datetime_index(data)
            path = self._file_path(symbol, timeframe)

            if path.exists():
                try:
                    existing = pd.read_parquet(path)
                    existing = TimestampOps.ensure_datetime_index(existing)
                    data = pd.concat([existing, data])
                    data = TimestampOps.remove_duplicate_timestamps(data, keep="last")
                    data = TimestampOps.sort_by_timestamp(data)
                except Exception as read_err:
                    logger.error(
                        "Existing parquet file appears corrupted for %s (%s): %s",
                        symbol,
                        timeframe,
                        read_err,
                    )
                    raise StoreWriteError(
                        f"Corrupted parquet file at {path}. Delete or repair the file and retry."
                    ) from read_err

            table = pa.Table.from_pandas(data, preserve_index=True)
            tmp_path = path.with_suffix(path.suffix + ".tmp")
            pq.write_table(table, tmp_path, compression="snappy")
            os.replace(tmp_path, path)
        except Exception as e:
            logger.error(f"Failed to write data for {symbol}: {e}", exc_info=True)
            raise StoreWriteError(f"Failed to write data for {symbol}: {e}") from e

    def read_bars(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
    ) -> pd.DataFrame:
        try:
            logger.info(f"Reading {symbol} ({timeframe}) from {start} to {end}")

            path = self._file_path(symbol, timeframe)
            if not path.exists():
                raise NoDataFound(f"No data found for {symbol} ({timeframe})")

            try:
                data = pd.read_parquet(path)
                data = TimestampOps.ensure_datetime_index(data)
                data = TimestampOps.filter_date_range(data, start, end)
            except Exception as read_err:
                logger.error(
                    "Failed to read parquet for %s (%s): %s", symbol, timeframe, read_err
                )
                raise StoreReadError(
                    f"Parquet file at {path} may be corrupted. Delete or repair the file and retry."
                ) from read_err

            if data.empty:
                raise NoDataFound(f"No data found for {symbol} ({timeframe}) between {start} and {end}")

            return TimestampOps.sort_by_timestamp(data)
        except NoDataFound:
            raise
        except Exception as e:
            logger.error(f"Failed to read data for {symbol}: {e}", exc_info=True)
            raise StoreReadError(f"Failed to read data for {symbol}: {e}") from e

    def has_data(self, symbol: str, timeframe: Timeframe) -> bool:
        return self._file_path(symbol, timeframe).exists()

    def delete_data(self, symbol: str, timeframe: Timeframe) -> None:
        path = self._file_path(symbol, timeframe)
        if path.exists():
            path.unlink()


__all__ = ["ParquetStore"]
