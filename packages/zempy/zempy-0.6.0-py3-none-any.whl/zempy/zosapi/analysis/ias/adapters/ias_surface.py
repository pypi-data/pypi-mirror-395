from __future__ import annotations
from zempy.zosapi.core.im_adapter import BaseAdapter, Z, N, run_native, dataclass, Optional
from zempy.zosapi.analysis.adapters.message import Message
from zempy.zosapi.analysis.enums.error_types import ErrorType


@dataclass
class IAS_Surface(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Analysis.Settings.IAS_Surface."""

    def GetSurfaceNumber(self) -> Optional[int]:
        """Return the current (1-based) surface index, or None if unavailable."""
        try:
            val = run_native(
                "IAS_Surface.GetSurfaceNumber",
                lambda: self.native.GetSurfaceNumber(),
                ensure=self.ensure_native,
            )
            return None if val is None else int(val)
        except (AttributeError, RuntimeError, Exception):
            # AttributeError: native missing / wrong interface
            # RuntimeError: ensure_native raised (object gone)
            # Exception: catch-all for COM interop errors
            return None

    def SetSurfaceNumber(self, n: int) -> Message:
        """Set the current surface index (1-based)."""
        try:
            native_msg = run_native(
                "IAS_Surface.SetSurfaceNumber",
                lambda: self.native.SetSurfaceNumber(int(n)),
                ensure=self.ensure_native,
            )
            return Message.from_native(self.zosapi, native_msg)
        except Exception as ex:
            return Message.from_error(self.zosapi, ErrorType.Unknown, str(ex))

    def UseImageSurface(self) -> Message:
        """Select the image surface."""
        try:
            native_msg = run_native(
                "IAS_Surface.UseImageSurface",
                lambda: self.native.UseImageSurface(),
                ensure=self.ensure_native,
            )
            return Message.from_native(self.zosapi, native_msg)
        except Exception as ex:
            return Message.from_error(self.zosapi, ErrorType.Unknown, str(ex))

    def UseObjectiveSurface(self) -> Message:
        """Select the objective surface."""
        try:
            native_msg = run_native(
                "IAS_Surface.UseObjectiveSurface",
                lambda: self.native.UseObjectiveSurface(),
                ensure=self.ensure_native,
            )
            return Message.from_native(self.zosapi, native_msg)
        except Exception as ex:
            return Message.from_error(self.zosapi, ErrorType.Unknown, str(ex))

    def __str__(self) -> str:
        num = None
        try:
            num = self.GetSurfaceNumber()
        except Exception:
            pass
        n_desc = "unknown" if num is None else str(num)
        return f" {n_desc}"
