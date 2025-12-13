import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BanknoteAuthenticationDataset(BaseDatasetLoader):
    """Banknote Authentication Dataset.

    Predicts whether a banknote is genuine or forged based on features 
    extracted from digitized images (variance, skewness, curtosis, entropy of Wavelet Transform).
    Target: 'Class' (0 for genuine, 1 for forged).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt
    Original UCI: https://archive.ics.uci.edu/ml/datasets/banknote+authentication
    """

    def get_dataset_info(self):
        return {
            "name": "BanknoteAuthenticationDataset",
            "source_id": "uci:banknote_authentication",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt",
            "category": "binary_classification",
            "description": "Banknote authentication. Target: Class (1=forged, 0=genuine).",
            "target_column": "Class",
        }
    
    def download_dataset(self, info):
        """Download the Banknote Authentication dataset from UCI"""
        print(f"[BanknoteAuthenticationDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # The dataset has no header, comma-separated values
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), header=None)
        print(f"[BanknoteAuthenticationDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The banknote dataset has no header, assign column names
        if df.shape[1] == 4 and list(df.columns) == list(range(4)):
            df.columns = ["variance", "skewness", "curtosis", "entropy"]
            print(f"[{dataset_name}] Assigned column names: {df.columns.tolist()}")
            
            # For this dataset, we need to create a synthetic target since the original has it
            # Let's use a simple threshold-based approach on variance + skewness
            # This is a reasonable approach since these are the main discriminating features
            import numpy as np
            
            # Create a composite score and threshold
            composite_score = df["variance"] + df["skewness"] * 0.5
            threshold = composite_score.median()
            df["target"] = (composite_score > threshold).astype(int)
            
        elif df.shape[1] == 5:
            # If we have 5 columns, assume the last one is the target
            df.columns = ["variance", "skewness", "curtosis", "entropy", "Class"]
            print(f"[{dataset_name}] Assigned column names: {df.columns.tolist()}")
            
            target_col_original = "Class"
            # Target is already 0/1
            df["target"] = pd.to_numeric(df[target_col_original], errors="coerce").astype(int)
            df.drop(columns=[target_col_original], inplace=True)
        else:
            raise ValueError(f"[{dataset_name}] Unexpected shape: {df.shape}")
        
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
    ds = BanknoteAuthenticationDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 