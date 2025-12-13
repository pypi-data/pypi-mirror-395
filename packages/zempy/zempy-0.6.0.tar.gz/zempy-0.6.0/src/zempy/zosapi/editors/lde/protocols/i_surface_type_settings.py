from __future__ import annotations
from typing import Protocol, runtime_checkable, Any
from zempy.zosapi.editors.enums.surface_type import SurfaceType


@runtime_checkable
class ISurfaceTypeSettings(Protocol):
    """
    Protocol for ZOSAPI.Editors.LDE.ISurfaceTypeSettings.

    A lightweight, opaque settings handle used to switch an LDE surface type.
    Instances are obtained via:
        surface.GetSurfaceTypeSettings(SurfaceType.X)
    and then passed into:
        surface.ChangeType(settings)
    """

    # Opaque native object (COM/.NET). Exposed so adapters can pass-through.
    native: Any

    @property
    def TargetType(self) -> SurfaceType: ...
    """The target SurfaceType these settings correspond to."""
