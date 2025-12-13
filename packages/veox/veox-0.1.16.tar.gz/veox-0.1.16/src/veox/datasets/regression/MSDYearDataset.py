import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class MSDYearDataset(BaseDatasetLoader):
    """Year Prediction MSD dataset: predict song release year from audio features."""

    def get_dataset_info(self):
        return {
            'name': 'MSDYearDataset',
            'source_id': 'uci:yearpredictionmsd',
            'category': 'regression',
            'description': 'Year Prediction MSD dataset: predict song release year from audio features.',
            'target_column': 'year'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00203/YearPredictionMSD.txt.zip"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            # Extract from zip
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                files = [f for f in z.namelist() if f.endswith(('.csv', '.data', '.txt'))]
                if files:
                    with z.open(files[0]) as f:
                        return f.read()
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # This dataset has no header. Target is the first column.
        df.columns = ['year'] + [f'feat_{i}' for i in range(1, 91)]
        
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set target - use first numeric column as target if specified target not found
        if 'year' in df.columns:
            df['target'] = df['year']
            df = df.drop('year', axis=1)
        else:
            raise ValueError("year column not found for target.")
        
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
    ds = MSDYearDataset()
    frame = ds.get_data()
    print(frame.head())
