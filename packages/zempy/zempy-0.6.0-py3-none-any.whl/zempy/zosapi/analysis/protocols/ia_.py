from __future__ import annotations
from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from zempy.zosapi.analysis.ias.protocols.ias_ import IAS_
    from zempy.zosapi.analysis.iar.protocols.iar_ import IAR_
    from zempy.zosapi.analysis.protocols.i_message import IMessage
    from zempy.zosapi.analysis.protocols.i_messages import IMessages
    from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM


@runtime_checkable
class IA_(Protocol):

    def GetSettings(self) -> IAS_: ...
    """Gets the settings for the current analysis."""

    def GetResults(self) -> IAR_: ...
    """Gets the result data (if available) for the current analysis."""

    def IsRunning(self) -> bool: ...
    """Determines whether this analysis is currently updating."""

    def Apply(self) -> "IMessage": ...
    """Re-run the analysis using current settings; returns a status message."""

    def ApplyAndWaitForCompletion(self) -> "IMessage": ...
    """Re-runs the analysis with current settings and blocks until completion."""

    def Terminate(self) -> bool: ...
    """Attempt to cancel the currently running analysis."""

    def WaitForCompletion(self) -> None: ...
    """Waits for the current analysis to finish running (if applicable)."""

    def Close(self) -> None: ...
    """Closes this analysis; removes it from the system permanently."""

    def Release(self) -> None: ...
    """Disconnect this object from the interface without removing analysis."""

    def ToFile(self, Filename: str, showSettings: bool = False, verify: bool = False) -> None: ...
    """Export the analysis to a file; optionally include settings and verify."""

    def run(self) -> IAR_: ...
    """Convenience: ApplyAndWaitForCompletion() then GetResults()."""

    @property
    def Title(self) -> str: ...
    """Window title of the analysis."""

    @property
    def GetAnalysisName(self) -> str: ...
    """Human-readable analysis name."""

    @property
    def AnalysisType(self) -> "AnalysisIDM": ...
    """Enum identifying the analysis type."""

    @property
    def StatusMessages(self) -> "IMessages": ...
    """Status message collection from the analysis."""

    @property
    def HasAnalysisSpecificSettings(self) -> bool: ...
    """
    True if a fully-implemented settings interface is available.
    If False, settings must be changed via IAS_.ModifySettings.
    """
