import pandas as pd
import logging
from typing import Dict, Any, Optional
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

logger = logging.getLogger(__name__)

class SteelEnergyConsumptionDataset_GROK3Dataset(BaseDatasetLoader):
    def get_dataset_info(self) -> Dict[str, Any]:
        return {
            'name': 'SteelEnergyConsumptionDataset_GROK3',
            'source_id': 'kaggle:steel-industry-energy',
            'category': 'models/binary_classification',
            'industry': 'materials_science',
            'description': 'Steel Industry Energy Consumption Dataset: 35040 samples, 9 features. Adapted for binary classification (high/low energy consumption).',
            'kaggle_dataset': 'csafrit2/steel-industry-energy-consumption',
            'format': 'csv',
            'target_column': 'Usage_kWh'
        }

    def download_dataset(self, info: Dict[str, Any]):
        dataset_name = info['name']
        kaggle_dataset = info.get('kaggle_dataset')
        
        if not kaggle_dataset:
            raise ValueError(f"[{dataset_name}] No kaggle_dataset provided for dataset")
        
        try:
            import kaggle
            import tempfile
            import os
            
            logger.info(f"[{dataset_name}] Downloading from Kaggle: {kaggle_dataset}")
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    kaggle_dataset,
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV file
                csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
                if not csv_files:
                    raise FileNotFoundError(f"[{dataset_name}] No CSV file found in Kaggle dataset")
                
                csv_path = os.path.join(temp_dir, csv_files[0])
                df = pd.read_csv(csv_path)
                logger.info(f"[{dataset_name}] Downloaded {df.shape[0]} rows from Kaggle")
                return df.to_csv(index=False).encode('utf-8')
        except ImportError:
            raise RuntimeError(
                f"[{dataset_name}] Kaggle module not available. "
                "Please install kaggle module and rebuild Docker containers. "
                "Synthetic fallback is disabled for Human datasets."
            )
        except Exception as e:
            logger.error(f"[{dataset_name}] Error downloading from Kaggle: {e}")
            raise RuntimeError(
                f"[{dataset_name}] Failed to download dataset from Kaggle: {e}. "
                "Synthetic fallback is disabled. Ensure this dataset is provisioned via Kaggle or S3/admin APIs."
            )

    def process_dataframe(self, df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
        dataset_name = info["name"]
        target_col = info.get('target_column', 'Usage_kWh')
        
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Find the target column
        if target_col not in df.columns:
            # Try to find a column with similar name
            possible_cols = [col for col in df.columns if 'usage' in col.lower() or 'kwh' in col.lower() or 'energy' in col.lower()]
            if possible_cols:
                target_col = possible_cols[0]
            else:
                # Use last numeric column
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    target_col = numeric_cols[-1]
                else:
                    raise ValueError(f"[{dataset_name}] Could not find target column")
        
        # Binarize the target variable for binary classification
        # Classify energy consumption as high (1) or low (0) based on the median value
        median_value = pd.to_numeric(df[target_col], errors='coerce').median()
        df['target'] = (pd.to_numeric(df[target_col], errors='coerce') > median_value).astype(int)
        
        # Drop the original target column
        if target_col != 'target':
            df = df.drop(columns=[target_col])
        
        # Ensure all features are numeric
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with NA values
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