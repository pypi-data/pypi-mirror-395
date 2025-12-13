from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class SampleSides(ZosEnumBase):
    """ZOSAPI.Editors.SampleSides"""
    _NATIVE_PATH = "ZOSAPI.Editors.SampleSides"

    Front = 0
    Back = 1

SampleSides._NATIVE_PATH = "ZOSAPI.Editors.SampleSides"
SampleSides._ALIASES_EXTRA = {}

__all__ = ["SampleSides"]
