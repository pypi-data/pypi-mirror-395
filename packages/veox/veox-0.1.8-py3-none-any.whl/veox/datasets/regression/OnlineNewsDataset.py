import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class OnlineNewsDataset(BaseDatasetLoader):
    """Online News Popularity dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'OnlineNewsDataset',
            'source_id': 'uci:online_news_popularity',
            'category': 'regression',
            'description': 'Online News Popularity dataset: predict news article shares from content features.',
            'target_column': 'shares'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00332/OnlineNewsPopularity.zip"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            # Extract CSV from zip
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                with z.open('OnlineNewsPopularity/OnlineNewsPopularity.csv') as f:
                    return f.read()
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Remove URL column if present (not useful for prediction)
        if 'url' in df.columns:
            df = df.drop('url', axis=1)
        
        # Set target (shares)
        if 'shares' in df.columns:
            df['target'] = df['shares']
            df = df.drop('shares', axis=1)
        elif ' shares' in df.columns:
            df['target'] = df[' shares']
            df = df.drop(' shares', axis=1)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Log transform target to reduce skewness
        import numpy as np
        df['target'] = np.log1p(df['target'])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Log(shares) range: {df['target'].min():.2f}-{df['target'].max():.2f}")
        return df 