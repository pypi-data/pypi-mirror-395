from zempy.zosapi.core.enum_base import ZosEnumBase

class CADToleranceType(ZosEnumBase):
    N_TenEMinus4 = 0
    N_TenEMinus5 = 1
    N_TenEMinus6 = 2
    N_TenEMinus7 = 3

CADToleranceType._NATIVE_PATH = "ZOSAPI.Tools.General.CADToleranceType"
CADToleranceType._ALIASES_EXTRA = {}

__all__ = ["CADToleranceType"]
