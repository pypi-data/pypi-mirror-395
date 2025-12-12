"""
Masked Predictor Synthesizer

A masked predictor-based synthetic data generator that uses iterative masking
and prediction to generate synthetic tabular data.
"""

from .config.config import MaskedPredictorConfig
from .models.synthesizer import MaskedPredictorSynthesizer
from .models.predictor import SingleColumnPredictor
from .samplers.chunker import Chunker
from .utils.data_utils import detect_column_types, infer_metadata

# Import these directly to avoid circular imports
from .utils.factory import MaskedPredictorFactory
from .utils.api import MaskedPredictorAPI

__version__ = "0.1.0"
__author__ = "Genuity Team"

__all__ = [
    "MaskedPredictorConfig",
    "MaskedPredictorSynthesizer",
    "SingleColumnPredictor",
    "Chunker",
    "detect_column_types",
    "infer_metadata",
    "MaskedPredictorFactory",
    "MaskedPredictorAPI",
]
