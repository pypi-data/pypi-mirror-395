import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CropDiseaseDataset(BaseDatasetLoader):
    """Tomato Leaf Disease Dataset.

    Real dataset for plant disease classification based on leaf characteristics.
    Dataset contains tomato plant samples with various disease symptoms and measurements.
    Used for agricultural disease detection and crop health management.
    Target: Disease presence (1=diseased, 0=healthy).
    
    Source: https://raw.githubusercontent.com/AlejoMMateus/Tomato-Leaf-Disease-Detection/main/tomato_leaf_disease_dataset.csv
    Original: Plant pathology research data for tomato disease classification
    """

    def get_dataset_info(self):
        return {
            "name": "CropDiseaseDataset",
            "source_id": "agriculture:tomato_leaf_disease",
            "source_url": "https://raw.githubusercontent.com/AlejoMMateus/Tomato-Leaf-Disease-Detection/main/tomato_leaf_disease_dataset.csv",
            "category": "binary_classification",
            "description": "Tomato leaf disease detection. Target: disease_presence (1=diseased, 0=healthy).",
            "target_column": "target",
        }

    def download_dataset(self, info):
        """Download from working GitHub source - no synthetic fallback allowed"""
        dataset_name = info["name"]
        
        # Try primary URL
        try:
            print(f"[{dataset_name}] Downloading from {info['source_url']}")
            r = requests.get(info["source_url"], timeout=30)
            r.raise_for_status()
            print(f"[{dataset_name}] Successfully downloaded from GitHub")
            return r.content
        except Exception as e:
            # Try alternative GitHub URLs
            fallback_urls = [
                "https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/metadata.csv",
                "https://raw.githubusercontent.com/arunponnusamy/plant-disease-detection/master/data/plant_disease_dataset.csv"
            ]
            
            for url in fallback_urls:
                try:
                    print(f"[{dataset_name}] Trying fallback URL: {url}")
                    r = requests.get(url, timeout=30)
                    r.raise_for_status()
                    print(f"[{dataset_name}] Successfully downloaded from fallback URL")
                    return r.content
                except Exception as fallback_error:
                    print(f"[{dataset_name}] Fallback URL failed: {fallback_error}")
                    continue
            
            # No synthetic fallback - fail with clear error
            raise RuntimeError(
                f"[{dataset_name}] Failed to download dataset from all sources: {e}. "
                "Synthetic fallback is disabled. Ensure this dataset is provisioned via GitHub or S3/admin APIs."
            )

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # Handle different possible target column names
        possible_targets = ["target", "disease", "class", "label", "diseased"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] Using last column as target: {actual_target}")

        # Ensure target is binary 0/1
        if actual_target != "target":
            df["target"] = pd.to_numeric(df[actual_target], errors="coerce")
            df["target"] = (df["target"] > 0).astype(int)
            df.drop(columns=[actual_target], inplace=True)
        else:
            df["target"] = pd.to_numeric(df["target"], errors="coerce").astype(int)

        # Convert all feature columns to numeric
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

if __name__ == "__main__":
    ds = CropDiseaseDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 