import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class HeartFailureDataset(BaseDatasetLoader):
    """Heart Failure Clinical Records dataset (binary classification).

    299 patients, 12 clinical features; target `DEATH_EVENT` (0/1).
    Source: https://archive.ics.uci.edu/ml/datasets/Heart+failure+clinical+records
    """

    def get_dataset_info(self):
        return {
            "name": "HeartFailureDataset",
            "source_id": "uci:heart_failure_clinical",
            "category": "binary_classification",
            "description": "Heart failure clinical records – predict death event.",
        }

    def download_dataset(self, info):
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00519/heart_failure_clinical_records_dataset.csv"
        print("[HeartFailureDataset] Downloading CSV")
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}")
        return r.content

    def process_dataframe(self, df, info):
        print(f"[HeartFailureDataset] Raw shape: {df.shape}")
        if "DEATH_EVENT" not in df.columns:
            df.columns = list(df.columns[:-1]) + ["DEATH_EVENT"]
        df["target"] = pd.to_numeric(df["DEATH_EVENT"], errors="coerce").astype(int)
        df.drop(columns=["DEATH_EVENT"], inplace=True)
        for col in df.columns.difference(["target"]):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df.dropna(inplace=True)
        df = df[[c for c in df.columns if c != "target"] + ["target"]]
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[HeartFailureDataset] Final shape: {df.shape}")
        return df


if __name__ == "__main__":
    print(HeartFailureDataset().get_data().head()) 