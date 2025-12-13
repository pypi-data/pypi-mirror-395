from zempy.zosapi.core.enum_base import ZosEnumBase

class RayPatternOption(ZosEnumBase):
    XyFan             = 0
    XFan              = 1
    YFan              = 2
    ChiefAndRing      = 3
    List              = 4
    Grid              = 6
    ChiefAndMarginals = 8

RayPatternOption._NATIVE_PATH = "ZOSAPI.Tools.General.RayPatternOption"
RayPatternOption._ALIASES_EXTRA = {}

__all__ = ["RayPatternOption"]
