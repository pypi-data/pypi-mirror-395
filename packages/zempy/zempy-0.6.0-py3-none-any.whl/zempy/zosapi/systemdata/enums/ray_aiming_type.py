from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class RayAimingType(ZosEnumBase):
    """ZOSAPI.SystemData.RayAimingType"""
    Heuristic                       = 0
    Optimize                        = 1

RayAimingType._NATIVE_PATH = "ZOSAPI.SystemData.RayAimingType"
RayAimingType._ALIASES_EXTRA = {}

__all__ = ["RayAimingType"]
