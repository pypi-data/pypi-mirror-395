import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BlogFeedbackDataset(BaseDatasetLoader):
    """Blog Feedback dataset: predict blog comments from content features."""

    def get_dataset_info(self):
        return {
            'name': 'BlogFeedbackDataset',
            'source_id': 'uci:blogfeedback',
            'category': 'regression',
            'description': 'Blog Feedback dataset: predict blog comments from content features.',
            'target_column': 'comments'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00304/BlogFeedback.zip"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            # Extract CSV from zip
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                # The training data is in blogData_train.csv
                if 'blogData_train.csv' in z.namelist():
                    with z.open('blogData_train.csv') as f:
                        return f.read()
            raise Exception("blogData_train.csv not found in zip")
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Set column names, as the file has none
        # 50 features are page stats, 5 are text-based, 1 is weekday, 1 is parent stats, then target
        base_features = [f'feat_{i}' for i in range(1, 281)] # Based on description, many features
        df.columns = base_features + ['target']

        # Set target
        if 'comments' in df.columns: # Keep for compatibility, but it won't exist with the above naming
            df['target'] = df['comments']
            df = df.drop('comments', axis=1)
        
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
    ds = BlogFeedbackDataset()
    frame = ds.get_data()
    print(frame.head())
