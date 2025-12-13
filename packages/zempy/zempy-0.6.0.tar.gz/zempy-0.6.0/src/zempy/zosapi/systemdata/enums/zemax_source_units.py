from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxSourceUnits(ZosEnumBase):
    Watts = 0
    Lumens = 1
    Joules = 2

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxSourceUnits'
