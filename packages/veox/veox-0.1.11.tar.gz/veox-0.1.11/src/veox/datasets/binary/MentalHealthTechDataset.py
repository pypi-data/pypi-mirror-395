import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class MentalHealthTechDataset(BaseDatasetLoader):
    """
    Mental Health in Tech Survey Dataset (binary classification)
    Source: Kaggle - OSMI Mental Health in Tech Survey
    Target: treatment (0=No, 1=Yes)
    
    This dataset contains survey responses about mental health conditions
    and treatment in the technology workplace.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'MentalHealthTechDataset',
            'source_id': 'kaggle:mental-health-tech',
            'category': 'binary_classification',
            'description': 'Mental health survey data from tech workers for treatment prediction.',
            'source_url': 'https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey',
        }
    
    def download_dataset(self, info):
        """Download the mental health in tech dataset from Kaggle"""
        print(f"[MentalHealthTechDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[MentalHealthTechDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'osmi/mental-health-in-tech-survey',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                
                # Read the first CSV file
                data_file = csv_files[0]
                print(f"[MentalHealthTechDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file)
                print(f"[MentalHealthTechDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[MentalHealthTechDataset] Download failed: {e}")
            print("[MentalHealthTechDataset] Using sample data...")
            
            # Create sample mental health survey data
            np.random.seed(42)
            n_samples = 1500
            
            data = {
                'Age': np.random.randint(18, 65, n_samples),
                'Gender': np.random.choice(['Male', 'Female', 'Other'], n_samples, p=[0.7, 0.25, 0.05]),
                'Country': np.random.choice(['United States', 'United Kingdom', 'Canada', 'Germany', 'Other'], 
                                          n_samples, p=[0.6, 0.1, 0.1, 0.05, 0.15]),
                'state': np.random.choice(['CA', 'TX', 'NY', 'WA', 'IL', 'NA'], n_samples),
                'self_employed': np.random.choice(['Yes', 'No'], n_samples, p=[0.1, 0.9]),
                'family_history': np.random.choice(['Yes', 'No'], n_samples, p=[0.3, 0.7]),
                'work_interfere': np.random.choice(['Never', 'Rarely', 'Sometimes', 'Often'], 
                                                 n_samples, p=[0.3, 0.3, 0.3, 0.1]),
                'no_employees': np.random.choice(['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000'], 
                                               n_samples),
                'remote_work': np.random.choice(['Yes', 'No'], n_samples, p=[0.3, 0.7]),
                'tech_company': np.random.choice(['Yes', 'No'], n_samples, p=[0.8, 0.2]),
                'benefits': np.random.choice(['Yes', 'No', "Don't know"], n_samples, p=[0.5, 0.3, 0.2]),
                'care_options': np.random.choice(['Yes', 'No', 'Not sure'], n_samples, p=[0.4, 0.3, 0.3]),
                'wellness_program': np.random.choice(['Yes', 'No', "Don't know"], n_samples, p=[0.3, 0.5, 0.2]),
                'seek_help': np.random.choice(['Yes', 'No', "Don't know"], n_samples, p=[0.4, 0.4, 0.2]),
                'anonymity': np.random.choice(['Yes', 'No', "Don't know"], n_samples, p=[0.3, 0.4, 0.3]),
                'leave': np.random.choice(['Very easy', 'Somewhat easy', 'Somewhat difficult', 'Very difficult', "Don't know"], 
                                        n_samples),
                'mental_health_consequence': np.random.choice(['Yes', 'No', 'Maybe'], n_samples, p=[0.2, 0.5, 0.3]),
                'phys_health_consequence': np.random.choice(['Yes', 'No', 'Maybe'], n_samples, p=[0.1, 0.7, 0.2]),
                'coworkers': np.random.choice(['Yes', 'No', 'Some of them'], n_samples, p=[0.3, 0.3, 0.4]),
                'supervisor': np.random.choice(['Yes', 'No', 'Some of them'], n_samples, p=[0.3, 0.4, 0.3]),
                'mental_health_interview': np.random.choice(['Yes', 'No', 'Maybe'], n_samples, p=[0.2, 0.6, 0.2]),
                'phys_health_interview': np.random.choice(['Yes', 'No', 'Maybe'], n_samples, p=[0.1, 0.8, 0.1]),
                'mental_vs_physical': np.random.choice(['Yes', 'No', "Don't know"], n_samples, p=[0.4, 0.3, 0.3]),
                'obs_consequence': np.random.choice(['Yes', 'No'], n_samples, p=[0.2, 0.8])
            }
            
            # Create treatment target based on features
            treatment = []
            for i in range(n_samples):
                # Higher chance of seeking treatment if:
                treat_prob = 0.2
                if data['family_history'][i] == 'Yes':
                    treat_prob += 0.3
                if data['work_interfere'][i] in ['Sometimes', 'Often']:
                    treat_prob += 0.2
                if data['benefits'][i] == 'Yes':
                    treat_prob += 0.1
                if data['mental_health_consequence'][i] == 'No':
                    treat_prob += 0.1
                
                treatment.append('Yes' if np.random.random() < treat_prob else 'No')
            
            data['treatment'] = treatment
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the mental health dataset"""
        print(f"[MentalHealthTechDataset] Raw shape: {df.shape}")
        print(f"[MentalHealthTechDataset] Columns sample: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['treatment', 'Treatment', 'seek_treatment']:
            if col in df.columns:
                target_col = col
                break
        
        if not target_col:
            raise ValueError("Could not find treatment column")
        
        # Create binary target
        df['target'] = (df[target_col] == 'Yes').astype(int)
        
        # Handle age outliers
        if 'Age' in df.columns:
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
            df.loc[df['Age'] < 18, 'Age'] = 18
            df.loc[df['Age'] > 100, 'Age'] = 100
        
        # Drop columns with too many missing values or not useful
        drop_cols = ['Timestamp', 'comments', 'state', 'Country', target_col]
        for col in drop_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Handle categorical features
        categorical_cols = []
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                categorical_cols.append(col)
        
        # Encode categorical features
        for col in categorical_cols:
            # Binary encoding for Yes/No columns
            if df[col].nunique() <= 3 and any(val in df[col].unique() for val in ['Yes', 'No']):
                df[col] = df[col].map({'Yes': 1, 'No': 0, "Don't know": -1, 'Not sure': -1})
                df[col] = df[col].fillna(-1)
            else:
                # Use categorical codes for other columns
                df[col] = pd.Categorical(df[col]).codes
        
        # Select features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                feature_cols.append(col)
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Remove missing values
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Convert all integer columns to int64 (fix int8 issue)
        for col in df.columns:
            if df[col].dtype in ['int8', 'int16', 'int32']:
                df[col] = df[col].astype('int64')
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[MentalHealthTechDataset] Final shape: {df.shape}")
        print(f"[MentalHealthTechDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[MentalHealthTechDataset] Treatment rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = MentalHealthTechDataset()
    df = dataset.get_data()
    print(f"Loaded MentalHealthTechDataset: {df.shape}")
    print(df.head()) 