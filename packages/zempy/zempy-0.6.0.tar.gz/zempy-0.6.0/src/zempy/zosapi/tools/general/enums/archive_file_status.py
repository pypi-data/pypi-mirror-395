from zempy.zosapi.core.enum_base import ZosEnumBase

class ArchiveFileStatus(ZosEnumBase):
    Okay           = 0
    UnableToOpen   = -1
    InvalidFile    = -2
    InvalidVersion = -3

ArchiveFileStatus._NATIVE_PATH = "ZOSAPI.Tools.General.ArchiveFileStatus"
ArchiveFileStatus._ALIASES_EXTRA = {}

__all__ = ["ArchiveFileStatus"]
