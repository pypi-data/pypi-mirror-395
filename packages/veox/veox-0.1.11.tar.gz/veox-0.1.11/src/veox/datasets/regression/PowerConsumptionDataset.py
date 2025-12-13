import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class PowerConsumptionDataset(BaseDatasetLoader):
    """Power Consumption dataset: predict household power consumption from appliance usage."""

    def get_dataset_info(self):
        return {
            'name': 'PowerConsumptionDataset',
            'source_id': 'uci:individual_household_power_consumption',
            'category': 'regression',
            'description': 'Power Consumption dataset: predict household power consumption from appliance usage.',
            'target_column': 'Global_active_power'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
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
        
        
        df = pd.read_csv(io.StringIO(df.iloc[0, 0]), sep=';') if df.shape[1] == 1 else df
        
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Set target - use first numeric column as target if specified target not found
        if 'Global_active_power' in df.columns:
            df['target'] = df['Global_active_power']
            df = df.drop('Global_active_power', axis=1)
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
