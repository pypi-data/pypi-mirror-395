import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WebsitePhishingDataset(BaseDatasetLoader):
    """Website Phishing Detection Dataset.

    Predicts whether a website is a phishing site or legitimate based on various URL and website features.
    Target: 'Result' (1 for phishing, -1 for legitimate).
    Mapped to target: 1 for phishing, 0 for legitimate.
    
    Source: https://raw.githubusercontent.com/GregaVrbancic/Phishing-Dataset/master/dataset_small.csv
    Alternative source: UCI repository via ucimlrepo package
    Original UCI: https://archive.ics.uci.edu/ml/datasets/Website+Phishing
    """

    def get_dataset_info(self):
        return {
            "name": "WebsitePhishingDataset",
            "source_id": "uci:website_phishing",
            "source_url": "https://raw.githubusercontent.com/GregaVrbancic/Phishing-Dataset/master/dataset_small.csv",
            "category": "binary_classification",
            "description": "Website phishing detection. Target: phishing (1=phishing, 0=legitimate).",
            "target_column": "phishing",
        }

    def download_dataset(self, info):
        """Override to implement fallback URLs"""
        dataset_name = info["name"]
        
        # Use ucimlrepo as primary source
        try:
            print(f"[{dataset_name}] Trying UCI repository via ucimlrepo...")
            # Try using ucimlrepo package first
            try:
                from ucimlrepo import fetch_ucirepo
                phishing_websites = fetch_ucirepo(id=379)  # Website Phishing dataset
                X = phishing_websites.data.features
                y = phishing_websites.data.targets
                df = pd.concat([X, y], axis=1)
                import io
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                print(f"[{dataset_name}] Successfully downloaded from UCI via ucimlrepo")
                return csv_buffer.getvalue().encode('utf-8')
            except ImportError:
                print(f"[{dataset_name}] ucimlrepo not available, trying direct URLs...")
        except Exception as e:
            print(f"[{dataset_name}] UCI repository failed: {e}")
        
        # Fallback to direct URLs
        urls = [
            "https://raw.githubusercontent.com/GregaVrbancic/Phishing-Dataset/master/dataset_small.csv"
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
        
        raise RuntimeError(f"[{dataset_name}] All download sources failed")

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        if target_col_original not in df.columns:
            # Check for alternative target column names
            possible_targets = ["phishing", "Result", "Class"]
            for target in possible_targets:
                if target in df.columns:
                    target_col_original = target
                    print(f"[{dataset_name}] Using '{target}' as target column")
                    break
            else:
                raise ValueError(f"[{dataset_name}] No suitable target column found. Available: {df.columns.tolist()}")

        # Map target: 1 (phishing) -> 1, -1 or 0 (legitimate) -> 0
        if df[target_col_original].dtype == 'object':
            # Handle string targets
            df["target"] = df[target_col_original].map({"phishing": 1, "legitimate": 0, "1": 1, "0": 0})
        else:
            # Handle numeric targets
            df["target"] = df[target_col_original].map({1: 1, -1: 0, 0: 0})
        
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # All other features are expected to be numeric (0, 1, or -1).
        # Convert all feature columns to numeric, coercing errors.
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values (e.g. if target mapping failed or data issue)
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
    ds = WebsitePhishingDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 