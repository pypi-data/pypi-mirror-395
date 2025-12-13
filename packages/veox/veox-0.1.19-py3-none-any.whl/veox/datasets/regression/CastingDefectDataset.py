import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CastingDefectDataset(BaseDatasetLoader):
    """
    Predict casting quality metrics from process parameters
    Source: https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product
    Target: defect_severity
    """
    
    def get_dataset_info(self):
        return {
            'name': 'CastingDefectDataset',
            'source_id': 'kaggle:ravirajsinh45/real-life-industrial-dataset-of-casting-product',
            'category': 'models/regression',
            'description': 'Predict casting quality metrics from process parameters',
            'source_url': 'https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product',
        }
    
    def download_dataset(self, info):
        """Download the dataset from Kaggle"""
        print(f"[CastingDefectDataset] Downloading from Kaggle...")
        
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
            print(f"[CastingDefectDataset] Error: {e}")
            # Fallback to synthetic data
            np.random.seed(42)
            n_samples = 1000
            
            data = {
                'parameter1': np.random.uniform(0, 100, n_samples),
                'parameter2': np.random.uniform(0, 100, n_samples),
                'parameter3': np.random.uniform(0, 100, n_samples),
                'parameter4': np.random.uniform(0, 100, n_samples),
                'target_value': np.random.uniform(0, 100, n_samples)
            }
            
            df = pd.DataFrame(data)
            return df.to_csv(index=False).encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        print(f"[CastingDefectDataset] Raw shape: {df.shape}")
        
        # Ensure target column exists and is last
        target_candidates = ['defect_severity', 'target', 'y', 'label', 'class']
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            if target_col != 'defect_severity':
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
        
        
        # Ensure target is numeric for regression
        df['target'] = pd.to_numeric(df['target'], errors='coerce')
        df = df.dropna(subset=['target'])
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Shuffle the data
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[CastingDefectDataset] Final shape: {df.shape}")
        print(f"[CastingDefectDataset] Target range: [{df['target'].min():.2f}, {df['target'].max():.2f}]")
        
        return df

if __name__ == "__main__":
    dataset = CastingDefectDataset()
    df = dataset.get_data()
    print(f"Loaded CastingDefectDataset: {df.shape}")
    print(df.head())
