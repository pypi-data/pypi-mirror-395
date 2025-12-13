import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class LiverPatientDataset(BaseDatasetLoader):
    """Indian Liver Patient Dataset (ILPD).

    Predicts liver disease presence based on various clinical measurements
    and patient demographics (age, gender, bilirubin levels, enzymes, proteins, etc.).
    Target: 'Dataset' (1 for no liver disease, 2 for liver disease).
    Mapped to target: 0 for no liver disease, 1 for liver disease.
    
    Source: https://raw.githubusercontent.com/shwetankdhruv/SUPERVISED-LEARNING-CLASSIFICATION-ILPD-DATASET-/main/ILPD.csv
    Alternative: https://raw.githubusercontent.com/harshilpatel1799/ML-Models-Comparion-Indian-Liver-Data-Set/master/indian_liver_patient.csv
    Original UCI: https://archive.ics.uci.edu/ml/datasets/ILPD+(Indian+Liver+Patient+Dataset)
    """

    def get_dataset_info(self):
        return {
            "name": "LiverPatientDataset",
            "source_id": "uci:indian_liver_patient",
            "source_url": "https://raw.githubusercontent.com/shwetankdhruv/SUPERVISED-LEARNING-CLASSIFICATION-ILPD-DATASET-/main/ILPD.csv",
            "category": "binary_classification",
            "description": "Indian Liver Patient Dataset. Target: liver disease (1=liver disease, 0=no liver disease).",
            "target_column": "Dataset",
        }

    def download_dataset(self, info):
        """Override to implement fallback URLs"""
        dataset_name = info["name"]
        urls = [
            "https://raw.githubusercontent.com/shwetankdhruv/SUPERVISED-LEARNING-CLASSIFICATION-ILPD-DATASET-/main/ILPD.csv",
            "https://raw.githubusercontent.com/harshilpatel1799/ML-Models-Comparion-Indian-Liver-Data-Set/master/indian_liver_patient.csv",
            "https://raw.githubusercontent.com/m0-k1/Indian-Liver-Patients/master/indian_liver_patient.csv"
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
        print(f"[{dataset_name}] Current columns: {df.columns.tolist()}")

        # Check if columns look like data rather than proper headers
        # ILPD dataset sometimes gets loaded with first data row as headers
        if (len(df.columns) == 11 and 
            (str(df.columns[0]).replace('.', '').isdigit() or  # Age as column name
             str(df.columns[1]) in ['Male', 'Female'])):      # Gender as column name
            
            print(f"[{dataset_name}] Detected data in column names, fixing headers")
            
            # Save the current "column names" as the first row
            first_row = pd.DataFrame([df.columns.tolist()], columns=range(len(df.columns)))
            
            # Reset column names to proper ILPD column names
            proper_cols = ['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase',
                          'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Protiens',
                          'Albumin', 'Albumin_and_Globulin_Ratio', 'Dataset']
            
            # Create new dataframe with proper structure
            df.columns = range(len(df.columns))  # Temporary numeric names
            df = pd.concat([first_row, df], ignore_index=True)  # Add first row back as data
            df.columns = proper_cols  # Set proper column names
            
            print(f"[{dataset_name}] Fixed headers, new shape: {df.shape}")

        # Now look for target column
        if target_col_original not in df.columns:
            # Check for alternative target column names
            possible_targets = ["Dataset", "Class", "target", "Selector"]
            for target in possible_targets:
                if target in df.columns:
                    target_col_original = target
                    print(f"[{dataset_name}] Using '{target}' as target column")
                    break
            else:
                raise ValueError(f"[{dataset_name}] No suitable target column found. Available: {df.columns.tolist()}")

        # Convert all columns to proper types first
        for col in df.columns:
            if col != target_col_original:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle target column
        df[target_col_original] = pd.to_numeric(df[target_col_original], errors='coerce')
        
        # Map target: typically 2 (liver disease) -> 1, 1 (no liver disease) -> 0
        unique_vals = df[target_col_original].dropna().unique()
        print(f"[{dataset_name}] Unique target values: {unique_vals}")
        
        if 2 in unique_vals and 1 in unique_vals:
            # Standard ILPD encoding: 2=liver disease, 1=no liver disease
            df["target"] = df[target_col_original].map({2: 1, 1: 0})
        else:
            # If different encoding, try to map automatically
            df["target"] = df[target_col_original].map({max(unique_vals): 1, min(unique_vals): 0})
        
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # Handle gender column: convert to numeric
        if 'Gender' in df.columns:
            df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0, 'male': 1, 'female': 0})
            # If still has non-numeric values, use label encoding
            if df['Gender'].isna().any():
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                df['Gender'] = le.fit_transform(df['Gender'].astype(str))

        # Drop rows with NA values (especially important for this dataset)
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
    ds = LiverPatientDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 