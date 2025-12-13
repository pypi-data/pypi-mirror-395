from zempy.zosapi.core.enum_base import ZosEnumBase


class DetectorViewerShowAsTypes(ZosEnumBase):
    FullListing = 0
    AzimuthCrossSection = 1
    Text_CrossSection_Row = 2
    Text_CrossSection_Column = 3
    FluxVsWaveLength = 4
    GreyScale = 5
    GreyScale_Inverted = 6
    FalseColor = 7
    FalseColor_Inverted = 8
    TrueColor = 9
    Color_CrossSection_Row = 10
    Color_CrossSection_Column = 11
    Color_FluxVsWavelength = 12
    CrossSection = 13
    Directivity_Full = 14
    Directivity_Half = 15
    CrossSection_Row = 16
    CrossSection_Column = 17
    GeometricMtf = 18

DetectorViewerShowAsTypes._NATIVE_PATH = "ZOSAPI.Analysis.DetectorViewerShowAsTypes"
DetectorViewerShowAsTypes._ALIASES_EXTRA = {}

__all__ = ["DetectorViewerShowAsTypes"]
