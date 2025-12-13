import pandas as pd
import numpy as np
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class MaterialFailureDataset(BaseDatasetLoader):
    """Material failure prediction under stress conditions"""

    def get_dataset_info(self):
        return {
            'name': 'MaterialFailureDataset',
            'source_id': 'kaggle:materialfailure',
            'category': 'models/binary_classification',
            'description': 'Material failure prediction under stress conditions',
            'kaggle_dataset': 'shivamb/machine-predictive-maintenance-classification',
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
        if 'failure' in df.columns:
            df['target'] = df['failure']
            df = df.drop('failure', axis=1)
        else:
            # Use last column as target
            last_col = df.columns[-1]
            df['target'] = df[last_col]
            df = df.drop(last_col, axis=1)
        
        # Handle text target values
        if df['target'].dtype == 'object':
            # Map text values to binary
            unique_vals = df['target'].unique()
            if len(unique_vals) == 2:
                # Binary text values
                val_map = {unique_vals[0]: 0, unique_vals[1]: 1}
                df['target'] = df['target'].map(val_map)
            else:
                # For multi-class, convert to binary (positive/negative sentiment)
                positive_vals = ['positive', 'good', 'yes', 'true', '1', 'pass']
                df['target'] = df['target'].str.lower().isin(positive_vals).astype(int)
        else:
            # Convert target to binary
            df['target'] = (df['target'] > df['target'].median()).astype(int)
        
        # Convert all columns to numeric
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle missing values - fill with median for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Drop any remaining rows with null values
        df = df.dropna()
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target distribution: {df['target'].value_counts().to_dict()}")
        return df