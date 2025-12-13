from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Sequence
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.editors.enums.surface_type import SurfaceType
from zempy.zosapi.editors.lde.enums.surface_column import SurfaceColumn
from zempy.zosapi.common.adapters.meta_data import Metadata
from zempy.zosapi.editors.lde.adapters.coating_performance_data import CoatingPerformanceData

@dataclass
class LDERow(BaseAdapter[Z, N]):

    IsActive        = PropertyScalar("IsActive", coerce_get=bool)
    SurfaceNumber   = PropertyScalar("SurfaceNumber", coerce_get=int)
    TypeName        = PropertyScalar("TypeName", coerce_get=str)
    IsObject        = PropertyScalar("IsObject", coerce_get=bool)
    IsImage         = PropertyScalar("IsImage", coerce_get=bool)
    IsStop          = PropertyScalar("IsStop", coerce_get=bool, coerce_set=bool)
    Comment         = PropertyScalar("Comment", coerce_get=str, coerce_set=str)
    Radius          = PropertyScalar("Radius", coerce_get=float, coerce_set=float)
    Thickness       = PropertyScalar("Thickness", coerce_get=float, coerce_set=float)
    Material        = PropertyScalar("Material", coerce_get=str, coerce_set=str)
    Coating         = PropertyScalar("Coating", coerce_get=str, coerce_set=str)
    SemiDiameter    = PropertyScalar("SemiDiameter", coerce_get=float, coerce_set=float)
    ChipZone        = PropertyScalar("ChipZone", coerce_get=float, coerce_set=float)
    MechanicalSemiDiameter = PropertyScalar("MechanicalSemiDiameter", coerce_get=float, coerce_set=float)
    Conic           = PropertyScalar("Conic", coerce_get=float, coerce_set=float)
    TCE             = PropertyScalar("TCE", coerce_get=float, coerce_set=float)
    SurfaceId       = PropertyScalar("SurfaceId", coerce_get=int)
    MaterialCatalog = PropertyScalar("MaterialCatalog", coerce_get=str)

    # ----- enum -----
    Type = property_enum("Type", SurfaceType, label="LDERow")  # uses self._ensure_native under the hood

    # ----- object helpers -----
    def GetMetadata(self) -> Metadata:
        md = self._rn("ILDERow.GetMetadata", lambda: self.native.GetMetadata())
        return Metadata.from_native(self.zosapi, md)

    def GetCoatingPerformanceData(self) -> CoatingPerformanceData:
        cpd = self._rn("ILDERow.GetCoatingPerformanceData", lambda: self.native.GetCoatingPerformanceData())
        return CoatingPerformanceData.from_native(self.zosapi, cpd)

    # ----- methods -----
    def GetSurfaceCell(self, Col: SurfaceColumn | Any) -> Any:
        raw = SurfaceColumn.to_native(self.zosapi, Col) if hasattr(Col, "name") else getattr(Col, "value", Col)
        return self._rn("ILDERow.GetSurfaceCell", lambda: self.native.GetSurfaceCell(raw))

    def AvailableSurfaceTypes(self) -> Sequence[SurfaceType]:
        seq = self._rn("ILDERow.AvailableSurfaceTypes", lambda: self.native.AvailableSurfaceTypes())
        if hasattr(SurfaceType, "from_native"):
            return tuple(SurfaceType.from_native(self.zosapi, x) for x in seq)
        return tuple(seq)

    def GetSurfaceTypeSettings(self, type_: SurfaceType | Any) -> Any:
        raw = SurfaceType.to_native(self.zosapi, type_) if hasattr(type_, "name") else getattr(type_, "value", type_)
        return self._rn("ILDERow.GetSurfaceTypeSettings", lambda: self.native.GetSurfaceTypeSettings(raw))

    def ChangeType(self, settings: Any) -> bool:
        return bool(self._rn("ILDERow.ChangeType", lambda: self.native.ChangeType(settings)))

    def __repr__(self) -> str:
        try:
            return f"LDERow(S={self.SurfaceNumber}, Type={self.TypeName}, Active={self.IsActive})"
        except Exception:
            return "LDERow(<unavailable>)"
