from zempy.zosapi.core.enum_base import ZosEnumBase


class DisplayOption(ZosEnumBase):
    AllRays = 0
    FailedRays = 1
    PassedRays = 2

DisplayOption._NATIVE_PATH = "ZOSAPI.Analysis.Settings.DisplayOption"
DisplayOption._ALIASES_EXTRA = {}

__all__ = ["DisplayOption"]
