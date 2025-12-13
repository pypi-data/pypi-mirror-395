from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class PsfRotation(ZosEnumBase):
    CW0   = "CW0"
    CW90  = "CW90"
    CW180 = "CW180"
    CW270 = "CW270"

PsfRotation._NATIVE_PATH = "ZOSAPI.Analysis.Settings.Psf.PsfRotation"
PsfRotation._ALIASES_EXTRA = {
    "CW0": ("CW0",),
    "CW90": ("CW90",),
    "CW180": ("CW180",),
    "CW270": ("CW270",),
}

__all__ = ["PsfRotation"]
