from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class DirectionOfRayTravel(ZosEnumBase):
    """ZOSAPI.Editors.DirectionOfRayTravel"""
    _NATIVE_PATH = "ZOSAPI.Editors.DirectionOfRayTravel"

    inward = 0
    outward = 1

DirectionOfRayTravel._NATIVE_PATH = "ZOSAPI.Editors.DirectionOfRayTravel"
DirectionOfRayTravel._ALIASES_EXTRA = {}

__all__ = ["DirectionOfRayTravel"]
