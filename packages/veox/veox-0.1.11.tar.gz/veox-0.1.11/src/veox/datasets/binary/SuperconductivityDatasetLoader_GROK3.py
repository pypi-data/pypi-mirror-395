from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import requests
import logging
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

logger = logging.getLogger(__name__)

class SuperconductivityDatasetLoader_GROK3Dataset(BaseDatasetLoader):
    def get_dataset_info(self) -> Dict[str, Any]:
        return {
            'name': 'SuperconductivityDatasetLoader_GROK3',
            'source_id': 'uci:superconductivity',
            'category': 'models/binary_classification',
            'industry': 'materials_science',
            'description': 'Superconductivity Dataset: Contains 81 features extracted from 21263 superconductors along with the critical temperature. Can be used for binary classification by setting a threshold for critical temperature.',
            'source_url': 'https://archive.ics.uci.edu/ml/machine-learning-databases/00464/superconduct.zip',
            'format': 'csv',
            'target_column': 'critical_temp'
        }

    def download_dataset(self, info: Dict[str, Any]):
        import zipfile
        import io
        import pandas as pd
        
        url = info.get('source_url')
        if not url:
            raise ValueError(f"[{info['name']}] No source_url provided for dataset")
            
        logger.info(f"[{info['name']}] GET {url}")
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
                
            # Extract the zip file content
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                # List files in zip to find CSV
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if not csv_files:
                    raise FileNotFoundError(f"No CSV file found in zip archive")
                
                # Use the first CSV file found
                csv_file = csv_files[0]
                logger.info(f"[{info['name']}] Extracting {csv_file} from zip")
                with z.open(csv_file) as f:
                    df = pd.read_csv(f)
                    logger.info(f"[{info['name']}] Loaded {df.shape[0]} rows from {csv_file}")
                    return df.to_csv(index=False).encode('utf-8')
        except Exception as e:
            logger.error(f"[{info['name']}] Error downloading or extracting from {url}: {e}")
            raise

    def process_dataframe(self, df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Find critical temperature column
        target_col = info.get('target_column', 'critical_temp')
        temp_cols = [col for col in df.columns if 'temp' in col.lower() or 'critical' in col.lower() or col == target_col]
        if not temp_cols:
            # Try to use last column if it looks numeric
            last_col = df.columns[-1]
            if pd.api.types.is_numeric_dtype(df[last_col]):
                temp_col = last_col
            else:
                raise ValueError(f"[{dataset_name}] Could not find critical temperature column")
        else:
            temp_col = temp_cols[0]
        
        # For binary classification, convert critical temperature to binary label
        # Using a threshold (e.g., 10K) to classify as superconductor or not
        df['target'] = (pd.to_numeric(df[temp_col], errors='coerce') > 10).astype(int)
        
        # Drop the original temperature column
        if temp_col != 'target':
            df = df.drop(columns=[temp_col])
        
        # Ensure all features are numeric
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill NA values with median for numeric columns instead of dropping
        # This preserves more data for training
        for col in df.columns:
            if col != "target":
                if df[col].isna().any():
                    median_val = df[col].median()
                    if pd.notna(median_val):
                        df[col].fillna(median_val, inplace=True)
                    else:
                        # If median is also NaN, fill with 0
                        df[col].fillna(0, inplace=True)
        
        # Only drop rows where target is NA (critical)
        before_dropna = len(df)
        df = df.dropna(subset=['target'])
        if before_dropna > len(df):
            print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA target values.")
        
        # Final check: ensure no NaN values remain - use multiple strategies
        remaining_nans = df.isna().sum().sum()
        if remaining_nans > 0:
            print(f"[{dataset_name}] Warning: {remaining_nans} NaN values still present, filling with 0")
            # Fill all remaining NaN values with 0
            df = df.fillna(0)
            # Also replace any inf values
            df = df.replace([np.inf, -np.inf], 0)
        
        # Double-check: ensure absolutely no NaN values remain
        final_nans = df.isna().sum().sum()
        if final_nans > 0:
            print(f"[{dataset_name}] Critical: {final_nans} NaN values still present after fillna, using dropna")
            df = df.dropna()
        
        # Ensure we have enough data
        if len(df) < 10:
            raise ValueError(f"[{dataset_name}] Insufficient data after processing: {len(df)} rows")
        
        # Convert target to int, ensuring no NaN
        df["target"] = pd.to_numeric(df["target"], errors='coerce').fillna(0).astype(int)
        
        # Check target distribution
        target_dist = df['target'].value_counts()
        if len(target_dist) < 2:
            raise ValueError(f"[{dataset_name}] Dataset has only one class after processing: {target_dist.to_dict()}")
        
        # Deduplicate
        before_dedup = len(df)
        df.drop_duplicates(inplace=True)
        if len(df) < before_dedup:
            print(f"[{dataset_name}] Removed {before_dedup - len(df)} duplicate rows.")
        
        # Ensure we still have enough data after deduplication
        if len(df) < 10:
            raise ValueError(f"[{dataset_name}] Insufficient data after deduplication: {len(df)} rows")
        
        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df