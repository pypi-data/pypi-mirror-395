import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class DiabeticRetinopathyDebrecenDataset(BaseDatasetLoader):
    """Diabetic Retinopathy Debrecen Dataset (UCI).

    Features extracted from the Messidor image set to predict whether an image 
    contains signs of diabetic retinopathy or not.
    Target: 'Class' (1=retinopathy, 0=no retinopathy).
    
    Source: UCI repository via ucimlrepo package with GitHub fallbacks
    Original UCI: https://archive.ics.uci.edu/ml/datasets/Diabetic+Retinopathy+Debrecen+Data+Set
    """

    def get_dataset_info(self):
        return {
            "name": "DiabeticRetinopathyDebrecenDataset",
            "source_id": "uci:diabetic_retinopathy_debrecen",
            "source_url": "uci_repo",  # Special marker for UCI repo
            "category": "binary_classification",
            "description": "Diabetic retinopathy prediction. Target: Class (1=retinopathy, 0=no retinopathy).",
            "target_column": "Class",
        }

    def download_dataset(self, info):
        """Download from UCI repository via ucimlrepo or fallback URLs"""
        dataset_name = info["name"]
        
        # Try ucimlrepo first
        try:
            print(f"[{dataset_name}] Attempting to fetch from UCI repository using ucimlrepo...")
            try:
                from ucimlrepo import fetch_ucirepo
                diabetic_retinopathy = fetch_ucirepo(id=329)  # Diabetic Retinopathy Debrecen dataset
                X = diabetic_retinopathy.data.features
                y = diabetic_retinopathy.data.targets
                df = pd.concat([X, y], axis=1)
                import io
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                print(f"[{dataset_name}] Successfully downloaded from UCI via ucimlrepo")
                return csv_buffer.getvalue().encode('utf-8')
            except ImportError:
                print(f"[{dataset_name}] ucimlrepo not available, trying direct URLs...")
        except Exception as e:
            print(f"[{dataset_name}] UCI repository failed: {e}")
        
        # Fallback URLs from GitHub repositories
        fallback_urls = [
            "https://raw.githubusercontent.com/Ashishsharma-12/Diabetic-Retinopathy-Debrecen-DS/main/Diabetic%20Retinopathy%20Debrecen.csv",
            "https://raw.githubusercontent.com/munibas/Diabetic_Retinopathy/main/train.csv",
            "https://raw.githubusercontent.com/datasets/diabetic-retinopathy/main/messidor_features.csv"
        ]
        
        for i, url in enumerate(fallback_urls):
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
        possible_targets = ["Class", "target", "label", "diagnosis", "result"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Target is already 0/1
        df["target"] = pd.to_numeric(df[actual_target], errors="coerce")
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)
        
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
    ds = DiabeticRetinopathyDebrecenDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 