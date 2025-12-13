from __future__ import annotations
from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase


class LensUpdateMode(ZosEnumBase):
    _NATIVE_PATH = "ZOSAPI.LensUpdateMode"
    _ALIASES_EXTRA = {
        "NONE": ("None",),
        "EDITORS_ONLY": ("EditorsOnly",),
        "ALL_WINDOWS": ("AllWindows",),
    }

    NONE = 0
    EDITORS_ONLY = 1
    ALL_WINDOWS = 2

    def is_editors_only(self) -> bool:
        return self is LensUpdateMode.EDITORS_ONLY

    def is_all_windows(self) -> bool:
        return self is LensUpdateMode.ALL_WINDOWS

    def is_none(self) -> bool:
        return self is LensUpdateMode.NONE


__all__ = ["LensUpdateMode"]
