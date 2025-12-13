# src/apathetic_schema/collect_msg.py
"""Message collection functionality for Apathetic Schema."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .types import ApatheticSchema_ValidationSummary


class ApatheticSchema_Internal_CollectMsg:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides message collection functionality.

    This class contains the collect_msg function for routing validation
    messages to appropriate buckets (errors, strict_warnings, warnings).
    When mixed into apathetic_schema, it provides the collect_msg method.
    """

    @staticmethod
    def collect_msg(
        msg: str,
        *,
        strict: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        is_error: bool = False,
    ) -> None:
        """Route a message to the appropriate bucket.

        Errors are always fatal.
        Warnings may escalate to strict_warnings in strict mode.

        Args:
            msg: The message to collect
            strict: Whether strict mode is enabled
            summary: Validation summary to modify in-place
            is_error: Whether this is an error (always fatal)
        """
        if is_error:
            summary.errors.append(msg)
        elif strict:
            summary.strict_warnings.append(msg)
        else:
            summary.warnings.append(msg)
