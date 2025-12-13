from zempy.zosapi.core.enum_base import ZosEnumBase

class SplineSegmentsType(ZosEnumBase):
    N_016 = 0
    N_032 = 1
    N_064 = 2
    N_128 = 3
    N_256 = 4
    N_512 = 5

SplineSegmentsType._NATIVE_PATH = "ZOSAPI.Tools.General.SplineSegmentsType"
SplineSegmentsType._ALIASES_EXTRA = {}

__all__ = ["SplineSegmentsType"]
