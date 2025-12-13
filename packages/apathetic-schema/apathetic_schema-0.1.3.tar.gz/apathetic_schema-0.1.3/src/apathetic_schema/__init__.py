"""Apathetic schema package."""

from typing import TYPE_CHECKING, cast


if TYPE_CHECKING:
    from .namespace import apathetic_schema as _apathetic_schema_class

# Import types for export (available at both type checking and runtime)
from .types import (
    ApatheticSchema_SchemaErrorAggregator,
    ApatheticSchema_SchErrAggEntry,
    ApatheticSchema_ValidationSummary,
)


# Get reference to the namespace class
# In stitched mode: class is already defined in namespace.py (executed before this)
# In package mode: import from namespace module
_apathetic_schema_is_stitched = globals().get("__STITCHED__", False)

if _apathetic_schema_is_stitched:
    # Stitched mode: class already defined in namespace.py
    # Get reference to the class (it's already in globals from namespace.py)
    _apathetic_schema_raw = globals().get("apathetic_schema")
    if _apathetic_schema_raw is None:
        # Fallback: should not happen, but handle gracefully
        msg = "apathetic_schema class not found in stitched mode"
        raise RuntimeError(msg)
    # Type cast to help mypy understand this is the apathetic_schema class
    # The import gives us type[apathetic_schema], so cast to
    # type[_apathetic_schema_class]
    apathetic_schema = cast("type[_apathetic_schema_class]", _apathetic_schema_raw)
else:
    # Package mode: import from namespace module
    # This block is only executed in package mode, not in stitched builds
    from .namespace import apathetic_schema

    # Ensure the else block is not empty (build script may remove import)
    _ = apathetic_schema

# Export mixin classes and types directly
# Types are exported from apathetic_schema class below


# Export methods and attributes from apathetic_schema class for direct import
check_schema_conformance = apathetic_schema.check_schema_conformance
collect_msg = apathetic_schema.collect_msg
flush_schema_aggregators = apathetic_schema.flush_schema_aggregators
warn_keys_once = apathetic_schema.warn_keys_once
validate_typed_dict = apathetic_schema.validate_typed_dict

# Export constants from apathetic_schema class
DEFAULT_HINT_CUTOFF = apathetic_schema.DEFAULT_HINT_CUTOFF
AGG_STRICT_WARN = apathetic_schema.AGG_STRICT_WARN
AGG_WARN = apathetic_schema.AGG_WARN

# Export type aliases and dataclasses
# Types are imported from types module above


__all__ = [
    "AGG_STRICT_WARN",
    "AGG_WARN",
    "DEFAULT_HINT_CUTOFF",
    "ApatheticSchema_SchErrAggEntry",
    "ApatheticSchema_SchemaErrorAggregator",
    "ApatheticSchema_ValidationSummary",
    "apathetic_schema",
    "check_schema_conformance",
    "collect_msg",
    "flush_schema_aggregators",
    "validate_typed_dict",
    "warn_keys_once",
]
