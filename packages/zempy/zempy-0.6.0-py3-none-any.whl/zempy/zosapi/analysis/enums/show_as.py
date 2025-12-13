from zempy.zosapi.core.enum_base import ZosEnumBase


class ShowAsEnum(ZosEnumBase):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5

ShowAs._NATIVE_PATH = "ZOSAPI.Analysis.ShowAs"
ShowAs._ALIASES_EXTRA = {}

__all__ = ["ShowAsEnum"]
