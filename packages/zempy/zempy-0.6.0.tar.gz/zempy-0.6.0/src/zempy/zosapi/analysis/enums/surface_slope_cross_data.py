from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfaceSlopeCrossData(ZosEnumBase):
    TangentialSlope = 0
    SagittalSlope = 1
    XSlope = 2
    YSlope = 3
    SlopeModulus = 4
    SlopeUnused = 5

SurfaceSlopeCrossData._NATIVE_PATH = "ZOSAPI.Analysis.SurfaceSlopeCrossData"
SurfaceSlopeCrossData._ALIASES_EXTRA = {}

__all__ = ["SurfaceSlopeCrossData"]
