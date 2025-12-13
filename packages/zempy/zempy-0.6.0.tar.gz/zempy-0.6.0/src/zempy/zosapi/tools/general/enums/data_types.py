from zempy.zosapi.core.enum_base import ZosEnumBase

class DataTypes(ZosEnumBase):
    NotSet        = 0
    Boolean       = 1
    Integer       = 2
    IntegerArray  = 3
    IntegerMatrix = 4
    Float         = 5
    FloatArray    = 6
    FloatMatrix   = 7
    Double        = 8
    DoubleArray   = 9
    DoubleMatrix  = 10
    String        = 11
    StringArray   = 12
    StringMatrix  = 13
    ByteArray     = 14
    Dictionary    = 15
    Serializable  = 16
    File          = 17

DataTypes._NATIVE_PATH = "ZOSAPI.Tools.General.DataTypes"
DataTypes._ALIASES_EXTRA = {}

__all__ = ["DataTypes"]
