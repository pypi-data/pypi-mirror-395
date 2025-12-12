"""Logging setup."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Get logger with consistent formatting.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
