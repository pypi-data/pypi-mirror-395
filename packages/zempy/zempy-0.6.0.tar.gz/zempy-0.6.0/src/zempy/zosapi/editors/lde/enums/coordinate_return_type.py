from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class CoordinateReturnType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.CoordinateReturnType"""
    NoneType                    = 0
    OrientationOnly             = 1
    OrientationXY               = 2
    OrientationXYZ              = 3

CoordinateReturnType._NATIVE_PATH = "ZOSAPI.Editors.LDE.CoordinateReturnType"
CoordinateReturnType._ALIASES_EXTRA = {
    "NoneType": [
        "None"
    ]
}

__all__ = ["CoordinateReturnType"]
