from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class IndexDataType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.IndexDataType"""
    Unknown                     = 0
    NoneType                    = 1
    PhysicsBasedIndex           = 2
    DirectRefractiveIndex       = 3

IndexDataType._NATIVE_PATH = "ZOSAPI.Editors.LDE.IndexDataType"
IndexDataType._ALIASES_EXTRA = {
    "NoneType": [
        "None"
    ]
}

__all__ = ["IndexDataType"]
