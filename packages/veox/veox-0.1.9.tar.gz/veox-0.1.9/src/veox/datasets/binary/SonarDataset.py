import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class SonarDataset(BaseDatasetLoader):
    """UCI Sonar (Mines vs. Rocks) dataset (binary classification).

    Sonar signals bounced off metal cylinders (mines) and rocks.
    Task: Classify objects as either mines (M) or rocks (R).
    208 instances, 60 continuous attributes (energy values at different frequencies).
    Source: https://archive.ics.uci.edu/ml/datasets/Connectionist+Bench+(Sonar,+Mines+vs.+Rocks)
    """

    def get_dataset_info(self):
        return {
            "name": "SonarDataset",
            "source_id": "uci:sonar_mines_rocks",
            "category": "binary_classification",
            "description": "Sonar signals dataset. Binary classification of mines vs rocks.",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 20000:  # Expect ~80KB
                preview = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. Preview:\n" + os.linesep.join(preview))
                raise RuntimeError(f"Downloaded file too small: {file_size} bytes")
                
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        
        # The sonar.all-data file has no header
        # 60 numeric attributes + 1 class label (M=mine, R=rock)
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Always assign column names (no header in raw file)
        expected_cols = 61  # 60 features + 1 target
        if df.shape[1] != expected_cols:
            print(f"[{dataset_name}] Warning: expected {expected_cols} columns, got {df.shape[1]}")
            if df.shape[1] > expected_cols:
                df = df.iloc[:, :expected_cols]
            else:
                # Pad with NaN if needed
                for _ in range(expected_cols - df.shape[1]):
                    df[df.shape[1]] = pd.NA
        
        # Assign column names
        feature_cols = [f"freq_{i}" for i in range(1, 61)]
        df.columns = feature_cols + ["class_label"]
        
        # Convert class_label to binary target
        # M (mine) -> 1, R (rock) -> 0
        df["target"] = df["class_label"].map({"M": 1, "R": 0})
        
        # Handle any unmapped values
        if df["target"].isna().any():
            print(f"[{dataset_name}] Warning: Found unmapped class labels")
            # Check what the actual values are
            unique_labels = df["class_label"].unique()
            print(f"[{dataset_name}] Unique class labels found: {unique_labels}")
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
    dataset = SonarDataset()
    df = dataset.get_data()
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns") 