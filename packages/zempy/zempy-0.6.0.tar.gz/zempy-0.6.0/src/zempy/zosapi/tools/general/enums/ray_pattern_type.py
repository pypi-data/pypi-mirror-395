from zempy.zosapi.core.enum_base import ZosEnumBase

class RayPatternType(ZosEnumBase):
    XYFan     = 0
    XFan      = 1
    YFan      = 2
    Ring      = 3
    List      = 4
    Random    = 5
    Grid      = 6
    SolidRing = 7

RayPatternType._NATIVE_PATH = "ZOSAPI.Tools.General.RayPatternType"
RayPatternType._ALIASES_EXTRA = {}

__all__ = ["RayPatternType"]
