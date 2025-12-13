from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class IWavelength(Protocol):
    """
    Protocol mirror of ZOSAPI.SystemData.IWavelength.
    Represents a single system wavelength (accessible via IWavelengths).
    """

    # -------- Methods --------
    def MakePrimary(self) -> None:
        """Make this wavelength the primary system wavelength."""
        ...

    # -------- Properties --------
    @property
    def WavelengthNumber(self) -> int:
        """1-based index of this wavelength in the system list."""
        ...

    @property
    def IsActive(self) -> bool:
        """True if this wavelength is active/enabled."""
        ...

    @property
    def IsPrimary(self) -> bool:
        """True if this is the primary wavelength."""
        ...

    @property
    def Wavelength(self) -> float:
        """Wavelength value (in system units, e.g., micrometers)."""
        ...
    @Wavelength.setter
    def Wavelength(self, value: float) -> None:
        ...

    @property
    def Weight(self) -> float:
        """Merit-function weight for this wavelength."""
        ...
    @Weight.setter
    def Weight(self, value: float) -> None:
        ...
