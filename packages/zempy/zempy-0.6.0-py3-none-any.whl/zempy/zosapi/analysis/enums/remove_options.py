from zempy.zosapi.core.enum_base import ZosEnumBase


class RemoveOptions(ZosEnumBase):
    None = 0
    BaseROC = 1
    BestFitSphere = 2
    BaseSag = 3
    CompositeSag = 4

RemoveOptions._NATIVE_PATH = "ZOSAPI.Analysis.RemoveOptions"
RemoveOptions._ALIASES_EXTRA = {}

__all__ = ["RemoveOptions"]
