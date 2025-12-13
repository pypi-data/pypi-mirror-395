from zempy.zosapi.core.enum_base import ZosEnumBase


class Polarizations(ZosEnumBase):
    None = 0
    Ex = 1
    Ey = 2
    Ez = 3

Polarizations._NATIVE_PATH = "ZOSAPI.Analysis.Settings.Polarizations"
Polarizations._ALIASES_EXTRA = {}

__all__ = ["Polarizations"]
