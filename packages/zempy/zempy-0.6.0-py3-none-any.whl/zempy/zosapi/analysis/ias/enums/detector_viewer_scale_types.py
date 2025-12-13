from zempy.zosapi.core.enum_base import ZosEnumBase


class DetectorViewerScaleTypes(ZosEnumBase):
    Linear = 0
    Log_Minus_5 = 1
    Normalized = 2
    Log_Minus_10 = 3
    Log_Minus_15 = 4

DetectorViewerScaleTypes._NATIVE_PATH = "ZOSAPI.Analysis.Settings.DetectorViewerScaleTypes"
DetectorViewerScaleTypes._ALIASES_EXTRA = {}

__all__ = ["DetectorViewerScaleTypes"]
