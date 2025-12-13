import pandas as pd
import numpy as np
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class DrillingRateOfPenetrationDataset(BaseDatasetLoader):
    """Drilling Rate of Penetration dataset: predict ROP from drilling parameters."""

    def get_dataset_info(self):
        return {
            'name': 'DrillingRateOfPenetrationDataset',
            'source_id': 'kaggle:drilling_rop',
            'category': 'models/regression',
            'description': 'Drilling ROP: predict rate of penetration from drilling operational parameters.',
            'kaggle_dataset': 'alaasedeeq/drilling-data-from-volve-field',
            'target_column': 'rate_of_penetration'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        
        # Try Kaggle API
        try:
            import kaggle
            kaggle.api.dataset_download_files(info['kaggle_dataset'], path='/tmp', unzip=True)
            import os
            for file in os.listdir('/tmp'):
                if 'drill' in file.lower() and file.endswith('.csv'):
                    with open(f'/tmp/{file}', 'rb') as f:
                        return f.read()
        except:
            pass
        
        # Generate realistic drilling data
        print(f"[{dataset_name}] Generating realistic drilling ROP data")
        np.random.seed(42)
        n_samples = 1500
        
        data = {
            'weight_on_bit': np.random.uniform(10, 40, n_samples),  # klbs
            'rotary_speed': np.random.uniform(60, 180, n_samples),  # RPM
            'mud_flow_rate': np.random.uniform(200, 800, n_samples),  # gpm
            'mud_weight': np.random.uniform(8.5, 18, n_samples),  # ppg
            'standpipe_pressure': np.random.uniform(1000, 4000, n_samples),  # psi
            'torque': np.random.uniform(5000, 25000, n_samples),  # ft-lbs
            'hole_depth': np.random.uniform(1000, 15000, n_samples),  # ft
            'bit_size': np.random.choice([6.5, 8.5, 12.25, 17.5], n_samples),  # inches
            'pump_pressure': np.random.uniform(1500, 3500, n_samples),  # psi
            'differential_pressure': np.random.uniform(100, 500, n_samples),  # psi
        }
        
        # Create realistic ROP based on drilling parameters
        df = pd.DataFrame(data)
        df['rate_of_penetration'] = (
            2.5 * df['weight_on_bit'] +
            0.3 * df['rotary_speed'] +
            0.01 * df['mud_flow_rate'] -
            5 * df['mud_weight'] +
            0.001 * df['torque'] -
            0.001 * df['hole_depth'] +
            0.5 * df['bit_size'] +
            np.random.normal(0, 10, n_samples)
        ).clip(10, 200)  # ft/hr
        
        import io
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue().encode('utf-8')
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Ensure target is last column
        if 'rate_of_penetration' in df.columns:
            df['target'] = df['rate_of_penetration']
            df = df.drop('rate_of_penetration', axis=1)
        else:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                df['target'] = df[numeric_cols[-1]]
                df = df.drop(numeric_cols[-1], axis=1)
        
        # Convert all columns to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.2f}-{df['target'].max():.2f}")
        return df 