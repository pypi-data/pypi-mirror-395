from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class ReflectTransmitCode(ZosEnumBase):
    """ZOSAPI.Editors.ReflectTransmitCode"""
    _NATIVE_PATH = "ZOSAPI.Editors.ReflectTransmitCode"

    Success = 0
    NoReflectDataInFile = 1
    NoTransmitDataInFile = 2

ReflectTransmitCode._NATIVE_PATH = "ZOSAPI.Editors.ReflectTransmitCode"
ReflectTransmitCode._ALIASES_EXTRA = {}

__all__ = ["ReflectTransmitCode"]
