# src/apathetic_schema/namespace.py
"""Shared Apathetic Schema namespace implementation.

This namespace class provides a structure to minimize global namespace pollution
when the library is embedded in a stitched script.
"""

from __future__ import annotations

from .check_schema_conformance import (
    ApatheticSchema_Internal_CheckSchemaConformance,
)
from .collect_msg import ApatheticSchema_Internal_CollectMsg
from .constants import (
    ApatheticSchema_Internal_Constants,
)
from .flush_schema_aggregators import (
    ApatheticSchema_Internal_FlushSchemaAggregators,
)
from .validate_typed_dict import (
    ApatheticSchema_Internal_ValidateTypedDict,
)
from .warn_keys_once import ApatheticSchema_Internal_WarnKeysOnce


# --- Apathetic Schema Namespace -------------------------------------------


class apathetic_schema(  # noqa: N801
    ApatheticSchema_Internal_Constants,
    ApatheticSchema_Internal_CollectMsg,
    ApatheticSchema_Internal_FlushSchemaAggregators,
    ApatheticSchema_Internal_WarnKeysOnce,
    ApatheticSchema_Internal_ValidateTypedDict,
    ApatheticSchema_Internal_CheckSchemaConformance,
):
    """Namespace for apathetic schema functionality.

    All schema validation functionality is accessed via this namespace class to
    minimize global namespace pollution when the library is embedded in a
    stitched script.
    """


# Note: All exports are handled in __init__.py
# - For library builds (package/stitched): __init__.py is included, exports happen
# - For embedded builds: __init__.py is excluded, no exports (only class available)
