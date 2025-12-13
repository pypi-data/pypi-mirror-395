import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CastingDefectBinaryDataset(BaseDatasetLoader):
    """
    Binary classification of casting defects
    Source: https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product
    Target: has_defect
    """
    
    def get_dataset_info(self):
        return {
            'name': 'CastingDefectBinaryDataset',
            'source_id': 'kaggle:ravirajsinh45/real-life-industrial-dataset-of-casting-product',
            'category': 'models/binary_classification',
            'description': 'Binary classification of casting defects',
            'source_url': 'https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product',
        }
    
    def download_dataset(self, info):
        """Download the dataset from Kaggle"""
        print(f"[CastingDefectBinaryDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'ravirajsinh45/real-life-industrial-dataset-of-casting-product',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV file
                csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                
                csv_path = os.path.join(temp_dir, csv_files[0])
                df = pd.read_csv(csv_path)
                
                return df.to_csv(index=False).encode('utf-8')
                
        except Exception as e:
            # Strict: synthetic fallback is not allowed for Human datasets
            raise RuntimeError(
                f"[CastingDefectBinaryDataset] Failed to download dataset from Kaggle: {e}. "
                "Synthetic fallback is disabled. Ensure this dataset is provisioned in S3 via admin APIs."
            )
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        print(f"[CastingDefectBinaryDataset] Raw shape: {df.shape}")
        
        # Ensure target column exists and is last
        target_candidates = ['has_defect', 'target', 'y', 'label', 'class']
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            if target_col != 'has_defect':
                df = df.drop(target_col, axis=1)
        
        # If no target found, use last column
        if 'target' not in df.columns:
            last_col = df.columns[-1]
            df['target'] = df[last_col]
            if last_col != 'target':
                df = df.drop(last_col, axis=1)
        
        # Remove non-numeric columns except target
        numeric_cols = []
        for col in df.columns:
            if col == 'target':
                continue
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                numeric_cols.append(col)
            except:
                pass
        
        # Keep only numeric columns and target
        df = df[numeric_cols + ['target']]
        
        # Remove rows with missing values
        df = df.dropna()
        
        
        # Convert target to binary
        if df['target'].dtype == 'object':
            # Convert string labels to binary
            unique_vals = df['target'].unique()
            if len(unique_vals) == 2:
                df['target'] = (df['target'] == unique_vals[0]).astype(int)
            else:
                # Use median split for numeric
                df['target'] = pd.to_numeric(df['target'], errors='coerce')
                df = df.dropna(subset=['target'])
                df['target'] = (df['target'] > df['target'].median()).astype(int)
        else:
            # Ensure binary values
            df['target'] = df['target'].astype(int)
            if df['target'].nunique() > 2:
                df['target'] = (df['target'] > df['target'].median()).astype(int)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Shuffle the data
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[CastingDefectBinaryDataset] Final shape: {df.shape}")
        print(f"[CastingDefectBinaryDataset] Class distribution: {df['target'].value_counts().to_dict()}")
        
        return df

if __name__ == "__main__":
    dataset = CastingDefectBinaryDataset()
    df = dataset.get_data()
    print(f"Loaded CastingDefectBinaryDataset: {df.shape}")
    print(df.head())
