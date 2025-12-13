from __future__ import annotations
from zempy.zosapi.core.im_adapter import BaseAdapter, Z, N, run_native, dataclass, Optional
from zempy.zosapi.analysis.adapters.message import Message
from zempy.zosapi.analysis.enums.error_types import ErrorType


@dataclass
class IAS_Wavelength(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Analysis.Settings.IAS_Wavelength."""

    def GetWavelengthNumber(self) -> Optional[int]:
        """Return the current (1-based) wavelength index, or None if unavailable."""
        try:
            val = run_native(
                "IAS_Wavelength.GetWavelengthNumber",
                lambda: self.native.GetWavelengthNumber(),
                ensure=self.ensure_native,
            )
            return None if val is None else int(val)
        except (AttributeError, RuntimeError, Exception):
            return None

    def SetWavelengthNumber(self, n: int) -> Message:
        """Set the current wavelength index (1-based)."""
        try:
            native_msg = run_native(
                "IAS_Wavelength.SetWavelengthNumber",
                lambda: self.native.SetWavelengthNumber(int(n)),
                ensure=self.ensure_native,
            )
            return Message.from_native(self.zosapi, native_msg)
        except Exception as ex:
            return Message.from_error(self.zosapi, ErrorType.Unknown, str(ex))

    def UseAllWavelengths(self) -> Message:
        """Select all wavelengths."""
        try:
            native_msg = run_native(
                "IAS_Wavelength.UseAllWavelengths",
                lambda: self.native.UseAllWavelengths(),
                ensure=self.ensure_native,
            )
            return Message.from_native(self.zosapi, native_msg)
        except Exception as ex:
            return Message.from_error(self.zosapi, ErrorType.Unknown, str(ex))

    def __str__(self) -> str:
        num = None
        try:
            num = self.GetWavelengthNumber()
        except Exception:
            pass
        n_desc = "unknown" if num is None else str(num)
        return f" {n_desc}"
