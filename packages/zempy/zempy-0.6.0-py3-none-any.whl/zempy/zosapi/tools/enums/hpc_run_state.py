from zempy.zosapi.core.enum_base import ZosEnumBase

class HPCRunState(ZosEnumBase):
    NotRunning        = 0
    Initializing      = 1
    ClusterAllocating = 2
    UploadingData     = 3
    Queued            = 4
    RunStarting       = 5
    WaitingForResults = 6
    Complete          = 7

HPCRunState._NATIVE_PATH = "ZOSAPI.Tools.General.HPCRunState"
HPCRunState._ALIASES_EXTRA = {}

__all__ = ["HPCRunState"]
