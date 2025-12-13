from __future__ import annotations
from typing import Protocol, runtime_checkable
from zempy.zosapi.analysis.enums.sample_sizes import SampleSizes

@runtime_checkable
class IAS_ZernikeStandardCoefficients(Protocol):
    """Protocol for ZOSAPI.Analysis.Settings.Aberrations.IAS_ZernikeStandardCoefficients."""

    @property
    def SampleSize(self) -> SampleSizes:
        ...

    @SampleSize.setter
    def SampleSize(self, v: SampleSizes) -> None:
        ...

    @property
    def ReferenceOBDToVertex(self) -> bool:
        ...

    @ReferenceOBDToVertex.setter
    def ReferenceOBDToVertex(self, v: bool) -> None:
        ...

    @property
    def Sx(self) -> float:
        ...

    @Sx.setter
    def Sx(self, v: float) -> None:
        ...

    @property
    def Sy(self) -> float:
        ...

    @Sy.setter
    def Sy(self, v: float) -> None:
        ...

    @property
    def Sr(self) -> float:
        ...

    @Sr.setter
    def Sr(self, v: float) -> None:
        ...

    @property
    def Epsilon(self) -> float:
        ...

    @Epsilon.setter
    def Epsilon(self, v: float) -> None:
        ...

    @property
    def MaximumNumberOfTerms(self) -> int:
        ...

    @MaximumNumberOfTerms.setter
    def MaximumNumberOfTerms(self, v: int) -> None:
        ...
