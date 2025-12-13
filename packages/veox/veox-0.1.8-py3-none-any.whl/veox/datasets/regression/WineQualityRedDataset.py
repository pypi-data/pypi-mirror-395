import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WineQualityRedDataset(BaseDatasetLoader):
    """Wine Quality Red dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'WineQualityRedDataset',
            'source_id': 'uci:wine_quality_red',
            'category': 'regression',
            'description': 'Wine Quality Red dataset: predict wine quality rating from physicochemical properties.',
            'target_column': 'quality'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
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
        
        # Handle semicolon separator
        if df.shape[1] == 1:
            text = '\n'.join(df.iloc[:, 0].astype(str))
            df = pd.read_csv(io.StringIO(text), sep=';')
        
        # Rename target column to be last
        if 'quality' in df.columns:
            df['target'] = df['quality']
            df = df.drop('quality', axis=1)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min()}-{df['target'].max()}")
        return df 

if __name__ == "__main__":
    ds = WineQualityRedDataset()
    frame = ds.get_data()
    print(frame.head()) 