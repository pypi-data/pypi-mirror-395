"""
Basic tests for Masked Predictor Synthesizer
"""

import pandas as pd
import numpy as np
import pytest
from ..config.config import MaskedPredictorConfig
from ..models.synthesizer import MaskedPredictorSynthesizer
from ..utils.api import MaskedPredictorAPI


class TestMaskedPredictorConfig:
    """Test configuration class"""

    def test_config_initialization(self):
        """Test config initialization with default values"""
        config = MaskedPredictorConfig()
        assert config.chunk_size == 0.1
        assert config.device == "cpu"
        assert config.cat_threshold == 15
        assert config.random_state == 42

    def test_config_custom_values(self):
        """Test config initialization with custom values"""
        config = MaskedPredictorConfig(
            chunk_size=0.2, device="cuda", cat_threshold=10, random_state=123
        )
        assert config.chunk_size == 0.2
        assert config.device == "cuda"
        assert config.cat_threshold == 10
        assert config.random_state == 123


class TestMaskedPredictorSynthesizer:
    """Test synthesizer class"""

    def setup_method(self):
        """Setup test data"""
        np.random.seed(42)
        self.test_data = pd.DataFrame(
            {
                "age": np.random.normal(35, 10, 100),
                "income": np.random.normal(50000, 15000, 100),
                "education": np.random.choice(["High School", "Bachelor"], 100),
                "satisfaction": np.random.randint(1, 6, 100),
            }
        )
        self.config = MaskedPredictorConfig()
        self.synthesizer = MaskedPredictorSynthesizer(self.config)

    def test_synthesizer_initialization(self):
        """Test synthesizer initialization"""
        assert self.synthesizer.config == self.config
        assert self.synthesizer.chunk_size == self.config.chunk_size
        assert self.synthesizer.device == self.config.device

    def test_fit_and_generate(self):
        """Test fit and generate methods"""
        self.synthesizer.fit(self.test_data)
        synthetic_data = self.synthesizer.generate()

        assert synthetic_data.shape == self.test_data.shape
        assert list(synthetic_data.columns) == list(self.test_data.columns)
        assert len(self.synthesizer.models) == len(self.test_data.columns)

    def test_generate_without_fit(self):
        """Test generate without calling fit first"""
        with pytest.raises(ValueError, match="No synthetic data available"):
            self.synthesizer.generate()


class TestMaskedPredictorAPI:
    """Test API class"""

    def setup_method(self):
        """Setup test data"""
        np.random.seed(42)
        self.test_data = pd.DataFrame(
            {
                "age": np.random.normal(35, 10, 50),
                "education": np.random.choice(["High School", "Bachelor"], 50),
            }
        )

    def test_api_initialization(self):
        """Test API initialization"""
        api = MaskedPredictorAPI(chunk_size=0.1, random_state=42)
        assert api.config.chunk_size == 0.1
        assert api.config.random_state == 42

    def test_fit_generate(self):
        """Test fit_generate method"""
        api = MaskedPredictorAPI(chunk_size=0.1, random_state=42)
        synthetic_data = api.fit_generate(self.test_data)

        assert synthetic_data.shape == self.test_data.shape
        assert list(synthetic_data.columns) == list(self.test_data.columns)

    def test_separate_fit_generate(self):
        """Test separate fit and generate methods"""
        api = MaskedPredictorAPI(chunk_size=0.1, random_state=42)
        api.fit(self.test_data)
        synthetic_data = api.generate()

        assert synthetic_data.shape == self.test_data.shape
        assert list(synthetic_data.columns) == list(self.test_data.columns)


if __name__ == "__main__":
    pytest.main([__file__])
