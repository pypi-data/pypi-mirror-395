from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.types_var import Z, N
from zempy.zosapi.tools.enums.run_status import RunStatus


@dataclass
class SystemTool(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Tools.ISystemTool.
    Pattern matches other adapters (e.g., IAR) with PropertyScalar, run_native, and context mgmt.
    """

    Progress = PropertyScalar("Progress", coerce_get=int)
    Status = PropertyScalar("Status", coerce_get=str)
    IsRunning = PropertyScalar("IsRunning", coerce_get=bool)
    CanCancel = PropertyScalar("CanCancel", coerce_get=bool)
    IsAsynchronous = PropertyScalar("IsAsynchronous", coerce_get=bool)
    IsFiniteDuration = PropertyScalar("IsFiniteDuration", coerce_get=bool)
    IsValid = PropertyScalar("IsValid", coerce_get=bool)
    Succeeded = PropertyScalar("Succeeded", coerce_get=bool)

    # ErrorMessage may be null/None in .NET; expose Optional[str]
    @property
    def ErrorMessage(self) -> Optional[str]:
        val = run_native(
            "ISystemTool.ErrorMessage",
            lambda: self.native.ErrorMessage,
            ensure=self.ensure_native,
        )
        # Normalize empty strings to None for nicer Python UX
        if val is None:
            return None
        s = str(val)
        return s if s else None


    def Run(self) -> bool:
        return bool(run_native("ISystemTool.Run", lambda: self.native.Run(), ensure=self.ensure_native))

    def RunAndWaitForCompletion(self) -> bool:
        return bool(run_native("ISystemTool.RunAndWaitForCompletion", lambda: self.native.RunAndWaitForCompletion(), ensure=self.ensure_native))

    def WaitForCompletion(self) -> bool:
        return bool(run_native("ISystemTool.WaitForCompletion", lambda: self.native.WaitForCompletion(), ensure=self.ensure_native))

    def Cancel(self) -> bool:
        return bool(run_native("ISystemTool.Cancel", lambda: self.native.Cancel(), ensure=self.ensure_native))

    def Close(self) -> bool:
        return bool(run_native("ISystemTool.Close", lambda: self.native.Close(), ensure=self.ensure_native))

    def WaitWithTimeout(self, timeOutSeconds: float) -> RunStatus:
        return run_native("ISystemTool.WaitWithTimeout", lambda: self.native.WaitWithTimeout(float(timeOutSeconds)), ensure=self.ensure_native)

    def RunAndWaitWithTimeout(self, timeOutSeconds: float) -> RunStatus:
        return run_native("ISystemTool.RunAndWaitWithTimeout", lambda: self.native.RunAndWaitWithTimeout(float(timeOutSeconds)), ensure=self.ensure_native)

    # -------- Pythonic conveniences --------
    def __enter__(self) -> "SystemTool":
        """Allow `with` blocks; if tool is synchronous, you can call Run() inside."""
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # Always try to close to respect: "only one ISystemTool can be open at a time"
        try:
            self.Close()
        except Exception:
            pass

    def __repr__(self) -> str:
        try:
            return (
                f"SystemTool("
                f"Running={self.IsRunning}, "
                f"Progress={self.Progress}, "
                f"Succeeded={self.Succeeded}, "
                f"Valid={self.IsValid})"
            )
        except Exception:
            return "SystemTool(<unavailable>)"
