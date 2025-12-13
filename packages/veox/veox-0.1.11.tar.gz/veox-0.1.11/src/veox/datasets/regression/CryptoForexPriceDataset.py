import pandas as pd
import numpy as np
import os
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class CryptoForexPriceDataset(BaseDatasetLoader):
    """
    Crypto/Forex Price Dataset (regression)
    
    This dataset handles cryptocurrency or forex data with bid and ask prices.
    The target is continuous: predicting the future mid-price.
    
    Expected columns: timestamp, bid, ask (or variations like bid_price, asking_price)
    """
    
    def get_dataset_info(self):
        return {
            'name': 'CryptoForexPriceDataset',
            'source_id': 'crypto_forex_price_v1',
            'category': 'models/regression',
            'description': 'Crypto/Forex data for price prediction',
            'source_url': 'local_file',  # Will be loaded from local directory
        }
    
    def download_dataset(self, info):
        """
        Try to load dataset from local crypto_forex_data directory
        or download from a known source
        """
        print(f"[CryptoForexPriceDataset] Looking for data files...")
        
        # Check local directory first
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'crypto_forex_data')
        
        if os.path.exists(data_dir):
            # Look for CSV files with bid/ask columns
            for file in os.listdir(data_dir):
                if file.endswith('.csv'):
                    filepath = os.path.join(data_dir, file)
                    print(f"[CryptoForexPriceDataset] Found file: {file}")
                    
                    # Read and check if it has bid/ask columns
                    try:
                        df = pd.read_csv(filepath, nrows=5)
                        columns_lower = [col.lower() for col in df.columns]
                        
                        has_bid = any('bid' in col for col in columns_lower)
                        has_ask = any('ask' in col or 'offer' in col for col in columns_lower)
                        
                        if has_bid and has_ask:
                            print(f"[CryptoForexPriceDataset] Using file: {file}")
                            with open(filepath, 'rb') as f:
                                return f.read()
                    except Exception as e:
                        print(f"[CryptoForexPriceDataset] Error checking {file}: {e}")
        
        # Generate sample data if no real data available
        print("[CryptoForexPriceDataset] Generating sample bid-ask data...")
        
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
        """Process the bid-ask dataset for regression"""
        print(f"[CryptoForexPriceDataset] Raw shape: {df.shape}")
        print(f"[CryptoForexPriceDataset] Columns: {list(df.columns)}")
        
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
        
        print(f"[CryptoForexPriceDataset] Using bid column: {bid_col}, ask column: {ask_col}")
        
        # Convert to numeric
        df[bid_col] = pd.to_numeric(df[bid_col], errors='coerce')
        df[ask_col] = pd.to_numeric(df[ask_col], errors='coerce')
        
        # Calculate spread and mid price
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
        df['mid_change'] = df['mid_price'].pct_change()
        feature_cols.extend(['bid_change', 'ask_change', 'mid_change'])
        
        # Rolling statistics
        for window in [5, 10, 30, 60]:
            df[f'mid_ma_{window}'] = df['mid_price'].rolling(window=window).mean()
            df[f'mid_std_{window}'] = df['mid_price'].rolling(window=window).std()
            df[f'spread_ma_{window}'] = df['spread'].rolling(window=window).mean()
            
            feature_cols.extend([f'mid_ma_{window}', f'mid_std_{window}', f'spread_ma_{window}'])
        
        # Price momentum
        df['momentum_5'] = df['mid_price'] - df['mid_price'].shift(5)
        df['momentum_10'] = df['mid_price'] - df['mid_price'].shift(10)
        df['momentum_30'] = df['mid_price'] - df['mid_price'].shift(30)
        feature_cols.extend(['momentum_5', 'momentum_10', 'momentum_30'])
        
        # Volume features if available
        volume_col = None
        for col in df.columns:
            if 'volume' in col.lower():
                volume_col = col
                break
        
        if volume_col:
            df['volume'] = pd.to_numeric(df[volume_col], errors='coerce')
            df['volume_ma_10'] = df['volume'].rolling(window=10).mean()
            df['volume_ma_30'] = df['volume'].rolling(window=30).mean()
            feature_cols.extend(['volume', 'volume_ma_10', 'volume_ma_30'])
        
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
            df['is_trading_hours'] = ((df['hour'] >= 8) & (df['hour'] <= 17)).astype(int)
            feature_cols.extend(['hour', 'minute', 'dayofweek', 'is_trading_hours'])
        
        # Create regression target: future mid price
        df['target'] = df['mid_price'].shift(-5)  # Predict price 5 minutes ahead
        
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
        
        print(f"[CryptoForexPriceDataset] Final shape: {df.shape}")
        print(f"[CryptoForexPriceDataset] Target stats: mean={df['target'].mean():.6f}, std={df['target'].std():.6f}")
        print(f"[CryptoForexPriceDataset] Price range: [{df['target'].min():.6f}, {df['target'].max():.6f}]")
        
        return df


if __name__ == "__main__":
    dataset = CryptoForexPriceDataset()
    df = dataset.get_data()
    print(f"Loaded CryptoForexPriceDataset: {df.shape}")
    print(df.head()) 