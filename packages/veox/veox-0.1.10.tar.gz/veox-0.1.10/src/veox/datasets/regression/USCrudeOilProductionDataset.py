import pandas as pd
import numpy as np
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class USCrudeOilProductionDataset(BaseDatasetLoader):
    """
    U.S. Crude Oil Production Data from Energy Information Administration (EIA).
    
    This dataset contains monthly crude oil production data that can be used for:
    - Production Forecasting and Optimization
    - Energy Market Analysis
    - Supply Chain Planning
    
    Data source: EIA Petroleum Data - Monthly Crude Oil Production
    https://www.eia.gov/dnav/pet/xls/PET_CRD_CRPDN_ADC_MBBL_M.xls
    
    The dataset includes monthly production data by state.
    """
    
    def get_dataset_info(self):
        return {
            "name": "USCrudeOilProductionDataset",
            "source_id": "eia_crude_oil_production",
            "source_url": "https://www.eia.gov/dnav/pet/xls/PET_CRD_CRPDN_ADC_MBBL_M.xls",
            "category": "regression",
            "description": "U.S. crude oil production data for production forecasting",
            "target_column": "production_volume"
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
        """Process the production data to create features and target"""
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
        
        # Create cyclical features for month
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Melt the dataframe to convert states from columns to rows
        value_vars = [col for col in df.columns if col not in ['date', 'year', 'month', 'quarter', 
                                                                'days_in_month', 'month_sin', 'month_cos', date_col]]
        
        df_melted = pd.melt(df, 
                           id_vars=['date', 'year', 'month', 'quarter', 'days_in_month', 
                                   'month_sin', 'month_cos'],
                           value_vars=value_vars,
                           var_name='state',
                           value_name='production')
        
        # Clean production values
        df_melted['production'] = pd.to_numeric(df_melted['production'], errors='coerce')
        
        # Remove invalid production values
        df_melted = df_melted[df_melted['production'].notna()]
        df_melted = df_melted[df_melted['production'] > 0]
        
        # Create state dummy variables
        state_dummies = pd.get_dummies(df_melted['state'], prefix='state')
        df_melted = pd.concat([df_melted, state_dummies], axis=1)
        
        # Create lag features (previous month's production)
        df_melted = df_melted.sort_values(['state', 'date'])
        df_melted['production_lag1'] = df_melted.groupby('state')['production'].shift(1)
        df_melted['production_lag2'] = df_melted.groupby('state')['production'].shift(2)
        df_melted['production_lag3'] = df_melted.groupby('state')['production'].shift(3)
        
        # Calculate moving averages
        df_melted['production_ma3'] = df_melted.groupby('state')['production'].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )
        df_melted['production_ma6'] = df_melted.groupby('state')['production'].transform(
            lambda x: x.rolling(window=6, min_periods=1).mean()
        )
        
        # Set target
        df_melted['target'] = df_melted['production']
        
        # Remove rows with missing lag features
        df_melted = df_melted.dropna(subset=['production_lag1', 'production_lag2', 'production_lag3'])
        
        # Select features for modeling
        feature_cols = ['year', 'month', 'quarter', 'days_in_month', 'month_sin', 'month_cos',
                       'production_lag1', 'production_lag2', 'production_lag3',
                       'production_ma3', 'production_ma6']
        
        # Add state dummy columns
        state_cols = [col for col in df_melted.columns if col.startswith('state_')]
        feature_cols.extend(state_cols)
        
        # Keep only features and target
        final_cols = feature_cols + ['target']
        df_final = df_melted[final_cols]
        
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
            elif df_final[col].dtype not in ['int64', 'float64']:
                # Try to convert to float64
                df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('float64')
        
        print(f"[{dataset_name}] Final shape: {df_final.shape}")
        print(f"[{dataset_name}] Target statistics:")
        print(f"  Mean production: {df_final['target'].mean():.2f} thousand barrels")
        print(f"  Std production: {df_final['target'].std():.2f} thousand barrels")
        print(f"  Min production: {df_final['target'].min():.2f} thousand barrels")
        print(f"  Max production: {df_final['target'].max():.2f} thousand barrels")
        
        return df_final

if __name__ == "__main__":
    dataset = USCrudeOilProductionDataset()
    df = dataset.get_data()
    print(f"\nLoaded {len(df)} samples")
    print(f"Features: {df.columns.tolist()}")
    print(f"\nFirst 5 rows:")
    print(df.head()) 