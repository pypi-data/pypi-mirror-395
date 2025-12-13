from zempy.zosapi.core.enum_base import ZosEnumBase

class EntryCompressionModes(ZosEnumBase):
    Auto = 0
    On   = 1
    Off  = 2

EntryCompressionModes._NATIVE_PATH = "ZOSAPI.Tools.General.EntryCompressionModes"
EntryCompressionModes._ALIASES_EXTRA = {}

__all__ = ["EntryCompressionModes"]
