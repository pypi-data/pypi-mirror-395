from __future__ import annotations
from typing import Protocol, runtime_checkable, Optional
from zempy.zosapi.tools.enums.run_status import RunStatus


@runtime_checkable
class ISystemTool(Protocol):
    """Protocol mirroring ZOSAPI.Tools.ISystemTool with PascalCase members.

    - Methods return bool for success unless ZOSAPI specifies a RunStatus.
    - Properties are read-only as per the ZOSAPI interface.
    """

    # -------- Public Member Functions --------
    def Run(self) -> bool:
        """Start the tool (blocks for synchronous tools, returns immediately for async)."""

    def RunAndWaitForCompletion(self) -> bool:
        """Equivalent to calling Run() followed by WaitForCompletion()."""

    def WaitForCompletion(self) -> bool:
        """Wait for an asynchronous tool to complete."""

    def Cancel(self) -> bool:
        """Cancel a currently running asynchronous tool."""

    def Close(self) -> bool:
        """Close the tool and free associated resources."""

    def WaitWithTimeout(self, timeOutSeconds: float) -> RunStatus:
        """Wait for completion with timeout; if exceeded, returns while tool may continue running."""

    def RunAndWaitWithTimeout(self, timeOutSeconds: float) -> RunStatus:
        """Start and wait with timeout; if exceeded, returns while tool may continue running."""

    # -------- Properties --------
    @property
    def Progress(self) -> int:
        """Progress of the current tool, if supported."""

    @property
    def Status(self) -> str:
        """Status string of the current tool, if supported."""

    @property
    def IsRunning(self) -> bool:
        """Whether the tool is currently running asynchronously."""

    @property
    def CanCancel(self) -> bool:
        """Whether the tool supports cancellation."""

    @property
    def IsAsynchronous(self) -> bool:
        """Whether the tool runs asynchronously (on a thread)."""

    @property
    def IsFiniteDuration(self) -> bool:
        """Whether this tool will complete on its own."""

    @property
    def IsValid(self) -> bool:
        """Whether the current input settings are valid."""

    @property
    def Succeeded(self) -> bool:
        """Whether the last execution of the tool succeeded."""

    @property
    def ErrorMessage(self) -> Optional[str]:
        """Error message if Succeeded is False; otherwise None."""
