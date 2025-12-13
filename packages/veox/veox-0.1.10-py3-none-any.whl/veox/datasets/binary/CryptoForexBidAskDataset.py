import pandas as pd
import numpy as np
import os
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class CryptoForexBidAskDataset(BaseDatasetLoader):
    """
    Crypto/Forex Bid-Ask Dataset (binary classification)
    
    This dataset handles cryptocurrency or forex data with bid and ask prices.
    The target is binary: whether the spread will widen (1) or narrow (0) in the next period.
    
    Expected columns: timestamp, bid, ask (or variations like bid_price, asking_price)
    """
    
    def get_dataset_info(self):
        return {
            'name': 'CryptoForexBidAskDataset',
            'source_id': 'crypto_forex_bid_ask_v1',
            'category': 'models/binary_classification',  # Fixed to match expected format
            'description': 'Crypto/Forex data with bid-ask spread prediction',
            'source_url': 'local_file',  # Will be loaded from local directory
        }
    
    def download_dataset(self, info):
        """
        Try to load dataset from local crypto_forex_data directory
        or download from a known source
        """
        print(f"[CryptoForexBidAskDataset] Looking for data files...")
        
        # Check local directory first
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'crypto_forex_data')
        
        if os.path.exists(data_dir):
            # Look for CSV files with bid/ask columns
            for file in os.listdir(data_dir):
                if file.endswith('.csv'):
                    filepath = os.path.join(data_dir, file)
                    print(f"[CryptoForexBidAskDataset] Found file: {file}")
                    
                    # Read and check if it has bid/ask columns
                    try:
                        df = pd.read_csv(filepath, nrows=5)
                        columns_lower = [col.lower() for col in df.columns]
                        
                        has_bid = any('bid' in col for col in columns_lower)
                        has_ask = any('ask' in col or 'offer' in col for col in columns_lower)
                        
                        if has_bid and has_ask:
                            print(f"[CryptoForexBidAskDataset] Using file: {file}")
                            with open(filepath, 'rb') as f:
                                return f.read()
                    except Exception as e:
                        print(f"[CryptoForexBidAskDataset] Error checking {file}: {e}")
        
        # If no local file found, try downloading from a public source
        # Example: Download EUR/USD data from a public API or dataset
        try:
            # This is a placeholder URL - replace with actual data source
            url = "https://raw.githubusercontent.com/FX-Data/FX-Data-EURUSD-DS/EURUSD-2021/EURUSD-2021.csv"
            print(f"[CryptoForexBidAskDataset] Attempting to download from: {url}")
            
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            print(f"[CryptoForexBidAskDataset] Download failed: {e}")
        
        # Generate sample data if no real data available
        print("[CryptoForexBidAskDataset] Generating sample bid-ask data...")
        
        np.random.seed(42)
        n_rows = 10000
        
        # Generate timestamps
        timestamps = pd.date_range(start='2023-01-01', periods=n_rows, freq='1min')
        
        # Generate realistic bid-ask prices
        mid_price = 1.0800  # Starting EUR/USD price
        spreads = []
        bids = []
        asks = []
        
        for i in range(n_rows):
            # Random walk for mid price
            mid_price += np.random.normal(0, 0.0001)
            
            # Spread varies with volatility and time of day
            hour = timestamps[i].hour
            base_spread = 0.0001  # 1 pip base spread
            
            # Wider spreads during off-hours
            if hour < 8 or hour > 17:
                base_spread *= 1.5
            
            # Add random variation
            spread = base_spread * np.random.uniform(0.8, 2.0)
            
            bid = mid_price - spread / 2
            ask = mid_price + spread / 2
            
            bids.append(bid)
            asks.append(ask)
            spreads.append(spread)
        
        # Create additional features
        volumes = np.random.lognormal(10, 1, n_rows)
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'bid': bids,
            'ask': asks,
            'spread': spreads,
            'volume': volumes,
            'mid_price': [(b + a) / 2 for b, a in zip(bids, asks)]
        })
        
        csv_data = df.to_csv(index=False)
        return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the bid-ask dataset"""
        print(f"[CryptoForexBidAskDataset] Raw shape: {df.shape}")
        print(f"[CryptoForexBidAskDataset] Columns: {list(df.columns)}")
        
        # Identify bid and ask columns
        bid_col = None
        ask_col = None
        
        columns_lower = {col: col.lower() for col in df.columns}
        
        # Find bid column
        for col, col_lower in columns_lower.items():
            if 'bid' in col_lower and 'spread' not in col_lower:
                bid_col = col
                break
        
        # Find ask column
        for col, col_lower in columns_lower.items():
            if ('ask' in col_lower or 'offer' in col_lower) and 'spread' not in col_lower:
                ask_col = col
                break
        
        if not bid_col or not ask_col:
            raise ValueError(f"Could not find bid and ask columns. Found columns: {list(df.columns)}")
        
        print(f"[CryptoForexBidAskDataset] Using bid column: {bid_col}, ask column: {ask_col}")
        
        # Convert to numeric
        df[bid_col] = pd.to_numeric(df[bid_col], errors='coerce')
        df[ask_col] = pd.to_numeric(df[ask_col], errors='coerce')
        
        # Calculate spread
        df['spread'] = df[ask_col] - df[bid_col]
        df['spread_pct'] = (df['spread'] / df[bid_col]) * 100
        df['mid_price'] = (df[bid_col] + df[ask_col]) / 2
        
        # Create features
        feature_cols = []
        
        # Basic price features
        df['bid'] = df[bid_col]
        df['ask'] = df[ask_col]
        feature_cols.extend(['bid', 'ask', 'spread', 'spread_pct', 'mid_price'])
        
        # Price changes
        df['bid_change'] = df['bid'].pct_change()
        df['ask_change'] = df['ask'].pct_change()
        df['spread_change'] = df['spread'].pct_change()
        feature_cols.extend(['bid_change', 'ask_change', 'spread_change'])
        
        # Rolling statistics
        for window in [5, 10, 30]:
            df[f'spread_ma_{window}'] = df['spread'].rolling(window=window).mean()
            df[f'spread_std_{window}'] = df['spread'].rolling(window=window).std()
            df[f'bid_ma_{window}'] = df['bid'].rolling(window=window).mean()
            df[f'ask_ma_{window}'] = df['ask'].rolling(window=window).mean()
            
            feature_cols.extend([f'spread_ma_{window}', f'spread_std_{window}', 
                               f'bid_ma_{window}', f'ask_ma_{window}'])
        
        # Volume features if available
        volume_col = None
        for col in df.columns:
            if 'volume' in col.lower():
                volume_col = col
                break
        
        if volume_col:
            df['volume'] = pd.to_numeric(df[volume_col], errors='coerce')
            df['volume_ma_10'] = df['volume'].rolling(window=10).mean()
            feature_cols.extend(['volume', 'volume_ma_10'])
        
        # Time features if timestamp available
        timestamp_col = None
        for col in df.columns:
            if 'time' in col.lower() or 'date' in col.lower():
                timestamp_col = col
                break
        
        if timestamp_col:
            df['timestamp'] = pd.to_datetime(df[timestamp_col], errors='coerce')
            df = df.dropna(subset=['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['minute'] = df['timestamp'].dt.minute
            df['dayofweek'] = df['timestamp'].dt.dayofweek
            feature_cols.extend(['hour', 'minute', 'dayofweek'])
        
        # Create binary target: will spread widen in next period?
        df['future_spread'] = df['spread'].shift(-1)
        df['target'] = (df['future_spread'] > df['spread']).astype(int)
        
        # Select final columns
        df = df[feature_cols + ['target']]
        
        # Remove NaN values
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Shuffle data
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[CryptoForexBidAskDataset] Final shape: {df.shape}")
        print(f"[CryptoForexBidAskDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[CryptoForexBidAskDataset] Spread stats: mean={df['spread'].mean():.6f}, std={df['spread'].std():.6f}")
        
        return df


if __name__ == "__main__":
    dataset = CryptoForexBidAskDataset()
    df = dataset.get_data()
    print(f"Loaded CryptoForexBidAskDataset: {df.shape}")
    print(df.head()) 