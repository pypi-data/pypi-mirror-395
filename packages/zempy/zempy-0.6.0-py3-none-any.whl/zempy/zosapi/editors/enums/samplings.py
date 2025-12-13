from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class Samplings(ZosEnumBase):
    """ZOSAPI.Editors.Samplings"""
    _NATIVE_PATH = "ZOSAPI.Editors.Samplings"

    FiveDegrees = 0
    TwoDegrees = 1
    OneDegree = 2

Samplings._NATIVE_PATH = "ZOSAPI.Editors.Samplings"
Samplings._ALIASES_EXTRA = {}

__all__ = ["Samplings"]