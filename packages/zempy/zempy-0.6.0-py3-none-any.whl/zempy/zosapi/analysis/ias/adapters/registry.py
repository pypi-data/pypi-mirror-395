from __future__ import annotations
from typing import Callable, Dict, Type
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.ias.adapters.ias import IAS, IAS_Generic

_SETTINGS_REGISTRY: Dict[AnalysisIDM, Type[IAS]] = {}

def register_settings(idm: AnalysisIDM) -> Callable[[Type[IAS]], Type[IAS]]:
    def _wrap(cls: Type[IAS]) -> Type[IAS]:
        _SETTINGS_REGISTRY[idm] = cls
        return cls
    return _wrap

def get_settings_class(idm: AnalysisIDM) -> Type[IAS]:
    return _SETTINGS_REGISTRY.get(idm, IAS_Generic)
