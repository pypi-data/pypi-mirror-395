from zempy.zosapi.core.enum_base import ZosEnumBase

class NSCTraceOptions(ZosEnumBase):
    None_                           = 0
    UsePolarization                 = 1
    UseSplitting                    = 2
    UseScattering                   = 4
    UsePolarizationSplitting        = 3
    UsePolarizationScattering       = 5
    UseSplittingScattering          = 6
    UsePolarizationSplittingScattering = 7

NSCTraceOptions._NATIVE_PATHS = ("ZOSAPI.Tools.RayTrace.NSCTraceOptions")

NSCTraceOptions._ALIASES_EXTRA = {}

__all__ = ["NSCTraceOptions"]
