from zempy.zosapi.core.enum_base import ZosEnumBase

class LTEdgeSasmpling(ZosEnumBase):
    S_1X_Low = 0
    S_4X     = 1
    S_16X    = 2
    S_64X    = 3
    S_256X   = 4

LTEdgeSasmpling._NATIVE_PATHS = ("ZOSAPI.Tools.RayTrace.LTEdgeSampling")
LTEdgeSasmpling._ALIASES_EXTRA = {}

__all__ = ["LTEdgeSasmpling"]
