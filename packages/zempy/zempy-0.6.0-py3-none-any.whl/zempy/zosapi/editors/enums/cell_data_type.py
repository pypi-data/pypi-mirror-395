from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class CellDataType(ZosEnumBase):
    _NATIVE_PATH = "ZOSAPI.Editors.CellDataType"

    Integer = 0
    Double = 1
    String = 2

CellDataType._NATIVE_PATH = "ZOSAPI.Editors.CellDataType"
CellDataType._ALIASES_EXTRA = {}

__all__ = ["CellDataType"]
