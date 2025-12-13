import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class RedWinePhysicsDataset(BaseDatasetLoader):
    """Red Wine Physics dataset: predict alcohol content from physicochemical properties."""

    def get_dataset_info(self):
        return {
            'name': 'RedWinePhysicsDataset',
            'source_id': 'uci:physicochemical_red_wine',
            'category': 'regression',
            'description': 'Red Wine Physics dataset: predict alcohol content from physicochemical properties.',
            'target_column': 'alcohol'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
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
        
        
        df = pd.read_csv(io.StringIO(df.iloc[0, 0]), sep=';') if df.shape[1] == 1 else df
        
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Set target - use first numeric column as target if specified target not found
        if 'alcohol' in df.columns:
            df['target'] = df['alcohol']
            df = df.drop('alcohol', axis=1)
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
