from __future__ import annotations
from typing import Protocol, runtime_checkable, Sequence, TYPE_CHECKING
from .i_wavelength import IWavelength
from zempy.zosapi.systemdata.enums import WavelengthPreset, QuadratureSteps

@runtime_checkable
class IWavelengths(Protocol):
    """Protocol mirror of ZOSAPI.SystemData.IWavelengths."""

    def GetWavelength(self, position: int) -> IWavelength:
        """Gets the wavelength at 1-based index 'position'."""
        ...

    def AddWavelength(self, Wavelength: float, Weight: float) -> IWavelength:
        """Adds a new wavelength at the end and returns it."""
        ...

    def RemoveWavelength(self, position: int) -> bool:
        """Removes the wavelength at 1-based index 'position'. Returns True on success."""
        ...

    # -------- Presets / generation --------
    def SelectWavelengthPreset(self, preset: "WavelengthPreset") -> bool:
        """
        Replaces all system wavelengths with a preset definition.
        Returns True on success.
        """
        ...

    def GaussianQuadrature(self, minWave: float, maxWave: float, numSteps: "QuadratureSteps") -> bool:
        """
        Generates system wavelengths using a Gaussian Quadrature method.
        Returns True on success.
        """
        ...

    # -------- Optional convenience (commonly present) --------
    @property
    def NumberOfWavelengths(self) -> int:
        """Total number of wavelengths currently defined."""
        ...

    @property
    def Primary(self) -> IWavelength:
        """The current primary wavelength."""
        ...

    # Optional helper to fetch all (if underlying API supports enumeration)
    def GetAllWavelengths(self) -> Sequence[IWavelength]:
        """Returns all wavelength entries. (May be implemented by adapters.)"""
        ...
