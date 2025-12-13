import pandas as pd
import requests
import io
import gzip
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class MetroTrafficDataset(BaseDatasetLoader):
    """Metro Traffic dataset: predict traffic volume from weather and date-time features."""

    def get_dataset_info(self):
        return {
            'name': 'MetroTrafficDataset',
            'source_id': 'uci:metro_interstate_traffic',
            'category': 'regression',
            'description': 'Metro Traffic dataset: predict traffic volume from weather and date-time features.',
            'target_column': 'traffic_volume'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00492/Metro_Interstate_Traffic_Volume.csv.gz"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            # Decompress gzip
            return gzip.decompress(response.content)
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        
        
        
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Set target - use first numeric column as target if specified target not found
        if 'traffic_volume' in df.columns:
            df['target'] = df['traffic_volume']
            df = df.drop('traffic_volume', axis=1)
        else:
            # Use last numeric column as target
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                df['target'] = df[numeric_cols[-1]]
                df = df.drop(numeric_cols[-1], axis=1)
        
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
