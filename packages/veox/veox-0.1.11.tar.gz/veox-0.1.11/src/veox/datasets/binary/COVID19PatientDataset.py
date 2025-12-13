import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class COVID19PatientDataset(BaseDatasetLoader):
    """
    COVID-19 Patient Pre-condition Dataset (binary classification)
    Source: Kaggle - COVID-19 patient pre-condition data
    Target: death (0=survived, 1=died)
    
    This dataset contains pre-existing conditions of COVID-19 patients
    and their survival outcomes.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'COVID19PatientDataset',
            'source_id': 'kaggle:covid19-patient-precondition',
            'category': 'binary_classification',
            'description': 'COVID-19 patient pre-condition data for mortality prediction.',
            'source_url': 'https://www.kaggle.com/datasets/tanmoyx/covid19-patient-precondition-dataset',
        }
    
    def download_dataset(self, info):
        """Download the COVID-19 patient dataset from Kaggle"""
        print(f"[COVID19PatientDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[COVID19PatientDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'tanmoyx/covid19-patient-precondition-dataset',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV file
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                
                # Read the first CSV file
                data_file = csv_files[0]
                print(f"[COVID19PatientDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file, encoding='latin-1')
                print(f"[COVID19PatientDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            # Strict: synthetic fallback is not allowed for Human datasets
            raise RuntimeError(
                f"[COVID19PatientDataset] Failed to download dataset from Kaggle: {e}. "
                "Synthetic fallback is disabled. Ensure this dataset is provisioned in S3 via admin APIs."
            )
    
    def process_dataframe(self, df, info):
        """Process the COVID-19 dataset"""
        print(f"[COVID19PatientDataset] Raw shape: {df.shape}")
        print(f"[COVID19PatientDataset] Columns: {list(df.columns)}")
        
        # Create binary target from date_died
        if 'date_died' in df.columns:
            df['target'] = (~df['date_died'].astype(str).str.contains('9999|99', na=False)).astype(int)
        elif 'died' in df.columns:
            df['target'] = df['died'].astype(int)
        else:
            raise ValueError("[COVID19PatientDataset] No suitable mortality indicator found in columns")
        
        # Select relevant features
        feature_cols = ['age', 'sex', 'patient_type', 'pneumonia', 'diabetes', 
                       'copd', 'asthma', 'inmsupr', 'hypertension', 
                       'cardiovascular', 'obesity', 'renal_chronic', 'tobacco']
        
        available_features = [col for col in feature_cols if col in df.columns]
        df = df[available_features + ['target']]
        
        # Convert categorical to numeric if needed
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                df[col] = pd.Categorical(df[col]).codes
        
        # Remove missing values
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[COVID19PatientDataset] Final shape: {df.shape}")
        print(f"[COVID19PatientDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[COVID19PatientDataset] Mortality rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = COVID19PatientDataset()
    df = dataset.get_data()
    print(f"Loaded COVID19PatientDataset: {df.shape}")
    print(df.head()) 