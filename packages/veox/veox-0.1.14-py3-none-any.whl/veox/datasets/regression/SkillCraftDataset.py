import pandas as pd
import requests
import io

from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SkillCraftDataset(BaseDatasetLoader):
    """SkillCraft1 dataset: predict gaming performance from behavioral metrics."""

    def get_dataset_info(self):
        return {
            'name': 'SkillCraftDataset',
            'source_id': 'uci:skillcraft1',
            'category': 'regression',
            'description': 'SkillCraft1 dataset: predict gaming performance from behavioral metrics.',
            'target_column': 'LeagueIndex'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00272/SkillCraft1_Dataset.csv"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Set target
        if 'LeagueIndex' in df.columns:
            df['target'] = df['LeagueIndex']
            df = df.drop('LeagueIndex', axis=1)
        else:
            # Use last column as target
            df['target'] = df.iloc[:, -1]
            df = df.iloc[:, :-1]
        
        # Convert categorical columns to numeric
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = pd.Categorical(df[col]).codes
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.2f}-{df['target'].max():.2f}")
        return df

if __name__ == "__main__":
    ds = SkillCraftDataset()
    frame = ds.get_data()
    print(frame.head())
