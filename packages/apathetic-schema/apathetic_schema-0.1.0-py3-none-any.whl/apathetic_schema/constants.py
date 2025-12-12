# src/apathetic_schema/constants.py
"""Constants for Apathetic Schema."""

from __future__ import annotations

from typing import ClassVar


class ApatheticSchema_Internal_Constants:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Constants for apathetic schema functionality.

    This class contains all constant values used by apathetic_schema.
    It's kept separate for organizational purposes.
    """

    # Default cutoff for similarity matching in error hints
    DEFAULT_HINT_CUTOFF: ClassVar[float] = 0.75

    # Aggregator severity bucket names
    AGG_STRICT_WARN: ClassVar[str] = "strict_warnings"
    AGG_WARN: ClassVar[str] = "warnings"
