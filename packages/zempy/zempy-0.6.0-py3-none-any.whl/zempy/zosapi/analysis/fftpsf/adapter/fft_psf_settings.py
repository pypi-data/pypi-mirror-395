from __future__ import annotations
from typing import Any
from zempy.zosapi.analysis.fftpsf.enums.psf_sampling import PsfSampling
from zempy.zosapi.analysis.fftpsf.enums.psf_rotation import PsfRotation
from zempy.zosapi.analysis.fftpsf.enums.fft_psf_type   import FftPsfType
from zempy.zosapi.analysis.ias.adapters.ias import IAS
from zempy.zosapi.analysis.ias.adapters.registry import register_settings
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.fftpsf.protocols.ias_fft_psf import IAS_FftPsf
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.core.types_var import Z

@register_settings(AnalysisIDM.FftPsf)
class FftPsfSettings(IAS[Z, IAS_FftPsf]):
    REQUIRED_NATIVE_ATTRS = IAS.REQUIRED_NATIVE_ATTRS + (
        "SampleSize",
        "OutputSize",
        "Rotation",
        "Type",
        "ImageDelta",
        "UsePolarization",
        "Normalize",
    )

    SampleSize      = property_enum("SampleSize", PsfSampling,)
    OutputSize      = property_enum("OutputSize", PsfSampling,)
    Rotation        = property_enum("Rotation",   PsfRotation,)
    Type            = property_enum("Type",       FftPsfType, )
    ImageDelta      = PropertyScalar("ImageDelta",      coerce_get=float, coerce_set=float)
    UsePolarization = PropertyScalar("UsePolarization", coerce_get=bool,  coerce_set=bool)
    Normalize       = PropertyScalar("Normalize",       coerce_get=bool,  coerce_set=bool)



    # Native coercion hook (same behavior as before)
    @staticmethod
    def _coerce_native(base: Any) -> Any:
        cast_fn = getattr(base, "As_ZOSAPI_Analysis_Settings_Psf_IAS_FftPsf", None)
        if callable(cast_fn):
            obj = cast_fn()
            if obj is not None:
                return obj
        return getattr(base, "__implementation__", base)

    NATIVE_COERCER = _coerce_native

    def __str__(self) -> str:
        return (
            "PSF settings:(\n"
            f"  field={self.Field},\n"
            f"  wavelength={self.Wavelength},\n"
            f"  surface={self.Surface},\n"
            f"  sample_size={self.SampleSize.name},\n"
            f"  output_size={self.OutputSize.name},\n"
            f"  rotation={self.Rotation.name},\n"
            f"  image_delta={self.ImageDelta},\n"
            f"  use_polarization={self.UsePolarization},\n"
            f"  normalize={self.Normalize},\n"
            f"  psf_type={self.Type.name}\n"
            ")"
        )
