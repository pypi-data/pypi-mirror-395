"""
Basic usage example for Masked Predictor Synthesizer
"""

import pandas as pd
import numpy as np
from ..utils.api import MaskedPredictorAPI


def main():
    """Basic usage example"""

    # Create sample data
    np.random.seed(42)
    n_samples = 1000

    data = {
        "age": np.random.normal(35, 10, n_samples),
        "income": np.random.normal(50000, 15000, n_samples),
        "education": np.random.choice(
            ["High School", "Bachelor", "Master", "PhD"], n_samples
        ),
        "city": np.random.choice(["NYC", "LA", "Chicago", "Houston"], n_samples),
        "satisfaction": np.random.randint(1, 6, n_samples),
    }

    df = pd.DataFrame(data)
    print("Original data shape:", df.shape)
    print("Original data sample:")
    print(df.head())

    # Initialize and use the API
    api = MaskedPredictorAPI(
        chunk_size=0.1, device="cpu", cat_threshold=15, random_state=42
    )

    # Fit and generate
    synthetic_df = api.fit_generate(df)

    print("\nSynthetic data shape:", synthetic_df.shape)
    print("Synthetic data sample:")
    print(synthetic_df.head())

    # Compare statistics
    print("\nOriginal vs Synthetic Statistics:")
    print(
        "Age - Original mean:",
        df["age"].mean(),
        "Synthetic mean:",
        synthetic_df["age"].mean(),
    )
    print(
        "Income - Original mean:",
        df["income"].mean(),
        "Synthetic mean:",
        synthetic_df["income"].mean(),
    )
    print("Education distribution:")
    print("Original:", df["education"].value_counts().to_dict())
    print("Synthetic:", synthetic_df["education"].value_counts().to_dict())


if __name__ == "__main__":
    main()
