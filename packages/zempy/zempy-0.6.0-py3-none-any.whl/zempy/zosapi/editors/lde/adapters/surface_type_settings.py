from __future__ import annotations
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.editors.enums.surface_type import SurfaceType

if TYPE_CHECKING:
    from zempy.zosapi.core.i_zosapi import IZosapi


@dataclass
class SurfaceTypeSettings(BaseAdapter[Z, N]):
    """
    Adapter for ZOSAPI.Editors.LDE.ISurfaceTypeSettings.

    Notes
    -----
    - This is intentionally minimal: its main role is to be created by
      ISurface.GetSurfaceTypeSettings(target_type) and then passed to
      ISurface.ChangeType(settings).
    - Some specific surface types may expose additional typed settings in their
      own native settings objects. Those can be modeled as specialized wrappers
      later and constructed from this adapter's `.native` handle.
    """

    _type: SurfaceType

    # ---- lifecycle ----
    @classmethod
    def from_native_with_type(
        cls, zosapi: IZosapi, native: Any, target_type: SurfaceType
    ) -> "SurfaceTypeSettings":
        if native is None:
            raise _exc.ZemaxObjectGone("SurfaceTypeSettings.from_native_with_type: native is None")
        return cls(zosapi, native, target_type)

    # ---- properties ----
    @property
    def TargetType(self) -> SurfaceType:
        return self._type

    # ---- repr ----
    def __repr__(self) -> str:
        try:
            return f"SurfaceTypeSettings(TargetType={self._type.name})"
        except Exception:
            return "SurfaceTypeSettings(<unavailable>)"
