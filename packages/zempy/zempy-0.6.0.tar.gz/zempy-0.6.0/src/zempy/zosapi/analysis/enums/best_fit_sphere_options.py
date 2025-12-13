from zempy.zosapi.core.enum_base import ZosEnumBase


class BestFitSphereOptions(ZosEnumBase):
    MinimumVolume = 0
    MinimumRMS = 1
    MinimumRMSWithOffset = 2

BestFitSphereOptions._NATIVE_PATH = "ZOSAPI.Analysis.BestFitSphereOptions"
BestFitSphereOptions._ALIASES_EXTRA = {}

__all__ = ["BestFitSphereOptions"]
