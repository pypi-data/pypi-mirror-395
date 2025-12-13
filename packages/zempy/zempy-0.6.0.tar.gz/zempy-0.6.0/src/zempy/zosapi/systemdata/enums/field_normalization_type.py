from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class FieldNormalizationType(ZosEnumBase):
    """ZOSAPI.SystemData.FieldNormalizationType"""
    Radial                          = 0
    Rectangular                     = 1

FieldNormalizationType._NATIVE_PATH = "ZOSAPI.SystemData.FieldNormalizationType"
FieldNormalizationType._ALIASES_EXTRA = {}

__all__ = ["FieldNormalizationType"]
