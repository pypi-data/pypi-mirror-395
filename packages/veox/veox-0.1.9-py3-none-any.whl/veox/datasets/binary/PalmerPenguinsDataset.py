from typing import Dict, Any
import pandas as pd
import requests
from io import StringIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class PalmerPenguinsDataset(BaseDatasetLoader):
    """Palmer Penguins Dataset - Binary Classification.
    
    Physical measurements for three penguin species.
    Source: seaborn built-in dataset
    """

    def get_dataset_info(self) -> Dict[str, Any]:
        return {
            "name": "PalmerPenguinsDataset",
            "category": "binary_classification",
            "source_id": "seaborn:palmer_penguins",
            "description": "Physical measurements for three penguin species. Binary classification by sex.",
            "target_column": "sex",
        }

    def download_dataset(self, info: Dict[str, Any]):
        """Load Palmer Penguins dataset from seaborn"""
        dataset_name = info["name"]
        try:
            import seaborn as sns
            df = sns.load_dataset('penguins').dropna().reset_index(drop=True)
            print(f"[{dataset_name}] Loaded {df.shape[0]} rows from seaborn")
            return df.to_csv(index=False).encode('utf-8')
        except ImportError:
            # Fallback: try to download from alternative source
            print(f"[{dataset_name}] seaborn not available, trying GitHub...")
            url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
            print(f"[{dataset_name}] Loaded {df.shape[0]} rows from GitHub")
            return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
        """Process Palmer Penguins dataset"""
        dataset_name = info["name"]
        target_col = info["target_column"]
        
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Drop NA values first
        df = df.dropna().reset_index(drop=True)
        
        if target_col not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col}' not found.")
        
        # Convert sex to binary: Male=1, Female=0
        df["target"] = (df[target_col] == "Male").astype(int)
        if target_col != "target":
            df.drop(columns=[target_col], inplace=True)
        
        # Encode categorical columns (species, island)
        for col in df.columns:
            if col != "target" and df[col].dtype == 'object':
                df[col] = pd.Categorical(df[col]).codes
        
        # Ensure all columns are numeric
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
