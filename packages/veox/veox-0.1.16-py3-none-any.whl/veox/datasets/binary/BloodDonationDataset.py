import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class BloodDonationDataset(BaseDatasetLoader):
    """UCI Blood Transfusion Service Center dataset (binary classification).

    Predict whether a blood donor donated in March 2007.
    748 instances, 4 numeric features + binary target.
    Source: https://archive.ics.uci.edu/ml/datasets/Blood+Transfusion+Service+Center
    """

    def get_dataset_info(self):
        return {
            "name": "BloodDonationDataset",
            "source_id": "uci:blood_transfusion",
            "category": "binary_classification",
            "description": "Blood donation dataset – predict donation in March 2007 (yes/no).",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/blood-transfusion/transfusion.data"
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            if len(r.content) < 5000:  # Expect ~30 KB
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

        # Ensure header is present; if pandas considered first row header incorrectly, fix it
        expected_cols = [
            "recency_months",
            "frequency_times",
            "monetary_cc",
            "time_months",
            "donated_march_2007",
        ]
        if list(df.columns) != expected_cols:
            # Assume no header present, assign
            if df.shape[1] == 5:
                df.columns = expected_cols
            else:
                # Coerce to 5 columns
                if df.shape[1] > 5:
                    df = df.iloc[:, :5]
                else:
                    for _ in range(5 - df.shape[1]):
                        df[df.shape[1]] = pd.NA
                df.columns = expected_cols

        # Convert target column to int and rename to target
        df["target"] = pd.to_numeric(df["donated_march_2007"], errors="coerce").fillna(0).astype(int)
        df.drop(columns=["donated_march_2007"], inplace=True)

        # Drop NA rows
        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA values")

        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df


if __name__ == "__main__":
    d = BloodDonationDataset()
    df = d.get_data()
    print(df.shape, df['target'].value_counts()) 