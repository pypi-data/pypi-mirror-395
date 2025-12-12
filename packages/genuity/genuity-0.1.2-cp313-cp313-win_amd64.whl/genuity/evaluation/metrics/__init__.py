"""
Comprehensive Metrics Package for Synthetic Data Evaluation

This package contains all evaluation metrics organized by category:
- similarity: Statistical similarity measures
- utility: Data utility assessment
- privacy: Privacy preservation evaluation
- detectability: Synthetic data detection
- missingness: Missing value pattern analysis
"""

from .similarity import (
    UnivariateSimilarityMetrics,
    MultivariateSimilarityMetrics,
    CorrelationSimilarityMetrics,
    SDMetricsSimilarity,
)
from .utility import (
    TSTRMetrics,
    TRTSMetrics,
    PredictionAgreementMetrics,
    LikelihoodLeakMetrics,
)
from .privacy import (
    MembershipInferenceMetrics,
    AttributeInferenceMetrics,
    NearestNeighborMetrics,
)
from .detectability import ClassifierAUCMetrics
from .missingness import MissingnessPatternMetrics

__version__ = "1.0.0"
__author__ = "Genuity Team"

__all__ = [
    # Similarity metrics
    "UnivariateSimilarityMetrics",
    "MultivariateSimilarityMetrics",
    "CorrelationSimilarityMetrics",
    "SDMetricsSimilarity",
    # Utility metrics
    "TSTRMetrics",
    "TRTSMetrics",
    "PredictionAgreementMetrics",
    "LikelihoodLeakMetrics",
    # Privacy metrics
    "MembershipInferenceMetrics",
    "AttributeInferenceMetrics",
    "NearestNeighborMetrics",
    # Detectability metrics
    "ClassifierAUCMetrics",
    # Missingness metrics
    "MissingnessPatternMetrics",
]

# Silenced verbose import messages - functionality unchanged
# print("📊 Metrics Package Loaded Successfully!")
# print("🎯 Available metric categories:")
# print("  - Similarity: Univariate, Multivariate, Correlation, SDMetrics")
# print("  - Utility: TSTR, TRTS, Prediction Agreement, Likelihood Leak")
# print("  - Privacy: Membership Inference, Attribute Inference, Nearest Neighbor")
# print("  - Detectability: Classifier AUC")
# print("  - Missingness: Pattern Analysis")
