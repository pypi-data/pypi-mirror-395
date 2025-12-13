import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ClimateModelCrashDataset(BaseDatasetLoader):
    """Climate Model Simulation Crashes Dataset.

    Predicts whether a climate model simulation will crash (fail) or succeed 
    based on various input parameters of the simulation.
    Target: 'outcome' (0 for success, 1 for failure/crash).
    
    Source: UCI repository via ucimlrepo package with GitHub fallbacks
    Original UCI: https://archive.ics.uci.edu/ml/datasets/climate+model+simulation+crashes
    """

    def get_dataset_info(self):
        return {
            "name": "ClimateModelCrashDataset",
            "source_id": "uci:climate_model_simulation_crashes",
            "source_url": "uci_repo",  # Special marker for UCI repo
            "category": "binary_classification",
            "description": "Climate model simulation crash prediction. Target: outcome (1=fail, 0=success).",
            "target_column": "outcome",
        }

    def download_dataset(self, info):
        """Download from UCI repository via ucimlrepo or fallback URLs"""
        dataset_name = info["name"]
        
        # Try ucimlrepo first
        try:
            print(f"[{dataset_name}] Attempting to fetch from UCI repository using ucimlrepo...")
            try:
                from ucimlrepo import fetch_ucirepo
                climate_model = fetch_ucirepo(id=252)  # Climate Model Simulation Crashes dataset
                X = climate_model.data.features
                y = climate_model.data.targets
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
            "https://raw.githubusercontent.com/kunal2712/CMScrashes/main/crashesdata.csv",
            "https://raw.githubusercontent.com/juschan/ml_climatemodelsim/master/pop_failures.dat"
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
        possible_targets = ["outcome", "target", "result", "success", "failure"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Target is already 0/1 (0=failure, 1=success) - convert to 0=success, 1=failure
        df["target"] = pd.to_numeric(df[actual_target], errors="coerce")
        # Invert if needed: original has 1=success, 0=failure; we want 1=failure, 0=success
        df["target"] = 1 - df["target"]
        df["target"] = df["target"].astype(int)
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)
        
        # Drop some less useful/identifier columns if they exist
        cols_to_drop = ['Study', 'Run'] 
        for col_drop in cols_to_drop:
            if col_drop in df.columns:
                df.drop(columns=[col_drop], inplace=True)

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
    ds = ClimateModelCrashDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 