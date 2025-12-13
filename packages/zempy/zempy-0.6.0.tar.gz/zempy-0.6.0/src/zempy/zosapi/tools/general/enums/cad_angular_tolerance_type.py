from zempy.zosapi.core.enum_base import ZosEnumBase

class CADAngularToleranceType(ZosEnumBase):
    Low         = 0
    Medium      = 1
    High        = 2
    Presentation = 3

CADAngularToleranceType._NATIVE_PATH = "ZOSAPI.Tools.General.CADAngularToleranceType"
CADAngularToleranceType._ALIASES_EXTRA = {}

__all__ = ["CADAngularToleranceType"]
