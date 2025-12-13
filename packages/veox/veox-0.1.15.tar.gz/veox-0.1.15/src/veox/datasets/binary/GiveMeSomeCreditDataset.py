import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class GiveMeSomeCreditDataset(BaseDatasetLoader):
    """Give Me Some Credit (Kaggle) – credit risk dataset.

    Predicts whether an individual will experience serious financial distress within 2 years.
    Target: SeriousDlqin2yrs (1=distress, 0=no distress).

    Source: https://raw.githubusercontent.com/JLZml/Credit-Scoring-Data-Sets/master/3.%20Kaggle/Give%20Me%20Some%20Credit/cs-training.csv
    """

    def get_dataset_info(self):
        return {
            "name": "GiveMeSomeCreditDataset",
            "source_id": "kaggle:give_me_some_credit",
            "source_url": "https://raw.githubusercontent.com/JLZml/Credit-Scoring-Data-Sets/master/3.%20Kaggle/Give%20Me%20Some%20Credit/cs-training.csv",
            "category": "binary_classification",
            "description": "Predict severe credit distress within 2 years. Target: SeriousDlqin2yrs (1/0).",
            "target_column": "SeriousDlqin2yrs",
        }
    
    def download_dataset(self, info):
        """Download the Give Me Some Credit dataset"""
        print(f"[GiveMeSomeCreditDataset] Downloading from GitHub...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # CSV with header
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        print(f"[GiveMeSomeCreditDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # Drop first unnamed index column if present
        if df.columns[0].lower().startswith("unnamed"):
            df.drop(columns=[df.columns[0]], inplace=True)

        if target_col not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col}' not found.")

        df["target"] = pd.to_numeric(df[target_col], errors="coerce").astype(int)
        if target_col != "target":
            df.drop(columns=[target_col], inplace=True)

        # Convert remaining columns to numeric
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors="coerce")

        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA values")

        df.drop_duplicates(inplace=True)
        df = df[[c for c in df.columns if c != "target"] + ["target"]]
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

if __name__ == "__main__":
    d = GiveMeSomeCreditDataset()
    d.get_data() 