import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class YachtHydrodynamicsDataset(BaseDatasetLoader):
    """Yacht Hydrodynamics dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'YachtHydrodynamicsDataset',
            'source_id': 'uci:yacht_hydrodynamics',
            'category': 'regression',
            'description': 'Yacht Hydrodynamics dataset: predict yacht residuary resistance from hull dimensions.',
            'target_column': 'residuary_resistance'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00243/yacht_hydrodynamics.data"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Handle whitespace separated format
        if df.shape[1] == 1:
            lines = df.iloc[:, 0].astype(str).tolist()
            data = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) == 7:
                        data.append(parts)
            df = pd.DataFrame(data)
        
        # Set column names
        df.columns = ['longitudinal_position', 'prismatic_coefficient', 'length_displacement_ratio',
                     'beam_draught_ratio', 'length_beam_ratio', 'froude_number', 'residuary_resistance']
        
        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set target
        df['target'] = df['residuary_resistance']
        df = df.drop('residuary_resistance', axis=1)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.3f}-{df['target'].max():.3f}")
        return df 

if __name__ == "__main__":
    ds = YachtHydrodynamicsDataset()
    frame = ds.get_data()
    print(frame.head()) 