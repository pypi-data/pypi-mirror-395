import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SteelFatigueDataset(BaseDatasetLoader):
    """
    Steel Fatigue Dataset (regression)
    Source: Kaggle - Steel Industry Energy Consumption
    Target: Usage_kWh (energy consumption as proxy for material stress)
    
    Real-world dataset from steel industry containing production parameters
    and energy consumption data which correlates with material processing stress.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'SteelFatigueDataset',
            'source_id': 'kaggle:steel-industry-energy',
            'category': 'regression',
            'description': 'Predict steel processing energy consumption from production parameters.',
            'source_url': 'https://www.kaggle.com/datasets/csafrit2/steel-industry-energy-consumption',
        }
    
    def download_dataset(self, info):
        """Download the steel industry dataset from Kaggle"""
        print(f"[SteelFatigueDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'csafrit2/steel-industry-energy-consumption',
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
            print(f"[SteelFatigueDataset] Error: {e}")
            raise e
    
    def process_dataframe(self, df, info):
        """Process the steel industry dataset"""
        print(f"[SteelFatigueDataset] Raw shape: {df.shape}")
        
        # Identify target column
        target_candidates = ['Usage_kWh', 'usage_kwh', 'energy_consumption', 'power_usage']
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
        
        if not target_col:
            # Look for columns containing 'usage' or 'kwh'
            for col in df.columns:
                if 'usage' in col.lower() or 'kwh' in col.lower():
                    target_col = col
                    break
        
        if target_col:
            df['target'] = df[target_col]
            if target_col != 'target':
                df = df.drop(columns=[target_col])
        else:
            # Use last numeric column as target
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                df['target'] = df[numeric_cols[-1]]
                df = df.drop(columns=[numeric_cols[-1]])
        
        # Drop date/time columns if present
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_cols:
            df = df.drop(columns=date_cols)
        
        # Handle categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col != 'target':
                df[col] = pd.Categorical(df[col]).codes
        
        # Ensure all columns are numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any missing values
        df = df.dropna()
        
        # Move target to last column
        if 'target' in df.columns:
            cols = [col for col in df.columns if col != 'target'] + ['target']
            df = df[cols]
        
        # Shuffle the data
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[SteelFatigueDataset] Final shape: {df.shape}")
        if 'target' in df.columns:
            print(f"[SteelFatigueDataset] Target range: [{df['target'].min():.1f}, {df['target'].max():.1f}] kWh")
        
        return df

if __name__ == "__main__":
    dataset = SteelFatigueDataset()
    df = dataset.get_data()
    print(f"Loaded SteelFatigueDataset: {df.shape}")
    print(df.head()) 