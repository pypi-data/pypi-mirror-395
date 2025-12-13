from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.systemdata.adapters.fields import Fields
from zempy.zosapi.systemdata.adapters.sd_title_notes import SDTitleNotes
from zempy.zosapi.systemdata.adapters.wavelengths import Wavelengths
from zempy.zosapi.core.types_var import *


class _SubAdapterBase(BaseAdapter[Z, N]): pass
class SDApertureData(_SubAdapterBase[Z, N]): pass

class SDEnvironmentData(_SubAdapterBase[Z, N]): pass
class SDPolarizationData(_SubAdapterBase[Z, N]): pass
class SDAdvancedData(_SubAdapterBase[Z, N]): pass
class SDRayAimingData(_SubAdapterBase[Z, N]): pass
class SDMaterialCatalogData(_SubAdapterBase[Z, N]): pass

class SDFiles(_SubAdapterBase[Z, N]): pass
class SDUnitsData(_SubAdapterBase[Z, N]): pass
class SDNonSeqData(_SubAdapterBase[Z, N]): pass
class SDNamedFilters(_SubAdapterBase[Z, N]): pass

@dataclass
class SystemData(BaseAdapter[Z, N]):
    """Python adapter for ZOSAPI.SystemData.ISystemData"""

    Aperture           = property_adapter("Aperture",           SDApertureData)
    Wavelengths        = property_adapter("Wavelengths",        Wavelengths)
    Fields             = property_adapter("Fields",             Fields)
    Environment        = property_adapter("Environment",        SDEnvironmentData)
    Polarization       = property_adapter("Polarization",       SDPolarizationData)
    Advanced           = property_adapter("Advanced",           SDAdvancedData)
    RayAiming          = property_adapter("RayAiming",          SDRayAimingData)
    MaterialCatalogs   = property_adapter("MaterialCatalogs",   SDMaterialCatalogData)
    TitleNotes         = property_adapter("TitleNotes",         SDTitleNotes)
    Files              = property_adapter("Files",              SDFiles)
    Units              = property_adapter("Units",              SDUnitsData)
    NonSequentialData  = property_adapter("NonSequentialData",  SDNonSeqData)
    NamedFiltersData   = property_adapter("NamedFiltersData",   SDNamedFilters)

    # Optional: dunder helpers
    def __repr__(self) -> str:
        return f"SystemData(native={type(self.native).__name__})"

