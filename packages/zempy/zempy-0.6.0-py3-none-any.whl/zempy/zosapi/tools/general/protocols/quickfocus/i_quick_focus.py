from __future__ import annotations
from typing import Protocol, runtime_checkable
from zempy.zosapi.tools.protocols.i_system_tool import ISystemTool
from zempy.zosapi.tools.general.enums.quick_focus_criterion import QuickFocusCriterion

@runtime_checkable
class IQuickFocus(ISystemTool, Protocol):
    """Python-facing contract for ZOSAPI.Tools.General.IQuickFocus."""
    # quick-focus specific properties

    @property
    def UseCentroid(self) -> bool: ...
    @UseCentroid.setter
    def UseCentroid(self, value: bool) -> None: ...

    @property
    def Criterion(self) -> QuickFocusCriterion: ...
    @Criterion.setter
    def Criterion(self, value): ...
