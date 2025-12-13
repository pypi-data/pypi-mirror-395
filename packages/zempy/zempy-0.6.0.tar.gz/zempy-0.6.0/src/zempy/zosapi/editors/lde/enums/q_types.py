from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class QTypes(ZosEnumBase):
    """ZOSAPI.Editors.LDE.QTypes"""
    Qbfs                        = 0
    Qcon                        = 1

QTypes._NATIVE_PATH = "ZOSAPI.Editors.LDE.QTypes"
QTypes._ALIASES_EXTRA = {}

__all__ = ["QTypes"]
