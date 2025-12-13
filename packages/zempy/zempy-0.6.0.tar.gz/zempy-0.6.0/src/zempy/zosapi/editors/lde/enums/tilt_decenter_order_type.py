from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class TiltDecenterOrderType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.TiltDecenterOrderType"""
    Decenter_Tilt                   = 0
    Tilt_Decenter                   = 1

TiltDecenterOrderType._NATIVE_PATH = "ZOSAPI.Editors.LDE.TiltDecenterOrderType"
TiltDecenterOrderType._ALIASES_EXTRA = {}

__all__ = ["TiltDecenterOrderType"]
