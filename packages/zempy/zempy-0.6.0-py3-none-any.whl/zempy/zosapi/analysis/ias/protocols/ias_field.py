from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from zempy.zosapi.analysis.protocols.i_message import IMessage

@runtime_checkable
class IAS_Field(Protocol):
    """ZOSAPI.Analysis.Settings.IAS_Field"""

    def GetFieldNumber(self) -> int: ...
    def SetFieldNumber(self, N: int) -> IMessage: ...
    def UseAllFields(self) -> IMessage: ...


