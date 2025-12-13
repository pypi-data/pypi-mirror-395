from __future__ import annotations
from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase


class UpdateStatus(ZosEnumBase):
    _NATIVE_PATH = "ZOSAPI.UpdateStatus"
    _ALIASES_EXTRA = {
        "CHECK_FAILED": ("CheckFailed",),
        "NOT_SUPPORTED": ("NotSupported",),
        "NOT_CHECKED": ("NotChecked",),
        "UP_TO_DATE": ("UpToDate",),
        "AVAILABLE_ELIGIBLE": ("AvailableEligible",),
        "AVAILABLE_INELIGIBLE": ("AvailableIneligible",),
    }

    CHECK_FAILED = -2
    NOT_SUPPORTED = -1
    NOT_CHECKED = 0
    UP_TO_DATE = 1
    AVAILABLE_ELIGIBLE = 2
    AVAILABLE_INELIGIBLE = 3

    def is_up_to_date(self) -> bool:
        return self is UpdateStatus.UP_TO_DATE

    def is_available(self) -> bool:
        return self in (
            UpdateStatus.AVAILABLE_ELIGIBLE,
            UpdateStatus.AVAILABLE_INELIGIBLE,
        )

    def is_failed(self) -> bool:
        return self in (
            UpdateStatus.CHECK_FAILED,
            UpdateStatus.NOT_SUPPORTED,
        )


__all__ = ["UpdateStatus"]
