from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfaceSagData(ZosEnumBase):
    SurfaceSag = 0

SurfaceSagData._NATIVE_PATH = "ZOSAPI.Analysis.SurfaceSagData"
SurfaceSagData._ALIASES_EXTRA = {}

__all__ = ["SurfaceSagData"]
