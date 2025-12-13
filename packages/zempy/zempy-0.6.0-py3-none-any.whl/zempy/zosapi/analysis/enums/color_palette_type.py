from zempy.zosapi.core.enum_base import ZosEnumBase

class ColorPaletteType(ZosEnumBase):
    """Enumeration: ZOSAPI.Analysis.ColorPaletteType"""

    GreyScale          = 0
    FalseColor         = 1
    FalseColorOriginal = 2
    Viridis            = 3
    Magma              = 4

ColorPaletteType._NATIVE_PATH = "ZOSAPI.Analysis.ColorPaletteType"
ColorPaletteType._ALIASES_EXTRA = {}

__all__ = ["ColorPaletteType"]
