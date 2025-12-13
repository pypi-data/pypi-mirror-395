from zempy.zosapi.core.enum_base import ZosEnumBase

class QuickAdjustType(ZosEnumBase):
    Radius      = 0
    Thickness   = 1

QuickAdjustType._NATIVE_PATH = "ZOSAPI.Tools.General.QuickAdjustType"
QuickAdjustType._ALIASES_EXTRA = {}

__all__ = ["QuickAdjustType"]
