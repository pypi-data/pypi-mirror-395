import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class HeartDiseaseDataset(BaseDatasetLoader):
    """
    Heart Disease dataset from UCI repository (Cleveland database).
    
    This dataset contains 303 instances with 14 attributes used to predict
    the presence of heart disease in patients. The original dataset has 5 classes
    (0-4) indicating severity, but we convert it to binary classification:
    0 = no disease, 1-4 = presence of disease.
    
    Features include age, sex, chest pain type, blood pressure, cholesterol, etc.
    Target: Binary (0: no heart disease, 1: heart disease present)
    """
    
    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'HeartDiseaseDataset',
            'source_id': 'uci:heart_disease_cleveland',  # Unique identifier
            'category': 'binary_classification',
            'description': 'Heart Disease dataset: binary classification to predict presence of heart disease.',
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository"""
        dataset_name = info['name']
        # Using the processed Cleveland dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            # Some environments inject invalid HTTPS proxy placeholders (e.g. "${HTTPS_PROXY:-}")
            # into the environment, which causes requests/urllib3 to fail URL parsing.
            # Use a dedicated Session with trust_env=False so we ignore env proxies entirely.
            session = requests.Session()
            session.trust_env = False
            r = session.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            # Validate file size (expecting ~18 KB)
            if file_size < 10000:  # 10 KB as a simple threshold
                first_lines = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. First few lines:\n{os.linesep.join(first_lines)}")
                raise Exception(f"Downloaded file too small: {file_size} bytes. Expected >10 KB.")
                
            return r.content
        except Exception as exc:
            print(f"[{dataset_name}] Download failed: {exc}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form. Assumes the LAST column is the binary target."""
        dataset_name = info['name']

        # ------------------------------------------------------------------
        # 1. Force column names – the raw UCI file has **no header**. When the
        #    loader later hits the local CSV cache, pandas will incorrectly
        #    treat the first data row as a header, breaking the original
        #    numeric-column test and causing the `target` column to vanish.
        #    The simplest and safest fix is to **always** overwrite the
        #    DataFrame's columns, regardless of how it was read.
        # ------------------------------------------------------------------
        columns = [
            'age',           # age in years
            'sex',           # sex (1 = male; 0 = female)
            'cp',            # chest pain type (1-4)
            'trestbps',      # resting blood pressure
            'chol',          # serum cholesterol in mg/dl
            'fbs',           # fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
            'restecg',       # resting electrocardiographic results (0-2)
            'thalach',       # maximum heart rate achieved
            'exang',         # exercise induced angina (1 = yes; 0 = no)
            'oldpeak',       # ST depression induced by exercise relative to rest
            'slope',         # slope of the peak exercise ST segment
            'ca',            # number of major vessels (0-3) colored by fluoroscopy
            'thal',          # thalassemia (3 = normal; 6 = fixed defect; 7 = reversable defect)
            'target'         # 0-4 diagnosis value (we will binarise below)
        ]

        if df.shape[1] != len(columns):
            print(f"[{dataset_name}] Warning: Expected {len(columns)} columns but got {df.shape[1]}. Will attempt to coerce.")
            # If there are too many columns, drop extras; if too few, add dummies
            if df.shape[1] > len(columns):
                df = df.iloc[:, :len(columns)]
            else:
                # Pad with NaNs for missing columns
                for _ in range(len(columns) - df.shape[1]):
                    df[df.shape[1]] = pd.NA
        # Assign the canonical headers
        df.columns = columns

        # ------------------------------------------------------------------
        # 2. Basic logging
        # ------------------------------------------------------------------
        print(f"[{dataset_name}] DataFrame shape after header fix: {df.shape}")
        print(f"[{dataset_name}] First 3 rows:\n{df.head(3).to_string()}")

        # ------------------------------------------------------------------
        # 3. Replace string '?' with NA and coerce numeric columns
        # ------------------------------------------------------------------
        df.replace('?', pd.NA, inplace=True)

        numeric_cols = [c for c in df.columns if c != 'target']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        df['target'] = pd.to_numeric(df['target'], errors='coerce')

        # ------------------------------------------------------------------
        # 4. Binarise target: 0 -> 0, 1–4 -> 1
        # ------------------------------------------------------------------
        df['target'] = df['target'].apply(lambda x: 0 if x == 0 else 1 if pd.notna(x) else pd.NA)

        # ------------------------------------------------------------------
        # 5. Drop rows with any missing values
        # ------------------------------------------------------------------
        before_drop = len(df)
        df.dropna(inplace=True)
        print(f"[{dataset_name}] Dropped {before_drop - len(df)} rows containing NA values")

        # ------------------------------------------------------------------
        # 6. Cast target to int and shuffle
        # ------------------------------------------------------------------
        df['target'] = df['target'].astype(int)
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        target_counts = df['target'].value_counts()
        print(f"[{dataset_name}] Target distribution after cleaning: {target_counts.to_dict()}")

        return df

# For testing
if __name__ == "__main__":
    dataset = HeartDiseaseDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 