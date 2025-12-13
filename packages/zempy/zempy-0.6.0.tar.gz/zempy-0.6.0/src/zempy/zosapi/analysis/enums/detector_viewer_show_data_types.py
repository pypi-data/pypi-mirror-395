from zempy.zosapi.core.enum_base import ZosEnumBase


class DetectorViewerShowDataTypes(ZosEnumBase):
    IncidentFlux = 0
    AbsorbedFlux = 1
    AbsorbedFluxVolume = 2
    PositionSpace = 3
    AngleSpace = 4
    Polar_AngleSpace = 5
    IncoherentIrradiance = 6
    CoherentIrradiance = 7
    CoherentPhase = 8
    RadiantIntensity = 9
    RadiancePositionSpace = 10
    RadianceAngleSpace = 11
    IncoherentIlluminance = 12
    CoherentIlluminance = 13
    LuminousIntensity = 14
    LuminancePositionSpace = 15
    LuminanceAngleSpace = 16
    IncoherentFluence = 17
    CoherentFluence = 18

DetectorViewerShowDataTypes._NATIVE_PATH = "ZOSAPI.Analysis.DetectorViewerShowDataTypes"
DetectorViewerShowDataTypes._ALIASES_EXTRA = {}

__all__ = ["DetectorViewerShowDataTypes"]
