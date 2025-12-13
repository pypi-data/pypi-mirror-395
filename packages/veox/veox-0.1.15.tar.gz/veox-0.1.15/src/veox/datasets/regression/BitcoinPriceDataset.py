import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BitcoinPriceDataset(BaseDatasetLoader):
    """
    Bitcoin Historical Price Dataset (regression)
    Source: Kaggle - Bitcoin Historical Data
    Target: close_price (continuous)
    
    This dataset contains historical Bitcoin price data including
    open, high, low, close prices and volume for time series analysis.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'BitcoinPriceDataset',
            'source_id': 'kaggle:bitcoin-historical-data',
            'category': 'regression',
            'description': 'Bitcoin historical price data for time series prediction.',
            'source_url': 'https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data',
        }
    
    def download_dataset(self, info):
        """Download the Bitcoin price dataset from Kaggle"""
        print(f"[BitcoinPriceDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[BitcoinPriceDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'mczielinski/bitcoin-historical-data',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv') and 'bitcoin' in file.lower():
                            csv_files.append(os.path.join(root, file))
                
                if not csv_files:
                    raise FileNotFoundError("No Bitcoin CSV file found")
                
                # Read the first Bitcoin file
                data_file = csv_files[0]
                print(f"[BitcoinPriceDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file)
                print(f"[BitcoinPriceDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[BitcoinPriceDataset] Download failed: {e}")
            print("[BitcoinPriceDataset] Using sample data...")
            
            # Create realistic sample Bitcoin data
            np.random.seed(42)
            n_days = 2000  # About 5.5 years of data
            
            # Generate dates
            dates = pd.date_range(start='2018-01-01', periods=n_days, freq='D')
            
            # Generate realistic Bitcoin price movements
            # Start at around $10,000
            prices = [10000]
            for i in range(1, n_days):
                # Daily return with volatility
                daily_return = np.random.normal(0.001, 0.03)  # 0.1% mean, 3% std dev
                
                # Add some trend based on period
                if i < 365:  # 2018 - bear market
                    daily_return -= 0.002
                elif i < 730:  # 2019 - recovery
                    daily_return += 0.001
                elif i < 1095:  # 2020 - bull run start
                    daily_return += 0.002
                elif i < 1460:  # 2021 - major bull run
                    daily_return += 0.003
                else:  # 2022+ - correction
                    daily_return -= 0.001
                
                new_price = prices[-1] * (1 + daily_return)
                # Keep price above $1000
                new_price = max(new_price, 1000)
                prices.append(new_price)
            
            data = {
                'Timestamp': dates.astype(str),
                'Open': [],
                'High': [],
                'Low': [],
                'Close': prices,
                'Volume_(BTC)': [],
                'Volume_(Currency)': [],
                'Weighted_Price': []
            }
            
            # Generate OHLC data
            for i, close_price in enumerate(prices):
                # Open is previous close with small gap
                open_price = prices[i-1] if i > 0 else close_price
                open_price *= np.random.uniform(0.995, 1.005)
                
                # High and Low based on daily volatility
                daily_range = close_price * np.random.uniform(0.01, 0.05)
                high_price = max(open_price, close_price) + daily_range * np.random.uniform(0, 1)
                low_price = min(open_price, close_price) - daily_range * np.random.uniform(0, 1)
                
                # Volume decreases as price increases (realistic pattern)
                base_volume = 10000 / (1 + close_price / 10000)
                volume_btc = base_volume * np.random.uniform(0.5, 2.0)
                
                data['Open'].append(open_price)
                data['High'].append(high_price)
                data['Low'].append(low_price)
                data['Volume_(BTC)'].append(volume_btc)
                data['Volume_(Currency)'].append(volume_btc * close_price)
                data['Weighted_Price'].append((high_price + low_price + close_price) / 3)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the Bitcoin price dataset"""
        print(f"[BitcoinPriceDataset] Raw shape: {df.shape}")
        print(f"[BitcoinPriceDataset] Columns: {list(df.columns)}")
        
        # Handle timestamp
        timestamp_col = None
        for col in ['Timestamp', 'timestamp', 'Date', 'date', 'time']:
            if col in df.columns:
                timestamp_col = col
                break
        
        if timestamp_col:
            df['timestamp'] = pd.to_datetime(df[timestamp_col], errors='coerce')
            df = df.dropna(subset=['timestamp'])
            df = df.sort_values('timestamp')
            
            # Extract time features
            df['year'] = df['timestamp'].dt.year.astype('int64')
            df['month'] = df['timestamp'].dt.month.astype('int64')
            df['day'] = df['timestamp'].dt.day.astype('int64')
            df['dayofweek'] = df['timestamp'].dt.dayofweek.astype('int64')
            df['dayofyear'] = df['timestamp'].dt.dayofyear.astype('int64')
        
        # Find price columns
        close_col = None
        for col in ['Close', 'close', 'close_price', 'Weighted_Price']:
            if col in df.columns:
                close_col = col
                break
        
        if not close_col:
            raise ValueError("Could not find close price column")
        
        # Create target (next day's close price for prediction)
        df['target'] = df[close_col].shift(-1)
        
        # Create features
        feature_cols = []
        
        # Price features
        for col in ['Open', 'High', 'Low', 'Close', 'Weighted_Price']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                feature_cols.append(col)
        
        # Volume features
        for col in ['Volume_(BTC)', 'Volume_(Currency)', 'Volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                feature_cols.append(col)
        
        # Technical indicators
        if 'Close' in df.columns:
            # Moving averages
            df['ma_7'] = df['Close'].rolling(window=7).mean()
            df['ma_30'] = df['Close'].rolling(window=30).mean()
            df['ma_90'] = df['Close'].rolling(window=90).mean()
            
            # Price changes
            df['price_change_1d'] = df['Close'].pct_change()
            df['price_change_7d'] = df['Close'].pct_change(7)
            df['price_change_30d'] = df['Close'].pct_change(30)
            
            # Volatility
            df['volatility_7d'] = df['price_change_1d'].rolling(window=7).std()
            df['volatility_30d'] = df['price_change_1d'].rolling(window=30).std()
            
            feature_cols.extend(['ma_7', 'ma_30', 'ma_90', 'price_change_1d', 
                               'price_change_7d', 'price_change_30d',
                               'volatility_7d', 'volatility_30d'])
        
        # Time features
        if timestamp_col:
            feature_cols.extend(['year', 'month', 'day', 'dayofweek', 'dayofyear'])
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Remove rows with NaN (from rolling calculations and target shift)
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Limit to recent data if too large
        if len(df) > 5000:
            df = df.tail(5000)
        
        # Reset index
        df = df.reset_index(drop=True)
        
        print(f"[BitcoinPriceDataset] Final shape: {df.shape}")
        print(f"[BitcoinPriceDataset] Target stats: mean=${df['target'].mean():.2f}, std=${df['target'].std():.2f}")
        print(f"[BitcoinPriceDataset] Price range: [${df['target'].min():.2f}, ${df['target'].max():.2f}]")
        
        return df

if __name__ == "__main__":
    dataset = BitcoinPriceDataset()
    df = dataset.get_data()
    print(f"Loaded BitcoinPriceDataset: {df.shape}")
    print(df.head()) 