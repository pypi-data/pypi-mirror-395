from zempy.zosapi.core.enum_base import ZosEnumBase

class LensShape(ZosEnumBase):
    Unknown  = 0
    Equi     = 1
    Bi       = 2
    Plano    = 3
    Meniscus = 4

LensShape._NATIVE_PATH = "ZOSAPI.Tools.General.LensShape"
LensShape._ALIASES_EXTRA = {}

__all__ = ["LensShape"]
