from __future__ import annotations
from typing import Any
from zempy.zosapi.analysis.enums.sample_sizes import SampleSizes
from zempy.zosapi.analysis.ias.adapters.ias import IAS
from zempy.zosapi.analysis.ias.adapters.registry import register_settings
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.zernike_standard.protocols.ias_zernike_standard_coefficients import IAS_ZernikeStandardCoefficients
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.core.types_var import Z


@register_settings(AnalysisIDM.ZernikeStandardCoefficients)
class ZernikeStandardCoefficientsSettings(IAS[Z, IAS_ZernikeStandardCoefficients]):
    REQUIRED_NATIVE_ATTRS = IAS.REQUIRED_NATIVE_ATTRS + (
        "SampleSize",
        "ReferenceOBDToVertex",
        "Sx",
        "Sy",
        "Sr",
        "Epsilon",
        "MaximumNumberOfTerms",
    )

    SampleSize = property_enum("SampleSize", SampleSizes)
    ReferenceOBDToVertex = PropertyScalar(
        "ReferenceOBDToVertex", coerce_get=bool, coerce_set=bool
    )

    Sx = PropertyScalar("Sx", coerce_get=float, coerce_set=float)
    Sy = PropertyScalar("Sy", coerce_get=float, coerce_set=float)
    Sr = PropertyScalar("Sr", coerce_get=float, coerce_set=float)

    Epsilon = PropertyScalar("Epsilon", coerce_get=float, coerce_set=float)

    MaximumNumberOfTerms = PropertyScalar(
        "MaximumNumberOfTerms", coerce_get=int, coerce_set=int
    )

    # --- Native coercion hook (same pattern as FftPsfSettings) ---

    @staticmethod
    def _coerce_native(base: Any) -> Any:
        cast_fn = getattr(
            base,
            "As_ZOSAPI_Analysis_Settings_Aberrations_IAS_ZernikeStandardCoefficients",
            None,
        )
        if callable(cast_fn):
            obj = cast_fn()
            if obj is not None:
                return obj
        return getattr(base, "__implementation__", base)

    NATIVE_COERCER = _coerce_native

    def __str__(self) -> str:
        return (
            "Zernike Standard Coefficients settings:(\n"
            f"  field={self.Field},\n"
            f"  wavelength={self.Wavelength},\n"
            f"  surface={self.Surface},\n"
            f"  sample_size={self.SampleSize.name},\n"
            f"  reference_obd_to_vertex={self.ReferenceOBDToVertex},\n"
            f"  sx={self.Sx}, sy={self.Sy}, sr={self.Sr},\n"
            f"  epsilon={self.Epsilon},\n"
            f"  max_terms={self.MaximumNumberOfTerms}\n"
            ")"
        )
