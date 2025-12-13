import pandas as pd
import numpy as np
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WellFailurePredictionDataset(BaseDatasetLoader):
    """Well Failure Prediction dataset: predict well failure from operational parameters."""

    def get_dataset_info(self):
        return {
            'name': 'WellFailurePredictionDataset',
            'source_id': 'kaggle:well_failure',
            'category': 'models/binary_classification',
            'description': 'Well failure prediction: predict equipment failure from operational data.',
            'kaggle_dataset': 'bletchley/oil-and-gas-facilities-maintenance',
            'target_column': 'failure'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        
        # Try Kaggle API - no synthetic fallback allowed
        try:
            import kaggle
            import tempfile
            import os
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(info['kaggle_dataset'], path=temp_dir, unzip=True)
                
                # Find CSV file (prefer maintenance-related files)
                csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
                if not csv_files:
                    raise FileNotFoundError(f"[{dataset_name}] No CSV file found in Kaggle dataset")
                
                # Prefer maintenance-related files if available
                maintenance_files = [f for f in csv_files if 'maintenance' in f.lower()]
                csv_file = maintenance_files[0] if maintenance_files else csv_files[0]
                
                csv_path = os.path.join(temp_dir, csv_file)
                with open(csv_path, 'rb') as f:
                    return f.read()
        except ImportError:
            raise RuntimeError(
                f"[{dataset_name}] Kaggle module not available. "
                "Please install kaggle module and rebuild Docker containers. "
                "Synthetic fallback is disabled for Human datasets."
            )
        except Exception as e:
            raise RuntimeError(
                f"[{dataset_name}] Failed to download dataset from Kaggle: {e}. "
                "Synthetic fallback is disabled. Ensure this dataset is provisioned via Kaggle or S3/admin APIs."
            )
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Ensure target is last column
        if 'failure' in df.columns:
            df['target'] = df['failure']
            df = df.drop('failure', axis=1)
        else:
            # Use last column as target
            last_col = df.columns[-1]
            df['target'] = df[last_col]
            df = df.drop(last_col, axis=1)
        
        # Convert target to binary
        df['target'] = (df['target'] > df['target'].median()).astype(int)
        
        # Convert all columns to numeric
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target distribution: {df['target'].value_counts().to_dict()}")
        return df 