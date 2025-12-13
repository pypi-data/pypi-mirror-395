from zempy.zosapi.core.enum_base import ZosEnumBase


class Rotations(ZosEnumBase):
    Rotate_0 = 0
    Rotate_90 = 1
    Rotate_180 = 2
    Rotate_270 = 3

Rotations._NATIVE_PATH = "ZOSAPI.Analysis.Settings.Rotations"
Rotations._ALIASES_EXTRA = {}

__all__ = ["Rotations"]
