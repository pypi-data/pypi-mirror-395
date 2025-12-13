from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxApodizationType(ZosEnumBase):
    Uniform = 0
    Gaussian = 1
    CosineCubed = 2

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxApodizationType'
