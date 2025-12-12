import pandas as pd
import numpy as np
from tqdm import tqdm
import torch

from .predictor import SingleColumnPredictor
from ..samplers.chunker import Chunker
from ..utils.data_utils import (
    detect_column_types,
    infer_metadata,
)


class MaskedPredictorSynthesizer:
    def __init__(self, config):
        """
        Initialize Masked Predictor Synthesizer

        Args:
            config: MaskedPredictorConfig instance
        """
        self.config = config
        self.chunk_size = config.chunk_size
        self.device = config.device
        self.real_df = None
        self.synthetic_df = None
        self.column_types = None
        self.metadata = None
        self.models = {}

    def fit(self, df: pd.DataFrame):
        """
        Fit the masked predictor synthesizer

        Args:
            df: Input DataFrame to synthesize
        """
        # 1) Shuffle and copy
        df = df.copy().reset_index(drop=True)
        self.real_df = df.sample(
            frac=1.0, random_state=self.config.random_state
        ).reset_index(drop=True)
        self.synthetic_df = self.real_df.copy()

        # 2) Column typing & metadata
        if self.config.column_types is not None:
            # Use user-specified column types
            self.column_types = self.config.column_types
        else:
            # Auto-detect column types
            self.column_types = detect_column_types(df, self.config.cat_threshold)

        self.metadata = infer_metadata(df, self.column_types)

        # 3) Mask-predict loop
        for col in tqdm(df.columns, desc="Masking & Predicting"):
            predictor = SingleColumnPredictor(col, self.column_types[col], self.config)
            chunker = Chunker(df, col, self.chunk_size)

            for train_idx, mask_idx in chunker:
                # Training split
                train_df = self.synthetic_df.iloc[train_idx]
                X_train = train_df.drop(columns=[col])
                y_train = train_df[col]

                predictor.fit(X_train, y_train)

                # Prediction split
                X_mask = self.synthetic_df.drop(columns=[col]).iloc[mask_idx]
                y_pred = predictor.predict(X_mask)

                # Fill synthetic with proper dtype conversion
                if len(mask_idx) > 0:
                    # Convert predictions to the original dtype
                    original_dtype = self.synthetic_df[col].dtype
                    if pd.api.types.is_numeric_dtype(original_dtype):
                        y_pred = pd.to_numeric(y_pred, errors="coerce")
                    else:
                        y_pred = pd.Series(y_pred).astype(original_dtype)

                    self.synthetic_df.loc[mask_idx, col] = y_pred

            self.models[col] = predictor

    def generate(self) -> pd.DataFrame:
        """
        Returns the synthetic DataFrame produced by the masked predictor logic.
        Make sure to call `fit()` before `generate()`.
        """
        if self.synthetic_df is None:
            raise ValueError("No synthetic data available. Please call `fit()` first.")
        return self.synthetic_df.copy()
