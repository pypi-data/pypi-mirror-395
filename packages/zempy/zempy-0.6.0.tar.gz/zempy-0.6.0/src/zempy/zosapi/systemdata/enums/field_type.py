from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class FieldType(ZosEnumBase):
    """ZOSAPI.SystemData.FieldType"""
    Angle                           = 0
    ObjectHeight                    = 1
    ParaxialImageHeight             = 2
    RealImageHeight                 = 3
    TheodoliteAngle                 = 4

FieldType._NATIVE_PATH = "ZOSAPI.SystemData.FieldType"
FieldType._ALIASES_EXTRA = {}

__all__ = ["FieldType"]
