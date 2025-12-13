import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ParkinsonsTelemonitoringDataset(BaseDatasetLoader):
    """Parkinsons Telemonitoring dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'ParkinsonsTelemonitoringDataset',
            'source_id': 'uci:parkinsons_telemonitoring',
            'category': 'regression',
            'description': 'Parkinsons Telemonitoring dataset: predict motor UPDRS score from voice measurements.',
            'target_column': 'motor_UPDRS'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/telemonitoring/parkinsons_updrs.data"
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
        
        # Handle comma separator if needed
        if df.shape[1] == 1:
            text = '\n'.join(df.iloc[:, 0].astype(str))
            df = pd.read_csv(io.StringIO(text), sep=',')
        
        # Set target (motor_UPDRS)
        if 'motor_UPDRS' in df.columns:
            df['target'] = df['motor_UPDRS']
            df = df.drop('motor_UPDRS', axis=1)
        
        # Remove subject identifier if present
        if 'subject#' in df.columns:
            df = df.drop('subject#', axis=1)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.1f}-{df['target'].max():.1f}")
        return df 