from __future__ import annotations
from typing import Any

from zempy.zosapi.analysis.enums.show_as import ShowAsEnum
from zempy.zosapi.analysis.enums.sample_sizes import SampleSizes
from zempy.zosapi.analysis.ias.enums.rotations import Rotations
from zempy.zosapi.analysis.ias.enums.polarizations import Polarizations
from zempy.zosapi.analysis.ias.enums.star_effects_options import STAREffectsOptions

from zempy.zosapi.analysis.ias.adapters.ias import IAS
from zempy.zosapi.analysis.ias.adapters.registry import register_settings
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM

from zempy.zosapi.analysis.wavefront_map.protocols.ias_wavefront_map import IAS_WavefrontMap

from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.core.types_var import Z


@register_settings(AnalysisIDM.WavefrontMap)
class WavefrontMapSettings(IAS[Z, IAS_WavefrontMap]):
    """
    Adapter for ZOSAPI.Analysis.Settings.IAS_WavefrontMap
    following the same pattern as HuygensPsfSettings.
    """

    REQUIRED_NATIVE_ATTRS = (
        "Field",
        "Surface",
        "Wavelength",
        "ShowAs",
        "Rotation",
        "SampleSize",
        "Polarization",
        "ReferenceToPrimary",
        "UseExitPupil",
        "RemoveTilt",
        "Scale",
        "Subaperture_X",
        "Subaperture_Y",
        "Subaperture_R",
        "ContourFormat",
        "STAREffects",
    )

    # --- Enums ---
    ShowAs       = property_enum("ShowAs",       ShowAsEnum)
    Rotation     = property_enum("Rotation",     Rotations)
    SampleSize   = property_enum("SampleSize",   SampleSizes)
    Polarization = property_enum("Polarization", Polarizations)
    STAREffects  = property_enum("STAREffects",  STAREffectsOptions)

    # --- Scalars / flags ---
    ReferenceToPrimary = PropertyScalar(
        "ReferenceToPrimary", coerce_get=bool, coerce_set=bool
    )
    UseExitPupil = PropertyScalar(
        "UseExitPupil", coerce_get=bool, coerce_set=bool
    )
    RemoveTilt = PropertyScalar(
        "RemoveTilt", coerce_get=bool, coerce_set=bool
    )
    Scale = PropertyScalar(
        "Scale", coerce_get=float, coerce_set=float
    )

    Subaperture_X = PropertyScalar(
        "Subaperture_X", coerce_get=float, coerce_set=float
    )
    Subaperture_Y = PropertyScalar(
        "Subaperture_Y", coerce_get=float, coerce_set=float
    )
    Subaperture_R = PropertyScalar(
        "Subaperture_R", coerce_get=float, coerce_set=float
    )

    ContourFormat = PropertyScalar(
        "ContourFormat", coerce_get=str, coerce_set=str
    )

    # --- Native coercion hook (same pattern as HuygensPsfSettings) ---
    @staticmethod
    def _coerce_native(base: Any) -> Any:
        # Likely cast helper from ZOSAPI:
        #   As_ZOSAPI_Analysis_Settings_Wavefront_IAS_WavefrontMap
        cast_fn = getattr(
            base,
            "As_ZOSAPI_Analysis_Settings_Wavefront_IAS_WavefrontMap",
            None,
        )
        if callable(cast_fn):
            obj = cast_fn()
            if obj is not None:
                return obj
        # Fallback: some wrappers store the real .NET object under __implementation__
        return getattr(base, "__implementation__", base)

    NATIVE_COERCER = _coerce_native

    def __str__(self) -> str:
        return (
            "Wavefront Map settings:(\n"
            f"  field={self.Field},\n"
            f"  surface={self.Surface},\n"
            f"  wavelength={self.Wavelength},\n"
            f"  show_as={self.ShowAs.name},\n"
            f"  rotation={self.Rotation.name},\n"
            f"  sample_size={self.SampleSize.name},\n"
            f"  polarization={self.Polarization.name},\n"
            f"  reference_to_primary={self.ReferenceToPrimary},\n"
            f"  use_exit_pupil={self.UseExitPupil},\n"
            f"  remove_tilt={self.RemoveTilt},\n"
            f"  scale={self.Scale},\n"
            f"  subaperture_x={self.Subaperture_X},\n"
            f"  subaperture_y={self.Subaperture_Y},\n"
            f"  subaperture_r={self.Subaperture_R},\n"
            f"  contour_format={self.ContourFormat},\n"
            f"  star_effects={self.STAREffects.name},\n"
            ")"
        )
