import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ForestFiresDataset(BaseDatasetLoader):
    """Forest Fires Dataset (UCI) - Binary Classification Version.

    Real dataset for forest fire occurrence prediction based on meteorological data.
    Original dataset predicts burned area, converted to binary: fire occurrence vs no fire.
    Features include weather conditions (temp, humidity, wind, rain) and fire weather indices.
    Target: Fire occurrence (1=fire occurred, 0=no fire).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv
    Original UCI: Forest Fires Dataset
    """

    def get_dataset_info(self):
        return {
            "name": "ForestFiresDataset",
            "source_id": "uci:forest_fires",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv",
            "category": "binary_classification",
            "description": "Forest fire occurrence prediction from meteorological data. Target: fire (1=fire, 0=no fire).",
            "target_column": "area",
        }
    
    def download_dataset(self, info):
        """Download the Forest Fires dataset from UCI"""
        print(f"[ForestFiresDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # CSV with header
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        print(f"[ForestFiresDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Convert burned area to binary: area > 0 means fire occurred (1), area = 0 means no fire (0)
        df["target"] = (pd.to_numeric(df[target_col_original], errors="coerce") > 0).astype(int)
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # Drop non-numeric categorical columns (month, day)
        categorical_cols = ["month", "day"]
        for col in categorical_cols:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)
        
        # Convert all remaining feature columns to numeric
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
    ds = ForestFiresDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 