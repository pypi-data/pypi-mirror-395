import os
import pandas as pd
import requests
import io
import numpy as np
from datetime import datetime, timedelta
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class OilPriceDataset(BaseDatasetLoader):
    """
    Brent Crude oil daily spot price (USD) regression dataset.

    Data source (public & direct CSV link – ~7 KB):
    https://raw.githubusercontent.com/datasets/brent-spot-prices/master/data.csv

    Columns in raw file:
        • Date  – ISO date string
        • Price – Spot price in USD per barrel

    The loader converts the file into a DataFrame and adds the required
    `target` column (identical to `price`) as the final column so that models
    can treat this as a univariate time-series regression task.
    """

    # ------------------------------------------------------------------
    # Required hooks
    # ------------------------------------------------------------------
    def get_dataset_info(self):
        return {
            "name": "OilPriceDataset",
            "source_id": "datahub:brent_spot_prices",  # unique identifier
            "source_url": "https://raw.githubusercontent.com/datasets/oil-prices/master/data/brent-daily.csv",
            "category": "regression",
            "description": "Daily Brent crude oil spot prices (USD) – regression task to predict the closing price.",
            "target_column": "price",
        }

    # ------------------------------------------------------------------
    def download_dataset(self, info):
        dataset_name = info["name"]
        url = info["source_url"]
        print(f"[{dataset_name}] Downloading from {url}")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        if len(r.content) < 500:  # sanity-check: file should be > 1 KB
            raise Exception("File too small – looks corrupted")
        return r.content

    # ------------------------------------------------------------------
    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Columns before processing: {df.columns.tolist()}")

        # ------------------------------------------------------------------
        # Normalise column names & types
        # ------------------------------------------------------------------
        rename_map = {}
        for col in df.columns:
            low = col.lower().strip()
            if low.startswith("date"):
                rename_map[col] = "date"
            elif low.startswith("price"):
                rename_map[col] = "price"
        df = df.rename(columns=rename_map)

        # Ensure correct dtypes
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # Drop rows where price is NA
        before = len(df)
        df.dropna(subset=["price"], inplace=True)
        after = len(df)
        dropped = before - after
        if dropped:
            print(f"[{dataset_name}] Dropped {dropped} rows with missing price values")

        # ------------------------------------------------------------------
        # Add / enforce target column as final column
        # ------------------------------------------------------------------
        df["target"] = df["price"]
        
        # Drop date column
        if "date" in df.columns:
            df = df.drop("date", axis=1)
            print(f"[{dataset_name}] Dropped 'date' column")
        
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle to remove temporal order (leave time series ordering for advanced users)
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        return df

# ------------------------------------------------------------------
# Quick manual test
# ------------------------------------------------------------------
if __name__ == "__main__":
    ds = OilPriceDataset()
    frame = ds.get_data()
    print(f"Loaded {len(frame)} rows – columns: {frame.columns.tolist()}") 