from zempy.zosapi.core.enum_base import ZosEnumBase

class CADFileType(ZosEnumBase):
    IGES       = 0
    STEP       = 1
    SAT        = 2
    STL        = 3
    SAB        = 4
    ASAT       = 5
    ASAB       = 6
    MODEL      = 7
    CATPART    = 8
    CATPRODUCT = 9
    XCGM       = 10
    ZMO        = 11
    XT         = 12
    XB         = 13
    PRC        = 14
    JT         = 15
    N3MF       = 16
    U3D        = 17
    VRML       = 18
    OBJ        = 19

CADFileType._NATIVE_PATH = "ZOSAPI.Tools.General.CADFileType"
CADFileType._ALIASES_EXTRA = {}

__all__ = ["CADFileType"]
