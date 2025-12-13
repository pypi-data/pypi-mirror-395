from zempy.zosapi.core.enum_base import ZosEnumBase

class ScaleToUnits(ZosEnumBase):
    Millimeters = 0
    Centimeters = 1
    Inches      = 2
    Meters      = 3

ScaleToUnits._NATIVE_PATH = "ZOSAPI.Tools.General.ScaleToUnits"
ScaleToUnits._ALIASES_EXTRA = {}

__all__ = ["ScaleToUnits"]
