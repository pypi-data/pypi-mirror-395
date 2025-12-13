from __future__ import annotations
from zempy.zosapi.core.im_adapter import BaseAdapter, Z, N, run_native, dataclass, Optional
from zempy.zosapi.analysis.adapters.message import Message
from zempy.zosapi.analysis.enums.error_types import ErrorType


@dataclass
class IAS_Field(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Analysis.Settings.IAS_Field."""

    def GetFieldNumber(self) -> Optional[int]:
        """Return the current (1-based) field index, or None if unavailable."""
        try:
            val = run_native(
                "IAS_Field.GetFieldNumber",
                lambda: self.native.GetFieldNumber(),
                ensure=self.ensure_native,
            )
            return None if val is None else int(val)
        except (AttributeError, RuntimeError, Exception):
            # AttributeError: native missing / wrong interface
            # RuntimeError: ensure_native raised (object gone)
            # Exception: catch-all for COM interop errors
            return None

    def SetFieldNumber(self, n: int) -> Message:
        """Set the current field index (1-based)."""
        try:
            native_msg = run_native(
                "IAS_Field.SetFieldNumber",
                lambda: self.native.SetFieldNumber(int(n)),
                ensure=self.ensure_native,
            )
            return Message.from_native(self.zosapi, native_msg)
        except Exception as ex:
            return Message.from_error(self.zosapi, ErrorType.Unknown, str(ex))

    def UseAllFields(self) -> Message:
        """Select all fields."""
        try:
            native_msg = run_native(
                "IAS_Field.UseAllFields",
                lambda: self.native.UseAllFields(),
                ensure=self.ensure_native,
            )
            return Message.from_native(self.zosapi, native_msg)
        except Exception as ex:
            return Message.from_error(self.zosapi, ErrorType.Unknown, str(ex))

    def __str__(self) -> str:
        num = None
        try:
            num = self.GetFieldNumber()
        except Exception:
            pass
        n_desc = "unknown" if num is None else str(num)
        return f" {n_desc}"
