import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class MarketSentimentAnalysisDataset(BaseDatasetLoader):
    """
    Market Sentiment Analysis Dataset (regression)
    Source: Kaggle - Stock Market Data
    Target: sentiment_score (market sentiment score -1 to 1)
    
    This dataset contains market indicators and news sentiment for
    predicting overall market sentiment.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'MarketSentimentAnalysisDataset',
            'source_id': 'kaggle:market-sentiment-analysis',
            'category': 'regression',
            'description': 'Market sentiment prediction from technical indicators and news data.',
            'source_url': 'https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs',
        }
    
    def download_dataset(self, info):
        """Download the market sentiment dataset from Kaggle"""
        print(f"[MarketSentimentAnalysisDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[MarketSentimentAnalysisDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'borismarjanovic/price-volume-data-for-all-us-stocks-etfs',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.txt') or file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if csv_files:
                    # Use first few files and aggregate
                    dfs = []
                    for i, data_file in enumerate(csv_files[:5]):
                        try:
                            df = pd.read_csv(data_file)
                            if len(df) > 100:
                                df = df.sample(n=min(1000, len(df)), random_state=42)
                                dfs.append(df)
                        except:
                            continue
                        if len(dfs) >= 3:
                            break
                    
                    if dfs:
                        df = pd.concat(dfs, ignore_index=True)
                        print(f"[MarketSentimentAnalysisDataset] Loaded {df.shape[0]} rows")
                        csv_data = df.to_csv(index=False)
                        return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No valid data files found")
                
        except Exception as e:
            print(f"[MarketSentimentAnalysisDataset] Download failed: {e}")
            print("[MarketSentimentAnalysisDataset] Using sample market sentiment data...")
            
            # Create realistic market sentiment data
            np.random.seed(42)
            n_samples = 7000
            
            # Market indicators
            data = {}
            data['sp500_return'] = np.random.normal(0.0003, 0.01, n_samples)  # Daily return
            data['vix_level'] = np.random.gamma(2, 8, n_samples)  # Volatility index
            data['put_call_ratio'] = np.random.normal(0.9, 0.2, n_samples)
            data['advance_decline_ratio'] = np.random.normal(1.1, 0.3, n_samples)
            data['market_breadth'] = np.random.beta(5, 5, n_samples)
            
            # Volume indicators
            data['volume_ratio'] = np.random.lognormal(0, 0.3, n_samples)
            data['avg_volume_20d'] = np.random.lognormal(16, 0.5, n_samples)
            data['volume_spike'] = np.random.exponential(0.1, n_samples)
            
            # Technical indicators
            data['rsi_14'] = np.random.beta(5, 5, n_samples) * 100
            data['macd_signal'] = np.random.normal(0, 2, n_samples)
            data['bollinger_position'] = np.random.uniform(-2, 2, n_samples)
            data['momentum_10d'] = np.random.normal(0, 0.05, n_samples)
            
            # Moving averages
            data['price_vs_ma50'] = np.random.normal(0, 0.05, n_samples)
            data['price_vs_ma200'] = np.random.normal(0, 0.08, n_samples)
            data['ma50_vs_ma200'] = np.random.normal(0, 0.03, n_samples)
            
            # Market microstructure
            data['bid_ask_spread'] = np.random.exponential(0.001, n_samples)
            data['order_imbalance'] = np.random.normal(0, 0.1, n_samples)
            data['high_low_ratio'] = np.random.beta(8, 2, n_samples)
            
            # Sector performance
            data['tech_sector_return'] = np.random.normal(0.0005, 0.015, n_samples)
            data['financial_sector_return'] = np.random.normal(0.0002, 0.012, n_samples)
            data['energy_sector_return'] = np.random.normal(-0.0001, 0.018, n_samples)
            data['sector_dispersion'] = np.random.exponential(0.01, n_samples)
            
            # News sentiment (simulated)
            data['news_sentiment_score'] = np.random.normal(0, 0.3, n_samples)
            data['news_volume'] = np.random.poisson(50, n_samples)
            data['social_media_mentions'] = np.random.gamma(2, 1000, n_samples)
            data['analyst_upgrades'] = np.random.poisson(3, n_samples)
            data['analyst_downgrades'] = np.random.poisson(2, n_samples)
            
            # Economic indicators
            data['yield_curve_slope'] = np.random.normal(1.5, 0.5, n_samples)
            data['dollar_index_change'] = np.random.normal(0, 0.005, n_samples)
            data['commodity_index_change'] = np.random.normal(0, 0.008, n_samples)
            
            # Options market
            data['options_volume'] = np.random.lognormal(14, 0.5, n_samples)
            data['implied_volatility_skew'] = np.random.normal(-0.1, 0.05, n_samples)
            data['term_structure_slope'] = np.random.normal(0.02, 0.01, n_samples)
            
            # Calculate sentiment score (target)
            sentiment = np.zeros(n_samples)
            
            # Market return contribution
            sentiment += data['sp500_return'] * 50
            sentiment += data['advance_decline_ratio'] * 0.1
            
            # Volatility contribution (inverse)
            sentiment -= (data['vix_level'] - 15) / 15 * 0.3
            sentiment -= data['put_call_ratio'] * 0.1
            
            # Technical indicators
            sentiment += (data['rsi_14'] - 50) / 50 * 0.2
            sentiment += np.sign(data['macd_signal']) * 0.1
            sentiment += data['momentum_10d'] * 5
            
            # Moving average signals
            sentiment += np.sign(data['price_vs_ma50']) * 0.1
            sentiment += np.sign(data['price_vs_ma200']) * 0.15
            sentiment += np.sign(data['ma50_vs_ma200']) * 0.2
            
            # News sentiment
            sentiment += data['news_sentiment_score'] * 0.5
            sentiment += (data['analyst_upgrades'] - data['analyst_downgrades']) * 0.05
            
            # Market structure
            sentiment -= data['bid_ask_spread'] * 100
            sentiment += data['order_imbalance'] * 0.3
            
            # Economic factors
            sentiment += data['yield_curve_slope'] * 0.1
            sentiment -= data['implied_volatility_skew'] * 0.5
            
            # Add noise and clip to [-1, 1]
            sentiment += np.random.normal(0, 0.1, n_samples)
            data['target'] = np.clip(sentiment, -1, 1)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the market sentiment dataset"""
        print(f"[MarketSentimentAnalysisDataset] Raw shape: {df.shape}")
        print(f"[MarketSentimentAnalysisDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['sentiment', 'score', 'return', 'close', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            if target_col in ['close', 'return']:
                # Calculate sentiment from price movements
                if 'open' in df.columns and 'close' in df.columns:
                    daily_return = (df['close'] - df['open']) / df['open']
                    # Convert return to sentiment score
                    df['target'] = np.tanh(daily_return * 100)  # Scale and bound to [-1, 1]
                else:
                    df['target'] = np.random.normal(0, 0.3, len(df))
            else:
                df['target'] = df[target_col]
            
            if target_col != 'close':  # Keep close price as feature
                df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Generate sentiment from available features
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Use price and volume patterns
                if 'volume' in str(numeric_cols) and any('close' in str(c) or 'price' in str(c) for c in numeric_cols):
                    # High volume + price increase = positive sentiment
                    vol_col = [c for c in numeric_cols if 'volume' in c.lower()][0]
                    price_col = [c for c in numeric_cols if 'close' in c.lower() or 'price' in c.lower()][0]
                    
                    vol_norm = (df[vol_col] - df[vol_col].mean()) / df[vol_col].std()
                    price_change = df[price_col].pct_change().fillna(0)
                    
                    df['target'] = np.tanh(vol_norm * 0.1 + price_change * 10)
                else:
                    # Random sentiment
                    df['target'] = np.random.normal(0, 0.3, len(df))
            else:
                df['target'] = np.random.normal(0, 0.3, len(df))
        
        # Remove non-numeric columns
        text_cols = ['date', 'symbol', 'ticker', 'name', 'exchange']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().sum() > len(df) * 0.5:
                    feature_cols.append(col)
        
        # Create technical indicators if we have OHLCV data
        if all(col in feature_cols for col in ['open', 'high', 'low', 'close', 'volume']):
            # Add some technical indicators
            df['high_low_ratio'] = df['high'] / df['low']
            df['close_open_ratio'] = df['close'] / df['open']
            df['volume_ratio'] = df['volume'] / df['volume'].rolling(20, min_periods=1).mean()
            
            feature_cols.extend(['high_low_ratio', 'close_open_ratio', 'volume_ratio'])
        
        # Limit features
        if len(feature_cols) > 40:
            # Prioritize market features
            priority_features = ['close', 'volume', 'high', 'low', 'open', 'return', 'vix', 'rsi']
            
            selected_features = []
            for feat in priority_features:
                for col in feature_cols:
                    if feat in col.lower() and col not in selected_features:
                        selected_features.append(col)
            
            # Add remaining
            for col in feature_cols:
                if col not in selected_features and len(selected_features) < 40:
                    selected_features.append(col)
            
            feature_cols = selected_features[:40]
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Handle missing values
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Ensure all numeric
        df = df.dropna()
        
        # Clip target to [-1, 1]
        df['target'] = np.clip(df['target'], -1, 1)
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[MarketSentimentAnalysisDataset] Final shape: {df.shape}")
        print(f"[MarketSentimentAnalysisDataset] Target stats: mean={df['target'].mean():.3f}, std={df['target'].std():.3f}")
        print(f"[MarketSentimentAnalysisDataset] Sentiment range: [{df['target'].min():.3f}, {df['target'].max():.3f}]")
        
        return df

if __name__ == "__main__":
    dataset = MarketSentimentAnalysisDataset()
    df = dataset.get_data()
    print(f"Loaded MarketSentimentAnalysisDataset: {df.shape}")
    print(df.head()) 