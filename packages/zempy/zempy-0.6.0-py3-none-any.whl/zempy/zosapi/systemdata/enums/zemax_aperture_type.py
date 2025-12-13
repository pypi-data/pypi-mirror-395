from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxApertureType(ZosEnumBase):
    EntrancePupilDiameter = 0
    ImageSpaceFNum = 1
    ObjectSpaceNA = 2
    FloatByStopSize = 3
    ParaxialWorkingFNum = 4
    ObjectConeAngle = 5

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxApertureType'
