import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SlumpTestDataset(BaseDatasetLoader):
    """Concrete Slump Test dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'SlumpTestDataset',
            'source_id': 'uci:concrete_slump_test',
            'category': 'regression',
            'description': 'Concrete Slump Test dataset: predict concrete slump from mixture components.',
            'target_column': 'slump'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/concrete/slump/slump_test.data"
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
        
        # Set target (SLUMP)
        if 'SLUMP(cm)' in df.columns:
            df['target'] = df['SLUMP(cm)']
            df = df.drop('SLUMP(cm)', axis=1)
        elif 'SLUMP' in df.columns:
            df['target'] = df['SLUMP']
            df = df.drop('SLUMP', axis=1)
        
        # Remove No column if present (just index)
        if 'No' in df.columns:
            df = df.drop('No', axis=1)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.1f}-{df['target'].max():.1f}")
        return df 

if __name__ == "__main__":
    ds = SlumpTestDataset()
    frame = ds.get_data()
    print(frame.head()) 