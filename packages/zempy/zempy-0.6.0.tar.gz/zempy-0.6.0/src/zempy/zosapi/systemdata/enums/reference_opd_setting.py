from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class ReferenceOPDSetting(ZosEnumBase):
    """ZOSAPI.SystemData.ReferenceOPDSetting"""
    Absolute                        = 0
    Infinity                        = 1
    ExitPupil                       = 2
    Absolute2                       = 3

ReferenceOPDSetting._NATIVE_PATH = "ZOSAPI.SystemData.ReferenceOPDSetting"
ReferenceOPDSetting._ALIASES_EXTRA = {}

__all__ = ["ReferenceOPDSetting"]
