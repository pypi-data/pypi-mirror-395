"""
High-level API for Masked Predictor Synthesizer
"""

import pandas as pd
from .factory import MaskedPredictorFactory


class MaskedPredictorAPI:
    """High-level API for Masked Predictor Synthesizer"""

    def __init__(self, **config_kwargs):
        """
        Initialize the API

        Args:
            **config_kwargs: Configuration parameters
        """
        self.config = MaskedPredictorFactory.create_config(**config_kwargs)
        self.synthesizer = MaskedPredictorFactory.create_synthesizer(self.config)

    def fit(self, df: pd.DataFrame):
        """
        Fit the synthesizer to the data

        Args:
            df: Input DataFrame to synthesize
        """
        self.synthesizer.fit(df)

    def generate(self) -> pd.DataFrame:
        """
        Generate synthetic data

        Returns:
            Synthetic DataFrame
        """
        return self.synthesizer.generate()

    def fit_generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fit and generate synthetic data in one step

        Args:
            df: Input DataFrame to synthesize

        Returns:
            Synthetic DataFrame
        """
        self.fit(df)
        return self.generate()
