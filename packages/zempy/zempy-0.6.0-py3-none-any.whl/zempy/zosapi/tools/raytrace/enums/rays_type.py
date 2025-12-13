from zempy.zosapi.core.enum_base import ZosEnumBase
class RaysType(ZosEnumBase):
    Real = 0
    Paraxial = 1


RaysType._NATIVE_PATH = "ZOSAPI.Tools.RayTrace.RaysType"
RaysType._ALIASES_EXTRA = {}


__all__ = ["RaysType"]
