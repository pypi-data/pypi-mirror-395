import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class HabermanSurvivalDataset(BaseDatasetLoader):
    """Haberman's Survival Data Set.

    Dataset contains cases from a study conducted on the survival of patients 
    who had undergone surgery for breast cancer.
    Features: Age of patient at time of operation, Patient's year of operation, 
    Number of positive axillary nodes detected.
    Target: Survival status (1 = patient survived 5 years or longer, 
    2 = patient died within 5 years).

    Source: https://raw.githubusercontent.com/jbrownlee/Datasets/master/haberman.csv
    Original UCI: https://archive.ics.uci.edu/ml/datasets/Haberman%27s+Survival
    The raw CSV file has no header.
    """

    def get_dataset_info(self):
        return {
            "name": "HabermanSurvivalDataset",
            "source_id": "uci:haberman_survival",
            "source_url": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/haberman.csv",
            "category": "binary_classification",
            "description": "Predict patient survival after breast cancer surgery. Target: Died within 5 years (1=died, 0=survived).",
            "target_column": 3,  # Index of target column as CSV has no header
        }
    
    def download_dataset(self, info):
        """Download the Haberman Survival dataset"""
        print(f"[HabermanSurvivalDataset] Downloading from GitHub...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # CSV with no header
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), header=None)
        print(f"[HabermanSurvivalDataset] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        # CSV has no header, so columns will be 0, 1, 2, 3
        # We expect 3 features and 1 target column
        expected_num_cols = 4
        
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Assign column names if they are default integers and shape matches
        if list(df.columns) == list(range(df.shape[1])) and df.shape[1] == expected_num_cols:
            df.columns = ["Age", "OperationYear", "PositiveAxillaryNodes", "SurvivalStatus"]
            print(f"[{dataset_name}] Assigned column names: {df.columns.tolist()}")
        elif "SurvivalStatus" not in df.columns and df.shape[1] == expected_num_cols:
            # If loaded from cache with names, but target_column was index
             df.columns = ["Age", "OperationYear", "PositiveAxillaryNodes", "SurvivalStatus"]
        
        target_col_original_name = "SurvivalStatus"
        if target_col_original_name not in df.columns:
             # If column names were not set as expected, assume target is last column by index
            if df.shape[1] == expected_num_cols:
                target_col_original_idx = info["target_column"]
                df.rename(columns={df.columns[target_col_original_idx]: "SurvivalStatus"}, inplace=True)
                print(f"[{dataset_name}] Renamed column {target_col_original_idx} to SurvivalStatus") 
            else:
                raise ValueError(f"[{dataset_name}] DataFrame has unexpected shape {df.shape} or columns {df.columns.tolist()}")

        # Map target: 1 (survived) -> 0, 2 (died) -> 1
        df["target"] = df["SurvivalStatus"].map({1: 0, 2: 1})
        if "SurvivalStatus" != "target":
            df.drop(columns=["SurvivalStatus"], inplace=True)
        
        # Ensure all features are numeric (they should be already for this dataset)
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values (e.g. if mapping failed or data issue)
        df.dropna(inplace=True)
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
    ds = HabermanSurvivalDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 