from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class FieldColumn(ZosEnumBase):
    """ZOSAPI.SystemData.FieldColumn"""
    Comment                         = 0
    X                               = 1
    Y                               = 2
    Weight                          = 3
    VDX                             = 4
    VDY                             = 5
    VCX                             = 6
    VCY                             = 7
    TAN                             = 8
    VAN                             = 9

FieldColumn._NATIVE_PATH = "ZOSAPI.SystemData.FieldColumn"
FieldColumn._ALIASES_EXTRA = {}

__all__ = ["FieldColumn"]
