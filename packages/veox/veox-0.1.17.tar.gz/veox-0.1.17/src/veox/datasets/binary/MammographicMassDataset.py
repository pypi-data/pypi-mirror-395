import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class MammographicMassDataset(BaseDatasetLoader):
    """UCI Mammographic Mass dataset (binary classification).

    961 mammography cases with BI-RADS attributes; target column 'Severity' (0 benign, 1 malignant).
    Source: https://archive.ics.uci.edu/ml/datasets/Mammographic+Mass
    """

    def get_dataset_info(self):
        return {
            "name": "MammographicMassDataset",
            "source_id": "uci:mammographic_mass",
            "category": "binary_classification",
            "description": "Mammographic mass dataset – predict tumor severity (benign/malignant).",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mammographic-masses/mammographic_masses.data"
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=30)
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        expected_cols = [
            "BI-RADS",
            "Age",
            "Shape",
            "Margin",
            "Density",
            "Severity",
        ]
        if df.shape[1] != 6:
            if df.shape[1] > 6:
                df = df.iloc[:, :6]
            else:
                for _ in range(6 - df.shape[1]):
                    df[df.shape[1]] = pd.NA
        df.columns = expected_cols

        df.replace("?", pd.NA, inplace=True)
        for col in expected_cols[:-1]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["target"] = pd.to_numeric(df["Severity"], errors="coerce")
        df.drop(columns=["Severity"], inplace=True)

        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA")

        df = df[[c for c in df.columns if c != "target"] + ["target"]]
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df


if __name__ == "__main__":
    d = MammographicMassDataset()
    df = d.get_data()
    print(df.shape, df['target'].value_counts()) 