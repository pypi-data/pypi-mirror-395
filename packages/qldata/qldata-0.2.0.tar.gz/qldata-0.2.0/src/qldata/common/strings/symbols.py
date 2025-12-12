"""Symbol normalization utilities."""

import re
from typing import cast


def normalize_symbol(symbol: str | list[str]) -> str | list[str]:
    """Normalize symbol format.

    - Convert to uppercase
    - Strip whitespace
    - Handle lists recursively

    Args:
        symbol: Symbol string or list of symbol strings

    Returns:
        Normalized symbol(s)
    """
    if isinstance(symbol, list):
        return [s.strip().upper() for s in symbol]

    return symbol.strip().upper()


def sanitize_symbol(symbol: str) -> str:
    """Convert a symbol into a filesystem-safe token.

    Replaces non-alphanumeric characters with underscores after uppercasing.
    """
    normalized = cast(str, normalize_symbol(symbol))
    return re.sub(r"[^A-Z0-9_-]", "_", normalized)
