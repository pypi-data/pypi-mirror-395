from zempy.zosapi.core.enum_base import ZosEnumBase


class PsfTypes(ZosEnumBase):
    X_Linear = 0
    Y_Linear = 1
    X_Logarithmic = 2
    Y_Logarithmic = 3
    X_Phase = 4
    Y_Phase = 5
    X_RealPart = 6
    Y_RealPart = 7
    X_ImaginaryPart = 8
    Y_ImaginaryPart = 9

PsfTypes._NATIVE_PATH = "ZOSAPI.Analysis.Settings.PsfTypes"
PsfTypes._ALIASES_EXTRA = {}

__all__ = ["PsfTypes"]
