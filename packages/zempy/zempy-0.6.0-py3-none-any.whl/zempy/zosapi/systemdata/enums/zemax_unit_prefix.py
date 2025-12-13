from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxUnitPrefix(ZosEnumBase):
    Femto = 0
    Pico = 1
    Nano = 2
    Micro = 3
    Milli = 4
    None_ = 5 #TODO wha
    Kilo = 6
    Mega = 7
    Giga = 8
    Tera = 9

    @classmethod
    def _native_path(cls):
        return 'SystemData.ZemaxUnitPrefix'
