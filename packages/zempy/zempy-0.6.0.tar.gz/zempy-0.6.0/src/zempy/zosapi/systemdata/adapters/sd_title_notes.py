from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N,
    PropertyScalar,
    dataclass,
)


@dataclass
class SDTitleNotes(BaseAdapter[Z,N]):
    """
    Adapter for ZOSAPI.SystemData.ISDTitleNotes.
    Provides access to Title, Notes, and Author fields in System Explorer → Notes.
    """

    Title  = PropertyScalar("Title",  coerce_get=str, coerce_set=str)
    Notes  = PropertyScalar("Notes",  coerce_get=str, coerce_set=str)
    Author = PropertyScalar("Author", coerce_get=str, coerce_set=str)

    def __repr__(self) -> str:
        try:
            return f"SDTitleNotes(Title={self.Title!r}, Author={self.Author!r})"
        except Exception:
            return "SDTitleNotes(<unavailable>)"
