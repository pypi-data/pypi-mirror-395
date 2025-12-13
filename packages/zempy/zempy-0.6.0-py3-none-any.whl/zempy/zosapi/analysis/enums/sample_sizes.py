from zempy.zosapi.core.enum_base import ZosEnumBase


class SampleSizes(ZosEnumBase):
    S_32x32 = 0
    S_64x64 = 1
    S_128x128 = 2
    S_256x256 = 3
    S_512x512 = 4
    S_1024x1024 = 5
    S_2048x2048 = 6
    S_4096x4096 = 7
    S_8192x8192 = 8
    S_16384x16384 = 9

SampleSizes._NATIVE_PATH = "ZOSAPI.Analysis.SampleSizes"
SampleSizes._ALIASES_EXTRA = {}

__all__ = ["SampleSizes"]
