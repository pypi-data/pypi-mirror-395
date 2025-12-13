import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SteelPlateDefectsDataset(BaseDatasetLoader):
    """
    Steel Plate Defects Dataset (binary classification)
    Source: Kaggle - Steel Plates Faults
    Target: Has defect (0=No, 1=Yes)
    
    Real-world dataset from steel manufacturing containing measurements
    of steel plates. We convert the multi-class fault types to binary.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'SteelPlateDefectsDataset',
            'source_id': 'kaggle:steel-plates-faults-binary',
            'category': 'binary_classification',
            'description': 'Detect defects in steel plates based on measurements (binary).',
            'source_url': 'https://www.kaggle.com/datasets/uciml/faulty-steel-plates',
        }
    
    def download_dataset(self, info):
        """Download the steel plates dataset from Kaggle"""
        print(f"[SteelPlateDefectsDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'uciml/faulty-steel-plates',
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
            print(f"[SteelPlateDefectsDataset] Error: {e}")
            raise e
    
    def process_dataframe(self, df, info):
        """Process the steel plates dataset"""
        print(f"[SteelPlateDefectsDataset] Raw shape: {df.shape}")
        
        # The dataset has 7 fault type columns at the end
        # We'll create a binary target: 0 = no defect, 1 = any defect
        fault_columns = []
        
        # Find binary columns (fault indicators)
        for col in df.columns:
            if df[col].isin([0, 1]).all() and df[col].sum() > 0:
                fault_columns.append(col)
        
        # Take the last 7 columns if they look like fault indicators
        if len(fault_columns) >= 7:
            fault_columns = fault_columns[-7:]
            # Create binary target: any fault present
            df['target'] = (df[fault_columns].sum(axis=1) > 0).astype(int)
            # Drop the original fault columns
            df = df.drop(columns=fault_columns)
        else:
            # Fallback: use the last column as target
            last_col = df.columns[-1]
            df['target'] = (df[last_col] > 0).astype(int)
            if last_col != 'target':
                df = df.drop(columns=[last_col])
        
        # Ensure all remaining columns are numeric
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any missing values
        df = df.dropna()
        
        # Ensure target is binary
        df['target'] = df['target'].astype(int)
        
        # Move target to last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Shuffle the data
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[SteelPlateDefectsDataset] Final shape: {df.shape}")
        print(f"[SteelPlateDefectsDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[SteelPlateDefectsDataset] Defect rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = SteelPlateDefectsDataset()
    df = dataset.get_data()
    print(f"Loaded SteelPlateDefectsDataset: {df.shape}")
    print(df.head()) 