"""Licensing public API.

The underlying implementation is in `validator.py` which exposes `activate` and
`check_cache`. Older code imports expect `activate_license` and
`check_activation` names — provide these aliases here so imports succeed.
"""
from .validator import verify_license
from .validator import activate as activate_license
from .validator import check_cache as check_activation

__all__ = ["check_activation", "activate_license", "verify_license"]
