import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class OilSpillDetectionDataset(BaseDatasetLoader):
    """Oil Spill Detection dataset (binary classification).

    This dataset was developed by starting with satellite images of the ocean, 
    some of which contain an oil spill and some that do not. Images were split 
    into sections and processed using computer vision algorithms to provide a 
    vector of features to describe the contents of the image section or patch.

    The task is to predict whether a patch contains an oil spill or not 
    (from illegal or accidental dumping of oil in the ocean).

    937 instances with 49 features + binary target.
    
    Real-world oil industry dataset for environmental monitoring.
    
    Source: Oil Spill Detection from satellite imagery
    Link: https://raw.githubusercontent.com/avtnguyen/Oil-Spill-Detection-ML-Model/main/oil_spill.csv
    """

    def get_dataset_info(self):
        return {
            "name": "OilSpillDetectionDataset",
            "source_id": "satellite:oil_spill_detection",
            "source_url": "https://raw.githubusercontent.com/avtnguyen/Oil-Spill-Detection-ML-Model/main/oil_spill.csv",
            "category": "binary_classification",
            "description": "Oil Spill Detection dataset - predict oil spills from satellite image features.",
            "target_column": "target",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = info["source_url"]
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=60)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            # Expect ~232KB for this dataset
            if len(r.content) < 50000:
                preview = r.content[:500].decode("utf-8", errors="replace")
                print(f"[{dataset_name}] Warning: file might be small. Preview:\n{preview}")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The target column might be named differently
        target_candidates = ["target", "class", "label", "spill"]
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
                
        if target_col is None:
            # If no standard name found, assume last column is target
            target_col = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {target_col}")

        # Ensure the target column contains binary values
        if target_col != "target":
            df["target"] = pd.to_numeric(df[target_col], errors="coerce").fillna(0).astype(int)
            df.drop(columns=[target_col], inplace=True)
        else:
            df["target"] = pd.to_numeric(df["target"], errors="coerce").fillna(0).astype(int)

        # Convert all feature columns to numeric 
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows with any NA values
        before = len(df)
        df.dropna(inplace=True)
        dropped = before - len(df)
        print(f"[{dataset_name}] Dropped {dropped} rows with NA values")

        # Deduplicate
        before = len(df)
        df.drop_duplicates(inplace=True)
        dups = before - len(df)
        if dups:
            print(f"[{dataset_name}] Removed {dups} duplicate rows")

        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

if __name__ == "__main__":
    ds = OilSpillDetectionDataset()
    frame = ds.get_data()
    print(frame.head()) 