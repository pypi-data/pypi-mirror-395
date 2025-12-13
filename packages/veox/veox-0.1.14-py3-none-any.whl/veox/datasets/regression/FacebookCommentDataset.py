import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class FacebookCommentDataset(BaseDatasetLoader):
    """Facebook Comment dataset: predict comment volume from page features."""

    def get_dataset_info(self):
        return {
            'name': 'FacebookCommentDataset',
            'source_id': 'uci:facebook_comment',
            'category': 'regression',
            'description': 'Facebook Comment dataset: predict comment volume from page features.',
            'target_column': 'comment_count'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00363/Dataset.zip"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            # Extract CSV from zip
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if csv_files:
                    with z.open(csv_files[0]) as f:
                        return f.read()
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Set target - check if comment_count exists first
        if 'comment_count' in df.columns:
            df['target'] = df['comment_count']
            df = df.drop('comment_count', axis=1)
        else:
            # Use last numeric column as target
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[-1]
                df['target'] = df[target_col]
                df = df.drop(target_col, axis=1)
            else:
                # If no numeric columns, use last column
                target_col = df.columns[-1]
                df['target'] = pd.to_numeric(df[target_col], errors='coerce')
                df = df.drop(target_col, axis=1)
        
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
    ds = FacebookCommentDataset()
    frame = ds.get_data()
    print(frame.head())
