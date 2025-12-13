from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class CoordinateConversionResult(ZosEnumBase):
    """ZOSAPI.Editors.LDE.CoordinateConversionResult"""
    Success                     = 0
    Error_InvalidRange          = 1
    Error_CoordinateBreak       = 2
    Error_IgnoredSurface        = 3
    Error_TiltDecenter          = 4
    Error_MultiConfig           = 5

CoordinateConversionResult._NATIVE_PATH = "ZOSAPI.Editors.LDE.CoordinateConversionResult"
CoordinateConversionResult._ALIASES_EXTRA = {
    "Error_CoordinateBreak": [
        "Error_CoordianteBreak"
    ]
}

__all__ = ["CoordinateConversionResult"]
