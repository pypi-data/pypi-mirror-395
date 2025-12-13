from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfaceSlopeData(ZosEnumBase):
    SurfaceSlope = 0
    TangentialSlope = 1
    SagittalSlope = 2
    XSlope = 3
    YSlope = 4
    SlopeModulus = 5
    SlopeUnused = 6

SurfaceSlopeData._NATIVE_PATH = "ZOSAPI.Analysis.SurfaceSlopeData"
SurfaceSlopeData._ALIASES_EXTRA = {}

__all__ = ["SurfaceSlopeData"]
