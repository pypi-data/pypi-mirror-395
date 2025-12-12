"""
Genuity: offline-licensed AI library

Usage:
    import genuity
    genuity.activate('PASTE_LICENSE')
"""
from genuity.licensing import activate_license as _activate_license, check_activation as _check_activation

# Enforce license check before any public API can be used

def _require_activation():
    if not check_activation():
        raise RuntimeError("No active license found. Please call genuity.activate_license('<LICENSE_STRING>') before using any library features.")

# --- Public API gatekeeping ---

def activate_license(license_string):
    """
    Activate this installation with a license string from your purchase portal.
    """
    return _activate_license(license_string)

def check_activation():
    """
    Returns True if a valid license activation cache is present.
    """
    return _check_activation()

# Core modules - Import only what exists and works, always after activation check
try:
    from .data_processor import TabularPreprocessor as _TabularPreprocessor, TabularPostprocessor as _TabularPostprocessor
    class TabularPreprocessor(_TabularPreprocessor):
        def __init__(self, *args, **kwargs):
            _require_activation()
            super().__init__(*args, **kwargs)
    class TabularPostprocessor(_TabularPostprocessor):
        def __init__(self, *args, **kwargs):
            _require_activation()
            super().__init__(*args, **kwargs)
except:
    TabularPreprocessor = None
    TabularPostprocessor = None

try:
    from .core_generator.copula import CopulaAPI as _CopulaAPI
    class CopulaAPI(_CopulaAPI):
        def __init__(self, *args, **kwargs):
            _require_activation()
            super().__init__(*args, **kwargs)
except:
    CopulaAPI = None

try:
    from .core_generator.differential_privacy import DifferentialPrivacyProcessor as _DifferentialPrivacyProcessor, apply_differential_privacy as _apply_differential_privacy
    class DifferentialPrivacyProcessor(_DifferentialPrivacyProcessor):
        def __init__(self, *args, **kwargs):
            _require_activation()
            super().__init__(*args, **kwargs)
    def apply_differential_privacy(*args, **kwargs):
        _require_activation()
        return _apply_differential_privacy(*args, **kwargs)
except:
    DifferentialPrivacyProcessor = None
    apply_differential_privacy = None

try:
    from .evaluation import evaluate_synthetic_data_comprehensive as _evaluate_synthetic_data_comprehensive
    def evaluate_synthetic_data_comprehensive(*args, **kwargs):
        _require_activation()
        return _evaluate_synthetic_data_comprehensive(*args, **kwargs)
except:
    evaluate_synthetic_data_comprehensive = None

try:
    from .utils import print_genuity_banner
except:
    def print_genuity_banner():
        print("Genuity v1.0.0")

__version__ = "0.1.2"
__author__ = "Genuity Team"

__all__ = [
    'TabularPreprocessor',
    'TabularPostprocessor',
    'CopulaAPI',
    'DifferentialPrivacyProcessor',
    'apply_differential_privacy',
    'evaluate_synthetic_data_comprehensive',
    'print_genuity_banner',
    'activate_license',
    'check_activation',
]

# Print banner on import
print_genuity_banner()
