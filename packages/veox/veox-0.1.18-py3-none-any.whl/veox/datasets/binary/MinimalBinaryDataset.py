"""Minimal synthetic binary classification dataset for testing."""

import numpy as np
import pandas as pd
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class MinimalBinaryDataset(BaseDatasetLoader):
    """Minimal synthetic binary classification dataset.
    
    NOTE: Synthetic datasets are not allowed under Human datasets. This loader is
    retained only as a stub and will raise if invoked. Use Generative datasets instead.
    """
    
    def get_dataset_info(self):
        return {
            "name": "MinimalBinaryDataset",
            "source_id": "synthetic:minimal_binary",
            "category": "binary_classification",
            "description": "Minimal synthetic binary classification dataset for testing",
            "origin": "synthetic",  # Flag for synthetic data
            "tags": "synthetic,minimal,test"
        }
    
    def download_dataset(self, info):
        # Strict: forbid synthetic generation under Human datasets
        raise RuntimeError(
            "[MinimalBinaryDataset] Synthetic dataset generation is not allowed under Human datasets. "
            "Use a Generative dataset instead or provision real data via S3/admin APIs."
        )
    
    def process_dataframe(self, df, info):
        """Minimal processing - just ensure target is last column."""
        dataset_name = info["name"]
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Columns: {list(df.columns)}")
        
        # Target should already be last column
        if 'target' not in df.columns:
            raise ValueError(f"[{dataset_name}] No 'target' column found")
        
        # Ensure target is last
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        
        return df