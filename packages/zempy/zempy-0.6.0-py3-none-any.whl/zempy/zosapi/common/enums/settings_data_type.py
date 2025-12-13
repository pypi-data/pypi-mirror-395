from zempy.zosapi.core.enum_base import ZosEnumBase


class SettingsDataType(ZosEnumBase):
    """Wrapper for ZOSAPI.Common.SettingsDataType enum."""

    None_   = 0
    Integer = 1
    Double  = 2
    Float   = 3
    String  = 4
    Byte    = 5
    Boolean = 6

SettingsDataType._NATIVE_PATHS = ("ZOSAPI.Common.SettingsDataType")
SettingsDataType._ALIASES_EXTRA = {
    "None_": ("None",),
}

__all__ = ["SettingsDataType"]
