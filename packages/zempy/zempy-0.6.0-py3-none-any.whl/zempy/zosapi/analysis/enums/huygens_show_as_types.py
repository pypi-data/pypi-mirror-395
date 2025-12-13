from zempy.zosapi.core.enum_base import ZosEnumBase


class HuygensShowAsTypes(ZosEnumBase):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    TrueColor = 6

HuygensShowAsTypes._NATIVE_PATH = "ZOSAPI.Analysis.HuygensShowAsTypes"
HuygensShowAsTypes._ALIASES_EXTRA = {}

__all__ = ["HuygensShowAsTypes"]
