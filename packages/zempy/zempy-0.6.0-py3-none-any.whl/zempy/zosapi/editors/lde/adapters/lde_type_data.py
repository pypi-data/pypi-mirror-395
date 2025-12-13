from __future__ import annotations
from typing import ClassVar, Any
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.common.enums.zemax_color import ZemaxColor
from zempy.zosapi.common.enums.zemax_opacity import ZemaxOpacity
from zempy.zosapi.core.interop import ensure_not_none
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum


class LDETypeData(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Editors.LDE.ILDETypeData (Surface properties tab).

    Provides Pythonic access to surface coloring, opacity, stop/GCR flags, and
    related toggles. Validation follows the standard IAS conventions.
    """

    REQUIRED_NATIVE_ATTRS: ClassVar[tuple[str, ...]] = (
        "SurfaceColor",
        "SurfaceOpacity",
        "RowColor",
        "IsStop",
        "CanBeStop",
        "IsGlobalCoordinateReference",
        "CanBeGCR",
        "IgnoreSurface",
        "SurfaceCannotBeHyperhemispheric",
    )
    SurfaceColor    = property_enum("SurfaceColor", ZemaxColor)
    SurfaceOpacity  = property_enum("SurfaceOpacity", ZemaxOpacity)
    RowColor        = property_enum("RowColor", ZemaxColor)
    IsStop: bool = PropertyScalar("IsStop", coerce_get=bool, coerce_set=bool)  # type: ignore[assignment]
    CanBeStop: bool = PropertyScalar("CanBeStop", coerce_get=bool)             # read-only  # type: ignore[assignment]

    IsGlobalCoordinateReference: bool = PropertyScalar(
        "IsGlobalCoordinateReference", coerce_get=bool, coerce_set=bool
    )  # type: ignore[assignment]
    CanBeGCR: bool = PropertyScalar("CanBeGCR", coerce_get=bool)               # read-only  # type: ignore[assignment]

    IgnoreSurface: bool = PropertyScalar("IgnoreSurface", coerce_get=bool, coerce_set=bool)  # type: ignore[assignment]

    SurfaceCannotBeHyperhemispheric: bool = PropertyScalar(
        "SurfaceCannotBeHyperhemispheric", coerce_get=bool, coerce_set=bool
    )  # type: ignore[assignment]


