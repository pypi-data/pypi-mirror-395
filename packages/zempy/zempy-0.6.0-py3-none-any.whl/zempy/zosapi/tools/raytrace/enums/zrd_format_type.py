from zempy.zosapi.core.enum_base import ZosEnumBase

class ZRDFormatType(ZosEnumBase):
    """Wrapper for ZOSAPI.Tools.RayTrace.ZRDFormatType enum."""

    UncompressedFullData = 0
    CompressedBasicData  = 1
    CompressedFullData   = 2

ZRDFormatType._NATIVE_PATHS = ("ZOSAPI.Tools.RayTrace.ZRDFormatType")
ZRDFormatType._ALIASES_EXTRA = {}

__all__ = ["ZRDFormatType"]
