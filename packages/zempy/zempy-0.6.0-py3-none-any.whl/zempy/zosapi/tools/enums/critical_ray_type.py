from zempy.zosapi.core.enum_base import ZosEnumBase

class CriticalRayType(ZosEnumBase):
    Chief    = 0
    Marginal = 1
    Grid     = 2
    Ring     = 3
    Y_Fan    = 4
    X_Fan    = 5
    XY_Fan   = 6
    List     = 7

CriticalRayType._NATIVE_PATH = "ZOSAPI.Tools.General.CriticalRayType"
CriticalRayType._ALIASES_EXTRA = {}

__all__ = ["CriticalRayType"]
