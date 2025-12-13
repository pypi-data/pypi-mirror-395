from zempy.zosapi.core.enum_base import ZosEnumBase

class ZemaxOpacity(ZosEnumBase):
    """Wrapper for ZOSAPI.Common.ZemaxOpacity enum."""

    P100 = 0
    P90  = 1
    P80  = 2
    P70  = 3
    P60  = 4
    P50  = 5
    P40  = 6
    P30  = 7
    P20  = 8
    P10  = 9
    P00  = 10

ZemaxOpacity._NATIVE_PATHS = ("ZOSAPI.Common.ZemaxOpacity")
ZemaxOpacity._ALIASES_EXTRA = {}

__all__ = ["ZemaxOpacity"]
