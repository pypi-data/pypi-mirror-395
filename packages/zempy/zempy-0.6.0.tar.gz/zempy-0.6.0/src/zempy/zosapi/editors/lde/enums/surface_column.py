from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase


class SurfaceColumn(ZosEnumBase):
    """
    Python mirror of ZOSAPI.Editors.LDE.SurfaceColumn.

    Represents column identifiers used in the Lens Data Editor (LDE).
    """

    _NATIVE_PATH = "ZOSAPI.Editors.LDE.SurfaceColumn"

    # --- Standard columns ---
    COMMENT = 0
    RADIUS = 1
    THICKNESS = 2
    MATERIAL = 3
    COATING = 4
    SEMI_DIAMETER = 5
    CHIP_ZONE = 6
    MECHANICAL_SEMI_DIAMETER = 7
    CONIC = 8
    TCE = 9

    # --- Parameter columns ---
    # Dynamically generate PAR0–PAR254
    for i in range(255):
        locals()[f"PAR{i}"] = 10 + i
    del i

    # Optional alias map (helps tolerant matching from .NET casing)
    _ALIASES_EXTRA = {
        "SEMI_DIAM": ("SemiDiameter",),
        "MECH_SEMI_DIAM": ("MechanicalSemiDiameter",),
    }


__all__ = ["SurfaceColumn"]
