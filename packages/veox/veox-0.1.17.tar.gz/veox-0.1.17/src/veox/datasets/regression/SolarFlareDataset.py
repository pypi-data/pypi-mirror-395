import pandas as pd
import requests
import io

from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SolarFlareDataset(BaseDatasetLoader):
    """Solar Flare dataset: predict solar flare intensity from magnetic measurements."""

    def get_dataset_info(self):
        return {
            'name': 'SolarFlareDataset',
            'source_id': 'uci:solar_flare',
            'category': 'regression',
            'description': 'Solar Flare dataset: predict solar flare intensity from magnetic measurements.',
            'target_column': 'class'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/solar-flare/flare.data2"
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
        
        # This dataset is whitespace-delimited and has no header
        # It has 10 attributes for solar flare prediction
        expected_cols = ['Code_for_class', 'Code_for_largest_spot_size', 'Code_for_spot_distribution',
                        'Activity', 'Evolution', 'Previous_24hr_flare_activity', 'Historically_complex',
                        'Did_region_become_complex', 'Area', 'Area_of_largest_spot']
        
        if len(df.columns) == len(expected_cols):
            df.columns = expected_cols
        else:
            # Generic column names
            df.columns = [f'feature_{i+1}' for i in range(len(df.columns))]
            
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Set target - use area as it's a good regression target
        if 'Area' in df.columns:
            df['target'] = df['Area']
            df = df.drop('Area', axis=1)
        elif 'class' in df.columns:
            df['target'] = df['class']
            df = df.drop('class', axis=1)
        else:
            # Use last numeric column as target
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[-1]
                df['target'] = df[target_col]
                df = df.drop(target_col, axis=1)
            else:
                # If no numeric columns, use last column and try to convert
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
