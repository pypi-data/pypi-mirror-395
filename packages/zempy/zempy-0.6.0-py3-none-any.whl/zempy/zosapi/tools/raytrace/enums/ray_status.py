from zempy.zosapi.core.enum_base import ZosEnumBase

class RayStatus(ZosEnumBase):
    """Wrapper for ZOSAPI.Tools.RayTrace.RayStatus enum."""

    Parent           = 0
    Terminated       = 1
    Reflected        = 2
    Transmitted      = 3
    Scattered        = 4
    Diffracted       = 5
    GhostedFrom      = 6
    DiffractedFrom   = 7
    ScatteredFrom    = 8
    RayError         = 9
    BulkScattered    = 10
    WaveShifted      = 11
    TIR              = 12
    OrdinaryRay      = 13
    ExtraordinaryRay = 14
    WaveShiftPL      = 15

RayStatus._NATIVE_PATHS = ("ZOSAPI.Tools.RayTrace.RayStatus")
RayStatus._ALIASES_EXTRA = {}

__all__ = ["RayStatus"]
