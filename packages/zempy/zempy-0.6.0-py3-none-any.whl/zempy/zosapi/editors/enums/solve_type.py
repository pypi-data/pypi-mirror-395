from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase


class SolveType(ZosEnumBase):
    NONE = 0
    FIXED = 1
    VARIABLE = 2
    SURFACE_PICKUP = 3
    ZPL_MACRO = 4
    MARGINAL_RAY_ANGLE = 5
    MARGINAL_RAY_HEIGHT = 6
    CHIEF_RAY_ANGLE = 7
    MARGINAL_RAY_NORMAL = 8
    CHIEF_RAY_NORMAL = 9
    APLANATIC = 10
    ELEMENT_POWER = 11
    COCENTRIC_SURFACE = 12
    COCENTRIC_RADIUS = 13
    F_NUMBER = 14
    CHIEF_RAY_HEIGHT = 15
    EDGE_THICKNESS = 16
    OPTICAL_PATH_DIFFERENCE = 17
    POSITION = 18
    COMPENSATOR = 19
    CENTER_OF_CURVATURE = 20
    PUPIL_POSITION = 21
    MATERIAL_SUBSTITUTE = 22
    MATERIAL_OFFSET = 23
    MATERIAL_MODEL = 24
    AUTOMATIC = 25
    MAXIMUM = 26
    PICKUP_CHIEF_RAY = 27
    OBJECT_PICKUP = 28
    CONFIG_PICKUP = 29
    THERMAL_PICKUP = 30
    MARGIN_PERCENT = 31
    CA_FILL = 32
    DIA_FILL = 33
    CONCENTRIC_SURFACE = 34
    CONCENTRIC_RADIUS = 35
    DUPLICATE_SAG = 36
    INVERT_SAG = 37
    FIELD_PICKUP = 38

    def is_pickup(self) -> bool:
        return self in {
            SolveType.SURFACE_PICKUP,
            SolveType.PICKUP_CHIEF_RAY,
            SolveType.OBJECT_PICKUP,
            SolveType.CONFIG_PICKUP,
            SolveType.THERMAL_PICKUP,
            SolveType.FIELD_PICKUP,
        }


SolveType._NATIVE_PATH = "ZOSAPI.Editors.SolveType"
SolveType._ALIASES_EXTRA = {
        "COCENTRIC_SURFACE": ("ConcentricSurface", "CocentricSurface"),
        "CONCENTRIC_SURFACE": ("ConcentricSurface", "CocentricSurface"),
        "COCENTRIC_RADIUS": ("ConcentricRadius", "CocentricRadius"),
        "CONCENTRIC_RADIUS": ("ConcentricRadius", "CocentricRadius"),
        "NONE": ("None", "NONE"),
        "CA_FILL": ("CA_fill", "CA_Fill"),
        "DIA_FILL": ("DIA_fill", "DIA_Fill"),
        "F_NUMBER": ("FNumber",),
        "PICKUP_CHIEF_RAY": ("PickupChiefRay",),
    }

__all__ = ["SolveType"]
