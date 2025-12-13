import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class YeastDataset(BaseDatasetLoader):
    """Yeast Protein Localization Dataset (UCI).

    Real dataset for yeast protein localization classification.
    Dataset contains protein sequences with amino acid attributes and localization sites.
    Converted to binary: cytoplasm vs other cellular locations.
    Target: Protein localization (1=cytoplasm, 0=other locations).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/yeast/yeast.data
    Original UCI: Yeast Dataset (Biology/Protein Science application)
    """

    def get_dataset_info(self):
        return {
            "name": "YeastDataset",
            "source_id": "uci:yeast_protein_localization",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/yeast/yeast.data",
            "category": "binary_classification",
            "description": "Yeast protein localization from amino acid features. Target: localization (1=cytoplasm, 0=other).",
            "target_column": "localization",
        }
    
    def download_dataset(self, info):
        """Download the Yeast dataset from UCI"""
        print(f"[YeastDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # The dataset has no header, space-separated values
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), sep=r'\s+', header=None)
        print(f"[YeastDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The yeast dataset has no header, assign column names
        if df.shape[1] == 10:
            df.columns = ["sequence_name", "mcg", "gvh", "alm", "mit", "erl", "pox", "vac", "nuc", "localization"]
            print(f"[{dataset_name}] Assigned column names: {df.columns.tolist()}")
        
        # Drop sequence name column (identifier)
        if "sequence_name" in df.columns:
            df.drop(columns=["sequence_name"], inplace=True)
        
        target_col_original = "localization"
        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Convert localization to binary: CYT (cytoplasm) vs others
        df["target"] = (df[target_col_original] == "CYT").astype(int)
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # All other features are numeric (amino acid measurements)
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
    ds = YeastDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 