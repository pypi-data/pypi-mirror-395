"""
Factory for creating Masked Predictor components
"""

from ..config.config import MaskedPredictorConfig


class MaskedPredictorFactory:
    """Factory class for creating Masked Predictor components"""

    @staticmethod
    def create_config(**kwargs):
        """
        Create a configuration object

        Args:
            **kwargs: Configuration parameters

        Returns:
            MaskedPredictorConfig instance
        """
        return MaskedPredictorConfig(**kwargs)

    @staticmethod
    def create_synthesizer(config=None, **kwargs):
        """
        Create a synthesizer instance

        Args:
            config: Optional configuration object
            **kwargs: Configuration parameters (used if config is None)

        Returns:
            MaskedPredictorSynthesizer instance
        """
        # Lazy import to avoid circular dependency
        from ..models.synthesizer import MaskedPredictorSynthesizer

        if config is None:
            config = MaskedPredictorFactory.create_config(**kwargs)
        return MaskedPredictorSynthesizer(config)
