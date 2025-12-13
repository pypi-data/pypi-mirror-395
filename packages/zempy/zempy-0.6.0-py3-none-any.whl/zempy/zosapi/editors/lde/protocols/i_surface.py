from __future__ import annotations
from typing import Protocol, runtime_checkable
from zempy.zosapi.editors.enums.surface_type import SurfaceType
from zempy.zosapi.editors.lde.protocols.ilde_row import ILDERow

@runtime_checkable
class ISurface(Protocol):
    """
    Protocol mirror of ZOSAPI.Editors.LDE.ISurface.
    Only read-only properties exposed here, matching the .NET interface.
    """

    @property
    def SurfaceType(self) -> SurfaceType:
        """System.Type of the concrete surface class (e.g., Standard, EvenAsphere, Zernike Fringe, etc.)."""
        ...

    @property
    def Row(self) -> ILDERow:
        """The associated LDE row accessor."""
        ...

    @property
    def IsValid(self) -> bool:
        """True if the surface is valid (exists and can be accessed)."""
        ...

    @property
    def Id(self) -> int:
        """Unique surface identifier (long in .NET; int in Python)."""
        ...
