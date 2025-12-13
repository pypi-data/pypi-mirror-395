from zempy.zosapi.core.enum_base import ZosEnumBase

class VertexOrder(ZosEnumBase):
    First  = 0
    Second = 1
    Third  = 2

VertexOrder._NATIVE_PATH = "ZOSAPI.Tools.General.VertexOrder"
VertexOrder._ALIASES_EXTRA = {}

__all__ = ["VertexOrder"]
