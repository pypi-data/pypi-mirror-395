import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class GlassIdentificationDataset(BaseDatasetLoader):
    """Glass Identification Dataset (UCI) - Binary Classification Version.

    Real dataset for glass classification based on chemical composition.
    Original dataset has 7 glass types, converted to binary: window glass vs non-window glass.
    Features include oxide content (Na, Mg, Al, Si, K, Ca, Ba, Fe) and refractive index.
    Target: Glass type (1=window glass, 0=non-window glass).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data
    Original UCI: Glass Identification Dataset
    """

    def get_dataset_info(self):
        return {
            "name": "GlassIdentificationDataset",
            "source_id": "uci:glass_identification",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data",
            "category": "binary_classification",
            "description": "Glass identification from chemical composition. Target: glass type (1=window, 0=non-window).",
            "target_column": "Type",
        }
    
    def download_dataset(self, info):
        """Download the Glass Identification dataset from UCI"""
        print(f"[GlassIdentificationDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # The dataset has no header, comma-separated values
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), header=None)
        print(f"[GlassIdentificationDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The glass dataset has no header, assign column names
        expected_cols = ["Id", "RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "Type"]
        if df.shape[1] == len(expected_cols):
            df.columns = expected_cols
            print(f"[{dataset_name}] Assigned column names: {df.columns.tolist()}")
        
        # Drop ID column
        if "Id" in df.columns:
            df.drop(columns=["Id"], inplace=True)

        target_col_original = "Type"
        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Convert glass types to binary: 
        # Types 1-4 are window glass (1), Types 5-7 are non-window glass (0)
        window_glass_types = [1, 2, 3]  # Note: Type 4 doesn't exist in this dataset
        df["target"] = df[target_col_original].apply(lambda x: 1 if x in window_glass_types else 0)
        
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # All features are numeric
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
    ds = GlassIdentificationDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 