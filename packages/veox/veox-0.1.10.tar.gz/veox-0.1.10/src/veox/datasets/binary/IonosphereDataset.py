import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class IonosphereDataset(BaseDatasetLoader):
    """UCI Ionosphere dataset (binary classification).

    Radar data collected by a system in Goose Bay, Labrador. 
    Task: Classify radar returns from the ionosphere as "good" or "bad".
    351 instances, 34 continuous attributes, binary target.
    Source: https://archive.ics.uci.edu/ml/datasets/Ionosphere
    """

    def get_dataset_info(self):
        return {
            "name": "IonosphereDataset",
            "source_id": "uci:ionosphere",
            "category": "binary_classification",
            "description": "Ionosphere radar returns dataset. Binary classification of signal quality.",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/ionosphere/ionosphere.data"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 10000:  # Expect ~90KB
                preview = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. Preview:\n" + os.linesep.join(preview))
                raise RuntimeError(f"Downloaded file too small: {file_size} bytes")
                
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        
        # The ionosphere.data file has no header
        # 34 numeric attributes + 1 class label (g=good, b=bad)
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Always assign column names (no header in raw file)
        expected_cols = 35  # 34 features + 1 target
        if df.shape[1] != expected_cols:
            print(f"[{dataset_name}] Warning: expected {expected_cols} columns, got {df.shape[1]}")
            if df.shape[1] > expected_cols:
                df = df.iloc[:, :expected_cols]
            else:
                # Pad with NaN if needed
                for _ in range(expected_cols - df.shape[1]):
                    df[df.shape[1]] = pd.NA
        
        # Assign column names
        feature_cols = [f"attr_{i}" for i in range(1, 35)]
        df.columns = feature_cols + ["class_label"]
        
        # Convert class_label to binary target
        # g (good) -> 1, b (bad) -> 0
        df["target"] = df["class_label"].map({"g": 1, "b": 0})
        
        # Handle any unmapped values
        if df["target"].isna().any():
            print(f"[{dataset_name}] Warning: Found unmapped class labels")
            df["target"].fillna(0, inplace=True)
            
        df.drop(columns=["class_label"], inplace=True)
        
        # Convert all feature columns to numeric
        for col in feature_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Drop rows with any NA
        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA values")
        
        # Ensure target is integer
        df["target"] = df["target"].astype(int)
        
        # Reorder columns so target is last
        df = df[feature_cols + ["target"]]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        
        return df


if __name__ == "__main__":
    dataset = IonosphereDataset()
    df = dataset.get_data()
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns") 