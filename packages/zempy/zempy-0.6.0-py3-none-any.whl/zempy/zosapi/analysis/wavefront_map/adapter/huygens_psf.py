from __future__ import annotations
from typing import  cast, TYPE_CHECKING
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.analysis.adapters.ia import IA
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.adapters.analysis_registry import register_analysis
from zempy.zosapi.analysis.huygens_psf.adapters.huygens_psf_settings import HuygensPsfSettings

if TYPE_CHECKING:
    from zempy.zosapi.analysis.huygens_psf.protocols.ias_huygens_psf import IAS_HuygensPsf

@register_analysis(AnalysisIDM.HuygensPsf)
class HuygensPSF(IA[HuygensPsfSettings, Z, N]):

    def __str__(self) -> str:
        return f"FFT PSF settings={self.settings}"

    @property
    def settings(self) -> IAS_HuygensPsf:
        return cast(IAS_HuygensPsf, super().settings)