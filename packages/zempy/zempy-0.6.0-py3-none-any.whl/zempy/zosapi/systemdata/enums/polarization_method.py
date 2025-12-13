from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class PolarizationMethod(ZosEnumBase):
    """ZOSAPI.SystemData.PolarizationMethod"""
    XAxisMethod                     = 0
    YAxisMethod                     = 1
    ZAxisMethod                     = 2

PolarizationMethod._NATIVE_PATH = "ZOSAPI.SystemData.PolarizationMethod"
PolarizationMethod._ALIASES_EXTRA = {}

__all__ = ["PolarizationMethod"]
