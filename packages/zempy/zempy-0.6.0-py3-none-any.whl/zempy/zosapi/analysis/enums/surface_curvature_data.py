from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfaceCurvatureData(ZosEnumBase):
    TangentialCurvature = 0
    SagittalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3
    CurvatureModulus = 4
    CurvatureUnused = 5

SurfaceCurvatureData._NATIVE_PATH = "ZOSAPI.Analysis.SurfaceCurvatureData"
SurfaceCurvatureData._ALIASES_EXTRA = {}

__all__ = ["SurfaceCurvatureData"]
