from zempy.zosapi.core.enum_base import ZosEnumBase


class Parity(ZosEnumBase):
    Even = 0
    Odd = 1

Parity._NATIVE_PATH = "ZOSAPI.Analysis.Settings.Parity"
Parity._ALIASES_EXTRA = {}

__all__ = ["Parity"]
