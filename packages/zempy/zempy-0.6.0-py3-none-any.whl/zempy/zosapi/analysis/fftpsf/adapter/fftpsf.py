from __future__ import annotations
from typing import  cast, TYPE_CHECKING
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.analysis.adapters.ia import IA
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.adapters.analysis_registry import register_analysis
from zempy.zosapi.analysis.fftpsf.adapter.fft_psf_settings import FftPsfSettings

if TYPE_CHECKING:
    from zempy.zosapi.analysis.fftpsf.protocols.ias_fft_psf import IAS_FftPsf

@register_analysis(AnalysisIDM.FftPsf)
class FFTPSF(IA[FftPsfSettings, Z, N]):

    def __str__(self) -> str:
        return f"FFT PSF settings={self.settings}"

    @property
    def settings(self) -> IAS_FftPsf:
        return cast(IAS_FftPsf, super().settings)