from zempy.zosapi.core.enum_base import ZosEnumBase

class QuickFocusCriterion(ZosEnumBase):
    SpotSizeRadial  = 0
    SpotSizeXOnly   = 1
    SpotSizeYOnly   = 2
    RMSWavefront    = 3

QuickFocusCriterion._NATIVE_PATH = "ZOSAPI.Tools.General.QuickFocusCriterion"
QuickFocusCriterion._ALIASES_EXTRA = {}

__all__ = ["QuickFocusCriterion"]