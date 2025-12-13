import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class PimaDiabetesDataset(BaseDatasetLoader):
    """
    Pima Indians Diabetes dataset.
    Classification: Binary (diabetes/no diabetes)
    Features: 8 numeric features related to medical measurements
    Source: UCI Machine Learning Repository
    """
    
    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'PimaDiabetesDataset',
            'source_id': 'uci:pima_indians',  # Unique identifier
            'category': 'binary_classification',
            'description': 'Pima Indians Diabetes Dataset: 768 samples, 8 features. Binary classification (diabetes/no diabetes).',
        }
    
    def download_dataset(self, info):
        """Download dataset from source"""
        dataset_name = info['name']
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        # Download data
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        # Define columns if not already in CSV
        if df.shape[1] == 9 and 'target' not in df.columns:
            columns = [
                'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin',
                'bmi', 'diabetes_pedigree_function', 'age', 'target'
            ]
            df.columns = columns
        
        # Log DataFrame details
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows of the DataFrame:\n{df.head(5).to_string()}")
        
        # Check for missing values
        print(f"[{dataset_name}] Missing values per column:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing values ({100 * missing / len(df):.2f}%)")
        
        # Handle missing values (fill with median for numeric columns)
        print(f"[{dataset_name}] Filling missing numeric values with median...")
        df.fillna(df.median(numeric_only=True), inplace=True)
        
        # Log target distribution
        target_counts = df['target'].value_counts(dropna=False)
        print(f"[{dataset_name}] Target distribution:")
        print(f"  - Class 0 (no diabetes): {target_counts.get(0, 0)} instances ({100 * target_counts.get(0, 0) / len(df):.2f}%)")
        print(f"  - Class 1 (diabetes): {target_counts.get(1, 0)} instances ({100 * target_counts.get(1, 0) / len(df):.2f}%)")
        print(f"  - NaN values: {df['target'].isna().sum()} instances ({100 * df['target'].isna().sum() / len(df):.2f}%)")
        
        # Shuffle dataset
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indexes reset.")
        
        # Final logging
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Sample of first 5 rows:\n{df.head(5).to_string()}")
        
        return df

# Example usage (for testing purposes)
if __name__ == "__main__":
    dataset = PimaDiabetesDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.")
