from zempy.zosapi.core.enum_base import ZosEnumBase

class HPCEnvironments(ZosEnumBase):
    OnPremise       = 0
    AWSKubernetes   = 1
    AzureKubernetes = 2

HPCEnvironments._NATIVE_PATH = "ZOSAPI.Tools.General.HPCEnvironments"
HPCEnvironments._ALIASES_EXTRA = {}

__all__ = ["HPCEnvironments"]
