from zempy.zosapi.core.enum_base import ZosEnumBase

class ACISExportVersion(ZosEnumBase):
    Current = 0
    V25     = 1
    V26     = 2
    V27     = 3
    V28     = 4
    V29     = 5
    V30     = 6

ACISExportVersion._NATIVE_PATH = "ZOSAPI.Tools.General.ACISExportVersion"
ACISExportVersion._ALIASES_EXTRA = {}

__all__ = ["ACISExportVersion"]
