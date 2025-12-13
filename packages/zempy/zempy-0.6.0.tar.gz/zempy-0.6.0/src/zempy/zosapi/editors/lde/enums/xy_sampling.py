from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class XYSampling(ZosEnumBase):
    """ZOSAPI.Editors.LDE.XYSampling"""
    S32                             = 0
    S64                             = 1
    S128                            = 2
    S256                            = 3
    S512                            = 4
    S1024                           = 5
    S2048                           = 6
    S4096                           = 7
    S8192                           = 8
    S16384                          = 9

XYSampling._NATIVE_PATH = "ZOSAPI.Editors.LDE.XYSampling"
XYSampling._ALIASES_EXTRA = {}

__all__ = ["XYSampling"]
