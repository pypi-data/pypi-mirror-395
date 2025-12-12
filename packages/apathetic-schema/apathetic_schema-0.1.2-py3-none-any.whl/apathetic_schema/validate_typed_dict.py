# src/apathetic_schema/validate_typed_dict.py
"""TypedDict validation functionality for Apathetic Schema."""

from __future__ import annotations

from difflib import get_close_matches
from typing import TYPE_CHECKING, Any, cast, get_args, get_origin

from apathetic_utils import (
    cast_hint,
    fnmatchcase_portable,
    plural,
    safe_isinstance,
    schema_from_typeddict,
)
from typing_extensions import NotRequired

from .collect_msg import ApatheticSchema_Internal_CollectMsg
from .constants import ApatheticSchema_Internal_Constants


if TYPE_CHECKING:
    from .types import ApatheticSchema_ValidationSummary


class ApatheticSchema_Internal_ValidateTypedDict:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides TypedDict validation functionality.

    This class contains the validate_typed_dict function for validating
    dictionaries against TypedDict schemas. When mixed into apathetic_schema,
    it provides the validate_typed_dict method.
    """

    @staticmethod
    def _get_example_for_field(
        field_path: str,
        field_examples: dict[str, str] | None = None,
    ) -> str | None:
        """Get example for field if available in field_examples.

        Args:
            field_path: The full field path
                (e.g. "root.include" or "root.watch_interval")
            field_examples: Optional dict mapping field patterns to example values.
            If None, returns None (no examples available).
        """
        if field_examples is None:
            return None

        # First, try exact match (O(1) lookup)
        if field_path in field_examples:
            return field_examples[field_path]

        # Then try wildcard matches
        for pattern, example in field_examples.items():
            if "*" in pattern and fnmatchcase_portable(field_path, pattern):
                return example

        return None

    @staticmethod
    def _infer_type_label(
        expected_type: Any,
    ) -> str:
        """Return a readable label for logging (e.g. 'list[str]', 'BuildConfig')."""
        try:
            origin = get_origin(expected_type)
            args = get_args(expected_type)

            # Unwrap NotRequired to get the actual type
            if origin is NotRequired and args:
                return ApatheticSchema_Internal_ValidateTypedDict._infer_type_label(
                    args[0]
                )

            if origin is list and args:
                inner = ApatheticSchema_Internal_ValidateTypedDict._infer_type_label(
                    args[0]
                )
                return f"list[{inner}]"

            if isinstance(expected_type, type):
                return expected_type.__name__

            # Fallback for other types
            return str(expected_type)
        except Exception:  # noqa: BLE001
            return str(expected_type)

    @staticmethod
    def _validate_scalar_value(
        context: str,
        key: str,
        val: Any,
        expected_type: Any,
        *,
        strict: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        field_path: str,
        field_examples: dict[str, str] | None = None,
    ) -> bool:
        """Validate a single non-container value against its expected type."""
        try:
            if safe_isinstance(val, expected_type):  # self-ref guard
                return True
        except Exception:  # noqa: BLE001
            # Defensive fallback — e.g. weird typing generics
            fallback_type = (
                expected_type
                if isinstance(expected_type, type)
                else type(expected_type)
            )
            if isinstance(val, fallback_type):
                return True

        exp_label = ApatheticSchema_Internal_ValidateTypedDict._infer_type_label(
            expected_type
        )
        example = ApatheticSchema_Internal_ValidateTypedDict._get_example_for_field(
            field_path, field_examples
        )
        exmsg = ""
        if example:
            exmsg = f" (e.g. {example})"

        msg = (
            f"{context}: key `{key}` expected {exp_label}{exmsg},"
            f" got {type(val).__name__}"
        )
        ApatheticSchema_Internal_CollectMsg.collect_msg(
            msg, summary=summary, strict=strict, is_error=True
        )
        return False

    @staticmethod
    def _validate_list_value(
        context: str,
        key: str,
        val: Any,
        subtype: Any,
        *,
        strict: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        prewarn: set[str],
        field_path: str,
        field_examples: dict[str, str] | None = None,
    ) -> bool:
        """Validate a homogeneous list value.

        Delegates to scalar/TypedDict validators.
        """
        if not isinstance(val, list):
            type_label = ApatheticSchema_Internal_ValidateTypedDict._infer_type_label(
                subtype
            )
            exp_label = f"list[{type_label}]"
            example = ApatheticSchema_Internal_ValidateTypedDict._get_example_for_field(
                field_path, field_examples
            )
            exmsg = ""
            if example:
                exmsg = f" (e.g. {example})"
            msg = (
                f"{context}: key `{key}` expected {exp_label}{exmsg},"
                f" got {type(val).__name__}"
            )
            ApatheticSchema_Internal_CollectMsg.collect_msg(
                msg,
                strict=strict,
                summary=summary,
                is_error=True,
            )
            return False

        # Treat val as a real list for static type checkers
        items = cast_hint(list[Any], val)

        # Empty list → fine, nothing to check
        if not items:
            return True

        valid = True
        for i, item in enumerate(items):
            # Detect TypedDict-like subtypes
            if (
                isinstance(subtype, type)
                and hasattr(subtype, "__annotations__")
                and hasattr(subtype, "__total__")
            ):
                if not isinstance(item, dict):
                    ApatheticSchema_Internal_CollectMsg.collect_msg(
                        f"{context}: key `{key}` #{i + 1} expected an "
                        " object with named keys for "
                        f"{subtype.__name__}, got {type(item).__name__}",
                        strict=strict,
                        summary=summary,
                        is_error=True,
                    )
                    valid = False
                    continue

                valid &= ApatheticSchema_Internal_ValidateTypedDict.validate_typed_dict(
                    f"{context}.{key}[{i}]",
                    item,
                    subtype,
                    strict=strict,
                    summary=summary,
                    prewarn=prewarn,
                    field_path=f"{field_path}[{i}]",
                    field_examples=field_examples,
                )
            else:
                valid &= (
                    ApatheticSchema_Internal_ValidateTypedDict._validate_scalar_value(
                        context,
                        f"{key}[{i}]",
                        item,
                        subtype,
                        strict=strict,
                        summary=summary,
                        field_path=f"{field_path}[{i}]",
                        field_examples=field_examples,
                    )
                )
        return valid

    @staticmethod
    def _dict_unknown_keys(
        context: str,
        val: Any,
        schema: dict[str, Any],
        *,
        strict: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        prewarn: set[str],
    ) -> bool:
        """Check for unknown keys in a dictionary value."""
        # --- Unknown keys ---
        val_dict = cast("dict[str, Any]", val)
        unknown: list[str] = [
            k for k in val_dict if k not in schema and k not in prewarn
        ]
        if unknown:
            joined = ", ".join(f"`{u}`" for u in unknown)

            location = context
            if "in top-level configuration." in location:
                location = "in " + location.split("in top-level configuration.")[-1]

            msg = f"Unknown key{plural(unknown)} {joined} {location}."

            hints: list[str] = []
            for k in unknown:
                close = get_close_matches(
                    k,
                    schema.keys(),
                    n=1,
                    cutoff=ApatheticSchema_Internal_Constants.DEFAULT_HINT_CUTOFF,
                )
                if close:
                    hints.append(f"'{k}' → '{close[0]}'")
            if hints:
                msg += "\nHint: did you mean " + ", ".join(hints) + "?"

            ApatheticSchema_Internal_CollectMsg.collect_msg(
                msg.strip(), strict=strict, summary=summary
            )
            if strict:
                return False

        return True

    @staticmethod
    def _dict_fields(
        context: str,
        val: Any,
        schema: dict[str, Any],
        *,
        strict: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        prewarn: set[str],
        ignore_keys: set[str],
        field_path: str,
        field_examples: dict[str, str] | None = None,
    ) -> bool:
        """Validate dictionary fields against schema."""
        valid = True

        for field, expected_type in schema.items():
            if field not in val or field in prewarn or field in ignore_keys:
                # Optional or missing field → not a failure
                continue

            inner_val = val[field]
            origin = get_origin(expected_type)
            args = get_args(expected_type)
            exp_label = ApatheticSchema_Internal_ValidateTypedDict._infer_type_label(
                expected_type
            )
            current_field_path = f"{field_path}.{field}" if field_path else field

            if origin is list:
                subtype = args[0] if args else Any
                valid &= (
                    ApatheticSchema_Internal_ValidateTypedDict._validate_list_value(
                        context,
                        field,
                        inner_val,
                        subtype,
                        strict=strict,
                        summary=summary,
                        prewarn=prewarn,
                        field_path=current_field_path,
                        field_examples=field_examples,
                    )
                )
            elif (
                isinstance(expected_type, type)
                and hasattr(expected_type, "__annotations__")
                and hasattr(expected_type, "__total__")
            ):
                # we don't pass ignore_keys down because
                # we don't recursively ignore these keys
                # and they have no depth syntax. Instead you
                # need to ignore the current level, then take ownership
                # and only validate what you want manually. calling validation
                # on anything that you aren't ignoring downstream.
                # rare case that is a lot of work, but keeps the rest
                # simple for now.
                if "in top-level configuration." in context:
                    location = field
                else:
                    location = f"{context}.{field}"
                valid &= ApatheticSchema_Internal_ValidateTypedDict.validate_typed_dict(
                    location,
                    inner_val,
                    expected_type,
                    strict=strict,
                    summary=summary,
                    prewarn=prewarn,
                    field_path=current_field_path,
                    field_examples=field_examples,
                )
            else:
                val_scalar = (
                    ApatheticSchema_Internal_ValidateTypedDict._validate_scalar_value(
                        context,
                        field,
                        inner_val,
                        expected_type,
                        strict=strict,
                        summary=summary,
                        field_path=current_field_path,
                        field_examples=field_examples,
                    )
                )
                if not val_scalar:
                    ApatheticSchema_Internal_CollectMsg.collect_msg(
                        f"{context}: key `{field}` expected {exp_label}, "
                        f"got {type(inner_val).__name__}",
                        strict=strict,
                        summary=summary,
                        is_error=True,
                    )
                    valid = False

        return valid

    @staticmethod
    def validate_typed_dict(
        context: str,
        val: Any,
        typedict_cls: type[Any],
        *,
        strict: bool,
        summary: ApatheticSchema_ValidationSummary,  # modified in-place
        prewarn: set[str],
        ignore_keys: set[str] | None = None,
        field_path: str = "",
        field_examples: dict[str, str] | None = None,
    ) -> bool:
        """Validate a dict against a TypedDict schema recursively.

        - Return False if val is not a dict
        - Recurse into its fields using _validate_scalar_value or _validate_list_value
        - Warn about unknown keys under strict=True
        """
        if ignore_keys is None:
            ignore_keys = set()

        if not isinstance(val, dict):
            ApatheticSchema_Internal_CollectMsg.collect_msg(
                f"{context}: expected an object with named keys for"
                f" {typedict_cls.__name__}, got {type(val).__name__}",
                strict=strict,
                summary=summary,
                is_error=True,
            )
            return False

        if not hasattr(typedict_cls, "__annotations__"):
            xmsg = (
                "Internal schema invariant violated: "
                f"{typedict_cls!r} has no __annotations__."
            )
            raise AssertionError(xmsg)

        schema = schema_from_typeddict(typedict_cls)
        valid = True

        # --- walk through all the fields recursively ---
        if not ApatheticSchema_Internal_ValidateTypedDict._dict_fields(
            context,
            val,
            schema,
            strict=strict,
            summary=summary,
            prewarn=prewarn,
            ignore_keys=ignore_keys,
            field_path=field_path,
            field_examples=field_examples,
        ):
            valid = False

        # --- Unknown keys ---
        if not ApatheticSchema_Internal_ValidateTypedDict._dict_unknown_keys(
            context,
            val,
            schema,
            strict=strict,
            summary=summary,
            prewarn=prewarn,
        ):
            valid = False

        return valid
