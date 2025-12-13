from __future__ import annotations
from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase


class STARUpdateMode(ZosEnumBase):
    _NATIVE_PATH = "ZOSAPI.STARUpdateMode"
    _ALIASES_EXTRA = {
        "NORMAL": ("Normal",),
        "SUSPENDED": ("Suspended",),
    }

    NORMAL = 0
    SUSPENDED = 1

    def is_normal(self) -> bool:
        return self is STARUpdateMode.NORMAL

    def is_suspended(self) -> bool:
        return self is STARUpdateMode.SUSPENDED


__all__ = ["STARUpdateMode"]
