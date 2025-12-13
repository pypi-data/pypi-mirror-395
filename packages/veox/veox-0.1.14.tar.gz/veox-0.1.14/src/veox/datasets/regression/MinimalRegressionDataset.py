"""Minimal synthetic regression dataset for testing."""

import numpy as np
import pandas as pd
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class MinimalRegressionDataset(BaseDatasetLoader):
    """Minimal synthetic regression dataset.
    
    Generates a simple regression dataset with linear relationships
    and small added noise.
    """
    
    def get_dataset_info(self):
        return {
            "name": "MinimalRegressionDataset",
            "source_id": "synthetic:minimal_regression",
            "category": "regression",
            "description": "Minimal synthetic regression dataset for testing",
            "origin": "synthetic",
            "tags": "synthetic,minimal,test"
        }
    
    def download_dataset(self, info):
        """Generate synthetic data instead of downloading."""
        dataset_name = info["name"]
        print(f"[{dataset_name}] Generating synthetic regression dataset...")
        
        np.random.seed(42)
        n_samples = 100
        
        X = np.random.randn(n_samples, 4)
        y = 2 * X[:, 0] - 1.5 * X[:, 1] + 0.5 * X[:, 2] + np.random.randn(n_samples) * 0.1
        
        df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)])
        df['target'] = y
        
        csv_string = df.to_csv(index=False)
        return csv_string.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Minimal processing - just ensure target is last column."""
        dataset_name = info["name"]
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        
        # Ensure target is last
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target stats: mean={df['target'].mean():.2f}, std={df['target'].std():.2f}")
        
        return df