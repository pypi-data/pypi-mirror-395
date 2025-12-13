from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class FieldPattern(ZosEnumBase):
    """ZOSAPI.SystemData.FieldPattern"""
    UniformY                        = 0
    EqualAreaY                      = 1
    UniformX                        = 2
    EqualAreaX                      = 3
    Grid                            = 4
    UniformRadial                   = 5
    EqualAreaRadial                 = 6

FieldPattern._NATIVE_PATH = "ZOSAPI.SystemData.FieldPattern"
FieldPattern._ALIASES_EXTRA = {}

__all__ = ["FieldPattern"]
