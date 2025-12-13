from __future__ import annotations
from typing import  cast, TYPE_CHECKING
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.analysis.adapters.ia import IA
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.adapters.analysis_registry import register_analysis
from zempy.zosapi.analysis.zernike_standard.adapters.zernike_standard_coefficients_settings import ZernikeStandardCoefficientsSettings

if TYPE_CHECKING:
    from zempy.zosapi.analysis.zernike_standard.protocols.ias_zernike_standard_coefficients import IAS_ZernikeStandardCoefficients

@register_analysis(AnalysisIDM.ZernikeStandardCoefficients)
class ZernikeStandardCoefficients(IA[ZernikeStandardCoefficientsSettings, Z, N]):

    def __str__(self) -> str:
        return f"FFT PSF settings={self.settings}"

    @property
    def settings(self) -> IAS_ZernikeStandardCoefficients:
        return cast(IAS_ZernikeStandardCoefficients, super().settings)