from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class InterpolationMethod(ZosEnumBase):
    """ZOSAPI.Editors.LDE.InterpolationMethod"""
    BicubicSpline               = 0
    Linear                      = 1

InterpolationMethod._NATIVE_PATH = "ZOSAPI.Editors.LDE.InterpolationMethod"
InterpolationMethod._ALIASES_EXTRA = {}

__all__ = ["InterpolationMethod"]
