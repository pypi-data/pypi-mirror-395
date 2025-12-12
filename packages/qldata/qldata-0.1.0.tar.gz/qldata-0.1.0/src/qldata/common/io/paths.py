"""Path handling utilities."""

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """Ensure directory exists, create if necessary.

    Args:
        path: Directory path

    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_path(path: str | Path) -> Path:
    """Normalize path to absolute Path object.

    Args:
        path: Input path

    Returns:
        Absolute Path object
    """
    return Path(path).resolve()
