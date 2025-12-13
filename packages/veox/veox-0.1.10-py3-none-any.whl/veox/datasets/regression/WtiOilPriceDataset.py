import os
import pandas as pd
import requests
import io
import numpy as np
from datetime import datetime, timedelta
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WtiOilPriceDataset(BaseDatasetLoader):
    """
    West Texas Intermediate (WTI) crude oil daily spot price (USD) regression dataset.

    Source: https://raw.githubusercontent.com/datasets/oil-prices/master/data/wti-daily.csv
    Columns: Date, Price
    """

    def get_dataset_info(self):
        return {
            "name": "WtiOilPriceDataset",
            "source_id": "datahub:wti_daily_prices",
            "source_url": "https://raw.githubusercontent.com/datasets/oil-prices/master/data/wti-daily.csv",
            "category": "regression",
            "description": "Daily WTI crude oil spot prices (USD) – regression task to predict the price.",
            "target_column": "Price",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = info["source_url"]
        print(f"[{dataset_name}] Downloading from {url}")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        if len(r.content) < 500:
            raise Exception("Downloaded content too small")
        return r.content

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        rename_map = {}
        for col in df.columns:
            low = col.lower()
            if low.startswith("date"):
                rename_map[col] = "date"
            elif low.startswith("price"):
                rename_map[col] = "price"
        df = df.rename(columns=rename_map)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

        before = len(df)
        df.dropna(subset=["price"], inplace=True)
        if before - len(df):
            print(f"[{dataset_name}] Dropped {before - len(df)} NA rows")

        df["target"] = df["price"]
        
        # Drop date column
        if "date" in df.columns:
            df = df.drop("date", axis=1)
            print(f"[{dataset_name}] Dropped 'date' column")
        
        df = df[[c for c in df.columns if c != "target"] + ["target"]]
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Final shape: {df.shape}")
        return df

if __name__ == "__main__":
    ds = WtiOilPriceDataset()
    print(ds.get_data().head()) 