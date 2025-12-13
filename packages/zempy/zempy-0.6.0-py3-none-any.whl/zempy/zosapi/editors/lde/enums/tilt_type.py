from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class TiltType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.TiltType"""
    XTilt                          = 0
    YTilt                          = 1

TiltType._NATIVE_PATH = "ZOSAPI.Editors.LDE.TiltType"
TiltType._ALIASES_EXTRA = {}

__all__ = ["TiltType"]
