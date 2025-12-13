from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxFileTypes(ZosEnumBase):
    Unknown = 0
    LMX     = 1
    User    = 2

ZemaxFileTypes._NATIVE_PATH = "ZOSAPI.Tools.General.ZemaxFileTypes"
ZemaxFileTypes._ALIASES_EXTRA = {}

__all__ = ["ZemaxFileTypes"]
