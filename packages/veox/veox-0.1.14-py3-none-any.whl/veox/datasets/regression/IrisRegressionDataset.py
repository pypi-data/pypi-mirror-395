import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class IrisRegressionDataset(BaseDatasetLoader):
    """Iris Regression dataset: predict petal length from other measurements."""

    def get_dataset_info(self):
        return {
            'name': 'IrisRegressionDataset',
            'source_id': 'uci:iris_regression',
            'category': 'regression',
            'description': 'Iris Regression dataset: predict petal length from other measurements.',
            'target_column': 'petal_length'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
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
        
        # This dataset has no header.
        df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

        # Set target - petal_length
        if 'petal_length' in df.columns:
            df['target'] = df['petal_length']
            df = df.drop('petal_length', axis=1)
        else:
            raise ValueError("petal_length column not found for target.")

        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
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
    ds = IrisRegressionDataset()
    frame = ds.get_data()
    print(frame.head())
