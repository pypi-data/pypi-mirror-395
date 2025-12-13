from zempy.zosapi.core.enum_base import ZosEnumBase


class ZemaxColor(ZosEnumBase):
    """Wrapper for ZOSAPI.Common.ZemaxColor enum."""

    Default = 0
    Color1  = 1
    Color2  = 2
    Color3  = 3
    Color4  = 4
    Color5  = 5
    Color6  = 6
    Color7  = 7
    Color8  = 8
    Color9  = 9
    Color10 = 10
    Color11 = 11
    Color12 = 12
    Color13 = 13
    Color14 = 14
    Color15 = 15
    Color16 = 16
    Color17 = 17
    Color18 = 18
    Color19 = 19
    Color20 = 20
    Color21 = 21
    Color22 = 22
    Color23 = 23
    Color24 = 24
    NoColor = 25


# Main and fallback ZOS-API enum paths
ZemaxColor._NATIVE_PATHS = ("ZOSAPI.Common.ZemaxColor")
ZemaxColor._ALIASES_EXTRA = {}

__all__ = ["ZemaxColor"]
