import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class AbaloneDataset(BaseDatasetLoader):
    """
    Loader for the Abalone dataset from the UCI Machine Learning Repository.
    
    This dataset is used to predict the age of abalone from physical measurements.
    The age is determined by the number of rings in the shell.
    
    Features include physical measurements (length, diameter, height, weights).
    Target is 'rings' which represents the age.
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'AbaloneDataset',
            'source_id': 'uci:abalone',  # Unique identifier
            'category': 'regression',
            'description': 'Abalone Dataset: physical measurements to predict the age (rings) of abalones.'
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository"""
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 10000:  # Abalone data is ~190KB
                first_lines = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. First few lines:\n{os.linesep.join(first_lines)}")
                raise Exception(f"Downloaded file too small: {file_size} bytes. Expected >10 KB.")
                
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        # Log initial state
        print(f"[{dataset_name}] Initial DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Initial column names: {df.columns.tolist()}")
        
        # Handle abalone.data format - it's a CSV without headers where the
        # last column is 'rings' (our target) and first column is 'sex'
        if df.shape[1] == 1:
            # Data might be loaded as a single column with comma-separated values
            print(f"[{dataset_name}] Data loaded as a single column, attempting to split")
            
            # Check if first row has commas - if so, we need to split
            first_row = df.iloc[0, 0]
            if isinstance(first_row, str) and ',' in first_row:
                # Split the text in the first column by commas
                rows = []
                for _, row in df.iterrows():
                    values = row[0].split(',')
                    rows.append(values)
                
                # Create a new DataFrame with the split data
                df = pd.DataFrame(rows)
                print(f"[{dataset_name}] Successfully split comma-delimited data into {df.shape[1]} columns")
        
        # Always assign proper column names for abalone dataset
        if df.shape[1] == 9:
            column_names = [
                "sex", "length", "diameter", "height", "whole_weight",
                "shucked_weight", "viscera_weight", "shell_weight", "rings"
            ]
            df.columns = column_names
            print(f"[{dataset_name}] Assigned proper column names: {', '.join(column_names)}")
        elif all(isinstance(col, int) for col in df.columns) or any(str(col).replace('.', '').isdigit() for col in df.columns):
            # If columns are numeric or look like data values, assign proper names
            column_names = [
                "sex", "length", "diameter", "height", "whole_weight",
                "shucked_weight", "viscera_weight", "shell_weight", "rings"
            ]
            
            # Adjust column names if DataFrame has different number of columns
            if df.shape[1] != len(column_names):
                print(f"[{dataset_name}] Warning: Expected 9 columns but got {df.shape[1]}")
                
                if df.shape[1] < len(column_names):
                    # If fewer columns than expected, use only what we need
                    column_names = column_names[:df.shape[1]]
                else:
                    # If more columns, add generic extra column names
                    for i in range(df.shape[1] - len(column_names)):
                        column_names.append(f"extra_{i+1}")
            
            df.columns = column_names
            print(f"[{dataset_name}] Assigned column names: {', '.join(column_names)}")
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Convert numeric columns to proper types
        numeric_cols = ["length", "diameter", "height", "whole_weight", "shucked_weight", 
                       "viscera_weight", "shell_weight", "rings"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert sex column to numeric (M=1, F=0, I=2)
        if 'sex' in df.columns:
            sex_mapping = {'M': 1, 'F': 0, 'I': 2}
            df['sex'] = df['sex'].map(sex_mapping)
            print(f"[{dataset_name}] Converted 'sex' column to numeric (M=1, F=0, I=2)")
        
        # Set target if not already set
        if 'target' not in df.columns:
            # Check if we have a 'rings' column
            if 'rings' in df.columns:
                df['target'] = df['rings']
                print(f"[{dataset_name}] Set 'rings' as the target column")
            else:
                # If no 'rings' column, assume the last column is the target
                last_col = df.columns[-1]
                print(f"[{dataset_name}] 'rings' column not found, using last column '{last_col}' as target")
                df['target'] = pd.to_numeric(df[last_col], errors='coerce')
        
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing")
        
        # Handle missing values if any
        if df.isna().any().any():
            print(f"[{dataset_name}] Filling missing values with column medians (for numeric) or mode (for categorical)...")
            for col in df.columns:
                if df[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df[col]):
                        df[col] = df[col].fillna(df[col].median())
                    else:
                        df[col] = df[col].fillna(df[col].mode()[0])  # Fill with the first mode
        
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indices reset.")
        
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
    dataset = AbaloneDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 