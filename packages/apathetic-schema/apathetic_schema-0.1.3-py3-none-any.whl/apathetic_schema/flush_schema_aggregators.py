# src/apathetic_schema/flush_schema_aggregators.py
"""Schema aggregator flushing functionality for Apathetic Schema."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .collect_msg import ApatheticSchema_Internal_CollectMsg
from .constants import ApatheticSchema_Internal_Constants


if TYPE_CHECKING:
    from .types import (
        ApatheticSchema_SchemaErrorAggregator,
        ApatheticSchema_ValidationSummary,
    )


class ApatheticSchema_Internal_FlushSchemaAggregators:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides schema aggregator flushing functionality.

    This class contains the flush_schema_aggregators function for flushing
    aggregated validation messages. When mixed into apathetic_schema, it
    provides the flush_schema_aggregators method.
    """

    @staticmethod
    def flush_schema_aggregators(
        *,
        summary: ApatheticSchema_ValidationSummary,
        agg: ApatheticSchema_SchemaErrorAggregator,
    ) -> None:
        """Flush aggregated schema validation messages to the summary.

        Args:
            summary: Validation summary to modify in-place
            agg: Schema error aggregator containing grouped messages
        """

        def _clean_context(ctx: str) -> str:
            """Normalize context strings by removing leading 'in' or 'on'."""
            ctx = ctx.strip()
            for prefix in ("in ", "on "):
                if ctx.lower().startswith(prefix):
                    return ctx[len(prefix) :].strip()
            return ctx

        def _flush_one(
            bucket: dict[str, dict[str, Any]],
            *,
            strict: bool,
        ) -> None:
            for tag, entry in bucket.items():
                msg_tmpl = entry["msg"]
                contexts = [_clean_context(c) for c in entry["contexts"]]
                joined_ctx = ", ".join(contexts)
                rendered = msg_tmpl.format(keys=tag, ctx=f"in {joined_ctx}")
                ApatheticSchema_Internal_CollectMsg.collect_msg(
                    rendered, strict=strict, summary=summary
                )
            bucket.clear()

        strict_bucket = agg.get(ApatheticSchema_Internal_Constants.AGG_STRICT_WARN, {})
        warn_bucket = agg.get(ApatheticSchema_Internal_Constants.AGG_WARN, {})

        if strict_bucket:
            summary.valid = False
            _flush_one(strict_bucket, strict=True)
        if warn_bucket:
            _flush_one(warn_bucket, strict=False)
