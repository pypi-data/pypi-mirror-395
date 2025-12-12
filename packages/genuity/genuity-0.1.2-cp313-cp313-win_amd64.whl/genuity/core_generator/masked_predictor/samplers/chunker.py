import numpy as np


class Chunker:
    def __init__(self, df, column_name, chunk_frac=0.1):
        """
        Initialize chunker for data splitting

        Args:
            df: Input DataFrame
            column_name: Name of the column being processed
            chunk_frac: Fraction of data to mask in each chunk
        """
        self.df = df
        self.col = column_name
        self.chunk_frac = chunk_frac
        self.n_rows = len(df)
        self.indices = np.arange(self.n_rows)

    def __iter__(self):
        """
        Iterate over chunks of data

        Yields:
            Tuple of (train_indices, mask_indices)
        """
        chunk_size = max(1, int(self.n_rows * self.chunk_frac))

        # For very small datasets, just do one iteration
        if chunk_size >= self.n_rows:
            # Use 1 sample for masking, rest for training
            mask_idx = self.indices[:1]
            train_idx = self.indices[1:]
            yield train_idx, mask_idx
            return

        for start in range(0, self.n_rows, chunk_size):
            end = min(start + chunk_size, self.n_rows)

            mask_idx = self.indices[start:end]
            train_idx = np.setdiff1d(self.indices, mask_idx)

            # Ensure we have training data
            if len(train_idx) > 0:
                yield train_idx, mask_idx
