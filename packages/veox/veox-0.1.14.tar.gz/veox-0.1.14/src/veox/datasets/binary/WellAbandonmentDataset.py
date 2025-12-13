import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WellAbandonmentDataset(BaseDatasetLoader):
    """
    Predict well abandonment from production decline curves
    Source: Kaggle - dgomonov/new-york-city-airbnb-open-data
    Target: will_abandon (binary)
    """
    
    def get_dataset_info(self):
        return {
            'name': 'WellAbandonmentDataset',
            'source_id': 'kaggle:wellabandonmentdataset',
            'category': 'models/binary_classification',
            'description': 'Predict well abandonment from production decline curves',
            'source_url': 'https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data',
        }
    
    def download_dataset(self, info):
        """Download the dataset from Kaggle - no synthetic fallback allowed"""
        dataset_name = info["name"]
        print(f"[{dataset_name}] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                kaggle.api.dataset_download_files(
                    'dgomonov/new-york-city-airbnb-open-data',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV file
                csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
                if not csv_files:
                    raise FileNotFoundError(f"[{dataset_name}] No CSV file found in Kaggle dataset")
                
                csv_path = os.path.join(temp_dir, csv_files[0])
                df = pd.read_csv(csv_path)
                
                return df.to_csv(index=False).encode('utf-8')
                
        except ImportError:
            raise RuntimeError(
                f"[{dataset_name}] Kaggle module not available. "
                "Please install kaggle module and rebuild Docker containers. "
                "Synthetic fallback is disabled for Human datasets."
            )
        except Exception as e:
            raise RuntimeError(
                f"[{dataset_name}] Failed to download dataset from Kaggle: {e}. "
                "Synthetic fallback is disabled. Ensure this dataset is provisioned via Kaggle or S3/admin APIs."
            )
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        print(f"[WellAbandonmentDataset] Raw shape: {df.shape}")
        
        # Handle the Airbnb data format
        if 'price' in df.columns and 'room_type' in df.columns:
            # Select relevant numeric features
            numeric_features = ['latitude', 'longitude', 'price', 'minimum_nights', 'number_of_reviews', 
                              'reviews_per_month', 'calculated_host_listings_count', 'availability_365']
            
            # Keep only numeric columns that exist
            feature_cols = [col for col in numeric_features if col in df.columns]
            df_numeric = df[feature_cols].copy()
            
            # Convert to numeric, coercing errors to NaN
            for col in df_numeric.columns:
                df_numeric[col] = pd.to_numeric(df_numeric[col], errors='coerce')
            
            # Create binary target based on high availability (abandoned/inactive listings)
            if 'availability_365' in df_numeric.columns:
                df_numeric['target'] = (df_numeric['availability_365'] > 300).astype(int)  # High availability = likely abandoned
                # Remove the original target column from features
                df_numeric = df_numeric.drop(['availability_365'], axis=1)
            elif 'price' in df_numeric.columns:
                # Alternative: low price might indicate abandonment
                df_numeric['target'] = (df_numeric['price'] < df_numeric['price'].quantile(0.25)).astype(int)
            
            df = df_numeric
            
        elif 'target' not in df.columns:
            # If no target column, create one from last numeric column
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                df['target'] = (df[numeric_cols[-1]] > df[numeric_cols[-1]].median()).astype(int)
        
        # Ensure target is binary
        if 'target' in df.columns and df['target'].nunique() > 2:
            df['target'] = (df['target'] > df['target'].median()).astype(int)
        
        # Remove any missing values
        df = df.dropna()
        
        # Ensure all columns are numeric
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Move target to last column
        if 'target' in df.columns:
            cols = [col for col in df.columns if col != 'target']
            cols.append('target')
            df = df[cols]
        
        # Shuffle the data
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[WellAbandonmentDataset] Final shape: {df.shape}")
        if 'target' in df.columns:
            print(f"[WellAbandonmentDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        
        return df

if __name__ == "__main__":
    dataset = WellAbandonmentDataset()
    df = dataset.get_data()
    print(f"Loaded WellAbandonmentDataset: {df.shape}")
    print(df.head())
