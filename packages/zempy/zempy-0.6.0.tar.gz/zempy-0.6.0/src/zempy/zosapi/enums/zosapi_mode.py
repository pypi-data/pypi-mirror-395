from __future__ import annotations
from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase


class ZOSAPIMode(ZosEnumBase):
    _NATIVE_PATH = "ZOSAPI.ZOSAPI_Mode"
    _ALIASES_EXTRA = {
        "SERVER": ("Server",),
        "OPERAND": ("Operand",),
        "PLUGIN": ("Plugin",),
        "USER_ANALYSIS": ("UserAnalysis",),
        "USER_ANALYSIS_SETTINGS": ("UserAnalysisSettings",),
    }

    SERVER = 0
    OPERAND = 1
    PLUGIN = 2
    USER_ANALYSIS = 3
    USER_ANALYSIS_SETTINGS = 4

    def is_server(self) -> bool:
        """Connection is running in server or headless mode."""
        return self is ZOSAPIMode.SERVER

    def is_operand(self) -> bool:
        """User operand mode."""
        return self is ZOSAPIMode.OPERAND

    def is_plugin(self) -> bool:
        """Extension (plugin) mode."""
        return self is ZOSAPIMode.PLUGIN

    def is_user_analysis(self) -> bool:
        """User analysis mode – perform the calculation."""
        return self is ZOSAPIMode.USER_ANALYSIS

    def is_user_analysis_settings(self) -> bool:
        """User analysis mode – display/configure the analysis settings."""
        return self is ZOSAPIMode.USER_ANALYSIS_SETTINGS


__all__ = ["ZOSAPIMode"]
