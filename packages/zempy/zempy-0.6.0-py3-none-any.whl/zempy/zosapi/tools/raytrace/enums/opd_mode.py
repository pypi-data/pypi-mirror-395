from zempy.zosapi.core.enum_base import ZosEnumBase

class OPDMode(ZosEnumBase):
    None_            = 0
    Current          = 1
    CurrentAndChief  = 2

OPDMode._NATIVE_PATH = ("ZOSAPI.Tools.RayTrace.OPDMode")
OPDMode._ALIASES_EXTRA = {}

__all__ = ["OPDMode"]
