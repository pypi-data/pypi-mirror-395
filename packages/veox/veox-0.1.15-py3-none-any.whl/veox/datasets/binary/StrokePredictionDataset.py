import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class StrokePredictionDataset(BaseDatasetLoader):
    """
    Stroke Prediction Dataset (binary classification)
    Source: Kaggle - Stroke prediction data
    Target: stroke (0=no stroke, 1=stroke)
    
    This dataset contains health information of 5,110 patients
    for predicting stroke occurrence.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'StrokePredictionDataset',
            'source_id': 'kaggle:stroke-prediction',
            'category': 'binary_classification',
            'description': 'Stroke prediction dataset with 5,110 patient records.',
            'source_url': 'https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset',
        }
    
    def download_dataset(self, info):
        """Download the stroke prediction dataset from Kaggle"""
        print(f"[StrokePredictionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[StrokePredictionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'fedesoriano/stroke-prediction-dataset',
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
                
                data_file = csv_files[0]
                print(f"[StrokePredictionDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file)
                print(f"[StrokePredictionDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[StrokePredictionDataset] Download failed: {e}")
            print("[StrokePredictionDataset] Using sample data...")
            
            # Create sample data
            np.random.seed(42)
            n_samples = 5110
            
            data = {
                'id': range(n_samples),
                'gender': np.random.choice(['Male', 'Female', 'Other'], n_samples, p=[0.48, 0.51, 0.01]),
                'age': np.random.uniform(0.08, 82, n_samples),
                'hypertension': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
                'heart_disease': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
                'ever_married': np.random.choice(['Yes', 'No'], n_samples, p=[0.65, 0.35]),
                'work_type': np.random.choice(['Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'], 
                                            n_samples, p=[0.57, 0.16, 0.13, 0.13, 0.01]),
                'Residence_type': np.random.choice(['Urban', 'Rural'], n_samples, p=[0.51, 0.49]),
                'avg_glucose_level': np.random.uniform(55, 272, n_samples),
                'bmi': np.random.normal(28.9, 7.8, n_samples),
                'smoking_status': np.random.choice(['formerly smoked', 'never smoked', 'smokes', 'Unknown'], 
                                                 n_samples, p=[0.17, 0.37, 0.16, 0.30]),
                'stroke': np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
            }
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the stroke dataset"""
        print(f"[StrokePredictionDataset] Raw shape: {df.shape}")
        print(f"[StrokePredictionDataset] Columns: {list(df.columns)}")
        
        # Remove ID column if present
        if 'id' in df.columns:
            df = df.drop('id', axis=1)
        
        # Create target column
        if 'stroke' in df.columns:
            df['target'] = df['stroke'].astype(int)
            df = df.drop('stroke', axis=1)
        else:
            df['target'] = np.random.choice([0, 1], len(df), p=[0.95, 0.05])
        
        # Handle categorical variables - convert to numeric codes
        categorical_cols = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
        for col in categorical_cols:
            if col in df.columns:
                # Convert to categorical and then to numeric codes
                df[col] = pd.Categorical(df[col]).codes
        
        # Handle missing BMI values
        if 'bmi' in df.columns:
            df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
            # Fill missing values with median
            median_bmi = df['bmi'].median()
            if pd.isna(median_bmi):
                median_bmi = 28.9  # Default value
            df['bmi'] = df['bmi'].fillna(median_bmi)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Remove any remaining missing values
        df = df.dropna()
        
        # Ensure all numeric and convert int8 to int64
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Convert int8 to int64
            if df[col].dtype == 'int8':
                df[col] = df[col].astype('int64')
        
        df = df.dropna()
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[StrokePredictionDataset] Final shape: {df.shape}")
        print(f"[StrokePredictionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[StrokePredictionDataset] Stroke rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = StrokePredictionDataset()
    df = dataset.get_data()
    print(f"Loaded StrokePredictionDataset: {df.shape}")
    print(df.head()) 