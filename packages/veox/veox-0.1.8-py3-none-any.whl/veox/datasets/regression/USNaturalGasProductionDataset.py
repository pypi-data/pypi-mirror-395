import pandas as pd
import numpy as np
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class USNaturalGasProductionDataset(BaseDatasetLoader):
    """
    U.S. Natural Gas Production Data from Energy Information Administration (EIA).
    
    This dataset contains monthly natural gas production data that can be used for:
    - Gas Production Forecasting
    - Energy Market Analysis
    - Infrastructure Planning
    
    Data source: EIA Natural Gas Data - Monthly Gross Withdrawals
    https://www.eia.gov/dnav/ng/xls/NG_PROD_SUM_A_EPG0_FGW_MMCF_M.xls
    
    The dataset includes monthly natural gas production by state.
    """
    
    def get_dataset_info(self):
        return {
            "name": "USNaturalGasProductionDataset",
            "source_id": "eia_natural_gas_production",
            "source_url": "https://www.eia.gov/dnav/ng/xls/NG_PROD_SUM_A_EPG0_FGW_MMCF_M.xls",
            "category": "regression",
            "description": "U.S. natural gas production data for production forecasting",
            "target_column": "gas_production"
        }
    
    def download_dataset(self, info):
        """Download the Excel file from EIA and convert to CSV"""
        dataset_name = info["name"]
        url = info["source_url"]
        
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            # Read Excel file and convert to CSV
            import io
            excel_data = io.BytesIO(response.content)
            df = pd.read_excel(excel_data, sheet_name='Data 1', header=2)
            
            # Convert to CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue().encode()
            
        except Exception as e:
            print(f"[{dataset_name}] Error downloading: {e}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the natural gas production data to create features and target"""
        dataset_name = info["name"]
        
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        print(f"[{dataset_name}] Columns: {df.columns.tolist()[:10]}...")
        
        # Find date column (usually first column)
        date_col = df.columns[0]
        df['date'] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Remove rows with invalid dates
        df = df[df['date'].notna()]
        
        # Extract time features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['days_in_month'] = df['date'].dt.days_in_month
        
        # Create cyclical features for month and quarter
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['quarter_sin'] = np.sin(2 * np.pi * df['quarter'] / 4)
        df['quarter_cos'] = np.cos(2 * np.pi * df['quarter'] / 4)
        
        # Melt the dataframe to convert states from columns to rows
        value_vars = [col for col in df.columns if col not in ['date', 'year', 'month', 'quarter', 
                                                                'days_in_month', 'month_sin', 'month_cos',
                                                                'quarter_sin', 'quarter_cos', date_col]]
        
        df_melted = pd.melt(df, 
                           id_vars=['date', 'year', 'month', 'quarter', 'days_in_month', 
                                   'month_sin', 'month_cos', 'quarter_sin', 'quarter_cos'],
                           value_vars=value_vars,
                           var_name='state',
                           value_name='production')
        
        # Clean production values
        df_melted['production'] = pd.to_numeric(df_melted['production'], errors='coerce')
        
        # Remove invalid production values
        df_melted = df_melted[df_melted['production'].notna()]
        df_melted = df_melted[df_melted['production'] > 0]
        
        # Create state dummy variables (limit to major producing states)
        state_counts = df_melted['state'].value_counts()
        major_states = state_counts.head(20).index.tolist()
        df_melted['state_category'] = df_melted['state'].apply(
            lambda x: x if x in major_states else 'Other'
        )
        state_dummies = pd.get_dummies(df_melted['state_category'], prefix='state')
        df_melted = pd.concat([df_melted, state_dummies], axis=1)
        
        # Create lag features (previous months' production)
        df_melted = df_melted.sort_values(['state', 'date'])
        df_melted['production_lag1'] = df_melted.groupby('state')['production'].shift(1)
        df_melted['production_lag2'] = df_melted.groupby('state')['production'].shift(2)
        df_melted['production_lag3'] = df_melted.groupby('state')['production'].shift(3)
        df_melted['production_lag6'] = df_melted.groupby('state')['production'].shift(6)
        
        # Calculate moving averages
        df_melted['production_ma3'] = df_melted.groupby('state')['production'].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )
        df_melted['production_ma12'] = df_melted.groupby('state')['production'].transform(
            lambda x: x.rolling(window=12, min_periods=1).mean()
        )
        
        # Calculate year-over-year growth
        df_melted['production_yoy'] = df_melted.groupby('state')['production'].pct_change(12)
        df_melted['production_yoy'] = df_melted['production_yoy'].fillna(0)
        df_melted['production_yoy'] = np.clip(df_melted['production_yoy'], -1, 2)
        
        # Set target
        df_melted['target'] = df_melted['production']
        
        # Remove rows with missing lag features
        df_melted = df_melted.dropna(subset=['production_lag1', 'production_lag2', 'production_lag3'])
        
        # Select features for modeling
        feature_cols = ['year', 'month', 'quarter', 'days_in_month', 
                       'month_sin', 'month_cos', 'quarter_sin', 'quarter_cos',
                       'production_lag1', 'production_lag2', 'production_lag3', 'production_lag6',
                       'production_ma3', 'production_ma12', 'production_yoy']
        
        # Add state dummy columns
        state_cols = [col for col in df_melted.columns if col.startswith('state_')]
        feature_cols.extend(state_cols)
        
        # Keep only features and target
        final_cols = feature_cols + ['target']
        df_final = df_melted[final_cols]
        
        # Remove state_category if it exists
        if 'state_category' in df_final.columns:
            df_final = df_final.drop('state_category', axis=1)
        
        # Remove any remaining NaN values
        df_final = df_final.dropna()
        
        # Limit dataset size for efficiency
        if len(df_final) > 50000:
            df_final = df_final.sample(n=50000, random_state=42)
        
        # Shuffle the data
        df_final = df_final.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        # Convert all columns to int64 or float64
        for col in df_final.columns:
            if df_final[col].dtype == 'bool':
                df_final[col] = df_final[col].astype('int64')
            elif df_final[col].dtype == 'int32':
                df_final[col] = df_final[col].astype('int64')
            elif df_final[col].dtype == 'object':
                # Try to convert to numeric, otherwise drop
                try:
                    df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('float64')
                except:
                    print(f"[{dataset_name}] Dropping non-numeric column: {col}")
                    df_final = df_final.drop(col, axis=1)
            elif df_final[col].dtype not in ['int64', 'float64']:
                # Try to convert to float64
                df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('float64')
        
        print(f"[{dataset_name}] Final shape: {df_final.shape}")
        print(f"[{dataset_name}] Target statistics:")
        print(f"  Mean gas production: {df_final['target'].mean():.2f} MMCF")
        print(f"  Std gas production: {df_final['target'].std():.2f} MMCF")
        print(f"  Min gas production: {df_final['target'].min():.2f} MMCF")
        print(f"  Max gas production: {df_final['target'].max():.2f} MMCF")
        
        return df_final

if __name__ == "__main__":
    dataset = USNaturalGasProductionDataset()
    df = dataset.get_data()
    print(f"\nLoaded {len(df)} samples")
    print(f"Features: {df.columns.tolist()}")
    print(f"\nFirst 5 rows:")
    print(df.head()) 