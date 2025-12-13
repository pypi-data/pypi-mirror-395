from zempy.zosapi.core.enum_base import ZosEnumBase

class MaterialFormulas(ZosEnumBase):
    Schott        = 1
    Sellmeier1    = 2
    Herzberger    = 3
    Sellmeier2    = 4
    Conrady       = 5
    Sellmeier3    = 6
    Handbook1     = 7
    Handbook2     = 8
    Sellmeier4    = 9
    Extended      = 10
    Sellmeier5    = 11
    Extended2     = 12
    Extended3     = 13

MaterialFormulas._NATIVE_PATH = "ZOSAPI.Tools.General.MaterialFormulas"
MaterialFormulas._ALIASES_EXTRA = {}

__all__ = ["MaterialFormulas"]
