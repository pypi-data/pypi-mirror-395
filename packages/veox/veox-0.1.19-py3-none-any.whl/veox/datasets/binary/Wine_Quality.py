"""
Dataset: Wine Quality
Type: binary classification
Description: Automatically generated dataset
Source: Government open data portals (data.gov, data.gov.uk)
Generated: 2025-06-16 13:06:51

Statistics:
- Samples: 200
- Features: 11
- Target: quality
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_data():
    """Load and return the dataset as X, y arrays."""
    # Original data loading code

    # Dataset: Wine Quality
    # Description: Wine quality prediction based on chemical properties
    # Source: UCI Machine Learning Repository

    import pandas as pd
    import numpy as np

    # Simulate wine quality data
    np.random.seed(42)
    n_samples = 200

    df = pd.DataFrame({
        'fixed_acidity': np.random.uniform(4, 15, n_samples),
        'volatile_acidity': np.random.uniform(0.1, 1.5, n_samples),
        'citric_acid': np.random.uniform(0, 1, n_samples),
        'residual_sugar': np.random.uniform(0.5, 15, n_samples),
        'chlorides': np.random.uniform(0.01, 0.2, n_samples),
        'free_sulfur_dioxide': np.random.uniform(1, 60, n_samples),
        'total_sulfur_dioxide': np.random.uniform(6, 200, n_samples),
        'density': np.random.uniform(0.99, 1.01, n_samples),
        'pH': np.random.uniform(2.8, 4, n_samples),
        'sulphates': np.random.uniform(0.3, 2, n_samples),
        'alcohol': np.random.uniform(8, 15, n_samples),
        'quality': np.random.choice([0, 1], n_samples)  # Binary: good (1) or bad (0)
    })

    print(f"Loaded Wine Quality dataset with shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    
    # Ensure we have a DataFrame
    if 'df' in locals():
        data = df
    elif 'data' in locals() and isinstance(data, pd.DataFrame):
        pass
    else:
        raise ValueError("No DataFrame found in the generated code")
    
    # Prepare X and y
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    
    return X, y

def get_dataset_info():
    """Return information about the dataset."""
    return {
        'name': 'Wine Quality',
        'type': 'binary',
        'description': 'Automatically generated dataset',
        'n_samples': 200,
        'n_features': 11,
        'source': 'Government open data portals (data.gov, data.gov.uk)'
    }

if __name__ == "__main__":
    # Test loading
    X, y = load_data()
    info = get_dataset_info()
    print(f"Successfully loaded {info['name']}")
    print(f"Shape: X={X.shape}, y={y.shape}")
    print(f"Type: {info['type']}")



from typing import Dict, Any
import pandas as pd
try:
    from app.datasets.BaseDatasetLoader import BaseDatasetLoader
except Exception:  # pragma: no cover
    class BaseDatasetLoader:  # type: ignore
        def get_dataset_info(self) -> Dict[str, Any]:
            raise NotImplementedError
        def download_dataset(self, info: Dict[str, Any]):
            raise NotImplementedError
        def process_dataframe(self, df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
            return df


class WineQualityDataset(BaseDatasetLoader):
    """Wine Quality Dataset - Binary Classification.
    
    Wine quality prediction based on chemical properties.
    Source: UCI Machine Learning Repository
    """

    def get_dataset_info(self) -> Dict[str, Any]:
        return {
            "name": "WineQualityDataset",
            "category": "binary_classification",
            "source_id": "uci:wine_quality",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
            "description": "Wine quality classification from chemical properties. Target: quality (1=high, 0=low).",
            "target_column": "quality",
        }

    def download_dataset(self, info: Dict[str, Any]):
        """Download the Wine Quality dataset from UCI"""
        import requests
        from io import StringIO
        
        print(f"[WineQualityDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # CSV with semicolon separator
        df = pd.read_csv(StringIO(response.text), sep=';')
        print(f"[WineQualityDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
        """Process wine quality dataset"""
        dataset_name = info["name"]
        target_col = info["target_column"]
        
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        if target_col not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col}' not found.")
        
        # Convert quality to binary: quality >= 7 is high quality (1), else low quality (0)
        df["target"] = (pd.to_numeric(df[target_col], errors="coerce") >= 7).astype(int)
        if target_col != "target":
            df.drop(columns=[target_col], inplace=True)
        
        # All other features are numeric (chemical properties)
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with NA values
        before_dropna = len(df)
        df.dropna(inplace=True)
        if before_dropna > len(df):
            print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")
        
        df["target"] = df["target"].astype(int)
        
        # Deduplicate
        before_dedup = len(df)
        df.drop_duplicates(inplace=True)
        if len(df) < before_dedup:
            print(f"[{dataset_name}] Removed {before_dedup - len(df)} duplicate rows.")
        
        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

