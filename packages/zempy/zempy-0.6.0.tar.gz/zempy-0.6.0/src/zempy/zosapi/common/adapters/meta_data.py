from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Iterable, Tuple

from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar


@dataclass(frozen=True, slots=True)
class Metadata:
    """
    Adapter for ZOSAPI.Common.IMetadata.
    Follows the IAR-style pattern (frozen dataclass, from_native, ensure_native).
    """
    zosapi: object
    native: object

    # ---- lifecycle ----
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "Metadata":
        if native is None:
            raise ValueError("Metadata.from_native: native is None")
        return cls(zosapi, native)  # type: ignore[arg-type]

    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="Metadata.native", exc_type=_exc.ZemaxObjectGone)

    # ---- scalar property (descriptor) ----
    NumberOfKeys = PropertyScalar("NumberOfKeys", coerce_get=int)

    # ---- core API (thin passthroughs with run_native) ----
    def GetKeyName(self, keyNumber: int) -> str:
        return run_native(
            "IMetadata.GetKeyName",
            lambda: self.native.GetKeyName(int(keyNumber)),
            ensure=self.ensure_native,
        )

    def GetData(self, key: str) -> str:
        return run_native(
            "IMetadata.GetData",
            lambda: self.native.GetData(str(key)),
            ensure=self.ensure_native,
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

    def ConvertFromBinary(self, data: bytes) -> str:
        return run_native(
            "IMetadata.ConvertFromBinary",
            lambda: self.native.ConvertFromBinary(bytes(data)),
            ensure=self.ensure_native,
        )

    def ConvertToBinary(self, s: str) -> bytes:
        return run_native(
            "IMetadata.ConvertToBinary",
            lambda: self.native.ConvertToBinary(str(s)),
            ensure=self.ensure_native,
        )

    def CreateGuid(self) -> str:
        return run_native(
            "IMetadata.CreateGuid",
            lambda: self.native.CreateGuid(),
            ensure=self.ensure_native,
        )

    # ---- convenience helpers (pure Python; optional) ----
    def keys_seq(self) -> Sequence[str]:
        """Return all key names in 1..NumberOfKeys order."""
        n = self.NumberOfKeys
        return [self.GetKeyName(i) for i in range(1, n + 1)]

    def items(self) -> Iterable[Tuple[str, str]]:
        for k in self.keys_seq():
            yield k, self.GetData(k)

    def to_dict(self) -> dict[str, str]:
        return {k: v for k, v in self.items()}

    def set_binary(self, key: str, data: bytes) -> None:
        self.SetData(key, self.ConvertFromBinary(data))

    def get_binary(self, key: str) -> bytes:
        return self.ConvertToBinary(self.GetData(key))

    # ---- repr ----
    def __repr__(self) -> str:
        try:
            return f"Metadata(Keys={self.NumberOfKeys})"
        except Exception:
            return "Metadata(<unavailable>)"
