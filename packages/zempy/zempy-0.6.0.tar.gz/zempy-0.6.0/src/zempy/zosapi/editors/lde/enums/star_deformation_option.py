from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class STARDeformationOption(ZosEnumBase):
    """ZOSAPI.Editors.LDE.STARDeformationOption"""
    DeformationWithRBMs         = 0
    DeformationWithoutRBMs      = 1
    OnlyRBMs                    = 2
    NoDeformation               = 3

STARDeformationOption._NATIVE_PATH = "ZOSAPI.Editors.LDE.STARDeformationOption"
STARDeformationOption._ALIASES_EXTRA = {}

__all__ = ["STARDeformationOption"]
