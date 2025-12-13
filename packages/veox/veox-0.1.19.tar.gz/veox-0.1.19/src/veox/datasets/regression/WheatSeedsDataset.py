import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WheatSeedsDataset(BaseDatasetLoader):
    """Wheat Seeds dataset: predict seed area from geometric measurements."""

    def get_dataset_info(self):
        return {
            'name': 'WheatSeedsDataset',
            'source_id': 'uci:seeds',
            'category': 'regression',
            'description': 'Wheat Seeds dataset: predict seed area from geometric measurements.',
            'target_column': 'area'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"
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
        
        # This dataset is whitespace-separated and has no header.
        if df.shape[1] == 1:
            lines = df.iloc[:, 0].astype(str).tolist()
            data = [line.split() for line in lines if line.strip()]
            df = pd.DataFrame(data)
        
        # Assign column names based on UCI description
        df.columns = ['area', 'perimeter', 'compactness', 'length_of_kernel', 'width_of_kernel', 'asymmetry_coefficient', 'length_of_kernel_groove', 'type']
        df = df.drop('type', axis=1) # Not needed for this regression task

        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set target - use first numeric column as target if specified target not found
        if 'area' in df.columns:
            df['target'] = df['area']
            df = df.drop('area', axis=1)
        else:
            raise ValueError("area column not found for target.")

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
    ds = WheatSeedsDataset()
    frame = ds.get_data()
    print(frame.head())
