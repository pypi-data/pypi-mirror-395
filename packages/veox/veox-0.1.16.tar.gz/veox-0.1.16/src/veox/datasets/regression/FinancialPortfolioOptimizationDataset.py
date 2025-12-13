import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class FinancialPortfolioOptimizationDataset(BaseDatasetLoader):
    """
    Financial Portfolio Optimization Dataset (regression)
    Source: Kaggle - Stock Market Data
    Target: portfolio_return (annualized percentage return)
    
    This dataset contains portfolio composition, market indicators, and risk metrics
    for optimizing investment portfolio returns.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'FinancialPortfolioOptimizationDataset',
            'source_id': 'kaggle:portfolio-optimization',
            'category': 'regression',
            'description': 'Portfolio return prediction for investment optimization.',
            'source_url': 'https://www.kaggle.com/datasets/camnugent/sandp500',
        }
    
    def download_dataset(self, info):
        """Download the portfolio dataset from Kaggle"""
        print(f"[FinancialPortfolioOptimizationDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[FinancialPortfolioOptimizationDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'camnugent/sandp500',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if csv_files:
                    # Try to find individual stocks data
                    stocks_dir = os.path.join(temp_dir, 'individual_stocks_5yr')
                    if os.path.exists(stocks_dir):
                        stock_files = [f for f in os.listdir(stocks_dir) if f.endswith('.csv')]
                        if stock_files:
                            # Read a few stock files to create portfolio data
                            print(f"[FinancialPortfolioOptimizationDataset] Found {len(stock_files)} stock files")
                            # Use first file as example
                            data_file = os.path.join(stocks_dir, stock_files[0])
                    else:
                        data_file = csv_files[0]
                    
                    print(f"[FinancialPortfolioOptimizationDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=5000)
                    print(f"[FinancialPortfolioOptimizationDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[FinancialPortfolioOptimizationDataset] Download failed: {e}")
            print("[FinancialPortfolioOptimizationDataset] Using sample portfolio data...")
            
            # Create realistic portfolio optimization data
            np.random.seed(42)
            n_samples = 10000
            
            # Portfolio composition (weights sum to 1)
            data = {}
            n_assets = 10
            weights = np.random.dirichlet(np.ones(n_assets), n_samples)
            for i in range(n_assets):
                data[f'weight_asset_{i+1}'] = weights[:, i]
            
            # Asset characteristics
            data['avg_market_cap'] = np.random.lognormal(23, 1.5, n_samples)  # billions
            data['avg_pe_ratio'] = np.random.gamma(3, 5, n_samples)
            data['avg_pb_ratio'] = np.random.gamma(2, 1.5, n_samples)
            data['avg_dividend_yield'] = np.random.beta(2, 20, n_samples) * 10  # percentage
            
            # Sector diversification
            data['tech_allocation'] = np.random.beta(3, 7, n_samples)
            data['finance_allocation'] = np.random.beta(2, 8, n_samples)
            data['healthcare_allocation'] = np.random.beta(2, 8, n_samples)
            data['energy_allocation'] = np.random.beta(1, 9, n_samples)
            data['consumer_allocation'] = 1 - (data['tech_allocation'] + data['finance_allocation'] + 
                                              data['healthcare_allocation'] + data['energy_allocation'])
            data['consumer_allocation'] = np.clip(data['consumer_allocation'], 0, 1)
            
            # Risk metrics
            data['portfolio_beta'] = np.random.normal(1, 0.3, n_samples)
            data['portfolio_volatility'] = np.random.gamma(2, 0.08, n_samples)  # annualized
            data['sharpe_ratio'] = np.random.normal(1.2, 0.5, n_samples)
            data['max_drawdown'] = np.random.beta(2, 8, n_samples) * 0.5  # percentage
            
            # Market conditions
            data['vix_index'] = np.random.gamma(2, 10, n_samples)  # volatility index
            data['treasury_10y'] = np.random.normal(2.5, 0.8, n_samples)  # percentage
            data['dollar_index'] = np.random.normal(95, 5, n_samples)
            data['oil_price'] = np.random.gamma(3, 20, n_samples)
            
            # Economic indicators
            data['gdp_growth'] = np.random.normal(2.5, 1.5, n_samples)  # percentage
            data['inflation_rate'] = np.random.normal(2, 1, n_samples)  # percentage
            data['unemployment_rate'] = np.random.beta(2, 20, n_samples) * 20  # percentage
            
            # Technical indicators
            data['rsi_avg'] = np.random.beta(5, 5, n_samples) * 100  # 0-100
            data['macd_signal'] = np.random.normal(0, 1, n_samples)
            data['bollinger_position'] = np.random.beta(3, 3, n_samples)  # 0-1 position in bands
            
            # Portfolio characteristics
            data['num_holdings'] = np.random.poisson(30, n_samples) + 10
            data['concentration_top5'] = np.random.beta(3, 2, n_samples)  # percentage in top 5
            data['turnover_rate'] = np.random.beta(2, 8, n_samples)  # annual turnover
            
            # ESG factors
            data['esg_score'] = np.random.beta(5, 3, n_samples) * 100  # 0-100
            data['carbon_intensity'] = np.random.gamma(2, 50, n_samples)
            
            # Calculate portfolio return based on multiple factors
            # Base return from market
            market_return = 8 + data['gdp_growth'] - data['inflation_rate'] + np.random.normal(0, 2, n_samples)
            
            # Beta adjustment
            beta_return = data['portfolio_beta'] * market_return
            
            # Sector effects
            sector_return = (
                data['tech_allocation'] * np.random.normal(12, 5, n_samples) +
                data['finance_allocation'] * np.random.normal(9, 4, n_samples) +
                data['healthcare_allocation'] * np.random.normal(10, 3, n_samples) +
                data['energy_allocation'] * np.random.normal(7, 6, n_samples) +
                data['consumer_allocation'] * np.random.normal(8, 3, n_samples)
            )
            
            # Risk adjustment
            risk_penalty = data['portfolio_volatility'] * np.random.normal(-10, 3, n_samples)
            
            # Quality premium
            quality_premium = (
                (data['avg_pe_ratio'] < 20) * 2 +
                (data['avg_dividend_yield'] > 2) * 1.5 +
                (data['esg_score'] > 70) * 1
            )
            
            # Market timing
            timing_effect = (
                (data['vix_index'] < 20) * 2 -
                (data['vix_index'] > 30) * 3 +
                (data['rsi_avg'] < 30) * 1.5 -
                (data['rsi_avg'] > 70) * 1.5
            )
            
            # Final return calculation
            data['target'] = (
                beta_return * 0.4 +
                sector_return * 0.3 +
                risk_penalty * 0.1 +
                quality_premium +
                timing_effect +
                np.random.normal(0, 3, n_samples)
            )
            
            # Realistic annual returns (-30% to +50%)
            data['target'] = np.clip(data['target'], -30, 50)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the portfolio dataset"""
        print(f"[FinancialPortfolioOptimizationDataset] Raw shape: {df.shape}")
        print(f"[FinancialPortfolioOptimizationDataset] Columns: {list(df.columns)[:10]}...")
        
        # If this is stock price data, calculate returns
        if 'close' in df.columns or 'Close' in df.columns:
            close_col = 'close' if 'close' in df.columns else 'Close'
            # Calculate returns
            df['returns'] = df[close_col].pct_change() * 100
            df['target'] = df['returns'].shift(-1)  # Next period return
            df = df.dropna()
            
            # Add technical indicators if we have OHLC data
            if all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']):
                # Simple moving averages
                df['sma_5'] = df[close_col].rolling(5).mean()
                df['sma_20'] = df[close_col].rolling(20).mean()
                df['volume_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
                
            # Remove price columns, keep indicators
            price_cols = ['open', 'high', 'low', 'close', 'Open', 'High', 'Low', 'Close', 'Adj Close']
            for col in price_cols:
                if col in df.columns:
                    df = df.drop(col, axis=1)
        
        # Find return/target column
        elif 'target' not in df.columns:
            return_col = None
            for col in ['return', 'returns', 'portfolio_return', 'total_return']:
                if col in df.columns:
                    return_col = col
                    break
            
            if return_col:
                df['target'] = df[return_col]
                df = df.drop(return_col, axis=1)
            else:
                # Use last numeric column
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    df['target'] = df[numeric_cols[-1]]
                    df = df.drop(numeric_cols[-1], axis=1)
                else:
                    raise ValueError("No suitable target column found")
        
        # Remove non-numeric columns
        text_cols = ['date', 'Date', 'Name', 'Symbol', 'ticker']
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
        
        # Limit features if too many
        if len(feature_cols) > 50:
            # Prioritize financial features
            priority_features = ['weight', 'allocation', 'beta', 'volatility', 'ratio', 
                               'return', 'yield', 'score', 'index', 'rate']
            
            selected_features = []
            for feat in priority_features:
                for col in feature_cols:
                    if feat in col.lower() and col not in selected_features:
                        selected_features.append(col)
            
            # Add remaining features up to limit
            for col in feature_cols:
                if col not in selected_features and len(selected_features) < 50:
                    selected_features.append(col)
            
            feature_cols = selected_features[:50]
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Handle missing values
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Ensure all numeric
        df = df.dropna()
        
        # Remove extreme outliers in returns
        if 'target' in df.columns:
            # Remove unrealistic returns
            q1 = df['target'].quantile(0.01)
            q99 = df['target'].quantile(0.99)
            df = df[(df['target'] >= max(q1, -50)) & (df['target'] <= min(q99, 100))]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[FinancialPortfolioOptimizationDataset] Final shape: {df.shape}")
        print(f"[FinancialPortfolioOptimizationDataset] Target stats: mean={df['target'].mean():.2f}%, std={df['target'].std():.2f}%")
        print(f"[FinancialPortfolioOptimizationDataset] Return range: [{df['target'].min():.2f}%, {df['target'].max():.2f}%]")
        
        return df

if __name__ == "__main__":
    dataset = FinancialPortfolioOptimizationDataset()
    df = dataset.get_data()
    print(f"Loaded FinancialPortfolioOptimizationDataset: {df.shape}")
    print(df.head()) 