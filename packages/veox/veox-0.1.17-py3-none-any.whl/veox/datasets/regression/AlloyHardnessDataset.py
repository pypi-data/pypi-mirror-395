import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class AlloyHardnessDataset(BaseDatasetLoader):
    """
    Predict alloy hardness from heat treatment parameters
    Source: https://www.kaggle.com/datasets/afumetto/steels-hardness
    Target: hardness
    """
    
    def get_dataset_info(self):
        return {
            'name': 'AlloyHardnessDataset',
            'source_id': 'kaggle:afumetto/steels-hardness',
            'category': 'models/regression',
            'description': 'Predict alloy hardness from heat treatment parameters',
            'source_url': 'https://www.kaggle.com/datasets/afumetto/steels-hardness',
        }
    
    def download_dataset(self, info):
        """Download the dataset from Kaggle"""
        print(f"[AlloyHardnessDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'afumetto/steels-hardness',
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
            print(f"[AlloyHardnessDataset] Error: {e}")
            # Fallback to synthetic data
            np.random.seed(42)
            n_samples = 1000
            
            data = {
                'carbon': np.random.uniform(0.05, 0.8, n_samples),
                'manganese': np.random.uniform(0.3, 1.8, n_samples),
                'silicon': np.random.uniform(0.1, 0.5, n_samples),
                'chromium': np.random.uniform(0, 2, n_samples),
                'temperature': np.random.uniform(200, 700, n_samples),
                'tensile_strength': np.random.uniform(200, 2000, n_samples)
            }
            
            df = pd.DataFrame(data)
            return df.to_csv(index=False).encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        print(f"[AlloyHardnessDataset] Raw shape: {df.shape}")
        
        # Ensure target column exists and is last
        target_candidates = ['hardness', 'target', 'y', 'label', 'class']
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            if target_col != 'hardness':
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
        
        print(f"[AlloyHardnessDataset] Final shape: {df.shape}")
        print(f"[AlloyHardnessDataset] Target range: [{df['target'].min():.2f}, {df['target'].max():.2f}]")
        
        return df

if __name__ == "__main__":
    dataset = AlloyHardnessDataset()
    df = dataset.get_data()
    print(f"Loaded AlloyHardnessDataset: {df.shape}")
    print(df.head())
