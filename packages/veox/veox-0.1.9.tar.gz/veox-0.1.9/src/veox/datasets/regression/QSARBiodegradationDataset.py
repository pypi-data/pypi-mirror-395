import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class QSARBiodegradationDataset(BaseDatasetLoader):
    """QSAR Biodegradation dataset: predict biodegradation rate from molecular descriptors."""

    def get_dataset_info(self):
        return {
            'name': 'QSARBiodegradationDataset',
            'source_id': 'uci:qsar_biodegradation',
            'category': 'regression',
            'description': 'QSAR Biodegradation dataset: predict biodegradation rate from molecular descriptors.',
            'target_column': 'biodegradation_rate'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00254/biodeg.csv"
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
        
        # This dataset is semicolon-separated and has no header.
        # Handle the parsing correctly if it comes as single column
        if df.shape[1] == 1:
            # Read the raw text and split properly
            text_data = df.iloc[:, 0].astype(str)
            # Join all rows and split by newlines, then by semicolons
            full_text = '\n'.join(text_data)
            df = pd.read_csv(io.StringIO(full_text), sep=';', header=None, na_values=[''])

        print(f"[{dataset_name}] DataFrame shape after parsing: {df.shape}")
        print(f"[{dataset_name}] First few rows:\n{df.head()}")

        # This dataset has 41 features + 1 binary target (biodegradable/not biodegradable)
        # But we can treat it as regression by converting the binary to numeric
        if df.shape[1] >= 40:
            # Last column should be the target (biodegradable: RB/NRB or 1/0)
            target_col = df.columns[-1]
            
            # Convert target to numeric - handle text labels
            target_values = df[target_col]
            if target_values.dtype == 'object':
                # Convert RB/NRB to 1/0 or similar text patterns
                unique_vals = target_values.unique()
                print(f"[{dataset_name}] Unique target values: {unique_vals}")
                
                if 'RB' in str(unique_vals) or 'NRB' in str(unique_vals):
                    # RB = readily biodegradable (1), NRB = not readily biodegradable (0)
                    df[target_col] = df[target_col].map({'RB': 1.0, 'NRB': 0.0})
                else:
                    # Try to convert to numeric directly
                    df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
            
            df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
            
            # Name the feature columns
            feature_cols = [f'V{i}' for i in range(1, df.shape[1])]  # Exclude target
            df.columns = feature_cols + ['target']
        else:
            # Fallback - use all columns as features except last as target
            df['target'] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
            df = df.iloc[:, :-1]
            df.columns = [f'V{i}' for i in range(1, df.shape[1] + 1)]
            df['target'] = pd.to_numeric(df['target'], errors='coerce')

        # Convert all feature columns to numeric
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check target values
        print(f"[{dataset_name}] Target value counts: {df['target'].value_counts()}")
        print(f"[{dataset_name}] Target nulls: {df['target'].isnull().sum()}")
        
        # Drop rows where target is null
        before_drop = len(df)
        df = df.dropna(subset=['target'])
        after_drop = len(df)
        if before_drop != after_drop:
            print(f"[{dataset_name}] Dropped {before_drop - after_drop} rows with null targets")
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values in features
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.2f}-{df['target'].max():.2f}")
        return df

if __name__ == "__main__":
    ds = QSARBiodegradationDataset()
    frame = ds.get_data()
    print(frame.head())
