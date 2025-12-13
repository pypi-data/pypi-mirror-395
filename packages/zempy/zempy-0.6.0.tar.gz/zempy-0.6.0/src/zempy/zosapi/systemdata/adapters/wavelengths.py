from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native, validate_cast,
    PropertyScalar, property_enum, property_adapter, PropertySequence, PropertyEnum,
    dataclass, Optional, TYPE_CHECKING, logging,
)
from typing import Sequence
from zempy.zosapi.systemdata.adapters.wavelength import Wavelength
from zempy.zosapi.systemdata.enums.wavelength_preset import WavelengthPreset
from zempy.zosapi.systemdata.enums.quadrature_steps import QuadratureSteps


@dataclass
class Wavelengths(BaseAdapter[Z, N]):
    """
    Adapter for ZOSAPI.SystemData.IWavelengths.
    Provides full wavelength management (add/remove/get, presets, quadrature).
    """


    NumberOfWavelengths = PropertyScalar("NumberOfWavelengths", coerce_get=int)
    Primary = property_adapter("Primary", Wavelength)


    def GetWavelength(self, position: int) -> Wavelength:
        native = self._rn(
            "IWavelengths.GetWavelength",
            lambda: self.native.GetWavelength(position)
        )
        return Wavelength.from_native(self.zosapi, native)

    def AddWavelength(self, WavelengthValue: float, Weight: float) -> Wavelength:
        native = self._rn(
            "IWavelengths.AddWavelength",
            lambda: self.native.AddWavelength(WavelengthValue, Weight)
        )
        return Wavelength.from_native(self.zosapi, native)

    def RemoveWavelength(self, position: int) -> bool:
        return bool(self._rn(
            "IWavelengths.RemoveWavelength",
            lambda: self.native.RemoveWavelength(position)
        ))

    def SelectWavelengthPreset(self, preset: WavelengthPreset) -> bool:
        native_enum = WavelengthPreset.to_native(self.zosapi, preset)
        return bool(self._rn(
            "IWavelengths.SelectWavelengthPreset",
            lambda: self.native.SelectWavelengthPreset(native_enum)
        ))

    def GaussianQuadrature(self, minWave: float, maxWave: float, numSteps: QuadratureSteps) -> bool:
        native_enum = QuadratureSteps.to_native(self.zosapi, numSteps)
        return bool(self._rn(
            "IWavelengths.GaussianQuadrature",
            lambda: self.native.GaussianQuadrature(minWave, maxWave, native_enum)
        ))

    def GetAllWavelengths(self) -> Sequence[Wavelength]:
        """
        Returns all wavelength entries, using direct native enumeration if present,
        otherwise falling back to indexed access.
        """
        try:
            # Native enumerable (depends on ZOSAPI version)
            seq = self._rn(
                "IWavelengths.GetAllWavelengths",
                lambda: self.native.GetAllWavelengths()
            )
            return tuple(Wavelength.from_native(self.zosapi, x) for x in seq)
        except Exception:
            # Fallback – safe for all OpticStudio versions
            count = int(self.NumberOfWavelengths)
            return tuple(self.GetWavelength(i) for i in range(1, count + 1))

    def __repr__(self) -> str:
        try:
            cnt = self.NumberOfWavelengths
            prim = self.Primary
            return f"Wavelengths(count={cnt}, primary={prim.Wavelength}µm)"
        except Exception:
            return "Wavelengths(<unavailable>)"
