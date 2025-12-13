from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.adapters.ia import IA

_ANALYSIS_REGISTRY: dict[AnalysisIDM, type[IA]] = {}

def register_analysis(idm: AnalysisIDM):
    def _wrap(cls: type[IA]) -> type[IA]:
        _ANALYSIS_REGISTRY[idm] = cls
        return cls
    return _wrap

def get_analysis_class(idm: AnalysisIDM) -> type[IA]:
    return _ANALYSIS_REGISTRY.get(idm, IA)
