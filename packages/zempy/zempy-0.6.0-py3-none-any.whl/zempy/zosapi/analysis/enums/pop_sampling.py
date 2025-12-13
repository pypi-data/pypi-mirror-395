from zempy.zosapi.core.enum_base import ZosEnumBase


class POPSampling(ZosEnumBase):
    S_32 = 0
    S_64 = 1
    S_128 = 2
    S_256 = 3
    S_512 = 4
    S_1024 = 5
    S_2048 = 6
    S_4096 = 7
    S_8192 = 8
    S_16384 = 9
    S_32768 = 10
    S_65536 = 11
    S_131072 = 12
    S_262144 = 13
    S_524288 = 14
    S_1048576 = 15
    S_2097152 = 16
    S_4194304 = 17
    S_8388608 = 18
    S_16777216 = 19
    S_33554432 = 20
    S_67108864 = 21
    S_134217728 = 22
    S_268435456 = 23
    S_536870912 = 24
    S_1073741824 = 25
    S_1K = 26
    S_2K = 27
    S_4K = 28
    S_8K = 29
    S_16K = 30
    S_32K = 31
    S_64K = 32
    S_128K = 33
    S_256K = 34
    S_512K = 35
    S_1M = 36
    S_2M = 37
    S_4M = 38
    S_8M = 39
    S_16M = 40
    S_32M = 41
    S_64M = 42
    S_128M = 43
    S_256M = 44
    S_512M = 45
    S_1G = 46

POPSampling._NATIVE_PATH = "ZOSAPI.Analysis.POPSampling"
POPSampling._ALIASES_EXTRA = {}

__all__ = ["POPSampling"]
