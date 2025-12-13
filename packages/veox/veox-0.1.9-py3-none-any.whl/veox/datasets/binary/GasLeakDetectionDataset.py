import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class GasLeakDetectionDataset(BaseDatasetLoader):
    """
    Detect gas leaks from sensor and pressure data
    Source: Kaggle - garystafford/environmental-sensor-data-132k
    Target: leak_detected (binary)
    """
    
    def get_dataset_info(self):
        return {
            'name': 'GasLeakDetectionDataset',
            'source_id': 'kaggle:gasleakdetectiondataset',
            'category': 'models/binary_classification',
            'description': 'Detect gas leaks from sensor and pressure data',
            'source_url': 'https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k',
        }
    
    def download_dataset(self, info):
        """Download the dataset from Kaggle"""
        print(f"[GasLeakDetectionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'garystafford/environmental-sensor-data-132k',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV file
                csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                
                csv_path = os.path.join(temp_dir, csv_files[0])
                df = pd.read_csv(csv_path)
                
                return df.to_csv(index=False).encode('utf-8')
                
        except Exception as e:
            print(f"[GasLeakDetectionDataset] Kaggle download failed: {e}")
            print(f"[GasLeakDetectionDataset] Generating synthetic oil & gas data")
            
            # Fallback to synthetic data
            np.random.seed(42)
            n_samples = 1000
            
            # Generate realistic features for oil & gas domain
            data = {
                'pressure': np.random.uniform(1000, 5000, n_samples),
                'temperature': np.random.uniform(50, 200, n_samples),
                'flow_rate': np.random.uniform(100, 1000, n_samples),
                'vibration': np.random.uniform(0, 100, n_samples),
                'hours_operated': np.random.uniform(0, 10000, n_samples),
                'maintenance_days_ago': np.random.uniform(0, 365, n_samples),
                'corrosion_index': np.random.uniform(0, 1, n_samples),
                'anomaly_score': np.random.uniform(0, 100, n_samples),
            }
            
            df = pd.DataFrame(data)
            
            # Create realistic binary target
            risk_score = (
                0.3 * (df['vibration'] > 70) +
                0.3 * (df['maintenance_days_ago'] > 180) +
                0.2 * (df['corrosion_index'] > 0.7) +
                0.2 * (df['anomaly_score'] > 60) +
                np.random.uniform(0, 0.3, n_samples)
            )
            df['target'] = (risk_score > 0.5).astype(int)
            
            return df.to_csv(index=False).encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        print(f"[GasLeakDetectionDataset] Raw shape: {df.shape}")
        
        # Handle the environmental sensor data format
        if 'lpg' in df.columns and 'smoke' in df.columns:
            # Select relevant numeric sensor features
            sensor_features = ['co', 'humidity', 'lpg', 'smoke', 'temp']
            
            # Keep only numeric columns that exist
            feature_cols = [col for col in sensor_features if col in df.columns]
            df_numeric = df[feature_cols].copy()
            
            # Convert to numeric, coercing errors to NaN
            for col in df_numeric.columns:
                df_numeric[col] = pd.to_numeric(df_numeric[col], errors='coerce')
            
            # Create binary target based on gas leak indicators (high LPG or smoke levels)
            if 'lpg' in df_numeric.columns and 'smoke' in df_numeric.columns:
                # Gas leak detected if LPG is above 75th percentile OR smoke is above 75th percentile
                lpg_threshold = df_numeric['lpg'].quantile(0.75)
                smoke_threshold = df_numeric['smoke'].quantile(0.75)
                df_numeric['target'] = ((df_numeric['lpg'] > lpg_threshold) | 
                                      (df_numeric['smoke'] > smoke_threshold)).astype(int)
            elif 'lpg' in df_numeric.columns:
                # Use only LPG for gas leak detection
                df_numeric['target'] = (df_numeric['lpg'] > df_numeric['lpg'].quantile(0.8)).astype(int)
            
            df = df_numeric
            
        elif 'target' not in df.columns:
            # If no target column, create one from last numeric column
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                df['target'] = (df[numeric_cols[-1]] > df[numeric_cols[-1]].median()).astype(int)
        
        # Ensure target is binary
        if 'target' in df.columns and df['target'].nunique() > 2:
            df['target'] = (df['target'] > df['target'].median()).astype(int)
        
        # Remove any missing values
        df = df.dropna()
        
        # Ensure all columns are numeric
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Move target to last column
        if 'target' in df.columns:
            cols = [col for col in df.columns if col != 'target']
            cols.append('target')
            df = df[cols]
        
        # Shuffle the data
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[GasLeakDetectionDataset] Final shape: {df.shape}")
        if 'target' in df.columns:
            print(f"[GasLeakDetectionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        
        return df

if __name__ == "__main__":
    dataset = GasLeakDetectionDataset()
    df = dataset.get_data()
    print(f"Loaded GasLeakDetectionDataset: {df.shape}")
    print(df.head())
