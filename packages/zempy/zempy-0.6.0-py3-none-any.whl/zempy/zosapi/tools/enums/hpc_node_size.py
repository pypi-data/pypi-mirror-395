from zempy.zosapi.core.enum_base import ZosEnumBase

class HPCNodeSize(ZosEnumBase):
    Default = 0
    Tiny    = 1
    Small   = 2
    Medium  = 3
    Large   = 4
    XLarge  = 5

HPCNodeSize._NATIVE_PATH = "ZOSAPI.Tools.General.HPCNodeSize"
HPCNodeSize._ALIASES_EXTRA = {}

__all__ = ["HPCNodeSize"]
