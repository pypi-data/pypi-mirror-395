from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class PilotRadiusMode(ZosEnumBase):
    """ZOSAPI.Editors.LDE.PilotRadiusMode"""
    BestFit                     = 0
    Shorter                     = 1
    Longer                      = 2
    X                           = 3
    Y                           = 4
    Plane                       = 5
    User                        = 6

PilotRadiusMode._NATIVE_PATH = "ZOSAPI.Editors.LDE.PilotRadiusMode"
PilotRadiusMode._ALIASES_EXTRA = {}

__all__ = ["PilotRadiusMode"]
