from zempy.zosapi.core.enum_base import ZosEnumBase


class ReferenceGia(ZosEnumBase):
    ChiefRay = 0
    Vertex = 1
    PrimaryChief = 2
    Centroid = 3

ReferenceGia._NATIVE_PATH = "ZOSAPI.Analysis.Settings.ReferenceGia"
ReferenceGia._ALIASES_EXTRA = {}

__all__ = ["ReferenceGia"]
