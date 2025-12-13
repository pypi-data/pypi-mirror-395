from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.editors.adapters.solve_data import SolveData

@dataclass(frozen=True, slots=True)
class SolveAplanatic(SolveData):
    pass

@dataclass(frozen=True, slots=True)
class SolveAutomatic(SolveData):
    by = PropertyScalar('by', coerce_get=str)

@dataclass(frozen=True, slots=True)
class SolveCenterOfCurvature(SolveData):
    pass


@dataclass(frozen=True, slots=True)
class SolveChiefRayAngle(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveChiefRayHeight(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveChiefRayNormal(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveCocentricRadius(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveCocentricSurface(SolveData):
    pass


@dataclass(frozen=True, slots=True)
class SolveCompensator(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveConfigPickup(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveDuplicateSag(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveEdgeThickness(SolveData):
    Thickness = PropertyScalar('Thickness', coerce_get=float, coerce_set=float)
    RadialHeight = PropertyScalar('RadialHeight', coerce_get=float, coerce_set=float)
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveElementPower(SolveData):
    Power = PropertyScalar('Power', coerce_get=float, coerce_set=float)
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveFieldPickup(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveFixed(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveFNumber(SolveData):
    FNumber = PropertyScalar('FNumber', coerce_get=float, coerce_set=float)
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveInvertSag(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveMarginalRayAngle(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveMarginalRayHeight(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveMarginalRayNormal(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveMaterialModel(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveMaterialOffset(SolveData):
    Offset = PropertyScalar('Offset', coerce_get=float, coerce_set=float)
    # Some STAR solves expose Offset; if not present at runtime, your run_native wrapper will surface it.
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveMaterialSubstitute(SolveData):
    Catalog = PropertyScalar('Catalog', coerce_get=str, coerce_set=str)
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveMaximum(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveNone(SolveData):
    pass


@dataclass(frozen=True, slots=True)
class SolveObjectPickup(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveOpticalPathDifference(SolveData):
    OPD = PropertyScalar('OPD', coerce_get=float, coerce_set=float)
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolvePickupChiefRay(SolveData):
    Field = PropertyScalar('Field', coerce_get=int, coerce_set=int)
    Wavelength = PropertyScalar('Wavelength', coerce_get=int, coerce_set=int)
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolvePosition(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolvePupilPosition(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveSurfacePickup(SolveData):
    pass


@dataclass(frozen=True, slots=True)
class SolveThermalPickup(SolveData):
    Documentation = PropertyScalar('Documentation', coerce_get=str)
    set = PropertyScalar('set', coerce_get=str)
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveVariable(SolveData):
    by = PropertyScalar('by', coerce_get=str)


@dataclass(frozen=True, slots=True)
class SolveZPLMacro(SolveData):
    by = PropertyScalar('by', coerce_get=str)

__all__ = [
    "SolveData",
    "SolveAplanatic",
    "SolveAutomatic",
    "SolveCenterOfCurvature",
    "SolveChiefRayAngle",
    "SolveChiefRayHeight",
    "SolveChiefRayNormal",
    "SolveCocentricRadius",
    "SolveCocentricSurface",
    "SolveCompensator",
    "SolveConfigPickup",
    "SolveDuplicateSag",
    "SolveEdgeThickness",
    "SolveElementPower",
    "SolveFieldPickup",
    "SolveFixed",
    "SolveFNumber",
    "SolveInvertSag",
    "SolveMarginalRayAngle",
    "SolveMarginalRayHeight",
    "SolveMarginalRayNormal",
    "SolveMaterialModel",
    "SolveMaterialOffset",
    "SolveMaterialSubstitute",
    "SolveMaximum",
    "SolveNone",
    "SolveObjectPickup",
    "SolveOpticalPathDifference",
    "SolvePickupChiefRay",
    "SolvePosition",
    "SolvePupilPosition",
    "SolveSurfacePickup",
    "SolveThermalPickup",
    "SolveVariable",
    "SolveZPLMacro",
]