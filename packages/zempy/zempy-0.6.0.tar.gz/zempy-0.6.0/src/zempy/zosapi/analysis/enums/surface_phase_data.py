from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfacePhaseData(ZosEnumBase):
    SurfacePhase = 0

SurfacePhaseData._NATIVE_PATH = "ZOSAPI.Analysis.SurfacePhaseData"
SurfacePhaseData._ALIASES_EXTRA = {}

__all__ = ["SurfacePhaseData"]
