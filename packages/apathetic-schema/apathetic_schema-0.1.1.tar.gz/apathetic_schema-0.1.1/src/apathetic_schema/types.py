# src/apathetic_schema/types.py
"""Type definitions for Apathetic Schema."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias, TypedDict


# --- TypedDict definitions ---------------------------------------------


class ApatheticSchema_SchErrAggEntry(TypedDict):  # noqa: N801
    """Type for schema error aggregator entries."""

    msg: str
    contexts: list[str]


# --- Type aliases -------------------------------------------------------

# Type alias for schema error aggregator
# Structure: dict[severity, dict[tag, dict[key, SchErrAggEntry]]]
# Example:
# {
#   "strict_warnings": {
#       "dry-run": {"msg": DRYRUN_MSG, "contexts": ["in build #0", "in build #2"]},
#       ...
#   },
#   "warnings": { ... }
# }
ApatheticSchema_SchemaErrorAggregator: TypeAlias = dict[
    str, dict[str, dict[str, ApatheticSchema_SchErrAggEntry]]
]


class ApatheticSchema_Internal_Types:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides type definitions for Apathetic Schema.

    This class contains type aliases and dataclasses used throughout the
    apathetic_schema namespace. When mixed into apathetic_schema, it provides
    access to these types via the namespace class.
    """

    # --- Dataclasses --------------------------------------------------------

    @dataclass
    class ValidationSummary:
        """Validation summary dataclass.

        Tracks validation results including errors, warnings, and strict warnings.
        """

        valid: bool
        errors: list[str]
        strict_warnings: list[str]
        warnings: list[str]
        strict: bool  # strictness somewhere in our config?


# --- Module-level exports for external use ---------------------------------

# Export types with ApatheticSchema_ prefix for external packages
# (e.g., serger) that import directly from types module
# Note: ApatheticSchema_SchErrAggEntry and ApatheticSchema_SchemaErrorAggregator
# are already defined above with the correct prefix
ApatheticSchema_ValidationSummary = ApatheticSchema_Internal_Types.ValidationSummary
