from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class ConversionOrder(ZosEnumBase):
    """ZOSAPI.Editors.LDE.ConversionOrder"""
    Forward                     = 0
    Reverse                     = 1

ConversionOrder._NATIVE_PATH = "ZOSAPI.Editors.LDE.ConversionOrder"
ConversionOrder._ALIASES_EXTRA = {}

__all__ = ["ConversionOrder"]
