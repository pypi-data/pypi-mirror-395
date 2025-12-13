from zempy.zosapi.core.enum_base import ZosEnumBase


class GiaShowAsTypes(ZosEnumBase):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    SpotDiagram = 6
    CrossX = 7
    CrossY = 8

GiaShowAsTypes._NATIVE_PATH = "ZOSAPI.Analysis.GiaShowAsTypes"
GiaShowAsTypes._ALIASES_EXTRA = {}

__all__ = ["GiaShowAsTypes"]
