from __future__ import annotations
from zempy.zosapi.core.enum_base import ZosEnumBase

class WavelengthPreset(ZosEnumBase):
    """ZOSAPI.SystemData.WavelengthPreset"""
    FdC_Visible                     = 0
    Photopic_Bright                 = 1
    Scotopic_Dark                   = 2
    HeNe_0p6328                     = 3
    HeNe_0p5438                     = 4
    Argon_0p4880                    = 5
    Argon_0p5145                    = 6
    NDYAG_1p0641                    = 7
    NDGlass_1p054                   = 8
    CO2_10p60                       = 9
    CrLiSAF_0p840                   = 10
    TiAl203_0p760                   = 11
    Ruby_0p6943                     = 12
    HeCadmium_0p4416                = 13
    HeCadmium_0p3536                = 14
    HeCadmium_0p3250                = 15
    t_1p014                         = 16
    r_0p707                         = 17
    C_0p656                         = 18
    d_0p587                         = 19
    F_0p486                         = 20
    g_0p436                         = 21
    i_0p365                         = 22
    Fp_0p365                        = 23
    e_0p54607                       = 24
    Cp_0p6438469                    = 25
    FpeCp_Visible                   = 26
    THz_193p10                      = 27

WavelengthPreset._NATIVE_PATH = "ZOSAPI.SystemData.WavelengthPreset"
WavelengthPreset._ALIASES_EXTRA = {}

__all__ = ["WavelengthPreset"]
