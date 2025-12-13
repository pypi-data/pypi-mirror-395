from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class HuygensIntegralSettings(ZosEnumBase):
    """ZOSAPI.SystemData.HuygensIntegralSettings"""
    Auto                            = 0
    Planar                          = 1
    Spherical                       = 2

HuygensIntegralSettings._NATIVE_PATH = "ZOSAPI.SystemData.HuygensIntegralSettings"
HuygensIntegralSettings._ALIASES_EXTRA = {}

__all__ = ["HuygensIntegralSettings"]
