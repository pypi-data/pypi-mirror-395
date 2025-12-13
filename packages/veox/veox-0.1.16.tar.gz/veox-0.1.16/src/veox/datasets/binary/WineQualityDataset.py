import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WineQualityDataset(BaseDatasetLoader):
    """Wine Quality Dataset (UCI).

    Real dataset for wine quality classification based on physicochemical properties.
    Dataset contains wine samples with chemical analysis and quality ratings.
    Converted to binary: high quality (>=7) vs low quality (<7).
    Target: Quality rating (1=high quality, 0=low quality).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
    Original UCI: Wine Quality Dataset (Food Science application)
    """

    def get_dataset_info(self):
        return {
            "name": "WineQualityDataset",
            "source_id": "uci:wine_quality_red",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
            "category": "binary_classification",
            "description": "Wine quality classification from chemical properties. Target: quality (1=high, 0=low).",
            "target_column": "quality",
        }
    
    def download_dataset(self, info):
        """Download the Wine Quality dataset from UCI"""
        print(f"[WineQualityDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # CSV with header
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), sep=';')
        print(f"[WineQualityDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Convert quality to binary: quality >= 7 is high quality (1), else low quality (0)
        df["target"] = (pd.to_numeric(df[target_col_original], errors="coerce") >= 7).astype(int)
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
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

if __name__ == "__main__":
    ds = WineQualityDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 