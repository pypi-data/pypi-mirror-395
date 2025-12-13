import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WaterTreatmentDataset(BaseDatasetLoader):
    """Water Treatment dataset: predict treatment plant performance from input parameters."""

    def get_dataset_info(self):
        return {
            'name': 'WaterTreatmentDataset',
            'source_id': 'uci:water_treatment_plant',
            'category': 'regression',
            'description': 'Water Treatment dataset: predict treatment plant performance from input parameters.',
            'target_column': 'output'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/water-treatment/water-treatment.data"
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
        
        # This dataset has no header and uses '?' for missing values.
        # It's also comma-separated.
        df.replace('?', pd.NA, inplace=True)
        
        # Assign column names based on UCI description
        df.columns = ['date'] + [f'v_{i}' for i in range(1, df.shape[1])]
        df = df.drop('date', axis=1) # date is not useful for this regression task

        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set target - use last numeric column as target
        if 'output' in df.columns: # As per get_dataset_info
            df['target'] = df['output']
            df = df.drop('output', axis=1)
        else:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[-1]
                df['target'] = df[target_col]
                df = df.drop(target_col, axis=1)
            else:
                raise ValueError("No numeric column to use as target.")
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df.dropna(inplace=True) # Drop rows with NA after '?' replacement
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.2f}-{df['target'].max():.2f}")
        return df

if __name__ == "__main__":
    ds = WaterTreatmentDataset()
    frame = ds.get_data()
    print(frame.head())
