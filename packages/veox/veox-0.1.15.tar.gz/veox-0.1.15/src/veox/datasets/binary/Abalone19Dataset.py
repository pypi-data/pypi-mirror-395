import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class Abalone19Dataset(BaseDatasetLoader):
    """
    Abalone19 binary dataset.
    Binary classification: rings == 19 (1) vs others (0)
    ~4177 instances, 8 features after preprocessing
    Source: Derived from UCI Abalone dataset; simple preprocessing here emulates '19 vs rest'.
    """

    def get_dataset_info(self):
        return {
            "name": "Abalone19Dataset",
            "source_id": "uci:abalone_19_vs_rest",
            "category": "binary_classification",
            "description": "Abalone dataset transformed to 19-rings vs rest binary classification.",
        }

    def download_dataset(self, info):
        # Raw abalone dataset (no header) from UCI mirror
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"
        session = requests.Session()
        session.trust_env = False
        r = session.get(url, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code} while downloading {url}")
        cols = [
            "sex",
            "length",
            "diameter",
            "height",
            "whole_weight",
            "shucked_weight",
            "viscera_weight",
            "shell_weight",
            "rings",
        ]
        import io
        df = pd.read_csv(io.BytesIO(r.content), header=None, names=cols)
        return df

    def process_dataframe(self, df: pd.DataFrame, info):
        # Build binary target for rings==19
        df["target"] = (df["rings"].astype(int) == 19).astype(int)
        # Drop original target
        df = df.drop(columns=["rings"])
        
        # Encode categorical 'sex' column before model training
        if "sex" in df.columns:
            # Convert M/F/I to numeric codes
            df["sex"] = pd.Categorical(df["sex"]).codes
        
        # Ensure all columns are numeric
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with NA values
        df = df.dropna()
        
        # Ensure target last
        cols = [c for c in df.columns if c != "target"] + ["target"]
        df = df[cols]
        return df


