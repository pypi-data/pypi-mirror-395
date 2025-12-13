from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class TiltDecenterPickupType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.TiltDecenterPickupType"""
    Explicit                        = 0
    PickupSurface                   = 1
    ReverseSurface                  = 2

TiltDecenterPickupType._NATIVE_PATH = "ZOSAPI.Editors.LDE.TiltDecenterPickupType"
TiltDecenterPickupType._ALIASES_EXTRA = {}

__all__ = ["TiltDecenterPickupType"]
