# src/apathetic_schema/warn_keys_once.py
"""Key warning functionality for Apathetic Schema."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apathetic_utils import cast_hint

from .collect_msg import ApatheticSchema_Internal_CollectMsg
from .constants import ApatheticSchema_Internal_Constants
from .types import (
    ApatheticSchema_SchemaErrorAggregator,
    ApatheticSchema_SchErrAggEntry,
)


if TYPE_CHECKING:
    from .types import ApatheticSchema_ValidationSummary


# Re-export for external packages (e.g., serger) that import from this module
__all__ = ["ApatheticSchema_SchemaErrorAggregator"]


class ApatheticSchema_Internal_WarnKeysOnce:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides key warning functionality.

    This class contains the warn_keys_once function for warning about
    known bad keys. When mixed into apathetic_schema, it provides the
    warn_keys_once method.
    """

    @staticmethod
    def warn_keys_once(
        tag: str,
        bad_keys: set[str],
        cfg: dict[str, Any],
        context: str,
        msg: str,
        *,
        strict_config: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        agg: ApatheticSchema_SchemaErrorAggregator | None,
    ) -> tuple[bool, set[str]]:
        """Warn once for known bad keys (e.g. dry-run, root-only).

        Args:
            tag: Tag for grouping warnings
            bad_keys: Set of keys that should trigger warnings
            cfg: Configuration dictionary to check
            context: Context string for the warning
            msg: Message template (supports {keys} and {ctx} placeholders)
            strict_config: Whether strict mode is enabled
            summary: Validation summary to modify in-place
            agg: Optional aggregator for collecting warnings

        Returns:
            Tuple of (valid, found_keys) where valid indicates if validation
            passed and found_keys contains the keys that were found.
        """
        valid = True

        # Normalize keys to lowercase for case-insensitive matching
        bad_keys_lower = {k.lower(): k for k in bad_keys}
        cfg_keys_lower = {k.lower(): k for k in cfg}
        found_lower = bad_keys_lower & cfg_keys_lower.keys()

        if not found_lower:
            return True, set()

        # Recover original-case keys for display
        found = {cfg_keys_lower[k] for k in found_lower}

        if agg is not None:
            # record context for later aggregation
            severity = (
                ApatheticSchema_Internal_Constants.AGG_STRICT_WARN
                if strict_config
                else ApatheticSchema_Internal_Constants.AGG_WARN
            )

            bucket = cast_hint(
                dict[str, ApatheticSchema_SchErrAggEntry],
                agg.setdefault(severity, {}),
            )

            default_entry: ApatheticSchema_SchErrAggEntry = {
                "msg": msg,
                "contexts": [],
            }
            entry = bucket.setdefault(tag, default_entry)
            entry["contexts"].append(context)
        else:
            # immediate fallback
            ApatheticSchema_Internal_CollectMsg.collect_msg(
                f"{msg.format(keys=', '.join(sorted(found)), ctx=context)}",
                strict=strict_config,
                summary=summary,
            )

        if strict_config:
            valid = False

        return valid, found
