from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class EditorType(ZosEnumBase):
    """ZOSAPI.Editors.EditorType"""
    _NATIVE_PATH = "ZOSAPI.Editors.EditorType"

    LDE = 0  # Lens Data Editor
    NCE = 1  # Non-sequential Component Editor
    MFE = 2  # Merit Function Editor
    TDE = 3  # Tolerance Data Editor
    MCE = 4  # Multiple Configuration Editor

EditorType._NATIVE_PATH = "ZOSAPI.Editors.EditorType"
EditorType._ALIASES_EXTRA = {}

__all__ = ["EditorType"]
