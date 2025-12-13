from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class QuadratureSteps(ZosEnumBase):
    """ZOSAPI.SystemData.QuadratureSteps"""
    S2                              = 0
    S4                              = 1
    S6                              = 2
    S8                              = 3
    S10                             = 4
    S12                             = 5

QuadratureSteps._NATIVE_PATH = "ZOSAPI.SystemData.QuadratureSteps"
QuadratureSteps._ALIASES_EXTRA = {}

__all__ = ["QuadratureSteps"]
