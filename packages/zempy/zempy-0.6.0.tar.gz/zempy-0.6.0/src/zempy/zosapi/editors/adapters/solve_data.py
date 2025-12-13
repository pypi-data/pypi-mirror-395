from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from typing import TYPE_CHECKING
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.editors.enums.solve_type import SolveType
from zempy.zosapi.editors.adapters.solves import *


if TYPE_CHECKING:
    from zempy.zosapi.editors.protocols.solve import *

@dataclass(frozen=True, slots=True)
class SolveData(BaseAdapter[Z, N]):


    IsValid = PropertyScalar('IsValid', coerce_get=bool)
    Type = property_enum('Type', SolveType, label='ISolveData')

    _S_None                = property_adapter("_S_None",                SolveNone)
    _S_Fixed               = property_adapter("_S_Fixed",               SolveFixed)
    _S_Variable            = property_adapter("_S_Variable",            SolveVariable)
    _S_SurfacePickup       = property_adapter("_S_SurfacePickup",       SolveSurfacePickup)
    _S_ZPLMacro            = property_adapter("_S_ZPLMacro",            SolveZPLMacro)
    _S_MarginalRayAngle    = property_adapter("_S_MarginalRayAngle",    SolveMarginalRayAngle)
    _S_MarginalRayHeight   = property_adapter("_S_MarginalRayHeight",   SolveMarginalRayHeight)
    _S_ChiefRayAngle       = property_adapter("_S_ChiefRayAngle",       SolveChiefRayAngle)
    _S_MarginalRayNormal   = property_adapter("_S_MarginalRayNormal",   SolveMarginalRayNormal)
    _S_ChiefRayNormal      = property_adapter("_S_ChiefRayNormal",      SolveChiefRayNormal)
    _S_Aplanatic           = property_adapter("_S_Aplanatic",           SolveAplanatic)
    _S_ElementPower        = property_adapter("_S_ElementPower",        SolveElementPower)
    _S_CocentricSurface    = property_adapter("_S_CocentricSurface",    SolveCocentricSurface)
    _S_CocentricRadius     = property_adapter("_S_CocentricRadius",     SolveCocentricRadius)
    _S_FNumber             = property_adapter("_S_FNumber",             SolveFNumber)
    _S_ChiefRayHeight      = property_adapter("_S_ChiefRayHeight",      SolveChiefRayHeight)
    _S_EdgeThickness       = property_adapter("_S_EdgeThickness",       SolveEdgeThickness)
    _S_OpticalPathDifference = property_adapter("_S_OpticalPathDifference", SolveOpticalPathDifference)
    _S_Position            = property_adapter("_S_Position",            SolvePosition)
    _S_Compensator         = property_adapter("_S_Compensator",         SolveCompensator)
    _S_CenterOfCurvature   = property_adapter("_S_CenterOfCurvature",   SolveCenterOfCurvature)
    _S_PupilPosition       = property_adapter("_S_PupilPosition",       SolvePupilPosition)
    _S_MaterialModel       = property_adapter("_S_MaterialModel",       SolveMaterialModel)
    _S_MaterialSubstitute  = property_adapter("_S_MaterialSubstitute",  SolveMaterialSubstitute)
    _S_MaterialOffset      = property_adapter("_S_MaterialOffset",      SolveMaterialOffset)
    _S_Automatic           = property_adapter("_S_Automatic",           SolveAutomatic)
    _S_Maximum             = property_adapter("_S_Maximum",             SolveMaximum)
    _S_PickupChiefRay      = property_adapter("_S_PickupChiefRay",      SolvePickupChiefRay)
    _S_ObjectPickup        = property_adapter("_S_ObjectPickup",        SolveObjectPickup)
    _S_ConfigPickup        = property_adapter("_S_ConfigPickup",        SolveConfigPickup)
    _S_ThermalPickup       = property_adapter("_S_ThermalPickup",       SolveThermalPickup)
    _S_FieldPickup         = property_adapter("_S_FieldPickup",         SolveFieldPickup)
    _S_DuplicateSag        = property_adapter("_S_DuplicateSag",        SolveDuplicateSag)
    _S_InvertSag           = property_adapter("_S_InvertSag",           SolveInvertSag)