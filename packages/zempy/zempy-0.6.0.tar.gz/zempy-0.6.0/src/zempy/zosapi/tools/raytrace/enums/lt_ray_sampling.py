from zempy.zosapi.core.enum_base import ZosEnumBase

class LTRaySampling(ZosEnumBase):
    S_1X_Low  = 0
    S_4X      = 1
    S_16X     = 2
    S_64X     = 3
    S_256X    = 4
    S_1024X   = 5

LTRaySampling._NATIVE_PATHS = ("ZOSAPI.Tools.RayTrace.LTRaySampling")
LTRaySampling._ALIASES_EXTRA = {}

__all__ = ["LTRaySampling"]
