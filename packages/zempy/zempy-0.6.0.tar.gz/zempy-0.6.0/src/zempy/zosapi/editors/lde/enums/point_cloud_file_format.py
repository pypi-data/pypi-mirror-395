from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class PointCloudFileFormat(ZosEnumBase):
    """ZOSAPI.Editors.LDE.PointCloudFileFormat"""
    ASCII                       = 0
    Binary                      = 1
    CompressedBinary            = 2

PointCloudFileFormat._NATIVE_PATH = "ZOSAPI.Editors.LDE.PointCloudFileFormat"
PointCloudFileFormat._ALIASES_EXTRA = {}

__all__ = ["PointCloudFileFormat"]
