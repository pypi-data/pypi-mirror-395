from zempy.zosapi.core.enum_base import ZosEnumBase


class PsfSpread(ZosEnumBase):
    Line = 0
    Edge = 1

PsfSpread._NATIVE_PATH = "ZOSAPI.Analysis.Settings.PsfSpread"
PsfSpread._ALIASES_EXTRA = {}

__all__ = ["PsfSpread"]
