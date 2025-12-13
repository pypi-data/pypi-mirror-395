import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class AustralianCreditApprovalDataset(BaseDatasetLoader):
    """Australian Credit Approval Dataset.

    Credit screening dataset from an Australian bank. All attribute names and 
    values have been anonymized for privacy protection.
    Features include various financial and personal attributes for credit assessment.
    Target: Credit approval decision (1=approved, 0=rejected).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/australian/australian.dat
    Original UCI: https://archive.ics.uci.edu/ml/datasets/Statlog+%28Australian+Credit+Approval%29
    """

    def get_dataset_info(self):
        return {
            "name": "AustralianCreditApprovalDataset",
            "source_id": "uci:australian_credit_approval",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/australian/australian.dat",
            "category": "binary_classification",
            "description": "Australian credit approval decisions. Target: approval (1=approved, 0=rejected).",
            "target_column": "A15",
        }
    
    def download_dataset(self, info):
        """Download the Australian Credit Approval dataset from UCI"""
        print(f"[AustralianCreditApprovalDataset] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # The dataset has no header, space-separated values
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), sep=r'\s+', header=None)
        print(f"[AustralianCreditApprovalDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The Australian dataset has no header, assign column names
        if df.shape[1] == 15:
            df.columns = [f"A{i}" for i in range(1, 16)]
            print(f"[{dataset_name}] Assigned column names A1-A15")
        
        target_col_original = info["target_column"]
        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Target is +/- mapped to 1/0
        df["target"] = df[target_col_original].map({"+": 1, "-": 0, "1": 1, "0": 0, 1: 1, 0: 0})
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # Convert numeric feature columns to numeric, coercing errors
        # Features A2, A3, A7, A10, A13, A14 are continuous
        numeric_cols = ["A2", "A3", "A7", "A10", "A13", "A14"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values (especially if target mapping failed)
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
    ds = AustralianCreditApprovalDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 