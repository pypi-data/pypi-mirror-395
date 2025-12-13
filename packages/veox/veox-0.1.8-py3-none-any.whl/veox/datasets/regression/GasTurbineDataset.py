import pandas as pd
import requests
import io
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class GasTurbineDataset(BaseDatasetLoader):
    """Gas Turbine dataset: predict turbine energy yield from operational parameters."""

    def get_dataset_info(self):
        return {
            'name': 'GasTurbineDataset',
            'source_id': 'uci:gas_turbine_co_nox',
            'category': 'regression',
            'description': 'Gas Turbine dataset: predict turbine energy yield from operational parameters.',
            'target_column': 'TEY'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00551/pp_gas_emission.zip"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            # Extract CSV from zip
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                # Find the correct csv file, could be gt_2011.csv, gt_2012.csv, etc.
                csv_files = [f for f in z.namelist() if f.endswith('.csv') and 'gt' in f]
                if csv_files:
                    all_dfs = []
                    for f_name in csv_files:
                        with z.open(f_name) as f:
                            all_dfs.append(pd.read_csv(f))
                    
                    if all_dfs:
                        combined_df = pd.concat(all_dfs, ignore_index=True)
                        csv_buffer = io.StringIO()
                        combined_df.to_csv(csv_buffer, index=False)
                        return csv_buffer.getvalue().encode('utf-8')

            raise Exception("No suitable CSV file found in zip")
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        
        # Set target
        if 'TEY' in df.columns:
            df['target'] = df['TEY']
            df = df.drop('TEY', axis=1)
        
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
    ds = GasTurbineDataset()
    frame = ds.get_data()
    print(frame.head())
