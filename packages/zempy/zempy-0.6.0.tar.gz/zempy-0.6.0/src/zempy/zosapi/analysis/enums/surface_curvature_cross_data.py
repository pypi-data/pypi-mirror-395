from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfaceCurvatureCrossData(ZosEnumBase):
    TangentialCurvature = 0
    SagittalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3
    CurvatureModulus = 4
    CurvatureUnused = 5

SurfaceCurvatureCrossData._NATIVE_PATH = "ZOSAPI.Analysis.SurfaceCurvatureCrossData"
SurfaceCurvatureCrossData._ALIASES_EXTRA = {}

__all__ = ["SurfaceCurvatureCrossData"]
