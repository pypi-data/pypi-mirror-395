from zempy.zosapi.core.enum_base import ZosEnumBase


class GridPlotType(ZosEnumBase):
    Surface = 0
    Contour = 1
    GrayScale = 2
    InverseGrayScale = 3
    FalseColor = 4
    InverseFalseColor = 5

GridPlotType._NATIVE_PATH = "ZOSAPI.Analysis.GridPlotType"
GridPlotType._ALIASES_EXTRA = {}

__all__ = ["GridPlotType"]
