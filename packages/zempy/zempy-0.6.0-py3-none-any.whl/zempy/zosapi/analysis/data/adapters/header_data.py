from __future__ import annotations
from dataclasses import dataclass
from allytools.types import str_or_empty
from zempy.zosapi.core.interop import ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_sequence import PropertySequence

@dataclass(frozen=True, slots=True)
class HeaderData:
    """Minimal adapter for IAR_HeaderData (Lines: Sequence[str])."""
    zosapi: object
    native: object

    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "HeaderData":
        if native is None:
            raise ValueError("HeaderData.from_native: native is None")
        return cls(zosapi, native)

    def ensure_native(self) -> None:
        ensure_not_none(
            self.native, what="HeaderData.native", exc_type=_exc.ZemaxObjectGone
        )

    Lines = PropertySequence("Lines", coerce_item=str_or_empty, container=list)

    def __repr__(self) -> str:
        try:
            return f"HeaderData({len(self.Lines)} lines)"
        except Exception:
            return "HeaderData(<unavailable>)"
