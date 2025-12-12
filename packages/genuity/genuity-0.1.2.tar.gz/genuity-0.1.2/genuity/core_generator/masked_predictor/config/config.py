"""
Configuration for Masked Predictor Synthesizer
"""


class MaskedPredictorConfig:
    """Configuration class for Masked Predictor Synthesizer"""

    def __init__(
        self,
        chunk_size: float = 0.1,
        device: str = "cpu",
        cat_threshold: int = 15,
        random_state: int = 42,
        model_type: str = "hist_gradient_boosting",
        column_types: dict = None,
    ):
        """
        Initialize configuration for Masked Predictor

        Args:
            chunk_size: Fraction of data to mask during each iteration
            device: Device to use for computation ('cpu' or 'cuda')
            cat_threshold: Threshold for determining categorical columns
            random_state: Random seed for reproducibility
            model_type: Type of model to use for prediction
            column_types: Dictionary mapping column names to their types ('categorical' or 'continuous')
                         If None, will be auto-detected
        """
        self.chunk_size = chunk_size
        self.device = device
        self.cat_threshold = cat_threshold
        self.random_state = random_state
        self.model_type = model_type
        self.column_types = column_types
