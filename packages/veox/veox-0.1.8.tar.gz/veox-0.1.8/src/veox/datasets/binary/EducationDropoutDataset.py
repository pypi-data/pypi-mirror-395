import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class EducationDropoutDataset(BaseDatasetLoader):
    """Education Dropout Prediction Dataset.

    Real dataset for student dropout prediction based on academic and demographic factors.
    Dataset contains student data with dropout occurrence labels.
    Used for educational policy and student intervention programs.
    Target: Dropout status (1=dropout, 0=graduate).
    
    Source: UCI Student Performance dataset via ucimlrepo or GitHub mirrors
    Original: UCI Student Performance dataset from educational institutions
    """

    def get_dataset_info(self):
        return {
            "name": "EducationDropoutDataset",
            "source_id": "education:student_dropout_prediction",
            "source_url": "uci_repo",  # Special marker for UCI repo
            "category": "binary_classification",
            "description": "Student dropout prediction from academic data. Target: dropout (1=dropout, 0=graduate).",
            "target_column": "G3",
        }

    def download_dataset(self, info):
        """Download from UCI repository via ucimlrepo or fallback URLs"""
        dataset_name = info["name"]
        from io import StringIO
        
        # Try ucimlrepo first
        try:
            print(f"[{dataset_name}] Attempting to fetch from UCI repository using ucimlrepo...")
            try:
                from ucimlrepo import fetch_ucirepo
                student_performance = fetch_ucirepo(id=320)  # Student Performance dataset
                X = student_performance.data.features
                y = student_performance.data.targets
                df = pd.concat([X, y], axis=1)
                print(f"[{dataset_name}] Successfully downloaded from UCI via ucimlrepo: {df.shape}")
                if df.empty:
                    raise ValueError("Downloaded dataframe is empty")
                return df.to_csv(index=False).encode('utf-8')
            except ImportError:
                print(f"[{dataset_name}] ucimlrepo not available, trying direct URLs...")
        except Exception as e:
            print(f"[{dataset_name}] UCI repository failed: {e}")
        
        # Fallback URLs from working GitHub repositories
        fallback_urls = [
            "https://raw.githubusercontent.com/arunk13/MSDA-Assignments/master/IS607Fall2015/Assignment3/student-por.csv",
            "https://raw.githubusercontent.com/meizmyang/Student-Performance-Classification-Analysis/master/student-por.csv",
            "https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip"
        ]
        
        for i, url in enumerate(fallback_urls):
            try:
                print(f"[{dataset_name}] Trying URL {i+1}: {url}")
                r = requests.get(url, timeout=30)
                r.raise_for_status()
                
                if url.endswith('.zip'):
                    # Handle zip file
                    import zipfile
                    import io as bio
                    with zipfile.ZipFile(bio.BytesIO(r.content)) as z:
                        csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                        if csv_files:
                            with z.open(csv_files[0]) as f:
                                df = pd.read_csv(f, sep=';')
                                print(f"[{dataset_name}] Successfully downloaded from zip: {df.shape}")
                                if df.empty:
                                    continue
                                return df.to_csv(index=False).encode('utf-8')
                else:
                    # Handle CSV directly
                    df = pd.read_csv(StringIO(r.text), sep=';')
                    print(f"[{dataset_name}] Successfully downloaded from URL {i+1}: {df.shape}")
                    if df.empty:
                        continue
                    return df.to_csv(index=False).encode('utf-8')
            except Exception as e:
                print(f"[{dataset_name}] URL {i+1} failed: {e}")
                continue
        
        raise RuntimeError(f"[{dataset_name}] All download URLs failed - dataset unavailable")

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        print(f"[{dataset_name}] Columns: {list(df.columns)[:10]}...")  # Show first 10 columns

        # Ensure dataframe has data
        if df.empty:
            raise ValueError(f"[{dataset_name}] Dataset dataframe is empty after download")
        
        if len(df.columns) == 0:
            raise ValueError(f"[{dataset_name}] Dataset dataframe has no columns")
        
        # Normalize column names (remove spaces, lowercase)
        df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
        
        # Check for different possible target column names (case-insensitive)
        possible_targets = ["g3", "target", "dropout", "grade", "final_grade", "g1", "g2"]
        actual_target = None
        
        for target in possible_targets:
            matching_cols = [col for col in df.columns if target in col.lower()]
            if matching_cols:
                actual_target = matching_cols[0]
                print(f"[{dataset_name}] Found target column: {actual_target}")
                break
        
        if actual_target is None:
            # If no standard target found, try to use last numeric column
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                actual_target = numeric_cols[-1]
                print(f"[{dataset_name}] No standard target column found, using last numeric column: {actual_target}")
            else:
                # Use last column as fallback
                actual_target = df.columns[-1]
                print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Convert final grade to binary: grade <= 10 is dropout (1), grade > 10 is graduate (0)
        final_grade = pd.to_numeric(df[actual_target], errors="coerce")
        df["target"] = (final_grade <= 10).astype(int)
        
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)
        
        # Ensure we have features and target
        if len(df.columns) < 2:
            raise ValueError(f"[{dataset_name}] Dataset dataframe must include features and a target column (only {len(df.columns)} columns after processing)")
        
        if "target" not in df.columns:
            raise ValueError(f"[{dataset_name}] Target column 'target' not found after processing. Columns: {list(df.columns)}")
        
        # Convert categorical columns to numeric using label encoding
        for col in df.columns:
            if col != "target" and df[col].dtype == 'object':
                # Simple label encoding for categorical variables
                unique_vals = df[col].unique()
                val_map = {val: i for i, val in enumerate(unique_vals)}
                df[col] = df[col].map(val_map)
        
        # Convert all feature columns to numeric, coercing errors
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values
        before_dropna = len(df)
        df.dropna(inplace=True)
        if before_dropna > len(df):
            print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")

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
    ds = EducationDropoutDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 