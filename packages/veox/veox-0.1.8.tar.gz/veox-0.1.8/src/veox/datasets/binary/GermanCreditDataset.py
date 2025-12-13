import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class GermanCreditDataset(BaseDatasetLoader):
    """UCI German Credit dataset (binary classification).

    Predict credit risk - whether a person is a good or bad credit risk.
    1,000 instances with 20 attributes (duration, credit amount, purpose, etc.).
    Original dataset uses 1=good credit, 2=bad credit. We convert to 1=good, 0=bad.
    Source: https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)
    """

    def get_dataset_info(self):
        return {
            "name": "GermanCreditDataset",
            "source_id": "uci:german_credit",
            "category": "binary_classification",
            "description": "German credit risk dataset – predict good credit risk (1) or bad credit risk (0).",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 50000:  # Expect ~184KB
                preview = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. Preview:\n" + os.linesep.join(preview))
                raise RuntimeError(f"Downloaded file too small: {file_size} bytes")
            
            # Parse the data immediately to ensure proper handling
            from io import StringIO
            import pandas as pd
            
            # The german.data file has no header and uses space as delimiter
            # 20 attributes + 1 class label (1=good credit, 2=bad credit)
            df = pd.read_csv(StringIO(r.text), sep=' ', header=None)
            print(f"[{dataset_name}] Parsed {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Return as CSV bytes
            return df.to_csv(index=False, header=False).encode('utf-8')
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        
        # The german.data file has no header and uses space as delimiter
        # 20 attributes + 1 class label (1=good credit, 2=bad credit)
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Always assign column names (no header in raw file)
        expected_cols = 21  # 20 features + 1 target
        if df.shape[1] != expected_cols:
            print(f"[{dataset_name}] Warning: expected {expected_cols} columns, got {df.shape[1]}")
            if df.shape[1] > expected_cols:
                df = df.iloc[:, :expected_cols]
            else:
                # Pad with 0 if needed (not NaN to avoid boolean ambiguity)
                for i in range(df.shape[1], expected_cols):
                    df[i] = 0
        
        # Assign column names based on UCI documentation
        columns = [
            "checking_status",        # Status of existing checking account
            "duration",              # Duration in month
            "credit_history",        # Credit history
            "purpose",               # Purpose
            "credit_amount",         # Credit amount
            "savings_status",        # Savings account/bonds
            "employment",            # Present employment since
            "installment_rate",      # Installment rate in percentage of disposable income
            "personal_status",       # Personal status and sex
            "other_parties",         # Other debtors / guarantors
            "residence_since",       # Present residence since
            "property_magnitude",    # Property
            "age",                   # Age in years
            "other_payment_plans",   # Other installment plans
            "housing",               # Housing
            "existing_credits",      # Number of existing credits at this bank
            "job",                   # Job
            "num_dependents",        # Number of people being liable to provide maintenance for
            "own_telephone",         # Telephone
            "foreign_worker",        # Foreign worker
            "class"                  # Class (1 = good credit, 2 = bad credit)
        ]
        df.columns = columns
        
        # Convert class to binary target
        # Original: 1=good credit, 2=bad credit
        # Convert to: 1=good credit, 0=bad credit
        df["target"] = df["class"].apply(lambda x: 1 if x == 1 else 0)
        df.drop(columns=["class"], inplace=True)
        
        # Convert numeric columns to proper types
        numeric_cols = ["duration", "credit_amount", "installment_rate", "residence_since", 
                       "age", "existing_credits", "num_dependents"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Check for missing values
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                print(f"  - {col}: {missing} missing")
        
        # Drop rows with any missing values
        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA values")
        
        # Strip whitespace from categorical columns (they use coded values but may have spaces)
        categorical_cols = [col for col in df.columns if col not in numeric_cols and col != "target"]
        for col in categorical_cols:
            # Convert to string first, handling any NA values
            if df[col].dtype == 'object':
                # Fill NA before string operations to avoid boolean ambiguity
                df[col] = df[col].fillna('').astype(str).str.strip()
                # Replace empty strings with 'UNKNOWN' (not NaN)
                df[col] = df[col].replace('', 'UNKNOWN')
            else:
                # If already numeric, ensure no NA
                df[col] = df[col].fillna(0)
        
        # Convert categorical columns to numeric
        # These are already coded (A11, A12, etc.) but we need to convert to numeric
        for col in categorical_cols:
            # Fill NA before categorical conversion to avoid boolean ambiguity
            df[col] = df[col].fillna('UNKNOWN')
            # Convert coded categorical values to numeric
            df[col] = pd.Categorical(df[col]).codes
            # Convert -1 (which represents NA in Categorical codes) to 0 or keep as is
            # Categorical codes use -1 for missing values, but we'll keep it as numeric
        
        # Convert all int8 columns to int64
        for col in df.columns:
            if df[col].dtype == 'int8':
                df[col] = df[col].astype('int64')
        
        # Ensure target is integer
        df["target"] = df["target"].astype(int)
        
        # CRITICAL: Drop ALL rows with ANY NA values to avoid boolean ambiguity
        # This must happen after all processing but before returning
        before_final_dropna = len(df)
        df.dropna(inplace=True)
        if before_final_dropna > len(df):
            print(f"[{dataset_name}] Final dropna: Dropped {before_final_dropna - len(df)} rows with remaining NA values")
        
        # Ensure all columns are numeric (no object/string types that could cause issues)
        for col in df.columns:
            if col != "target":
                if df[col].dtype == 'object':
                    # Convert any remaining object columns to numeric
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                # Ensure no NA values remain
                if df[col].isna().any():
                    df[col] = df[col].fillna(0)
        
        # Final check: ensure no NA values remain anywhere
        if df.isna().any().any():
            print(f"[{dataset_name}] WARNING: Still have NA values after processing, filling with 0")
            df = df.fillna(0)
        
        # Reorder columns so target is last
        feature_cols = [c for c in df.columns if c != "target"]
        df = df[feature_cols + ["target"]]
        
        # Shuffle dataset
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[{dataset_name}] Data types: {df.dtypes.to_dict()}")
        
        return df


if __name__ == "__main__":
    dataset = GermanCreditDataset()
    df = dataset.get_data()
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns") 