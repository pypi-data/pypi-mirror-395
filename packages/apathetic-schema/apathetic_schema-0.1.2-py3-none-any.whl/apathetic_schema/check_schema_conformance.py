# src/apathetic_schema/check_schema_conformance.py
"""Schema conformance checking functionality for Apathetic Schema."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict

from .validate_typed_dict import ApatheticSchema_Internal_ValidateTypedDict


if TYPE_CHECKING:
    from .types import ApatheticSchema_ValidationSummary


class ApatheticSchema_Internal_CheckSchemaConformance:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides schema conformance checking functionality.

    This class contains the check_schema_conformance function for validating
    configurations against schemas. When mixed into apathetic_schema, it
    provides the check_schema_conformance method.
    """

    @staticmethod
    def check_schema_conformance(
        cfg: dict[str, Any],
        schema: dict[str, Any],
        context: str,
        *,
        strict_config: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        prewarn: set[str] | None = None,
        ignore_keys: set[str] | None = None,
        base_path: str = "root",
        field_examples: dict[str, str] | None = None,
    ) -> bool:
        """Thin wrapper around validate_typed_dict for root-level schema checks.

        Args:
            cfg: Configuration dictionary to validate
            schema: Schema dictionary defining expected structure
            context: Context string for error messages
            strict_config: Whether strict mode is enabled
            summary: Validation summary to modify in-place
            prewarn: Optional set of keys to pre-warn about
            ignore_keys: Optional set of keys to ignore during validation
            base_path: Base path for field examples (default: "root")
            field_examples: Optional dict mapping field patterns to example values

        Returns:
            True if validation passed, False otherwise
        """
        if prewarn is None:
            prewarn = set()
        if ignore_keys is None:
            ignore_keys = set()

        # Pretend schema is a TypedDict for uniformity
        class _AnonTypedDict(TypedDict):
            pass

        # Attach the schema dynamically to mimic schema_from_typeddict output
        _AnonTypedDict.__annotations__ = schema

        return ApatheticSchema_Internal_ValidateTypedDict.validate_typed_dict(
            context,
            cfg,
            _AnonTypedDict,
            strict=strict_config,
            summary=summary,
            prewarn=prewarn,
            ignore_keys=ignore_keys,
            field_path=base_path,
            field_examples=field_examples,
        )
