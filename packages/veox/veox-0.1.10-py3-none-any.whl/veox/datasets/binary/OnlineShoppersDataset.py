import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class OnlineShoppersDataset(BaseDatasetLoader):
    """
    Loader for the UCI Online Shoppers Purchasing Intention dataset using
    the BaseDatasetLoader framework for intelligent caching with S3 and database.

    The dataset consists of 12,330 sessions from a genuine online
    retail store. The goal is to predict if a visitor session ends
    with a purchase (binary classification).

    Reference:
    https://archive.ics.uci.edu/ml/datasets/Online+Shoppers+Purchasing+Intention+Dataset

    Workflow
    --------
    1. Calculate URL hash to uniquely identify this dataset
    2. Check if dataset already exists in our database with this hash
    3. If it exists, use the S3 key to download it
    4. If not, download from the source URL, validate, and upload to S3
    5. Register the dataset in our database for future use
    6. Process the data into a clean DataFrame
    7. Return the cleaned, shuffled DataFrame with a 'target' column
    """

    def get_dataset_info(self):
        """Provide dataset-specific metadata."""
        return {
            'name': 'OnlineShoppersDataset',
            'source_id': 'https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv',
            'source_url': 'https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv',
            'category': 'binary_classification',
            'description': 'UCI Online Shoppers Purchasing Intention Dataset with 12,330 sessions. Target: whether a user made a purchase (1) or not (0).',
            'target_column': 'Revenue'
        }
    
    def download_dataset(self, info):
        """Download the Online Shoppers dataset from UCI"""
        print(f"[OnlineShoppersDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # CSV with header
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        print(f"[OnlineShoppersDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        """Process the data into the required format."""
        dataset_name = info['name']
        
        # Log basic info
        print(f"[{dataset_name}] Initial DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Check for Revenue column
        if 'Revenue' not in df.columns:
            raise ValueError(f"[{dataset_name}] No 'Revenue' column found in dataset.")
        
        # The "Revenue" column is True/False (boolean). We'll map it:
        # True  => 1
        # False => 0
        df['target'] = df['Revenue'].apply(lambda val: 1 if val else 0)
        df.drop(columns=['Revenue'], inplace=True)
        
        # Convert categorical columns to numeric
        print(f"[{dataset_name}] Converting categorical columns to numeric...")
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                # Use label encoding
                df[col] = pd.Categorical(df[col]).codes
                print(f"  - Encoded {col}")
            elif col != 'target' and df[col].dtype == 'bool':
                # Convert boolean to int
                df[col] = df[col].astype(int)
                print(f"  - Converted {col} from bool to int")
        
        # Check for missing values
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            pct = 100.0 * missing / len(df)
            print(f"  - {col}: {missing} missing ({pct:.2f}%)")
        
        # Drop rows with missing values
        initial_len = len(df)
        df.dropna(inplace=True)
        dropped_count = initial_len - len(df)
        if dropped_count > 0:
            print(f"[{dataset_name}] Dropped {dropped_count} rows with missing values.")
        
        # Shuffle dataset
        print(f"[{dataset_name}] Shuffling the dataset randomly (random_state=42)...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indices reset.")
        
        # Final logs
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution:")
        target_counts = df["target"].value_counts(dropna=False)
        print(f"  - Class 0 (no purchase): {target_counts.get(0, 0)} rows")
        print(f"  - Class 1 (purchase):    {target_counts.get(1, 0)} rows")
        
        return df

# Example usage (for testing purposes; remove in production)
if __name__ == "__main__":
    dataset = OnlineShoppersDataset()
    df = dataset.get_data()
    print(f"[TEST] Dataset loaded successfully with {len(df)} rows.")
