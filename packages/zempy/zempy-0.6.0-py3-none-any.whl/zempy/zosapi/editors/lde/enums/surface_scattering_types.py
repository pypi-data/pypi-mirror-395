from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class SurfaceScatteringTypes(ZosEnumBase):
    """ZOSAPI.Editors.LDE.SurfaceScatteringTypes"""
    NoneType                        = 0
    Lambertian                      = 1
    Gaussian                        = 2
    ABg                             = 3
    ABgFile                         = 4
    BSDF                            = 5
    User                            = 6
    ISScatterCatalog                = 7

SurfaceScatteringTypes._NATIVE_PATH = "ZOSAPI.Editors.LDE.SurfaceScatteringTypes"
SurfaceScatteringTypes._ALIASES_EXTRA = {
    "NoneType": [
        "None"
    ]
}

__all__ = ["SurfaceScatteringTypes"]
