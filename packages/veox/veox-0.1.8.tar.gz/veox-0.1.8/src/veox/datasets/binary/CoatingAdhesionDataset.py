import pandas as pd
import numpy as np
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CoatingAdhesionDataset(BaseDatasetLoader):
    """Coating adhesion quality from surface preparation"""

    def get_dataset_info(self):
        return {
            'name': 'CoatingAdhesionDataset',
            'source_id': 'kaggle:coatingadhesion',
            'category': 'models/binary_classification',
            'description': 'Coating adhesion quality from surface preparation',
            'kaggle_dataset': 'podsyp/coating-defects',
            'target_column': 'good_adhesion'
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
                
                # Find CSV file
                csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
                if not csv_files:
                    raise FileNotFoundError(f"[{dataset_name}] No CSV file found in Kaggle dataset")
                
                csv_path = os.path.join(temp_dir, csv_files[0])
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
        if 'good_adhesion' in df.columns:
            df['target'] = df['good_adhesion']
            df = df.drop('good_adhesion', axis=1)
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