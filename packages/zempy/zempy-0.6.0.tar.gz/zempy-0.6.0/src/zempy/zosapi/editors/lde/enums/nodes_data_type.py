from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class NodesDataType(ZosEnumBase):
    """ZOSAPI.Editors.LDE.NodesDataType"""
    SurfaceDeformationNoRBM     = 0
    RefractiveIndex             = 1
    TemperatureAndRefractiveIndex= 2
    SurfaceDeformation          = 3

NodesDataType._NATIVE_PATH = "ZOSAPI.Editors.LDE.NodesDataType"
NodesDataType._ALIASES_EXTRA = {}

__all__ = ["NodesDataType"]
