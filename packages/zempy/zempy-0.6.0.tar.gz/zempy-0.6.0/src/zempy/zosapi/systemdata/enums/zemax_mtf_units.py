from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxMTFUnits(ZosEnumBase):
    CyclesPerMillimeter = 0
    CyclesPerMilliradian = 1

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxMTFUnits'
