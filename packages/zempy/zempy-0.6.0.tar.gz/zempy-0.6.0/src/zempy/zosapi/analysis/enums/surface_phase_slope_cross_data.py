from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfacePhaseSlopeCrossData(ZosEnumBase):
    PhaseSlopeTangential = 0
    PhaseSlopeSagittal = 1
    PhaseSlopeX = 2
    PhaseSlopeY = 3
    PhaseSlopeModulus = 4
    PhaseSlopeUnused = 5

SurfacePhaseSlopeCrossData._NATIVE_PATH = "ZOSAPI.Analysis.SurfacePhaseSlopeCrossData"
SurfacePhaseSlopeCrossData._ALIASES_EXTRA = {}

__all__ = ["SurfacePhaseSlopeCrossData"]
