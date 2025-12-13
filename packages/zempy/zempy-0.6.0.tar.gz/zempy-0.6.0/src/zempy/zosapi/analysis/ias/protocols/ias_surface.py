from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from zempy.zosapi.analysis.protocols.i_message import IMessage


@runtime_checkable
class IAS_Surface(Protocol):
    """ZOSAPI.Analysis.Settings.IAS_Surface"""

    def GetSurfaceNumber(self) -> int: ...
    def SetSurfaceNumber(self, N: int) -> IMessage: ...

    def UseImageSurface(self) -> IMessage: ...
    def UseObjectiveSurface(self) -> IMessage: ...
