"""Gap detection and handling."""

from qldata.validation.gaps.detector import Gap, count_gaps, detect_gaps, has_gaps
from qldata.validation.gaps.handler import fill_gaps, remove_gaps

__all__ = [
    "Gap",
    "detect_gaps",
    "count_gaps",
    "has_gaps",
    "fill_gaps",
    "remove_gaps",
]
