import pandas as pd
import numpy as np


def detect_column_types(df: pd.DataFrame, cat_threshold: int = 15):
    """
    Detect column types (categorical vs continuous)

    Args:
        df: Input DataFrame
        cat_threshold: Threshold for determining categorical columns

    Returns:
        Dictionary mapping column names to their types
    """
    col_types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            unique_vals = df[col].nunique(dropna=True)
            if unique_vals <= cat_threshold:
                col_types[col] = "categorical"
            else:
                col_types[col] = "continuous"
        else:
            col_types[col] = "categorical"
    return col_types


def infer_metadata(df: pd.DataFrame, col_types: dict):
    """
    Infer metadata for columns

    Args:
        df: Input DataFrame
        col_types: Dictionary of column types

    Returns:
        List of metadata dictionaries
    """
    metadata = []
    for col in df.columns:
        meta = {"name": col, "type": col_types[col]}
        if col_types[col] == "categorical":
            meta["cardinality"] = df[col].nunique()
        metadata.append(meta)
    return metadata
