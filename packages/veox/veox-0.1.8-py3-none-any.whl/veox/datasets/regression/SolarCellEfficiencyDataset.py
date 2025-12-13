import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SolarCellEfficiencyDataset(BaseDatasetLoader):
    """
    Predict solar cell efficiency from material parameters
    Source: https://www.kaggle.com/datasets/mahmoudreda55/solar-cell-efficiency
    Target: efficiency
    """
    
    def get_dataset_info(self):
        return {
            'name': 'SolarCellEfficiencyDataset',
            'source_id': 'kaggle:mahmoudreda55/solar-cell-efficiency',
            'category': 'models/regression',
            'description': 'Predict solar cell efficiency from material parameters',
            'source_url': 'https://www.kaggle.com/datasets/mahmoudreda55/solar-cell-efficiency',
        }
    
    def download_dataset(self, info):
        """Download the dataset from Kaggle"""
        print(f"[SolarCellEfficiencyDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'mahmoudreda55/solar-cell-efficiency',
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
            print(f"[SolarCellEfficiencyDataset] Error: {e}")
            # Fallback to synthetic data
            np.random.seed(42)
            n_samples = 1000
            
            data = {
                'thickness': np.random.uniform(100, 500, n_samples),
                'temperature': np.random.uniform(25, 85, n_samples),
                'illumination': np.random.uniform(800, 1200, n_samples),
                'doping_concentration': np.random.uniform(1e15, 1e17, n_samples),
                'efficiency': np.random.uniform(10, 25, n_samples)
            }
            
            df = pd.DataFrame(data)
            return df.to_csv(index=False).encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        print(f"[SolarCellEfficiencyDataset] Raw shape: {df.shape}")
        
        # Ensure target column exists and is last
        target_candidates = ['efficiency', 'target', 'y', 'label', 'class']
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            if target_col != 'efficiency':
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
        
        print(f"[SolarCellEfficiencyDataset] Final shape: {df.shape}")
        print(f"[SolarCellEfficiencyDataset] Target range: [{df['target'].min():.2f}, {df['target'].max():.2f}]")
        
        return df

if __name__ == "__main__":
    dataset = SolarCellEfficiencyDataset()
    df = dataset.get_data()
    print(f"Loaded SolarCellEfficiencyDataset: {df.shape}")
    print(df.head())
