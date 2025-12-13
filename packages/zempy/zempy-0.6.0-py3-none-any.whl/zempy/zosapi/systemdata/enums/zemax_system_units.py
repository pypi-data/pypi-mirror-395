from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxSystemUnits(ZosEnumBase):
    Millimeters = 0
    Centimeters = 1
    Inches = 2
    Meters = 3

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxSystemUnits'
