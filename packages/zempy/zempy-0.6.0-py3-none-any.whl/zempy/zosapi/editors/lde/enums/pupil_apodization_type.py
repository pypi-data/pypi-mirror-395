from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class PupilApodizationType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.PupilApodizationType"""
    NoneType                    = 0
    Gaussian                    = 1
    Tangential                  = 2

PupilApodizationType._NATIVE_PATH = "ZOSAPI.Editors.LDE.PupilApodizationType"
PupilApodizationType._ALIASES_EXTRA = {
    "NoneType": [
        "None"
    ]
}

__all__ = ["PupilApodizationType"]
