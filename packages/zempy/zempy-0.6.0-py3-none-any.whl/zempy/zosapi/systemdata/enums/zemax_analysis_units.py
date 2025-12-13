from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxAnalysisUnits(ZosEnumBase):
    WattsPerMMSq = 0
    WattsPerCMSq = 1
    WattsPerinSq = 2
    WattsPerMSq = 3
    WattsPerftSq = 4

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxAnalysisUnits'
