"""Convenient, stable transform exports."""

import pandas as pd

from qldata.models.timeframe import Timeframe
from qldata.transforms.align import fill_backward, fill_forward, fill_interpolate
from qldata.transforms.clean import remove_duplicates, remove_invalid_prices, remove_outliers
from qldata.transforms.core import TransformPipeline
from qldata.transforms.resample import resample_bars, ticks_to_bars


def resample(
    data: pd.DataFrame, from_timeframe: str | Timeframe, to_timeframe: str | Timeframe
) -> pd.DataFrame:
    """Convenience wrapper around resample_bars with string or Timeframe inputs."""
    from_tf = (
        Timeframe.from_string(from_timeframe) if isinstance(from_timeframe, str) else from_timeframe
    )
    to_tf = Timeframe.from_string(to_timeframe) if isinstance(to_timeframe, str) else to_timeframe
    return resample_bars(data, from_tf, to_tf)


__all__ = [
    "TransformPipeline",
    "remove_duplicates",
    "remove_outliers",
    "remove_invalid_prices",
    "resample_bars",
    "resample",
    "ticks_to_bars",
    "fill_forward",
    "fill_backward",
    "fill_interpolate",
]
