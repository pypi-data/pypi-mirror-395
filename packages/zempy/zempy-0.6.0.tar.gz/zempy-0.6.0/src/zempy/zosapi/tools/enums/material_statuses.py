from zempy.zosapi.core.enum_base import ZosEnumBase

class MaterialStatuses(ZosEnumBase):
    Standard  = 0
    Preferred = 1
    Obsolete  = 2
    Special   = 3
    Melt      = 4

MaterialStatuses._NATIVE_PATH = "ZOSAPI.Tools.General.MaterialStatuses"
MaterialStatuses._ALIASES_EXTRA = {}

__all__ = ["MaterialStatuses"]
