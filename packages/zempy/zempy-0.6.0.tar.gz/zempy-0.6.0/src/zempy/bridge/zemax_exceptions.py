class ZemaxError(Exception): pass
class ZemaxNotFound(ZemaxError): pass
class ZemaxConnectError(ZemaxError): pass
class ZemaxFileMissing(ZemaxError): pass
class ZemaxInitializationError(ZemaxError): pass
class ZemaxLicenseError(ZemaxError): pass
class ZemaxSystemError(ZemaxError): pass
class ZemaxObjectGone(ZemaxError): pass

__all__ = [
    "ZemaxError",
    "ZemaxNotFound",
    "ZemaxConnectError",
    "ZemaxFileMissing",
    "ZemaxInitializationError",
    "ZemaxLicenseError",
    "ZemaxSystemError",
    "ZemaxObjectGone",]