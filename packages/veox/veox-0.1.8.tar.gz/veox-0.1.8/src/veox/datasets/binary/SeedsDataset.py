import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SeedsDataset(BaseDatasetLoader):
    """Seeds Dataset (UCI).

    Real dataset for seed classification based on geometric properties.
    Dataset contains wheat seeds from different varieties with measurements.
    Converted to binary: Kama wheat variety vs other varieties.
    Target: Seed variety (1=Kama variety, 0=other varieties).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt
    Original UCI: Seeds Dataset (Agriculture application)
    """

    def get_dataset_info(self):
        return {
            "name": "SeedsDataset",
            "source_id": "uci:seeds_wheat",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt",
            "category": "binary_classification",
            "description": "Wheat seeds classification from geometric properties. Target: variety (1=Kama, 0=other).",
            "target_column": "variety",
        }
    
    def download_dataset(self, info):
        """Download the Seeds dataset from UCI"""
        print(f"[SeedsDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # The dataset has no header, space-separated values
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), sep=r'\s+', header=None)
        print(f"[SeedsDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The seeds dataset has no header, assign column names
        if df.shape[1] == 8:
            df.columns = ["area", "perimeter", "compactness", "length_kernel", 
                         "width_kernel", "asymmetry_coefficient", "length_groove", "variety"]
            print(f"[{dataset_name}] Assigned column names: {df.columns.tolist()}")
        
        target_col_original = "variety"
        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Convert varieties to binary: 1 (Kama) vs 2,3 (Rosa, Canadian) -> 1 vs 0
        df["target"] = (pd.to_numeric(df[target_col_original], errors="coerce") == 1).astype(int)
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # All other features are numeric (geometric measurements)
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
    ds = SeedsDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 