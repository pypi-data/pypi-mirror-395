import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class GermanCreditRiskDataset(BaseDatasetLoader):
    """German Credit Risk dataset (binary classification).

    Dataset contains 1,000 entries with 20 categorical/symbolic attributes 
    from Prof. Hofmann. Each entry represents a person who takes a credit 
    from a bank. Each person is classified as either a good or bad credit 
    risk depending on a set of attributes.

    Real-world banking industry dataset for credit risk assessment.
    
    Source: German Credit Risk dataset, originally from UCI repository
    Link: https://raw.githubusercontent.com/ziadasal/Credit-Risk-Assessment/main/german_credit_data.csv
    """

    def get_dataset_info(self):
        return {
            "name": "GermanCreditRiskDataset",
            "source_id": "german:credit_risk_assessment",
            "source_url": "https://raw.githubusercontent.com/ziadasal/Credit-Risk-Assessment/main/german_credit_data.csv",
            "category": "binary_classification",
            "description": "German Credit Risk dataset - predict good/bad credit risk for banking customers.",
            "target_column": "Risk",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = info["source_url"]
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=60)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            # Expect ~50KB for this dataset
            if len(r.content) < 10000:
                preview = r.content[:500].decode("utf-8", errors="replace")
                print(f"[{dataset_name}] Warning: file might be small. Preview:\n{preview}")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # Ensure target column exists
        if "Risk" not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected 'Risk' column not found in columns: {df.columns.tolist()}")

        # Map Risk column to binary target: 0=good, 1=bad
        risk_map = {"good": 0, "bad": 1}
        df["target"] = df["Risk"].map(risk_map)
        
        # Handle any unmapped values
        if df["target"].isna().any():
            print(f"[{dataset_name}] Warning: Found unmapped risk values, filling with 0")
            df["target"].fillna(0, inplace=True)
            
        df["target"] = df["target"].astype(int)
        df.drop(columns=["Risk"], inplace=True)

        # Convert categorical columns to numeric
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                # Handle missing values before encoding
                df[col] = df[col].fillna('Unknown')
                # Use label encoding
                df[col] = pd.Categorical(df[col]).codes

        # Convert all int8 columns to int64
        for col in df.columns:
            if df[col].dtype == 'int8':
                df[col] = df[col].astype('int64')

        # Drop rows with any NA values
        before = len(df)
        df.dropna(inplace=True)
        dropped = before - len(df)
        print(f"[{dataset_name}] Dropped {dropped} rows with NA values")

        # Deduplicate
        before = len(df)
        df.drop_duplicates(inplace=True)
        dups = before - len(df)
        if dups:
            print(f"[{dataset_name}] Removed {dups} duplicate rows")

        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

if __name__ == "__main__":
    ds = GermanCreditRiskDataset()
    frame = ds.get_data()
    print(frame.head()) 