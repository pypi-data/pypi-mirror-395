import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BeijingMultiDataset(BaseDatasetLoader):
    """Beijing Multi-site PM2.5 dataset: predict air pollution from meteorological data."""

    def get_dataset_info(self):
        return {
            'name': 'BeijingMultiDataset',
            'source_id': 'uci:beijing_multi_pm25',
            'category': 'regression',
            'description': 'Beijing Multi-site PM2.5 dataset: predict air pollution from meteorological data.',
            'target_column': 'PM2.5'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00501/PRSA2017_Data_20130301-20170228.zip"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            # Extract from zip
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                all_dfs = []
                for f_name in z.namelist():
                    if f_name.endswith('.csv'):
                        with z.open(f_name) as f:
                            all_dfs.append(pd.read_csv(f))
                
                if all_dfs:
                    combined_df = pd.concat(all_dfs, ignore_index=True)
                    csv_buffer = io.StringIO()
                    combined_df.to_csv(csv_buffer, index=False)
                    return csv_buffer.getvalue().encode('utf-8')

            raise Exception("No CSV files found in zip")

        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Convert all columns to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Set target - use first numeric column as target if specified target not found
        if 'PM2.5' in df.columns:
            df['target'] = df['PM2.5']
            df = df.drop('PM2.5', axis=1)
        else:
            # Use last numeric column as target
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                df['target'] = df[numeric_cols[-1]]
                df = df.drop(numeric_cols[-1], axis=1)
        
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
    ds = BeijingMultiDataset()
    frame = ds.get_data()
    print(frame.head())
