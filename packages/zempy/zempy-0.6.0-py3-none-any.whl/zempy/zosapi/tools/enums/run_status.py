from zempy.zosapi.core.enum_base import ZosEnumBase

class RunStatus(ZosEnumBase):
    Completed      = 0
    FailedToStart  = 1
    TimedOut       = 2
    InvalidTimeout = 3

RunStatus._NATIVE_PATH = "ZOSAPI.Tools.General.RunStatus"
RunStatus._ALIASES_EXTRA = {}

__all__ = ["RunStatus"]
