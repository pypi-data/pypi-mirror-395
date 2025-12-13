from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native, validate_cast,
    PropertyScalar, property_enum, property_adapter, PropertySequence, PropertyEnum,
    dataclass, Optional, TYPE_CHECKING, logging,
)


@dataclass
class Wavelength(BaseAdapter[Z, N]):
    """
    Adapter for ZOSAPI.SystemData.IWavelength.
    Represents a single system wavelength.
    """

    # ---- Properties (read/write or read-only as per ZOSAPI) ----
    WavelengthNumber = PropertyScalar("WavelengthNumber", coerce_get=int)
    IsActive         = PropertyScalar("IsActive",         coerce_get=bool)
    IsPrimary        = PropertyScalar("IsPrimary",        coerce_get=bool)

    Wavelength       = PropertyScalar("Wavelength",       coerce_get=float, coerce_set=float)
    Weight           = PropertyScalar("Weight",           coerce_get=float, coerce_set=float)

    # ---- Methods ----
    def MakePrimary(self) -> None:
        self._rn("IWavelength.MakePrimary", lambda: self.native.MakePrimary())

    # ---- Debug ----
    def __repr__(self) -> str:
        try:
            return (f"Wavelength(No={self.WavelengthNumber}, "
                    f"λ={self.Wavelength}, w={self.Weight}, "
                    f"primary={self.IsPrimary}, active={self.IsActive})")
        except Exception:
            return "Wavelength(<unavailable>)"
