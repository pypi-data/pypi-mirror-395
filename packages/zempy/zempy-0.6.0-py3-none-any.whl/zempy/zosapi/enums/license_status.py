from zempy.zosapi.core.enum_base import ZosEnumBase

class LicenseStatusType(ZosEnumBase):
    _ignore_ = "_NATIVE_PATH _NATIVE_PATHS _ALIASES_EXTRA"
    # only enum values here …
    UNKNOWN = 0
    KEY_NOT_WORKING = 1
    NEW_LICENSE_NEEDED = 2
    STANDARD_EDITION = 3
    PROFESSIONAL_EDITION = 4
    PREMIUM_EDITION = 5
    TOO_MANY_INSTANCES = 6
    NOT_AUTHORIZED = 7
    KEY_NOT_FOUND = 8
    KEY_EXPIRED = 9
    TIMEOUT = 10
    INSTANCE_CONFLICT = 11
    OPTICS_VIEWER = 12
    OPTIC_STUDIO_HPC_EDITION = 13
    ENTERPRISE_EDITION = 14
    STUDENT_EDITION = 15

# attach after class (or keep inside if you prefer with _ignore_)
LicenseStatusType._NATIVE_PATHS = [
    "ZOSAPI.SystemData.LicenseStatusType",
    "ZOSAPI.LicenseStatusType",
]
LicenseStatusType._ALIASES_EXTRA = {
    "STANDARD_EDITION": ("StandardEdition",),
    "PROFESSIONAL_EDITION": ("ProfessionalEdition",),
    "PREMIUM_EDITION": ("PremiumEdition",),
    "OPTIC_STUDIO_HPC_EDITION": ("OpticStudioHPCEdition",),
    "ENTERPRISE_EDITION": ("EnterpriseEdition",),
    "STUDENT_EDITION": ("StudentEdition",),
    "KEY_NOT_WORKING": ("KeyNotWorking",),
    "NEW_LICENSE_NEEDED": ("NewLicenseNeeded",),
    "TOO_MANY_INSTANCES": ("TooManyInstances",),
    "NOT_AUTHORIZED": ("NotAuthorized",),
    "KEY_NOT_FOUND": ("KeyNotFound",),
    "KEY_EXPIRED": ("KeyExpired",),
    "INSTANCE_CONFLICT": ("InstanceConflict",),
    "OPTICS_VIEWER": ("OpticsViewer",),
}
