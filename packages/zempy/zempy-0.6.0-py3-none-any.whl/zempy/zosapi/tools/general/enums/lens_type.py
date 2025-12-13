from zempy.zosapi.core.enum_base import ZosEnumBase

class LensType(ZosEnumBase):
    Other     = 0
    Spherical = 1
    GRIN      = 2
    Aspheric  = 3
    Toroidal  = 4

LensType._NATIVE_PATH = "ZOSAPI.Tools.General.LensType"
LensType._ALIASES_EXTRA = {}

__all__ = ["LensType"]
