from zempy.zosapi.core.enum_base import ZosEnumBase

class SystemType(ZosEnumBase):
    """ZOSAPI.SystemType"""
    SEQUENTIAL = 0
    NON_SEQUENTIAL = 1

    def is_sequential(self) -> bool:
        """Return True if system is sequential."""
        return self is SystemType.SEQUENTIAL

    def is_nonsequential(self) -> bool:
        """Return True if system is non-sequential."""
        return self is SystemType.NON_SEQUENTIAL


SystemType._NATIVE_PATH = "ZOSAPI.SystemType"
SystemType._ALIASES_EXTRA = {
    "SEQUENTIAL": ("Sequential",),
    "NON_SEQUENTIAL": ("NonSequential",),
}

__all__ = ["SystemType"]
