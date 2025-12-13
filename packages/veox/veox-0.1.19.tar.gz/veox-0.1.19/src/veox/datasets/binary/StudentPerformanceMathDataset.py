import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class StudentPerformanceMathDataset(BaseDatasetLoader):
    """Student Performance Dataset (Math course).

    Predicts student academic performance (pass/fail based on final grade G3) 
    in a mathematics course in secondary school.
    Features include student grades, demographic, social and school related information.
    
    Source: https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip
    Alternative: https://raw.githubusercontent.com/RohithYogi/Student-Performance-Prediction/master/student-mat.csv
    Original UCI: https://archive.ics.uci.edu/ml/datasets/Student+Performance
    """

    def get_dataset_info(self):
        return {
            "name": "StudentPerformanceMathDataset",
            "source_id": "uci:student_performance_math",
            "source_url": "https://raw.githubusercontent.com/RohithYogi/Student-Performance-Prediction/master/student-mat.csv",
            "category": "binary_classification",
            "description": "Student academic performance (Math). Target: G3>=10 (pass=1, fail=0).",
            "target_column": "G3", 
        }

    def download_dataset(self, info):
        """Override to implement fallback URLs"""
        dataset_name = info["name"]
        urls = [
            "https://raw.githubusercontent.com/RohithYogi/Student-Performance-Prediction/master/student-mat.csv",
            "https://raw.githubusercontent.com/sachinsdate/82c9486e4f7d1dd387772ad105fb0544/main/uciml_portuguese_students_math_performance_subset.csv"
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

        if target_col_original not in df.columns:
            raise ValueError(f"[{dataset_name}] Expected target column '{target_col_original}' not found.")

        # Binarize G3: G3 >= 10 is pass (1), else fail (0)
        df["target"] = (pd.to_numeric(df[target_col_original], errors='coerce') >= 10).astype(int)
        if target_col_original != "target":
            df.drop(columns=[target_col_original], inplace=True)
        
        # Handle different column types
        # Numeric columns - convert directly
        numeric_cols = ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Binary categorical columns - map to 0/1
        binary_mappings = {
            'sex': {'F': 0, 'M': 1},
            'address': {'U': 1, 'R': 0},
            'famsize': {'LE3': 0, 'GT3': 1},
            'Pstatus': {'T': 1, 'A': 0},
            'schoolsup': {'yes': 1, 'no': 0},
            'famsup': {'yes': 1, 'no': 0},
            'paid': {'yes': 1, 'no': 0},
            'activities': {'yes': 1, 'no': 0},
            'nursery': {'yes': 1, 'no': 0},
            'higher': {'yes': 1, 'no': 0},
            'internet': {'yes': 1, 'no': 0},
            'romantic': {'yes': 1, 'no': 0}
        }
        
        for col, mapping in binary_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # For remaining categorical columns, use simple label encoding
        remaining_categorical = ['school', 'Mjob', 'Fjob', 'reason', 'guardian']
        for col in remaining_categorical:
            if col in df.columns:
                # Convert to categorical codes (0, 1, 2, ...)
                df[col] = pd.Categorical(df[col]).codes
                # Replace -1 (for NaN) with the mode
                if (df[col] == -1).any():
                    mode_val = df[col][df[col] != -1].mode()
                    if len(mode_val) > 0:
                        df[col] = df[col].replace(-1, mode_val[0])

        # Drop rows with NA values in target or after all conversions
        before_dropna = len(df)
        df = df[df["target"].notna()]  # Ensure target is not NA
        df.dropna(inplace=True) 
        print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")
        df["target"] = df["target"].astype(int) # Ensure target is int after dropna

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
    ds = StudentPerformanceMathDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 