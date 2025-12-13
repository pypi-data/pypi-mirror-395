from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from allytools.types import str_or_empty
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.property_scalar import PropertyScalar

def _to_datetime(value) -> datetime:
    # raise if None to enforce the contract
    if value is None:
        raise ValueError("MetaData.Date is unexpectedly None")
    if hasattr(value, "ToOADate"):
        return datetime(1899, 12, 30) + timedelta(days=float(value.ToOADate()))
    if isinstance(value, datetime):
        return value
    raise TypeError(f"Unexpected Date type: {type(value)}")

@dataclass
class MetaData(BaseAdapter[Z, N]):

    FeatureDescription  = PropertyScalar("FeatureDescription", coerce_get=str_or_empty)
    LensFile            = PropertyScalar("LensFile", coerce_get=str_or_empty)
    LensTitle           = PropertyScalar("LensTitle", coerce_get=str_or_empty)
    Date                = PropertyScalar("Date", coerce_get=_to_datetime)

    @property
    def DateISO(self) -> Optional[str]:
        dt = self.Date
        return dt.isoformat() if dt else None

    def __repr__(self) -> str:
        dt = self.Date
        date_str = (
            dt.strftime("%Y-%m-%d %H:%M:%S") if isinstance(dt, datetime) else "None"
        )
        return (
            f"MetaData("
            f"Feature='{self.FeatureDescription}', "
            f"Lens='{self.LensTitle}', "
            f"Date={date_str})"
        )

