from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxAfocalModeUnits(ZosEnumBase):
    Microradians = 0
    Milliradians = 1
    Radians = 2
    ArcSeconds = 3
    ArcMinutes = 4
    Degrees = 5

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxAfocalModeUnits'
