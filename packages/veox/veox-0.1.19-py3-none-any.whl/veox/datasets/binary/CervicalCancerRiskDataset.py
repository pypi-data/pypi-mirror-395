import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CervicalCancerRiskDataset(BaseDatasetLoader):
    """Cervical Cancer (Risk Factors) Dataset.

    Predicts biopsy results for cervical cancer based on patient risk factors.
    Missing values are denoted by '?'.
    Target: 'Biopsy' (0 for negative, 1 for positive cancer result).
    
    Source: Multiple working GitHub repositories with the UCI cervical cancer risk dataset
    Original UCI: https://archive.ics.uci.edu/ml/datasets/Cervical+cancer+%28Risk+Factors%29
    """

    def get_dataset_info(self):
        return {
            "name": "CervicalCancerRiskDataset",
            "source_id": "uci:cervical_cancer_risk",
            "source_url": "github_multiple",  # Special marker for multiple GitHub sources
            "category": "binary_classification",
            "description": "Cervical cancer risk factors. Target: Biopsy (1=cancer, 0=no cancer).",
            "target_column": "Biopsy",
        }

    def download_dataset(self, info):
        """Download from multiple working GitHub sources"""
        dataset_name = info["name"]
        
        # Multiple working GitHub URLs found during web search
        urls = [
            "https://raw.githubusercontent.com/datasets/cervical-cancer/main/data/cervical-cancer.csv",
            "https://raw.githubusercontent.com/SHAHIR123/Cervical-Cancer-Risk-Factor-Analysis/master/Risk_factors_cervical_cancer.csv",
            "https://raw.githubusercontent.com/Pratyusha-R/Cervical-cancer-risk-assessment-using-XGBoost/main/risk_factors_cervical_cancer.csv",
            "https://raw.githubusercontent.com/krishnakatyal/Cervical-Cancer-Risk-Factors-for-Biopsy/master/kag_risk_factors_cervical_cancer.csv",
            "https://raw.githubusercontent.com/sharmaroshan/Cervical-Cancer-Prediction/master/kag_risk_factors_cervical_cancer.csv"
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

        # Replace '?' with pd.NA before attempting numeric conversion
        df.replace('?', pd.NA, inplace=True)

        # Check for different possible target column names
        possible_targets = ["Biopsy", "target", "Dx:Cancer", "Cancer", "class"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Target is already 0/1 after NA replacement and numeric conversion
        df["target"] = pd.to_numeric(df[actual_target], errors="coerce")
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)
        
        # Convert all feature columns to numeric, coercing errors.
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values (especially important for target and key features)
        before_dropna = len(df)
        df.dropna(inplace=True)
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
    ds = CervicalCancerRiskDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 