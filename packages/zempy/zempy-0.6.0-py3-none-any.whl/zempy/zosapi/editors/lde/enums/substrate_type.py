from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class SubstrateType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.SubstrateType"""
    NoneType                    = 0
    Flat                        = 1
    Curved                      = 2

SubstrateType._NATIVE_PATH = "ZOSAPI.Editors.LDE.SubstrateType"
SubstrateType._ALIASES_EXTRA = {
    "NoneType": [
        "None"
    ]
}

__all__ = ["SubstrateType"]
