import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class HeartAttackPredictionDataset(BaseDatasetLoader):
    """Heart Attack Prediction Dataset.

    Predicts the likelihood of a heart attack based on various medical factors.
    Target: 'output' (0 for less chance, 1 for more chance of heart attack).
    
    Source: Multiple working GitHub repositories with UCI heart disease dataset variations
    (Commonly used version, often based on UCI Statlog Heart Disease data but simplified).
    """

    def get_dataset_info(self):
        return {
            "name": "HeartAttackPredictionDataset",
            "source_id": "custom:heart_attack_prediction_simplified",
            "source_url": "github_multiple",  # Special marker for multiple GitHub sources
            "category": "binary_classification",
            "description": "Simplified heart attack prediction. Target: output (1=more chance, 0=less chance).",
            "target_column": "output",
        }

    def download_dataset(self, info):
        """Download from multiple working GitHub sources"""
        dataset_name = info["name"]
        
        # Multiple working GitHub URLs found during web search
        urls = [
            "https://raw.githubusercontent.com/murilommen/heart-disease-uci/master/heart.csv",
            "https://raw.githubusercontent.com/nmiuddin/UCI-Heart-Disease-Dataset/main/data/heart.csv",
            "https://raw.githubusercontent.com/EyalMichaeli/heart_disease_UCI/main/heart.csv",
            "https://raw.githubusercontent.com/maiya11/heart-disease/main/heart.csv",
            "https://raw.githubusercontent.com/rashida048/Datasets/master/heart.csv"
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
        possible_targets = ["output", "target", "num", "disease", "heart_disease"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Target conversion - handle different encoding schemes
        if actual_target != "target":
            # For heart disease datasets, targets are usually 0/1 or 0-4 (multiclass converted to binary)
            df["target"] = pd.to_numeric(df[actual_target], errors="coerce")
            # Convert to binary: 0 = no disease, >0 = disease present
            df["target"] = (df["target"] > 0).astype(int)
            df.drop(columns=[actual_target], inplace=True)
        else:
            df["target"] = pd.to_numeric(df["target"], errors="coerce").astype(int)
        
        # All other features are expected to be numeric.
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values (should be none if source is clean)
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
    ds = HeartAttackPredictionDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 