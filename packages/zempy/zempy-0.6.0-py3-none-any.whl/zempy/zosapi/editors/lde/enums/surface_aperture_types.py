from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class SurfaceApertureTypes(ZosEnumBase):
    """ZOSAPI.Editors.LDE.SurfaceApertureTypes"""
    NoneType                        = 0
    CircularAperture                = 1
    CircularObscuration             = 2
    Spider                          = 3
    RectangularAperture             = 4
    RectangularObscuration          = 5
    EllipticalAperture              = 6
    EllipticalObscuration           = 7
    UserAperture                    = 8
    UserObscuration                 = 9
    FloatingAperture                = 10

SurfaceApertureTypes._NATIVE_PATH = "ZOSAPI.Editors.LDE.SurfaceApertureTypes"
SurfaceApertureTypes._ALIASES_EXTRA = {
    "NoneType": [
        "None"
    ]
}

__all__ = ["SurfaceApertureTypes"]
