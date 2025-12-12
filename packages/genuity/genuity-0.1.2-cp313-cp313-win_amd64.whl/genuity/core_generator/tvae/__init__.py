"""
TVAE-based synthetic data generation.

This is the public namespace for the TVAE core generator. It re-exports
the high-level APIs from the internal implementation packages.

Public APIs:
- TVAEAPI: basic TVAE
- TVAEPremiumAPI: premium/enterprise TVAE
"""

# Basic TVAE high-level API
from .tvae.utils.api import TVAEAPI

# Premium TVAE high-level API
from .tvae_premium.utils.api import TVAEPremiumAPI

__all__ = [
    "TVAEAPI",
    "TVAEPremiumAPI",
]



