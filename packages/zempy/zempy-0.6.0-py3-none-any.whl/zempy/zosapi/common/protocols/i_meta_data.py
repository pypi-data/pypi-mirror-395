from __future__ import annotations
from typing import Protocol, runtime_checkable

@runtime_checkable
class IMetadata(Protocol):
    """Typed facade of ZOSAPI.Common.IMetadata."""

    # --- Methods (Public Member Functions) ---
    def GetKeyName(self, keyNumber: int) -> str:
        """1-based key index: valid values are 1..NumberOfKeys (inclusive)."""
        ...

    def GetData(self, key: str) -> str:
        ...

    def SetData(self, key: str, value: str) -> None:
        ...

    def RemoveData(self, key: str) -> bool:
        ...

    def ConvertFromBinary(self, data: bytes) -> str:
        ...

    def ConvertToBinary(self, s: str) -> bytes:
        ...

    def CreateGuid(self) -> str:
        ...

    # --- Properties ---
    @property
    def NumberOfKeys(self) -> int:
        ...

