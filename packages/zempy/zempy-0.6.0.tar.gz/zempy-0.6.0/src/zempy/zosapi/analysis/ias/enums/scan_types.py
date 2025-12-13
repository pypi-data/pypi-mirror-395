from zempy.zosapi.core.enum_base import ZosEnumBase


class ScanTypes(ZosEnumBase):
    Plus_Y = 0
    Plus_X = 1
    Minus_Y = 2
    Minus_X = 3

ScanTypes._NATIVE_PATH = "ZOSAPI.Analysis.Settings.ScanTypes"
ScanTypes._ALIASES_EXTRA = {}

__all__ = ["ScanTypes"]
