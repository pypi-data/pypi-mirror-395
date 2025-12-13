from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar


BytesLike = Union[bytes, bytearray, memoryview]


@dataclass
class Metadata(BaseAdapter):
    """    Adapter for ZOSAPI.Common.IMetadata. """

    NumberOfKeys = PropertyScalar("NumberOfKeys", coerce_get=int)

    def GetKeyName(self, keyNumber: int) -> str:
        if keyNumber < 1:
            raise ValueError(f"keyNumber must be >= 1, got {keyNumber}.")
        # (Optional) enforce upper bound; cheap and friendly error message
        total = self.NumberOfKeys
        if keyNumber > total:
            raise ValueError(f"keyNumber out of range: {keyNumber} > NumberOfKeys({total}).")

        return str(
            run_native(
                "IMetadata.GetKeyName",
                lambda: self.native.GetKeyName(int(keyNumber)),
                ensure=self.ensure_native,
            )
        )

    def GetData(self, key: str) -> str:
        return str(
            run_native(
                "IMetadata.GetData",
                lambda: self.native.GetData(str(key)),
                ensure=self.ensure_native,
            )
        )

    def SetData(self, key: str, value: str) -> None:
        run_native(
            "IMetadata.SetData",
            lambda: self.native.SetData(str(key), str(value)),
            ensure=self.ensure_native,
        )

    def RemoveData(self, key: str) -> bool:
        return bool(
            run_native(
                "IMetadata.RemoveData",
                lambda: self.native.RemoveData(str(key)),
                ensure=self.ensure_native,
            )
        )

    # --- Binary helpers ---

    def ConvertFromBinary(self, data: BytesLike) -> str:
        """
        Convert a bytes-like payload (bytes/bytearray/memoryview) to a string
        using the native ZOSAPI conversion.
        """
        # pythonnet typically understands Python bytes-like as System.Byte[]
        payload = bytes(data)
        return str(
            run_native(
                "IMetadata.ConvertFromBinary",
                lambda: self.native.ConvertFromBinary(payload),
                ensure=self.ensure_native,
            )
        )

    def ConvertToBinary(self, s: str) -> bytes:
        """
        Convert a string to binary (returned as Python `bytes`) using the native conversion.
        """
        raw = run_native(
            "IMetadata.ConvertToBinary",
            lambda: self.native.ConvertToBinary(str(s)),
            ensure=self.ensure_native,
        )
        # `raw` is usually a .NET byte[]; `bytes(raw)` safely copies to Python bytes
        return bytes(raw)

    def CreateGuid(self) -> str:
        return str(
            run_native(
                "IMetadata.CreateGuid",
                lambda: self.native.CreateGuid(),
                ensure=self.ensure_native,
            )
        )


__all__ = ["Metadata"]
