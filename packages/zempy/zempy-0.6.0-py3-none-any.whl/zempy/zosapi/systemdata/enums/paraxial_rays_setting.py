from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class ParaxialRaysSetting(ZosEnumBase):
    """ZOSAPI.SystemData.ParaxialRaysSetting"""
    ConsiderCoordinateBreaks        = 0
    IgnoreCoordinateBreaks          = 1

ParaxialRaysSetting._NATIVE_PATH = "ZOSAPI.SystemData.ParaxialRaysSetting"
ParaxialRaysSetting._ALIASES_EXTRA = {}

__all__ = ["ParaxialRaysSetting"]
