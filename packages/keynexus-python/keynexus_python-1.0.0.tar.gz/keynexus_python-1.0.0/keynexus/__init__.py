"""
KeyNexus Python SDK
Official Python client for KeyNexus License Management System
"""

from .client import KeyNexusClient
from .exceptions import (
    KeyNexusError,
    InvalidLicenseError,
    HWIDMismatchError,
    ExpiredLicenseError,
    NetworkError
)

__version__ = "1.0.0"
__all__ = [
    "KeyNexusClient",
    "KeyNexusError",
    "InvalidLicenseError",
    "HWIDMismatchError",
    "ExpiredLicenseError",
    "NetworkError"
]
