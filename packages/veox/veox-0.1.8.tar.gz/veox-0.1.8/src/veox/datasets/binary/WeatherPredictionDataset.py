import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WeatherPredictionDataset(BaseDatasetLoader):
    """
    Weather Prediction Dataset (binary classification)
    Source: Kaggle - Historical weather data for prediction
    Target: rain_tomorrow (0=No, 1=Yes)
    
    This dataset contains historical weather data for predicting
    whether it will rain the next day.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'WeatherPredictionDataset',
            'source_id': 'kaggle:weather-prediction',
            'category': 'binary_classification',
            'description': 'Historical weather data for next day rain prediction.',
            'source_url': 'https://www.kaggle.com/datasets/ananthr1/weather-prediction',
        }
    
    def download_dataset(self, info):
        """Download the weather prediction dataset from Kaggle"""
        print(f"[WeatherPredictionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[WeatherPredictionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'ananthr1/weather-prediction',
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
                
                # Read the first CSV file
                data_file = csv_files[0]
                print(f"[WeatherPredictionDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file)
                print(f"[WeatherPredictionDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[WeatherPredictionDataset] Download failed: {e}")
            print("[WeatherPredictionDataset] Using sample data...")
            
            # Create sample weather data
            np.random.seed(42)
            n_samples = 3000
            
            # Generate date range
            dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='D')
            
            data = {
                'Date': dates,
                'Location': np.random.choice(['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'], n_samples),
                'MinTemp': np.random.normal(12, 5, n_samples),
                'MaxTemp': np.random.normal(23, 6, n_samples),
                'Rainfall': np.random.exponential(2, n_samples),
                'Evaporation': np.random.uniform(0, 10, n_samples),
                'Sunshine': np.random.uniform(0, 14, n_samples),
                'WindGustDir': np.random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], n_samples),
                'WindGustSpeed': np.random.gamma(2, 10, n_samples),
                'WindDir9am': np.random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], n_samples),
                'WindDir3pm': np.random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], n_samples),
                'WindSpeed9am': np.random.gamma(2, 5, n_samples),
                'WindSpeed3pm': np.random.gamma(2, 7, n_samples),
                'Humidity9am': np.random.beta(7, 3, n_samples) * 100,
                'Humidity3pm': np.random.beta(6, 4, n_samples) * 100,
                'Pressure9am': np.random.normal(1013, 7, n_samples),
                'Pressure3pm': np.random.normal(1010, 7, n_samples),
                'Cloud9am': np.random.randint(0, 9, n_samples),
                'Cloud3pm': np.random.randint(0, 9, n_samples),
                'Temp9am': np.random.normal(16, 5, n_samples),
                'Temp3pm': np.random.normal(21, 6, n_samples),
                'RainToday': np.random.choice(['No', 'Yes'], n_samples, p=[0.8, 0.2])
            }
            
            # Create target based on features
            rain_tomorrow = []
            for i in range(n_samples):
                # Higher chance of rain if: high humidity, low pressure, rain today
                rain_prob = 0.1
                if data['Humidity3pm'][i] > 70:
                    rain_prob += 0.3
                if data['Pressure3pm'][i] < 1005:
                    rain_prob += 0.2
                if data['RainToday'][i] == 'Yes':
                    rain_prob += 0.3
                if data['Cloud3pm'][i] > 6:
                    rain_prob += 0.1
                
                rain_tomorrow.append('Yes' if np.random.random() < rain_prob else 'No')
            
            data['RainTomorrow'] = rain_tomorrow
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the weather dataset"""
        print(f"[WeatherPredictionDataset] Raw shape: {df.shape}")
        print(f"[WeatherPredictionDataset] Columns: {list(df.columns)}")
        
        # Find target column
        target_col = None
        for col in ['RainTomorrow', 'rain_tomorrow', 'target', 'weather']:
            if col in df.columns:
                target_col = col
                break
        
        if not target_col:
            # For Seattle weather dataset, create target from weather column
            if 'weather' in df.columns:
                # Create binary target from weather type
                df['RainTomorrow'] = df['weather'].apply(lambda x: 'Yes' if 'rain' in str(x).lower() else 'No')
                target_col = 'RainTomorrow'
            else:
                # Create synthetic target based on precipitation
                if 'precipitation' in df.columns:
                    df['RainTomorrow'] = (df['precipitation'] > 0).apply(lambda x: 'Yes' if x else 'No')
                    target_col = 'RainTomorrow'
                else:
                    raise ValueError("Could not find or create target column")
        
        # Create binary target
        if target_col in ['weather']:
            df['target'] = df[target_col].apply(lambda x: 1 if 'rain' in str(x).lower() else 0)
        else:
            df['target'] = (df[target_col] == 'Yes').astype(int)
        
        # Drop non-feature columns
        drop_cols = ['Date', 'date', 'Location', target_col, 'weather']
        for col in drop_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Handle categorical features
        categorical_cols = []
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                categorical_cols.append(col)
        
        # Encode categorical features
        for col in categorical_cols:
            if col == 'RainToday':
                df[col] = (df[col] == 'Yes').astype(int)
            else:
                # Wind direction encoding
                df[col] = pd.Categorical(df[col]).codes
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
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
        
        print(f"[WeatherPredictionDataset] Final shape: {df.shape}")
        print(f"[WeatherPredictionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[WeatherPredictionDataset] Rain rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = WeatherPredictionDataset()
    df = dataset.get_data()
    print(f"Loaded WeatherPredictionDataset: {df.shape}")
    print(df.head()) 