from zempy.zosapi.core.enum_base import ZosEnumBase


class AxisType(ZosEnumBase):
    X = 0
    Y = 1
    Z = 2

AxisType._NATIVE_PATH = "ZOSAPI.Analysis.Settings.AxisType"
AxisType._ALIASES_EXTRA = {}

__all__ = ["AxisType"]
