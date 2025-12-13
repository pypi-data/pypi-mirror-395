from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class FftPsfType(ZosEnumBase):
    Linear    = "Linear"
    Log       = "Log"
    Phase     = "Phase"
    Real      = "Real"
    Imaginary = "Imaginary"

FftPsfType._NATIVE_PATH = "ZOSAPI.Analysis.Settings.Psf.FftPsfType"
FftPsfType._ALIASES_EXTRA = {
    "Linear": ("Linear",),
    "Log": ("Log",),
    "Phase": ("Phase",),
    "Real": ("Real",),
    "Imaginary": ("Imaginary",),
}

__all__ = ["FftPsfType"]
