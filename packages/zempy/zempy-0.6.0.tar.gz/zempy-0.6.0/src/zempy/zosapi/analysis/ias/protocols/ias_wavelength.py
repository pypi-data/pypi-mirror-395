from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from zempy.zosapi.analysis.protocols.i_message import IMessage

@runtime_checkable
class IAS_Wavelength(Protocol):
    """ZOSAPI.Analysis.Settings.IAS_Wavelength"""

    def GetWavelengthNumber(self) -> int: ...
    def SetWavelengthNumber(self, N: int) -> IMessage: ...
    def UseAllWavelengths(self) -> IMessage: ...
