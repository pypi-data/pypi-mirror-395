from zempy.zosapi.core.enum_base import ZosEnumBase


class SampleSizes_Pow2Plus1(ZosEnumBase):
    S_33 = 0
    S_65 = 1
    S_129 = 2
    S_257 = 3
    S_513 = 4
    S_1025 = 5
    S_2049 = 6
    S_4097 = 7
    S_8193 = 8

SampleSizes_Pow2Plus1._NATIVE_PATH = "ZOSAPI.Analysis.SampleSizes_Pow2Plus1"
SampleSizes_Pow2Plus1._ALIASES_EXTRA = {}

__all__ = ["SampleSizes_Pow2Plus1"]
