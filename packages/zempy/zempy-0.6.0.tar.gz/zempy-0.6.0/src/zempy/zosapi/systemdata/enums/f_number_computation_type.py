from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class FNumberComputationType(ZosEnumBase):
    """ZOSAPI.SystemData.FNumberComputationType"""
    TracingRays                     = 0
    PupilSizePosition               = 1

FNumberComputationType._NATIVE_PATH = "ZOSAPI.SystemData.FNumberComputationType"
FNumberComputationType._ALIASES_EXTRA = {}

__all__ = ["FNumberComputationType"]
