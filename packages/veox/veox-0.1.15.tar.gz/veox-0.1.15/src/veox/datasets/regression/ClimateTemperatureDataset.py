import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ClimateTemperatureDataset(BaseDatasetLoader):
    """
    Climate Change: Earth Surface Temperature Dataset (regression)
    Source: Kaggle - Berkeley Earth global temperature data since 1750
    Target: average_temperature (continuous)
    
    This dataset contains global land temperature data from 1750 to present,
    compiled by Berkeley Earth.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'ClimateTemperatureDataset',
            'source_id': 'kaggle:climate-temperature',
            'category': 'regression',
            'description': 'Global temperature data since 1750 for climate analysis.',
            'source_url': 'https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data',
        }
    
    def download_dataset(self, info):
        """Download the climate temperature dataset from Kaggle"""
        print(f"[ClimateTemperatureDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[ClimateTemperatureDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'berkeleyearth/climate-change-earth-surface-temperature-data',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                
                # Look for global temperature file
                data_file = None
                for f in csv_files:
                    if 'global' in f.lower() and 'land' in f.lower():
                        data_file = f
                        break
                
                if not data_file:
                    # Use the first file
                    data_file = csv_files[0]
                
                print(f"[ClimateTemperatureDataset] Reading: {os.path.basename(data_file)}")
                
                # Read with limited rows for performance
                df = pd.read_csv(data_file, nrows=50000)
                print(f"[ClimateTemperatureDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[ClimateTemperatureDataset] Download failed: {e}")
            print("[ClimateTemperatureDataset] Using sample data...")
            
            # Create sample climate data
            np.random.seed(42)
            n_samples = 5000
            
            # Generate time series from 1850 to 2020
            years = np.random.randint(1850, 2021, n_samples)
            months = np.random.randint(1, 13, n_samples)
            
            data = {
                'dt': [f'{year}-{month:02d}-01' for year, month in zip(years, months)],
                'LandAverageTemperature': np.zeros(n_samples),
                'LandAverageTemperatureUncertainty': np.zeros(n_samples),
                'LandMaxTemperature': np.zeros(n_samples),
                'LandMaxTemperatureUncertainty': np.zeros(n_samples),
                'LandMinTemperature': np.zeros(n_samples),
                'LandMinTemperatureUncertainty': np.zeros(n_samples),
                'LandAndOceanAverageTemperature': np.zeros(n_samples),
                'LandAndOceanAverageTemperatureUncertainty': np.zeros(n_samples)
            }
            
            # Generate temperature data with warming trend
            for i in range(n_samples):
                year = years[i]
                month = months[i]
                
                # Base temperature varies by month
                base_temp = 8.5 + 10 * np.sin((month - 1) * np.pi / 6)
                
                # Add warming trend (about 1°C per century)
                warming = (year - 1850) * 0.01
                
                # Add random variation
                variation = np.random.normal(0, 2)
                
                avg_temp = base_temp + warming + variation
                data['LandAverageTemperature'][i] = avg_temp
                data['LandAverageTemperatureUncertainty'][i] = np.random.uniform(0.1, 0.5)
                data['LandMaxTemperature'][i] = avg_temp + np.random.uniform(5, 15)
                data['LandMaxTemperatureUncertainty'][i] = np.random.uniform(0.2, 0.8)
                data['LandMinTemperature'][i] = avg_temp - np.random.uniform(5, 15)
                data['LandMinTemperatureUncertainty'][i] = np.random.uniform(0.2, 0.8)
                data['LandAndOceanAverageTemperature'][i] = avg_temp + np.random.normal(0, 0.5)
                data['LandAndOceanAverageTemperatureUncertainty'][i] = np.random.uniform(0.1, 0.3)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the climate temperature dataset"""
        print(f"[ClimateTemperatureDataset] Raw shape: {df.shape}")
        print(f"[ClimateTemperatureDataset] Columns: {list(df.columns)}")
        
        # Find temperature column for target
        target_col = None
        for col in ['LandAverageTemperature', 'AverageTemperature', 'Temperature']:
            if col in df.columns:
                target_col = col
                break
        
        if not target_col:
            # Use first numeric column that looks like temperature
            for col in df.columns:
                if 'temp' in col.lower() and df[col].dtype in ['float64', 'int64']:
                    target_col = col
                    break
        
        if not target_col:
            raise ValueError("Could not find temperature column")
        
        # Create target
        df['target'] = pd.to_numeric(df[target_col], errors='coerce')
        
        # Parse date if exists
        date_col = None
        for col in ['dt', 'date', 'Date']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            df['date'] = pd.to_datetime(df[date_col], errors='coerce')
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df = df.drop([date_col, 'date'], axis=1)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col not in [target_col, 'target'] and df[col].dtype in ['int64', 'float64']:
                feature_cols.append(col)
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Remove missing values
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[ClimateTemperatureDataset] Final shape: {df.shape}")
        print(f"[ClimateTemperatureDataset] Target stats: mean={df['target'].mean():.2f}°C, std={df['target'].std():.2f}°C")
        print(f"[ClimateTemperatureDataset] Target range: [{df['target'].min():.2f}°C, {df['target'].max():.2f}°C]")
        
        return df

if __name__ == "__main__":
    dataset = ClimateTemperatureDataset()
    df = dataset.get_data()
    print(f"Loaded ClimateTemperatureDataset: {df.shape}")
    print(df.head()) 