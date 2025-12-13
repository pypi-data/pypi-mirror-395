import os
import pandas as pd
import numpy as np
import io
from sklearn.datasets import load_diabetes
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class DiabetesDataset(BaseDatasetLoader):
    """
    Loader for the Diabetes dataset from scikit-learn.
    
    This dataset is used for regression to predict disease progression one year after baseline
    based on 10 physiological variables such as age, sex, body mass index, etc.
    
    Features: 10 variables (age, sex, BMI, blood pressure, etc.)
    Target: Disease progression one year after baseline
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'DiabetesDataset',
            'source_id': 'sklearn:diabetes',  # Unique identifier
            'category': 'regression',
            'description': 'Diabetes dataset: regression to predict disease progression based on physiological features.',
        }
    
    def download_dataset(self, info):
        """Get the diabetes dataset from scikit-learn"""
        dataset_name = info['name']
        print(f"[{dataset_name}] Loading diabetes dataset from scikit-learn...")
        
        try:
            # Load the dataset from scikit-learn
            diabetes = load_diabetes()
            
            # Create DataFrame
            feature_names = diabetes.feature_names
            df = pd.DataFrame(diabetes.data, columns=feature_names)
            df["target"] = diabetes.target
            
            # Convert to CSV bytes
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode('utf-8')
            
            file_size = len(csv_data)
            print(f"[{dataset_name}] Dataset loaded. Size: {file_size} bytes")
            
            if file_size < 5000:
                print(f"[{dataset_name}] Data too small. First few rows:\n{df.head().to_string()}")
                raise Exception(f"Generated data too small: {file_size} bytes. Expected >5 KB.")
                
            return csv_data
        except Exception as e:
            print(f"[{dataset_name}] Loading failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
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
                    if pd.api.types.is_numeric_dtype(df[col]):
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
    dataset = DiabetesDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.")
