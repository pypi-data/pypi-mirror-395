from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class RayAimingMethod(ZosEnumBase):
    """ZOSAPI.SystemData.RayAimingMethod"""
    Off                             = 0
    Paraxial                        = 1
    Real                            = 2

RayAimingMethod._NATIVE_PATH = "ZOSAPI.SystemData.RayAimingMethod"
RayAimingMethod._ALIASES_EXTRA = {}

__all__ = ["RayAimingMethod"]
