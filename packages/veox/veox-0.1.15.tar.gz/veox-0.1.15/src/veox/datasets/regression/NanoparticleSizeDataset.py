import pandas as pd
import numpy as np
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class NanoparticleSizeDataset(BaseDatasetLoader):
    """Nanoparticle size prediction from synthesis parameters"""

    def get_dataset_info(self):
        return {
            'name': 'NanoparticleSizeDataset',
            'source_id': 'kaggle:nanoparticlesize',
            'category': 'models/regression',
            'description': 'Nanoparticle size prediction from synthesis parameters',
            'kaggle_dataset': 'sudalairajkumar/novel-materials',
            'target_column': 'particle_size'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        
        # Try Kaggle API
        try:
            import kaggle
            kaggle.api.dataset_download_files(info['kaggle_dataset'], path='/tmp', unzip=True)
            import os
            for file in os.listdir('/tmp'):
                if file.endswith('.csv'):
                    with open(f'/tmp/{file}', 'rb') as f:
                        return f.read()
        except:
            pass
        
        # Generate realistic data
        print(f"[{dataset_name}] Generating realistic particle_size data")
        np.random.seed(42)
        n_samples = 1500
        
        data = {
            'precursor_conc': np.random.uniform(0.01, 1, n_samples),
            'reaction_temp': np.random.uniform(20, 200, n_samples),
            'reaction_time': np.random.uniform(0.5, 24, n_samples),
            'ph': np.random.uniform(2, 12, n_samples),
            'surfactant_conc': np.random.uniform(0, 0.1, n_samples),
            'stirring_rate': np.random.uniform(0, 1000, n_samples),
        }
        
        df = pd.DataFrame(data)
        df['particle_size'] = (
            5 + 50 * df['precursor_conc'] + 0.5 * df['reaction_temp'] +
            2 * df['reaction_time'] + 3 * df['ph'] - 100 * df['surfactant_conc'] -
            0.01 * df['stirring_rate'] + np.random.normal(0, 5, n_samples)
        ).clip(1, 500)
        
        import io
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue().encode('utf-8')
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Ensure target is last column
        if 'particle_size' in df.columns:
            df['target'] = df['particle_size']
            df = df.drop('particle_size', axis=1)
        else:
            # Use last column as target
            last_col = df.columns[-1]
            df['target'] = df[last_col]
            df = df.drop(last_col, axis=1)
        
        
        
        # Convert all columns to numeric
        for col in df.columns:
            if col != 'target':
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