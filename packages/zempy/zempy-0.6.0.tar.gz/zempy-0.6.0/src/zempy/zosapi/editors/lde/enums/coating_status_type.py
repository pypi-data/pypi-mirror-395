from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class CoatingStatusType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.CoatingStatusType"""
    Fixed                       = 0
    Variable                    = 1
    Pickup                      = 2

CoatingStatusType._NATIVE_PATH = "ZOSAPI.Editors.LDE.CoatingStatusType"
CoatingStatusType._ALIASES_EXTRA = {}

__all__ = ["CoatingStatusType"]
