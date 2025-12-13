from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar


@dataclass(frozen=True, slots=True)
class SpotDataResultMatrix:
    """
    Adapter for ZOSAPI.Analysis.Data.IAR_SpotDataResultMatrix.

    Methods mirror the native API:
      Get_X_For/ Get_Y_For/ Get_Z_For
      Get_L_For/ Get_M_For/ Get_N_For
      GetDetector_X_For/ GetDetector_Y_For/ GetDetector_Z_For
      GetGeoSpotSizeFor / GetRMSSpotSizeFor / GetRMSSpot_X_For / GetRMSSpot_Y_For
      GetReferenceCoordinate_X_For / GetReferenceCoordinate_Y_For

    Properties:
      HalfWidth_X, HalfWidth_Y, MaxRadius, MeanRadius,
      NumberOfFields, NumberOfWavelengths
    """
    zosapi: object
    native: object

    # --- Factory ---
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "SpotDataResultMatrix":
        if native is None:
            raise ValueError("SpotDataResultMatrix.from_native: native is None")
        return cls(zosapi, native)

    # --- Validation ---
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="SpotDataResultMatrix.native", exc_type=_exc.ZemaxObjectGone)

    # --- Methods (vectors / positions) ---
    def Get_X_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.Get_X_For",
                                lambda: self.native.Get_X_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def Get_Y_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.Get_Y_For",
                                lambda: self.native.Get_Y_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def Get_Z_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.Get_Z_For",
                                lambda: self.native.Get_Z_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def Get_L_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.Get_L_For",
                                lambda: self.native.Get_L_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def Get_M_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.Get_M_For",
                                lambda: self.native.Get_M_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def Get_N_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.Get_N_For",
                                lambda: self.native.Get_N_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    # --- Methods (detector coordinates) ---
    def GetDetector_X_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetDetector_X_For",
                                lambda: self.native.GetDetector_X_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def GetDetector_Y_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetDetector_Y_For",
                                lambda: self.native.GetDetector_Y_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def GetDetector_Z_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetDetector_Z_For",
                                lambda: self.native.GetDetector_Z_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    # --- Methods (metrics) ---
    def GetGeoSpotSizeFor(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetGeoSpotSizeFor",
                                lambda: self.native.GetGeoSpotSizeFor(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def GetRMSSpotSizeFor(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetRMSSpotSizeFor",
                                lambda: self.native.GetRMSSpotSizeFor(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def GetRMSSpot_X_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetRMSSpot_X_For",
                                lambda: self.native.GetRMSSpot_X_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def GetRMSSpot_Y_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetRMSSpot_Y_For",
                                lambda: self.native.GetRMSSpot_Y_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    # --- Methods (reference coords) ---
    def GetReferenceCoordinate_X_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetReferenceCoordinate_X_For",
                                lambda: self.native.GetReferenceCoordinate_X_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    def GetReferenceCoordinate_Y_For(self, fieldN: int, waveN: int) -> float:
        return float(run_native("SpotDataResultMatrix.GetReferenceCoordinate_Y_For",
                                lambda: self.native.GetReferenceCoordinate_Y_For(int(fieldN), int(waveN)),
                                ensure=self.ensure_native))

    # --- Properties (descriptors) ---
    HalfWidth_X        = PropertyScalar("HalfWidth_X",        coerce_get=float)
    HalfWidth_Y        = PropertyScalar("HalfWidth_Y",        coerce_get=float)
    MaxRadius          = PropertyScalar("MaxRadius",          coerce_get=float)
    MeanRadius         = PropertyScalar("MeanRadius",         coerce_get=float)
    NumberOfFields     = PropertyScalar("NumberOfFields",     coerce_get=int)
    NumberOfWavelengths= PropertyScalar("NumberOfWavelengths",coerce_get=int)

    # --- Convenience helpers (optional) ---
    def Get_DetectorXYZ_For(self, fieldN: int, waveN: int) -> Tuple[float, float, float]:
        """Convenience: returns (Xdet, Ydet, Zdet)."""
        return (
            self.GetDetector_X_For(fieldN, waveN),
            self.GetDetector_Y_For(fieldN, waveN),
            self.GetDetector_Z_For(fieldN, waveN),
        )

    def Get_RMS_Spot_XY_For(self, fieldN: int, waveN: int) -> Tuple[float, float]:
        """Convenience: returns (RMSx, RMSy)."""
        return (
            self.GetRMSSpot_X_For(fieldN, waveN),
            self.GetRMSSpot_Y_For(fieldN, waveN),
        )

    # --- Representation ---
    def __repr__(self) -> str:
        try:
            return (
                f"SpotDataResultMatrix("
                f"Fields={self.NumberOfFields}, "
                f"Waves={self.NumberOfWavelengths}, "
                f"HalfWidth=({self.HalfWidth_X:.6g}, {self.HalfWidth_Y:.6g}))"
            )
        except Exception:
            return "SpotDataResultMatrix(<unavailable>)"
