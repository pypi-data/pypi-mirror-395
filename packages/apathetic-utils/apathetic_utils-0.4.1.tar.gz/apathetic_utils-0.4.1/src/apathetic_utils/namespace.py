# src/apathetic_utils/namespace.py
"""Shared Apathetic Utils namespace implementation.

This namespace class provides a structure to minimize global namespace pollution
when the library is embedded in a stitched script.
"""

from __future__ import annotations

from .ci import (
    ApatheticUtils_Internal_CI,
)
from .constants import (
    ApatheticUtils_Internal_Constants,
)
from .files import (
    ApatheticUtils_Internal_Files,
)
from .matching import (
    ApatheticUtils_Internal_Matching,
)
from .modules import (
    ApatheticUtils_Internal_Modules,
)
from .paths import (
    ApatheticUtils_Internal_Paths,
)
from .runtime import (
    ApatheticUtils_Internal_Runtime,
)
from .subprocess_utils import (
    ApatheticUtils_Internal_Subprocess,
)
from .testing import (
    ApatheticUtils_Internal_Testing,
)
from .text import (
    ApatheticUtils_Internal_Text,
)
from .types import (
    ApatheticUtils_Internal_Types,
)
from .version import (
    ApatheticUtils_Internal_Version,
)


# --- Apathetic Utils Namespace -------------------------------------------


class apathetic_utils(  # noqa: N801
    ApatheticUtils_Internal_Constants,
    ApatheticUtils_Internal_CI,
    ApatheticUtils_Internal_Files,
    ApatheticUtils_Internal_Matching,
    ApatheticUtils_Internal_Modules,
    ApatheticUtils_Internal_Paths,
    ApatheticUtils_Internal_Runtime,
    ApatheticUtils_Internal_Subprocess,
    ApatheticUtils_Internal_Testing,
    ApatheticUtils_Internal_Text,
    ApatheticUtils_Internal_Types,
    ApatheticUtils_Internal_Version,
):
    """Namespace for apathetic utils functionality.

    All utility functionality is accessed via this namespace class to minimize
    global namespace pollution when the library is embedded in a stitched script.
    """


# Note: All exports are handled in __init__.py
# - For library builds (package/stitched): __init__.py is included, exports happen
# - For embedded builds: __init__.py is excluded, no exports (only class available)
