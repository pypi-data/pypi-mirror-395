import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WaterPotabilityDataset(BaseDatasetLoader):
    """Water Potability Dataset.

    Predicts water potability (safe to drink or not) based on various
    water quality metrics like pH, hardness, solids, etc.
    Target: 'Potability' (1 indicates potable, 0 indicates not potable).
    
    Source: https://raw.githubusercontent.com/NaNdalal-dev/water-potability/main/water_potability.csv
    (Alternative: https://raw.githubusercontent.com/ervikashgoyal/waterPotaabliityML/main/water_potability.csv)
    """

    def get_dataset_info(self):
        return {
            "name": "WaterPotabilityDataset",
            "source_id": "custom:water_potability",
            "source_url": "https://raw.githubusercontent.com/NaNdalal-dev/water-potability/main/water_potability.csv",
            "category": "binary_classification",
            "description": "Water potability prediction. Target: Potability (1=potable, 0=not potable).",
            "target_column": "Potability",
        }

    def download_dataset(self, info):
        """Override to implement fallback URLs"""
        dataset_name = info["name"]
        urls = [
            "https://raw.githubusercontent.com/NaNdalal-dev/water-potability/main/water_potability.csv",
            "https://raw.githubusercontent.com/ervikashgoyal/waterPotaabliityML/main/water_potability.csv"
        ]
        
        for i, url in enumerate(urls):
            try:
                print(f"[{dataset_name}] Trying URL {i+1}: {url}")
                r = requests.get(url, timeout=30)
                print(f"[{dataset_name}] HTTP {r.status_code}")
                if r.status_code == 200:
                    print(f"[{dataset_name}] Successfully downloaded from URL {i+1}")
                    return r.content
            except Exception as e:
                print(f"[{dataset_name}] URL {i+1} failed: {e}")
                continue
        
        raise RuntimeError(f"[{dataset_name}] All download URLs failed")

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Target is already 0/1
        df["target"] = pd.to_numeric(df[target_col_original], errors="coerce").astype(int)
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # All other features are expected to be numeric.
        # Convert all feature columns to numeric, coercing errors.
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # This dataset has missing values that should be handled.
        # For this basic loader, we will drop rows with any NaNs.
        before_dropna = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")
        df["target"] = df["target"].astype(int) # Ensure target is int after dropna

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
    ds = WaterPotabilityDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 