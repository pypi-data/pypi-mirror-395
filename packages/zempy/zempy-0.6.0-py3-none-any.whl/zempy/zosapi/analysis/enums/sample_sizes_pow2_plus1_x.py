from zempy.zosapi.core.enum_base import ZosEnumBase


class SampleSizes_Pow2Plus1_X(ZosEnumBase):
    S_33x33 = 0
    S_65x65 = 1
    S_129x129 = 2
    S_257x257 = 3
    S_513x513 = 4
    S_1025x1025 = 5
    S_2049x2049 = 6
    S_4097x4097 = 7
    S_8193x8193 = 8

SampleSizes_Pow2Plus1_X._NATIVE_PATH = "ZOSAPI.Analysis.SampleSizes_Pow2Plus1_X"
SampleSizes_Pow2Plus1_X._ALIASES_EXTRA = {}

__all__ = ["SampleSizes_Pow2Plus1_X"]
