import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class TelcoCustomerChurnDataset(BaseDatasetLoader):
    """Telco Customer Churn dataset (binary classification).

    Source: IBM Sample Data Sets – Telco Customer Churn.
    Link used: https://raw.githubusercontent.com/blastchar/telco-customer-churn/master/Telco-Customer-Churn.csv

    7,043 customer records with demographic & usage features, target `Churn` (Yes/No).
    The goal is to predict whether a customer will churn.
    """

    def get_dataset_info(self):
        return {
            "name": "TelcoCustomerChurnDataset",
            "source_id": "ibm:telco_customer_churn",
            "source_url": "https://raw.githubusercontent.com/Argetlam84/Telco_Customer_Churn/main/Telco-Customer-Churn.csv",
            "category": "binary_classification",
            "description": "Predict telco customer churn based on service & demographic features.",
            "target_column": "Churn",
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
            if len(r.content) < 100000:
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
        if "Churn" not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected 'Churn' column not found in columns: {df.columns.tolist()}")

        # Map Churn Yes/No to 1/0
        df["target"] = df["Churn"].map({"Yes": 1, "No": 0}).astype(int)
        df.drop(columns=["Churn"], inplace=True)

        # Convert TotalCharges to numeric (it has spaces for missing values)
        if "TotalCharges" in df.columns:
            df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

        # Drop customerID if it exists (it's just an identifier)
        if "customerID" in df.columns:
            print(f"[{dataset_name}] Dropping 'customerID' column")
            df.drop(columns=["customerID"], inplace=True)

        # Convert categorical columns to numeric
        print(f"[{dataset_name}] Converting categorical columns to numeric...")
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                # Binary yes/no columns
                if df[col].nunique() == 2:
                    unique_vals = df[col].unique()
                    if 'Yes' in unique_vals and 'No' in unique_vals:
                        df[col] = df[col].map({'Yes': 1, 'No': 0})
                        print(f"  - Converted {col} (Yes/No) to binary")
                    else:
                        # Other binary columns
                        df[col] = pd.Categorical(df[col]).codes
                        print(f"  - Encoded {col} (binary)")
                else:
                    # Multi-category columns
                    df[col] = pd.Categorical(df[col]).codes
                    print(f"  - Encoded {col} (multi-category)")

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
    ds = TelcoCustomerChurnDataset()
    frame = ds.get_data()
    print(frame.head()) 