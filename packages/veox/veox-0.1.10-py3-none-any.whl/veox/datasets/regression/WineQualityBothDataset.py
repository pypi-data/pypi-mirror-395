import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WineQualityBothDataset(BaseDatasetLoader):
    """Combined Wine Quality dataset (Red + White) from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'WineQualityBothDataset',
            'source_id': 'uci:wine_quality_combined',
            'category': 'regression',
            'description': 'Combined Wine Quality dataset: predict wine quality from physicochemical properties.',
            'target_column': 'quality'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        print(f"[{dataset_name}] Downloading red and white wine datasets...")
        
        try:
            # Download red wine data
            red_response = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv", timeout=30)
            white_response = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv", timeout=30)
            
            if red_response.status_code != 200 or white_response.status_code != 200:
                raise Exception(f"Download failed")
            
            # Combine datasets
            red_df = pd.read_csv(io.StringIO(red_response.text), sep=';')
            white_df = pd.read_csv(io.StringIO(white_response.text), sep=';')
            
            red_df['wine_type'] = 0  # Red wine
            white_df['wine_type'] = 1  # White wine
            
            combined_df = pd.concat([red_df, white_df], ignore_index=True)
            
            # Convert to CSV bytes
            csv_buffer = io.StringIO()
            combined_df.to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue().encode('utf-8')
            
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Set target
        if 'quality' in df.columns:
            df['target'] = df['quality']
            df = df.drop('quality', axis=1)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.1f}-{df['target'].max():.1f}")
        return df 

if __name__ == "__main__":
    ds = WineQualityBothDataset()
    frame = ds.get_data()
    print(frame.head()) 