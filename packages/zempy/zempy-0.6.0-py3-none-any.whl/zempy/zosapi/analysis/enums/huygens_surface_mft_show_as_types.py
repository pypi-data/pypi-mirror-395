from zempy.zosapi.core.enum_base import ZosEnumBase


class HuygensSurfaceMftShowAsTypes(ZosEnumBase):
    GreyScale = 0
    InverseGreyScale = 1
    FalseColor = 2
    InverseFalseColor = 3

HuygensSurfaceMftShowAsTypes._NATIVE_PATH = "ZOSAPI.Analysis.HuygensSurfaceMftShowAsTypes"
HuygensSurfaceMftShowAsTypes._ALIASES_EXTRA = {}

__all__ = ["HuygensSurfaceMftShowAsTypes"]
