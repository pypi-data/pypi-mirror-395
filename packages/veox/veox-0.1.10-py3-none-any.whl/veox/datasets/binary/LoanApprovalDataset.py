import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class LoanApprovalDataset(BaseDatasetLoader):
    """Loan Approval Prediction Dataset.

    Predicts loan approval based on customer details like gender, marital status, 
    education, income, loan amount, credit history etc.
    Target: 'Loan_Status' (Y=1, N=0).
    
    Source: Multiple working GitHub repositories with Analytics Vidhya loan dataset
    """

    def get_dataset_info(self):
        return {
            "name": "LoanApprovalDataset",
            "source_id": "hackathon:loan_approval_av",
            "source_url": "github_multiple",  # Special marker for multiple GitHub sources
            "category": "binary_classification",
            "description": "Loan approval prediction. Target: Loan_Status (Y=1, N=0).",
            "target_column": "Loan_Status",
        }

    def download_dataset(self, info):
        """Download from multiple working GitHub sources"""
        dataset_name = info["name"]
        
        # Multiple working GitHub URLs for Analytics Vidhya loan prediction dataset
        urls = [
            "https://raw.githubusercontent.com/prasertcbs/basic-dataset/master/Loan-Approval-Prediction.csv",
            "https://raw.githubusercontent.com/limchiahooi/loan-approval-prediction/master/train_u6lujuX_CVtuZ9i.csv",
            "https://raw.githubusercontent.com/aasu14/Analytics-Vidhya-Loan-Prediction/master/train.csv",
            "https://raw.githubusercontent.com/vkc0793/Predictive-analysis-on-Loan-Approval/main/Dataset.csv",
            "https://raw.githubusercontent.com/rishabdhar12/Loan-Prediction-Analytics-Vidhya-/master/Loan%20Prediction%20Analytics%20Vidhya/train.csv"
        ]
        
        for i, url in enumerate(urls):
            try:
                print(f"[{dataset_name}] Trying URL {i+1}: {url}")
                r = requests.get(url, timeout=30)
                print(f"[{dataset_name}] HTTP {r.status_code}")
                if r.status_code == 200:
                    print(f"[{dataset_name}] Successfully downloaded from URL {i+1}")
                    return r.content
            except Exception as e:
                print(f"[{dataset_name}] URL {i+1} failed: {e}")
                continue
        
        raise RuntimeError(f"[{dataset_name}] All download URLs failed")

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # Check for different possible target column names
        possible_targets = ["Loan_Status", "target", "status", "approval", "approved"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Target conversion: Y -> 1, N -> 0
        df["target"] = df[actual_target].map({"Y": 1, "N": 0})
        
        # Handle any missing mappings
        if df["target"].isna().any():
            print(f"[{dataset_name}] Warning: Found unmapped values in target column, filling with 0")
            df["target"] = df["target"].fillna(0)
        
        df["target"] = df["target"].astype(int)
        
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)

        # Drop Loan_ID column if it exists (not useful for prediction)
        if "Loan_ID" in df.columns:
            df.drop(columns=["Loan_ID"], inplace=True)

        # Handle categorical variables
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        categorical_cols = [col for col in categorical_cols if col != "target"]
        
        # Simple encoding for categorical variables
        for col in categorical_cols:
            if col in df.columns:
                # For binary categorical variables, map to 0/1
                unique_vals = df[col].dropna().unique()
                if len(unique_vals) == 2:
                    val_map = {unique_vals[0]: 0, unique_vals[1]: 1}
                    df[col] = df[col].map(val_map)
                else:
                    # For multi-category variables, use label encoding
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))

        # Convert all feature columns to numeric, coercing errors
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values in critical columns
        before_dropna = len(df)
        df.dropna(inplace=True)
        if before_dropna > len(df):
            print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")

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
    ds = LoanApprovalDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 