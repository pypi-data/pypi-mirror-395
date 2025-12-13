import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class AutoMPGClassificationDataset(BaseDatasetLoader):
    """Auto MPG Dataset (UCI) - Binary Classification Version.

    Real dataset for fuel efficiency classification based on vehicle characteristics.
    Original dataset contains city-cycle fuel consumption data for cars from 1970-1982.
    Converted to binary classification: high efficiency (mpg >= 25) vs low efficiency (mpg < 25).
    Target: Fuel efficiency class (1=high efficiency, 0=low efficiency).
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data
    Original UCI: Auto MPG Dataset
    """

    def get_dataset_info(self):
        return {
            "name": "AutoMPGClassificationDataset",
            "source_id": "uci:auto_mpg_classification",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data",
            "category": "binary_classification",
            "description": "Auto MPG fuel efficiency classification. Target: high_efficiency (1=high, 0=low).",
            "target_column": "mpg",
        }

    def download_dataset(self, info):
        """Override download to handle the special format of auto-mpg.data"""
        dataset_name = info["name"]
        url = info["source_url"]
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The Auto MPG dataset is whitespace-delimited with no header
        # If we got a single column, it means the parser didn't split properly
        if df.shape[1] == 1:
            # Parse the data manually by splitting on whitespace
            print(f"[{dataset_name}] Manual parsing of whitespace-delimited data")
            lines = []
            
            # Convert the single column to text and split each row
            for idx, row in df.iterrows():
                line = str(row.iloc[0]).strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    # Split on whitespace, but keep quoted strings together
                    parts = []
                    in_quotes = False
                    current_part = ""
                    
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char.isspace() and not in_quotes:
                            if current_part:
                                parts.append(current_part)
                                current_part = ""
                        else:
                            current_part += char
                    
                    if current_part:
                        parts.append(current_part)
                    
                    if len(parts) >= 8:  # Ensure we have at least the minimum expected columns
                        lines.append(parts)
            
            # Create new dataframe from parsed lines
            if lines:
                max_cols = max(len(line) for line in lines)
                # Pad shorter lines with None
                for line in lines:
                    while len(line) < max_cols:
                        line.append(None)
                
                df = pd.DataFrame(lines)
                print(f"[{dataset_name}] Reparsed to shape: {df.shape}")

        # Assign column names for Auto MPG dataset
        if df.shape[1] >= 8:
            col_names = [
                'mpg', 'cylinders', 'displacement', 'horsepower', 'weight',
                'acceleration', 'model_year', 'origin'
            ]
            # Add car_name if we have extra columns
            if df.shape[1] == 9:
                col_names.append('car_name')
            elif df.shape[1] > 9:
                # Handle case where car names might be split across multiple columns
                col_names.extend([f'car_name_{i}' for i in range(df.shape[1] - 8)])
            
            df.columns = col_names[:df.shape[1]]
            print(f"[{dataset_name}] Assigned column names: {df.columns.tolist()}")
        
        # Drop car name columns (string identifiers)
        name_cols = [col for col in df.columns if 'car_name' in col.lower()]
        if name_cols:
            df.drop(columns=name_cols, inplace=True)
        
        # Convert numeric columns
        numeric_cols = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin']
        for col in numeric_cols:
            if col in df.columns:
                # Handle '?' as missing values
                df[col] = df[col].replace('?', pd.NA)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert MPG to binary classification (threshold: 25 mpg)
        if 'mpg' in df.columns:
            mpg_values = pd.to_numeric(df['mpg'], errors='coerce')
            df["target"] = (mpg_values >= 25).astype(int)
            df.drop(columns=['mpg'], inplace=True)
        else:
            raise ValueError(f"[{dataset_name}] Expected 'mpg' column not found.")

        # Drop rows with NA values (especially horsepower missing values)
        before_dropna = len(df)
        df.dropna(inplace=True)
        if before_dropna > len(df):
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
    ds = AutoMPGClassificationDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 