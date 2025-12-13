from zempy.zosapi.core.enum_base import ZosEnumBase


class HuygensPsfTypes(ZosEnumBase):
    Linear = 0
    Log_Minus_1 = 1
    Log_Minus_2 = 2
    Log_Minus_3 = 3
    Log_Minus_4 = 4
    Log_Minus_5 = 5
    Real = 6
    Imaginary = 7
    Phase = 8

HuygensPsfTypes._NATIVE_PATH = "ZOSAPI.Analysis.Settings.HuygensPsfTypes"
HuygensPsfTypes._ALIASES_EXTRA = {}

__all__ = ["HuygensPsfTypes"]
