"""
CTGAN internal package namespace.

This file exposes the utils API so that the outer ctgan package can re-export it cleanly.
"""

from .utils.api import CTGANAPI
from .utils.factory import CTGANFactory

__all__ = ["CTGANAPI", "CTGANFactory"]
