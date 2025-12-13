from zempy.zosapi.core.enum_base import ZosEnumBase


class STAREffectsOptions(ZosEnumBase):
    On = 0
    Difference = 1

STAREffectsOptions._NATIVE_PATH = "ZOSAPI.Analysis.Settings.STAREffectsOptions"
STAREffectsOptions._ALIASES_EXTRA = {}

__all__ = ["STAREffectsOptions"]
