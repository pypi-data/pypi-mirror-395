from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class SurfaceEdgeDraw(ZosEnumBase):
    """ZOSAPI.Editors.LDE.SurfaceEdgeDraw"""
    Squared                         = 0
    Tapered                         = 1
    Flat                            = 2

SurfaceEdgeDraw._NATIVE_PATH = "ZOSAPI.Editors.LDE.SurfaceEdgeDraw"
SurfaceEdgeDraw._ALIASES_EXTRA = {}

__all__ = ["SurfaceEdgeDraw"]
