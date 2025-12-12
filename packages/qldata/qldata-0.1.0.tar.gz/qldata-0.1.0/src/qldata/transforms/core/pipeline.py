"""Transform pipeline for composing data transformations."""

from collections.abc import Callable

import pandas as pd

from qldata.logging import get_logger

logger = get_logger(__name__)


class TransformPipeline:
    """Pipeline for composing multiple data transforms.

    Allows chaining transforms and applying them in sequence.
    """

    def __init__(self, name: str = "pipeline") -> None:
        """Initialize pipeline.

        Args:
            name: Pipeline name for logging
        """
        self.name = name
        self._transforms: list[Callable[[pd.DataFrame], pd.DataFrame]] = []

    def add(
        self, transform: Callable[[pd.DataFrame], pd.DataFrame], name: str | None = None
    ) -> "TransformPipeline":
        """Add a transform to the pipeline.

        Args:
            transform: Function that takes DataFrame and returns DataFrame
            name: Optional name for logging

        Returns:
            Self for method chaining
        """
        self._transforms.append(transform)
        transform_name = name or getattr(transform, "__name__", "transform")
        logger.debug(f"Added transform '{transform_name}' to pipeline '{self.name}'")
        return self

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        """Execute all transforms in sequence.

        Args:
            data: Input DataFrame

        Returns:
            Transformed DataFrame
        """
        result = data.copy()

        for i, transform in enumerate(self._transforms):
            transform_name = getattr(transform, "__name__", f"transform_{i}")
            logger.debug(f"Executing transform '{transform_name}' in pipeline '{self.name}'")

            try:
                result = transform(result)
            except Exception as e:
                logger.error(f"Transform '{transform_name}' failed: {e}")
                raise

        return result

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        """Make pipeline callable.

        Args:
            data: Input DataFrame

        Returns:
            Transformed DataFrame
        """
        return self.execute(data)

    def __len__(self) -> int:
        """Get number of transforms in pipeline."""
        return len(self._transforms)
