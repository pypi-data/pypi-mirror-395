import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class GlassDataset(BaseDatasetLoader):
    """Glass dataset: predict refractive index from chemical composition."""

    def get_dataset_info(self):
        return {
            'name': 'GlassDataset',
            'source_id': 'uci:glass_identification',
            'category': 'regression',
            'description': 'Glass dataset: predict refractive index from chemical composition.',
            'target_column': 'RI'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # This dataset has no header.
        df.columns = ['Id', 'RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe', 'Type']
        df = df.drop('Id', axis=1)

        # Set target - RI (Refractive Index)
        if 'RI' in df.columns:
            df['target'] = df['RI']
            df = df.drop('RI', axis=1)
        else:
            raise ValueError("RI column not found for target.")

        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert categorical columns to numeric
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = pd.Categorical(df[col]).codes
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.2f}-{df['target'].max():.2f}")
        return df

if __name__ == "__main__":
    ds = GlassDataset()
    frame = ds.get_data()
    print(frame.head())
