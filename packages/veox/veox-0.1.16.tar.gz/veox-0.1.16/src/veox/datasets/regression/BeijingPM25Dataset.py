import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BeijingPM25Dataset(BaseDatasetLoader):
    """Beijing PM2.5 dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'BeijingPM25Dataset',
            'source_id': 'uci:beijing_pm25',
            'category': 'regression',
            'description': 'Beijing PM2.5 dataset: predict air pollution from weather conditions.',
            'target_column': 'pm2.5'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00381/PRSA_data_2010.1.1-2014.12.31.csv"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Remove index column if present
        if 'No' in df.columns:
            df = df.drop('No', axis=1)
        
        # Remove date/time columns for regression
        time_cols = ['year', 'month', 'day', 'hour']
        for col in time_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Set target (pm2.5)
        if 'pm2.5' in df.columns:
            df['target'] = df['pm2.5']
            df = df.drop('pm2.5', axis=1)
        
        # Convert categorical wind direction to numeric
        if 'cbwd' in df.columns:
            df['cbwd'] = pd.Categorical(df['cbwd']).codes
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Remove rows with missing target
        df = df.dropna(subset=['target'])
        
        # Handle missing values in features
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, PM2.5 range: {df['target'].min():.1f}-{df['target'].max():.1f}")
        return df 