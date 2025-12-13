import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class PulsarStarsDataset(BaseDatasetLoader):
    """Pulsar Stars Dataset.

    Real dataset for pulsar star detection based on radio telescope observations.
    Dataset contains candidate pulsar signals with various statistical measures.
    Used in astronomy for automated pulsar detection from radio observations.
    Target: Pulsar class (1=pulsar, 0=not pulsar).
    
    Source: https://raw.githubusercontent.com/kanishksh4rma/predicting-a-pulsar-Star/master/pulsar_stars.csv
    Original: HTRU2 dataset from High Time Resolution Universe Survey
    """

    def get_dataset_info(self):
        return {
            "name": "PulsarStarsDataset",
            "source_id": "astronomy:pulsar_detection_htru2",
            "source_url": "https://raw.githubusercontent.com/kanishksh4rma/predicting-a-pulsar-Star/master/pulsar_stars.csv",
            "category": "binary_classification",
            "description": "Pulsar star detection from radio telescope data. Target: target_class (1=pulsar, 0=not pulsar).",
            "target_column": "target_class",
        }

    def download_dataset(self, info):
        """Override to implement fallback URLs"""
        dataset_name = info["name"]
        urls = [
            "https://raw.githubusercontent.com/kanishksh4rma/predicting-a-pulsar-Star/master/pulsar_stars.csv",
            "https://raw.githubusercontent.com/alexandrehsd/predicting-pulsar-stars/master/pulsar_stars.csv"
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

        # Check for different possible target column names
        possible_targets = ["target_class", "target", "class", "pulsar_class"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Target is already 0/1 (0=not pulsar, 1=pulsar)
        df["target"] = pd.to_numeric(df[actual_target], errors="coerce").astype(int)
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)
        
        # All other features are numeric (radio telescope measurements)
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
    ds = PulsarStarsDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 