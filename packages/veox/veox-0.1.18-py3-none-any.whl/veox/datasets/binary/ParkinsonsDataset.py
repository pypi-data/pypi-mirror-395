import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class ParkinsonsDataset(BaseDatasetLoader):
    """UCI Parkinsons Telemonitoring dataset (binary classification).

    Original dataset: 195 voice recordings of 31 individuals, each classified as
    Parkinson's disease or healthy. 22 biomedical voice measures + status.
    Source URL: https://archive.ics.uci.edu/ml/datasets/parkinsons
    """

    def get_dataset_info(self):
        return {
            "name": "ParkinsonsDataset",
            "source_id": "uci:parkinsons",  # unique id for hash/caching
            "category": "binary_classification",
            "description": "Parkinsons voice measurement dataset – predict disease status (0/1).",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data"
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            if len(r.content) < 5000:
                preview = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print("Preview:\n" + os.linesep.join(preview))
                raise RuntimeError("Downloaded file too small – may be incorrect.")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The downloaded CSV includes a header. Ensure 'status' exists.
        if "status" not in df.columns:
            # If not, assume last column is status.
            df.rename(columns={df.columns[-1]: "status"}, inplace=True)

        # Move status to binary target
        df["target"] = pd.to_numeric(df["status"], errors="coerce").fillna(0).astype(int)
        df.drop(columns=["status"], inplace=True)

        # Drop the 'name' column if it exists (it's a patient identifier, not a feature)
        if "name" in df.columns:
            print(f"[{dataset_name}] Dropping 'name' column (patient identifier)")
            df.drop(columns=["name"], inplace=True)

        # Convert any remaining non-numeric columns
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                print(f"[{dataset_name}] Warning: non-numeric column '{col}' found, attempting to convert")
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with any NA values (should be none)
        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA values")

        # Reorder so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df


if __name__ == "__main__":
    d = ParkinsonsDataset()
    df = d.get_data()
    print(df.shape, df['target'].value_counts()) 