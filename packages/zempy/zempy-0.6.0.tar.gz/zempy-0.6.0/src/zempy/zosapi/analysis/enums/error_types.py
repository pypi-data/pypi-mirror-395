from zempy.zosapi.core.enum_base import ZosEnumBase

class ErrorType(ZosEnumBase):
    Success                           = 0
    InvalidParameter                  = 1
    InvalidSettings                   = 2
    Failed                            = 3
    AnalysisUnavailableForProgramMode = 4
    NotYetImplemented                 = 5
    NoSolverLicenseAvailable          = 6
    ToolAlreadyOpen                   = 7
    SequentialOnly                    = 8
    NonSequentialOnly                 = 9
    SingleNSCRayTraceSupported        = 10
    HPCNotAvailable                   = 11
    FeatureNotSupported               = 12
    NotAvailableInLegacy              = 13
    Unknown                           = -1   # fallback when we can't decode


ErrorType._NATIVE_PATH = "ZOSAPI.Analysis.ErrorType"
ErrorType._ALIASES_EXTRA = {}

__all__ = ["ErrorType"]
