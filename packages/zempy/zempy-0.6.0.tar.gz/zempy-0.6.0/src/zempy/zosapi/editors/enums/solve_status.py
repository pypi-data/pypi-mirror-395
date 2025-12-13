from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class SolveStatus(ZosEnumBase):
    SUCCESS = 0
    INVALID_SOLVE_TYPE = 1
    INVALID_ROW = 2
    INVALID_COLUMN = 3
    POST_SURFACE_STOP_ONLY = 4
    INVALID_MACRO = 5
    FAILED = 6

    def is_success(self) -> bool:
        return self is SolveStatus.SUCCESS

    def is_failure(self) -> bool:
        return not self.is_success()

SolveStatus._NATIVE_PATH = "ZOSAPI.Editors.SolveStatus"
SolveStatus._ALIASES_EXTRA = {
        "SUCCESS": ("Success",),
        "INVALID_SOLVE_TYPE": ("InvalidSolveType",),
        "INVALID_ROW": ("InvalidRow",),
        "INVALID_COLUMN": ("InvalidColumn",),
        "POST_SURFACE_STOP_ONLY": ("PostSurfaceStopOnly",),
        "INVALID_MACRO": ("InvalidMacro",),
        "FAILED": ("Failed",),
    }


__all__ = ["SolveStatus"]
