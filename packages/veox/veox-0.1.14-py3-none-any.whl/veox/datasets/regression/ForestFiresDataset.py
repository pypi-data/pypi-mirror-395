import os
import pandas as pd
import requests
from io import StringIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ForestFiresDataset(BaseDatasetLoader):
    """
    Loader for the Forest Fires dataset from the UCI Machine Learning Repository.
    
    This dataset contains meteorological and other data for predicting the burned area of forest fires in the northeast region of Portugal.
    The task is to predict the burned area (in hectares) from the features.
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'ForestFiresDataset',
            'source_id': 'uci:forest_fires',  # Unique identifier
            'category': 'regression',
            'description': 'Forest Fires Dataset: predict burned area of forest fires from meteorological data.'
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository"""
        dataset_name = info['name']
        print(f"[{dataset_name}] Downloading Forest Fires dataset...")
        
        try:
            # URL for the Forest Fires dataset
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv"
            print(f"[{dataset_name}] Downloading from URL: {url}")
            
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 5000:  # Sanity check for file size
                first_lines = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. First few lines:\n{os.linesep.join(first_lines)}")
                raise Exception(f"Downloaded file too small: {file_size} bytes. Expected >5 KB.")
                
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {str(e)}")
            raise

    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']

        print(f"[{dataset_name}] Initial DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")

        # Set the area column as the 'target' for regression
        if 'target' not in df.columns and 'area' in df.columns:
            df['target'] = df['area']
            print(f"[{dataset_name}] Set 'area' as the target column")

        # Convert month and day columns to numeric
        if 'month' in df.columns:
            month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
            df['month'] = df['month'].map(month_map)
            print(f"[{dataset_name}] Converted 'month' column to numeric")
        
        if 'day' in df.columns:
            day_map = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}
            df['day'] = df['day'].map(day_map)
            print(f"[{dataset_name}] Converted 'day' column to numeric")

        # Check for missing values
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing")

        # Fill missing values if any
        if df.isna().any().any():
            print(f"[{dataset_name}] Filling missing values with column medians...")
            for col in df.columns:
                if df[col].isna().any():
                    df[col] = df[col].fillna(df[col].median())

        # Shuffle dataset
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indices reset.")

        # Final logging
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Target summary:")
        print(f"  - Mean: {df['target'].mean():.2f}")
        print(f"  - Std: {df['target'].std():.2f}")
        print(f"  - Min: {df['target'].min():.2f}")
        print(f"  - Max: {df['target'].max():.2f}")
        print(f"[{dataset_name}] Sample of first 5 rows:\n{df.head().to_string()}")

        return df

# For testing
if __name__ == "__main__":
    dataset = ForestFiresDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 