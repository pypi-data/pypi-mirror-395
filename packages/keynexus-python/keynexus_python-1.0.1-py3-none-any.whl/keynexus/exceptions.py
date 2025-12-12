"""
KeyNexus Exceptions
"""


class KeyNexusError(Exception):
    """Base exception for all KeyNexus errors"""
    pass


class InvalidLicenseError(KeyNexusError):
    """Raised when license is invalid or not found"""
    pass


class HWIDMismatchError(KeyNexusError):
    """Raised when hardware ID doesn't match the licensed device"""
    pass


class ExpiredLicenseError(KeyNexusError):
    """Raised when license has expired"""
    pass


class NetworkError(KeyNexusError):
    """Raised when network request fails"""
    pass
