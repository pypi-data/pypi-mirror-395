from zempy.zosapi.core.enum_base import ZosEnumBase

class QuickAdjustCriterion(ZosEnumBase):
    SpotSizeRadial  = 0
    SpotSizeXOnly   = 1
    SpotSizeYOnly   = 2
    AngularRadial   = 3
    AngularXOnly    = 4
    AngularYOnly    = 5

QuickAdjustCriterion._NATIVE_PATH = "ZOSAPI.Tools.General.QuickAdjustCriterion"
QuickAdjustCriterion._ALIASES_EXTRA = {}

__all__ = ["QuickAdjustCriterion"]
