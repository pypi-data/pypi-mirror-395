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


# --- Dataclasses --------------------------------------------------------


@dataclass
class ApatheticSchema_ValidationSummary:  # noqa: N801
    """Validation summary dataclass.

    Tracks validation results including errors, warnings, and strict warnings.
    """

    valid: bool
    errors: list[str]
    strict_warnings: list[str]
    warnings: list[str]
    strict: bool  # strictness somewhere in our config?
