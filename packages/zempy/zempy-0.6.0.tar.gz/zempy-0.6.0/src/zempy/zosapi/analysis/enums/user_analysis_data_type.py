from zempy.zosapi.core.enum_base import ZosEnumBase


class UserAnalysisDataType(ZosEnumBase):
    None = 0
    Line2D = 1
    Grid = 2
    GridRGB = 3
    Text = 4

UserAnalysisDataType._NATIVE_PATH = "ZOSAPI.Analysis.UserAnalysisDataType"
UserAnalysisDataType._ALIASES_EXTRA = {}

__all__ = ["UserAnalysisDataType"]
