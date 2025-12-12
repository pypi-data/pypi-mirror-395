"""
Public API for TabuDiff generator.

This package provides two feature sets:
- basic TabuDiff
- premium TabuDiff
"""

from .basic.utils.api import TabuDiffAPI as TabuDiffBasicAPI
from .premium.utils.api import TabuDiffPremiumAPI

__all__ = [
    "TabuDiffBasicAPI",
    "TabuDiffPremiumAPI",
]
