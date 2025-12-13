import pandas as pd
import requests
import io
import gzip
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ForestCoverDataset(BaseDatasetLoader):
    """Forest Cover dataset: predict elevation from forest characteristics."""

    def get_dataset_info(self):
        return {
            'name': 'ForestCoverDataset',
            'source_id': 'uci:forest_cover_type',
            'category': 'regression',
            'description': 'Forest Cover dataset: predict elevation from forest characteristics.',
            'target_column': 'Elevation'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz"
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
        
        # This dataset has no header, so assign column names
        # 10 quantitative variables, 4 binary wilderness areas, 40 binary soil types, 1 target
        base_features = [f'feat_{i}' for i in range(1, 55)]
        df.columns = base_features + ['Cover_Type'] # Cover_Type is not used in this regression task
        df.rename(columns={'feat_1': 'Elevation'}, inplace=True)
        
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set target - Elevation
        if 'Elevation' in df.columns:
            df['target'] = df['Elevation']
            df = df.drop('Elevation', axis=1)
        else:
            raise ValueError("Elevation column not found to set as target.")

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
    ds = ForestCoverDataset()
    frame = ds.get_data()
    print(frame.head())
