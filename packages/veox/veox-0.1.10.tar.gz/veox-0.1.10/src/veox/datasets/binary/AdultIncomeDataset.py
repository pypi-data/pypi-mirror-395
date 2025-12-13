import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class AdultIncomeDataset(BaseDatasetLoader):
    """UCI Adult Income dataset (binary classification).

    Predict whether a person makes over 50K a year based on census data.
    32,561 instances with 14 attributes (age, workclass, education, etc.).
    Source: https://archive.ics.uci.edu/ml/datasets/Adult
    """

    def get_dataset_info(self):
        return {
            "name": "AdultIncomeDataset",
            "source_id": "uci:adult_income",
            "category": "binary_classification",
            "description": "Adult census income dataset – predict income >50K (1) or <=50K (0).",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 1000000:  # Expect ~3.8MB
                preview = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. Preview:\n" + os.linesep.join(preview))
                raise RuntimeError(f"Downloaded file too small: {file_size} bytes")
                
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        
        # The adult.data file has no header
        # 14 attributes + 1 class label (>50K, <=50K)
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Always assign column names (no header in raw file)
        expected_cols = 15  # 14 features + 1 target
        if df.shape[1] != expected_cols:
            print(f"[{dataset_name}] Warning: expected {expected_cols} columns, got {df.shape[1]}")
            if df.shape[1] > expected_cols:
                df = df.iloc[:, :expected_cols]
            else:
                # Pad with NaN if needed
                for _ in range(expected_cols - df.shape[1]):
                    df[df.shape[1]] = pd.NA
        
        # Assign column names based on UCI documentation
        columns = [
            "age", "workclass", "fnlwgt", "education", "education_num",
            "marital_status", "occupation", "relationship", "race", "sex",
            "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
        ]
        df.columns = columns
        
        # Convert income to binary target
        # ">50K" -> 1, "<=50K" -> 0
        # Note: values might have trailing periods, so we strip them
        df["income"] = df["income"].astype(str).str.strip()
        df["target"] = df["income"].apply(lambda x: 1 if x.startswith(">50K") else 0)
        df.drop(columns=["income"], inplace=True)
        
        # Replace " ?" (space + question mark) with NaN for missing values
        df.replace(" ?", pd.NA, inplace=True)
        df.replace("?", pd.NA, inplace=True)
        
        # Log missing values
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                print(f"  - {col}: {missing} missing")
        
        # Drop rows with any missing values
        before = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before - len(df)} rows with NA values")
        
        # Convert numeric columns to proper numeric types
        numeric_cols = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Strip whitespace from categorical columns
        categorical_cols = ["workclass", "education", "marital_status", "occupation", 
                          "relationship", "race", "sex", "native_country"]
        for col in categorical_cols:
            df[col] = df[col].astype(str).str.strip()
        
        # Convert categorical columns to numeric
        for col in categorical_cols:
            if col == 'education':
                # Ordinal encoding for education levels
                education_order = {
                    'Preschool': 0, '1st-4th': 1, '5th-6th': 2, '7th-8th': 3,
                    '9th': 4, '10th': 5, '11th': 6, '12th': 7, 'HS-grad': 8,
                    'Some-college': 9, 'Assoc-voc': 10, 'Assoc-acdm': 11,
                    'Bachelors': 12, 'Masters': 13, 'Prof-school': 14, 'Doctorate': 15
                }
                df[col] = df[col].map(education_order).fillna(-1).astype(int)
            elif col == 'sex':
                # Binary encoding
                df[col] = df[col].map({'Male': 1, 'Female': 0}).fillna(-1).astype(int)
            else:
                # Label encoding for other categorical variables
                df[col] = pd.Categorical(df[col]).codes
        
        # Convert all int8 columns to int64
        for col in df.columns:
            if df[col].dtype == 'int8':
                df[col] = df[col].astype('int64')
        
        # Ensure target is integer
        df["target"] = df["target"].astype(int)
        
        # Reorder columns so target is last
        feature_cols = [c for c in df.columns if c != "target"]
        df = df[feature_cols + ["target"]]
        
        # Shuffle dataset
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[{dataset_name}] Sample of first 3 rows:\n{df.head(3).to_string()}")
        
        return df


if __name__ == "__main__":
    dataset = AdultIncomeDataset()
    df = dataset.get_data()
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns") 