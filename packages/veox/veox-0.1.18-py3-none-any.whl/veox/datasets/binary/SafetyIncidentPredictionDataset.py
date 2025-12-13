import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SafetyIncidentPredictionDataset(BaseDatasetLoader):
    """
    Safety Incident Prediction Dataset (binary classification)
    Source: Kaggle - Workplace Injury Dataset
    Target: injury_occurred (0=no injury, 1=injury)
    
    This dataset contains workplace safety data for predicting injuries.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'SafetyIncidentPredictionDataset',
            'source_id': 'kaggle:workplace-injury',
            'category': 'binary_classification',
            'description': 'Workplace injury prediction from safety and operational data.',
            'source_url': 'https://www.kaggle.com/datasets/ihmstefanini/industrial-safety-and-health-analytics-database',
        }
    
    def download_dataset(self, info):
        """Download the safety incident dataset from Kaggle"""
        print(f"[SafetyIncidentPredictionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[SafetyIncidentPredictionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'ihmstefanini/industrial-safety-and-health-analytics-database',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if csv_files:
                    data_file = csv_files[0]
                    print(f"[SafetyIncidentPredictionDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=10000)
                    print(f"[SafetyIncidentPredictionDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[SafetyIncidentPredictionDataset] Kaggle download failed: {e}")
            
            # Try alternative Kaggle dataset
            try:
                print("[SafetyIncidentPredictionDataset] Trying alternative dataset...")
                kaggle.api.dataset_download_files(
                    'bobbyscience/employee-safety-and-health-in-mining-industry',
                    path=temp_dir,
                    unzip=True
                )
                
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if csv_files:
                    data_file = csv_files[0]
                    print(f"[SafetyIncidentPredictionDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file)
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                    
            except Exception as e2:
                print(f"[SafetyIncidentPredictionDataset] Alternative download also failed: {e2}")
                raise Exception("Could not download any safety dataset from Kaggle")
    
    def process_dataframe(self, df, info):
        """Process the safety incident dataset"""
        print(f"[SafetyIncidentPredictionDataset] Raw shape: {df.shape}")
        print(f"[SafetyIncidentPredictionDataset] Columns: {list(df.columns)}")
        
        # Find incident/injury/accident columns
        target_col = None
        injury_keywords = ['injury', 'accident', 'incident', 'injured', 'accident_type', 
                          'injury_type', 'severity', 'fatality', 'death']
        
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in injury_keywords):
                target_col = col
                print(f"[SafetyIncidentPredictionDataset] Found potential target column: {col}")
                break
        
        if target_col:
            # Convert to binary target
            if df[target_col].dtype == 'object':
                # Text values - any non-empty/non-'none' value indicates injury
                unique_vals = df[target_col].unique()
                print(f"[SafetyIncidentPredictionDataset] Unique values in {target_col}: {unique_vals}")
                
                # Map accident levels to binary
                # Common patterns: 'I' (minor), 'II' (moderate), 'III' (severe), 'IV' (fatal), 'V' (catastrophic)
                # Or numeric levels: 0, 1, 2, 3, 4, 5
                # For binary classification: 0 = no accident/minor, 1 = significant accident
                
                df['target'] = df[target_col].apply(
                    lambda x: 0 if pd.isna(x) or str(x).strip().lower() in ['', 'none', 'no', 'nan', '0', 'no injury', 'i', '1'] else 1
                )
            else:
                # Numeric - 0 or 1 = no/minor accident, > 1 = significant accident
                df['target'] = (df[target_col] > 1).astype(int)
            
            df = df.drop(target_col, axis=1)
        else:
            # No clear target column - look for severity or create from other indicators
            print("[SafetyIncidentPredictionDataset] No clear target column found, creating from indicators...")
            
            # Look for columns that might indicate incidents
            incident_indicators = []
            for col in df.columns:
                col_lower = col.lower()
                if any(term in col_lower for term in ['days_lost', 'days_away', 'restricted', 'medical']):
                    incident_indicators.append(col)
            
            if incident_indicators:
                print(f"[SafetyIncidentPredictionDataset] Using indicators: {incident_indicators}")
                # Any positive value in these columns indicates an incident
                df['target'] = (df[incident_indicators].fillna(0).sum(axis=1) > 0).astype(int)
            else:
                raise ValueError("Could not determine target column for safety incidents")
        
        # Remove non-feature columns
        drop_cols = ['date', 'time', 'description', 'narrative', 'name', 'id', 'report_id',
                    'employee_id', 'location', 'address', 'city', 'state', 'country']
        
        for col in df.columns:
            if col != 'target':
                col_lower = col.lower()
                if any(drop_term in col_lower for drop_term in drop_cols):
                    print(f"[SafetyIncidentPredictionDataset] Dropping column: {col}")
                    df = df.drop(col, axis=1)
        
        # Convert categorical columns to numeric
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                # Try to convert to numeric first
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # If still object, use label encoding
                if df[col].dtype == 'object':
                    print(f"[SafetyIncidentPredictionDataset] Encoding categorical column: {col}")
                    df[col] = pd.Categorical(df[col]).codes
        
        # Select only numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' not in numeric_cols:
            numeric_cols.append('target')
        df = df[numeric_cols]
        
        # Handle missing values
        for col in df.columns:
            if col != 'target':
                df[col] = df[col].fillna(df[col].median() if df[col].notna().any() else 0)
        
        # Drop rows with missing target
        df = df.dropna(subset=['target'])
        
        # Ensure target is binary
        df['target'] = df['target'].astype(int)
        df = df[df['target'].isin([0, 1])]
        
        # Limit features if too many
        feature_cols = [col for col in df.columns if col != 'target']
        if len(feature_cols) > 40:
            # Keep most variable features
            variances = df[feature_cols].var()
            top_features = variances.nlargest(40).index.tolist()
            df = df[top_features + ['target']]
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Check class balance
        target_counts = df['target'].value_counts()
        print(f"[SafetyIncidentPredictionDataset] Target distribution: {target_counts.to_dict()}")
        
        # If severely imbalanced, balance it
        if len(target_counts) == 2:
            minority_class = target_counts.idxmin()
            majority_class = target_counts.idxmax()
            
            if target_counts[minority_class] < target_counts[majority_class] * 0.1:
                # Undersample majority class
                n_minority = target_counts[minority_class]
                n_majority = min(n_minority * 5, target_counts[majority_class])
                
                df_minority = df[df['target'] == minority_class]
                df_majority = df[df['target'] == majority_class].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[SafetyIncidentPredictionDataset] Final shape: {df.shape}")
        print(f"[SafetyIncidentPredictionDataset] Injury rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = SafetyIncidentPredictionDataset()
    df = dataset.get_data()
    print(f"Loaded SafetyIncidentPredictionDataset: {df.shape}")
    print(df.head()) 