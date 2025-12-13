from zempy.zosapi.core.enum_base import ZosEnumBase


class SourceGia(ZosEnumBase):
    Uniform = 0
    Lambertian = 1

SourceGia._NATIVE_PATH = "ZOSAPI.Analysis.Settings.SourceGia"
SourceGia._ALIASES_EXTRA = {}

__all__ = ["SourceGia"]
