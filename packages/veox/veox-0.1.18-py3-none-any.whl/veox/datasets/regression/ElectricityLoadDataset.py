import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ElectricityLoadDataset(BaseDatasetLoader):
    """Electricity Load dataset: predict electrical load from time series data."""

    def get_dataset_info(self):
        return {
            'name': 'ElectricityLoadDataset',
            'source_id': 'uci:electricity_load',
            'category': 'regression',
            'description': 'Electricity Load dataset: predict electrical load from time series data.',
            'target_column': 'MT_001'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00321/LD2011_2014.txt.zip"
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
        
        # The data is in a single column, needs to be parsed correctly.
        # It's semicolon-separated, and commas are decimal separators.
        if df.shape[1] == 1:
            # The file is large, so process it carefully
            text_data = df.iloc[:, 0].astype(str).str.cat(sep='\\n')
            df = pd.read_csv(io.StringIO(text_data), sep=';', decimal=',', header=0)

        # Convert all columns to numeric where possible, handling errors
        for col in df.columns:
            if col != 'datetime': # Assuming a datetime column exists
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set target 
        if 'MT_001' in df.columns:
            df['target'] = df['MT_001']
            df = df.drop('MT_001', axis=1)
        else:
            # Fallback to a numeric column as target
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                # Use a specific, likely target if available
                pot_target = [c for c in numeric_cols if c.startswith('MT_')]
                if pot_target:
                    df['target'] = df[pot_target[0]]
                    df = df.drop(pot_target[0], axis=1)
                else: # Fallback to last numeric
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

if __name__ == "__main__":
    ds = ElectricityLoadDataset()
    frame = ds.get_data()
    print(frame.head())
