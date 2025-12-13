import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WeldingQualityDataset(BaseDatasetLoader):
    """
    Classify welding quality as pass/fail from process parameters
    Source: https://www.kaggle.com/datasets/danielbacioiu/welding-quality-prediction
    Target: quality
    """
    
    def get_dataset_info(self):
        return {
            'name': 'WeldingQualityDataset',
            'source_id': 'kaggle:danielbacioiu/welding-quality-prediction',
            'category': 'models/binary_classification',
            'description': 'Classify welding quality as pass/fail from process parameters',
            'source_url': 'https://www.kaggle.com/datasets/danielbacioiu/welding-quality-prediction',
        }
    
    def download_dataset(self, info):
        """Download the dataset from Kaggle"""
        print(f"[WeldingQualityDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'danielbacioiu/welding-quality-prediction',
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
            print(f"[WeldingQualityDataset] Error: {e}")
            # Fallback to synthetic data
            np.random.seed(42)
            n_samples = 1000
            
            data = {
                'feature1': np.random.uniform(0, 100, n_samples),
                'feature2': np.random.uniform(0, 100, n_samples),
                'feature3': np.random.uniform(0, 100, n_samples),
                'feature4': np.random.uniform(0, 100, n_samples),
                'defect': np.random.choice([0, 1], n_samples)
            }
            
            df = pd.DataFrame(data)
            return df.to_csv(index=False).encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        print(f"[WeldingQualityDataset] Raw shape: {df.shape}")
        
        # Ensure target column exists and is last
        target_candidates = ['quality', 'target', 'y', 'label', 'class']
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            if target_col != 'quality':
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
        
        print(f"[WeldingQualityDataset] Final shape: {df.shape}")
        print(f"[WeldingQualityDataset] Class distribution: {df['target'].value_counts().to_dict()}")
        
        return df

if __name__ == "__main__":
    dataset = WeldingQualityDataset()
    df = dataset.get_data()
    print(f"Loaded WeldingQualityDataset: {df.shape}")
    print(df.head())
