from __future__ import annotations
from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase


class SessionModes(ZosEnumBase):
    _NATIVE_PATH = "ZOSAPI.SessionModes"
    _ALIASES_EXTRA = {
        "FROM_PREFERENCES": ("FromPreferences",),
        "SESSION_ON": ("SessionOn",),
        "SESSION_OFF": ("SessionOff",),
    }

    FROM_PREFERENCES = 0
    SESSION_ON = 1
    SESSION_OFF = 2

    def is_from_preferences(self) -> bool:
        return self is SessionModes.FROM_PREFERENCES

    def is_on(self) -> bool:
        return self is SessionModes.SESSION_ON

    def is_off(self) -> bool:
        return self is SessionModes.SESSION_OFF


__all__ = ["SessionModes"]
