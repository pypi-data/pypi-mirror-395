import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class AirfoilSelfNoiseDataset(BaseDatasetLoader):
    """
    Loader for the Airfoil Self-Noise dataset from the UCI Machine Learning Repository.
    
    This dataset contains aerodynamic and geometric features of airfoils and their resulting sound pressure level (noise).
    The task is to predict the sound pressure level (in decibels) from the features.
    
    Features include frequency, angle of attack, chord length, free-stream velocity, and displacement thickness.
    Target is the sound pressure level in decibels.
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'AirfoilSelfNoiseDataset',
            'source_id': 'uci:airfoil_self_noise',  # Unique identifier
            'category': 'regression',
            'description': 'Airfoil Self-Noise dataset: regression to predict sound pressure level based on airfoil characteristics.',
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository"""
        dataset_name = info['name']
        # URL for the Airfoil Self-Noise dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00291/airfoil_self_noise.dat"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
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
        
        # If DataFrame is a single column, attempt to split by whitespace
        if df.shape[1] == 1:
            print(f"[{dataset_name}] Detected single-column DataFrame; attempting to split by whitespace")
            rows = df.iloc[:,0].str.split(expand=True)
            if rows.shape[1] >= 6:
                df = rows
                print(f"[{dataset_name}] Successfully split into {df.shape[1]} columns")
            else:
                print(f"[{dataset_name}] Warning: After split, got {rows.shape[1]} columns (<6)")
        
        # If dataframe has numeric column names or no column names, assign them properly
        if all(isinstance(col, int) for col in df.columns) or df.shape[1] == 6:
            column_names = [
                'frequency', 'angle_of_attack', 'chord_length', 'free_stream_velocity', 
                'suction_side_displacement_thickness', 'sound_pressure_level'
            ]
            # Adjust if column count mismatch
            if df.shape[1] != len(column_names):
                print(f"[{dataset_name}] Warning: expected 6 columns, got {df.shape[1]}")
                if df.shape[1] < len(column_names):
                    column_names = column_names[:df.shape[1]]
                else:
                    for i in range(df.shape[1] - len(column_names)):
                        column_names.append(f"extra_{i+1}")
            df.columns = column_names
            print(f"[{dataset_name}] Assigned column names")
        
        print(f"[{dataset_name}] DataFrame shape (pre-coerce): {df.shape}")
        print(f"[{dataset_name}] Dtypes (pre-coerce):\n{df.dtypes}")
        # Coerce all columns to numeric where possible to avoid string concatenation in reductions
        try:
            df = df.apply(pd.to_numeric, errors='coerce')
        except Exception as _e:
            print(f"[{dataset_name}] Warning: numeric coercion step encountered an error: {_e}")
        print(f"[{dataset_name}] Dtypes (post-coerce):\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Set the sound_pressure_level column as the 'target' for regression if not already set
        if 'target' not in df.columns and 'sound_pressure_level' in df.columns:
            df['target'] = df['sound_pressure_level']
            print(f"[{dataset_name}] Set 'sound_pressure_level' as the target column")
        
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
    dataset = AirfoilSelfNoiseDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 