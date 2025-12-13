import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class CreditCardFraudDataset(BaseDatasetLoader):
    """Credit Card Fraud Detection dataset (Kaggle/TensorFlow mirror).

    Contains European credit card transactions from Sept 2013; 284,807 rows with 30 anonymised
    principal components and `Amount`, plus binary `Class` (1=fraud, 0=legit).
    """

    def get_dataset_info(self):
        return {
            "name": "CreditCardFraudDataset",
            "source_id": "kaggle:credit_card_fraud",  # unique id
            "category": "binary_classification",
            "description": "Credit card transaction dataset with fraud/non-fraud labels.",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        # Public mirror hosted by TensorFlow
        url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=60)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            if len(r.content) < 1000000:  # expect > 150 MB compressed ~68MB; but threshold small to detect error
                print(f"[{dataset_name}] Warning: file size only {len(r.content)} bytes – may be truncated.")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # Ensure Class column exists
        if "Class" not in df.columns:
            # Assume last column is target
            df.rename(columns={df.columns[-1]: "Class"}, inplace=True)
        # Map to target
        df["target"] = pd.to_numeric(df["Class"], errors="coerce").fillna(0).astype(int)
        df.drop(columns=["Class"], inplace=True)

        # Basic sanity: drop rows with NA
        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA values")

        # Reorder columns to put target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle sample (dataset large; shuffle full dataset)
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df


if __name__ == "__main__":
    d = CreditCardFraudDataset()
    df = d.get_data()
    print(df.shape, df['target'].value_counts()) 