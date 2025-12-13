import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ProductionForecastingDataset(BaseDatasetLoader):
    """
    Production Forecasting Dataset (regression)
    Source: Kaggle - Oil Production Time Series
    Target: oil_production_bopd (barrels of oil per day)
    
    This dataset contains historical production data and reservoir parameters
    for forecasting future oil and gas production rates.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'ProductionForecastingDataset',
            'source_id': 'kaggle:production-forecasting',
            'category': 'regression',
            'description': 'Oil production rate forecasting from historical and reservoir data.',
            'source_url': 'https://www.kaggle.com/datasets/aemyjutt/oil-production',
        }
    
    def download_dataset(self, info):
        """Download the production forecasting dataset from Kaggle"""
        print(f"[ProductionForecastingDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[ProductionForecastingDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'aemyjutt/oil-production',
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
                    data_file = csv_files[0]
                    print(f"[ProductionForecastingDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=10000)
                    print(f"[ProductionForecastingDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[ProductionForecastingDataset] Download failed: {e}")
            print("[ProductionForecastingDataset] Using sample production data...")
            
            # Create realistic production forecasting data
            np.random.seed(42)
            n_samples = 8000
            
            # Well and reservoir characteristics
            data = {}
            data['well_age_days'] = np.random.uniform(0, 3650, n_samples)  # 0-10 years
            data['initial_production_bopd'] = np.random.lognormal(6, 1, n_samples)
            data['reservoir_pressure_psi'] = 3000 - data['well_age_days'] * 0.3 + np.random.normal(0, 100, n_samples)
            data['reservoir_temperature_degf'] = np.random.normal(180, 20, n_samples)
            
            # Production history features
            data['cumulative_oil_mbbl'] = data['initial_production_bopd'] * data['well_age_days'] / 1000 * np.random.uniform(0.7, 0.9, n_samples)
            data['cumulative_gas_mmcf'] = data['cumulative_oil_mbbl'] * np.random.uniform(0.5, 2, n_samples)
            data['cumulative_water_mbbl'] = data['cumulative_oil_mbbl'] * (1 - np.exp(-data['well_age_days'] / 1000)) * np.random.uniform(0.1, 0.5, n_samples)
            
            # Current production metrics
            decline_factor = np.exp(-data['well_age_days'] / 1000)
            data['current_oil_rate_bopd'] = data['initial_production_bopd'] * decline_factor * np.random.uniform(0.8, 1.2, n_samples)
            data['current_gas_rate_mcfd'] = data['current_oil_rate_bopd'] * np.random.uniform(0.5, 2, n_samples)
            data['current_water_rate_bwpd'] = data['current_oil_rate_bopd'] * (1 - decline_factor) * np.random.uniform(0.1, 0.5, n_samples)
            
            # Decline curve parameters
            data['decline_rate_annual'] = np.random.beta(2, 5, n_samples) * 0.5  # 0-50% annual decline
            data['b_factor'] = np.random.uniform(0, 1, n_samples)  # Arps b-factor
            data['decline_type'] = np.random.choice([1, 2, 3], n_samples)  # Exponential, Hyperbolic, Harmonic
            
            # Operating conditions
            data['choke_size_64ths'] = np.random.choice([16, 20, 24, 28, 32, 36, 40], n_samples)
            data['tubing_pressure_psi'] = data['reservoir_pressure_psi'] * np.random.uniform(0.3, 0.5, n_samples)
            data['casing_pressure_psi'] = data['tubing_pressure_psi'] * np.random.uniform(1.1, 1.3, n_samples)
            data['flowing_bottomhole_pressure_psi'] = data['reservoir_pressure_psi'] * np.random.uniform(0.5, 0.8, n_samples)
            
            # Artificial lift
            data['artificial_lift_type'] = np.random.choice([0, 1, 2, 3, 4], n_samples)  # None, Rod pump, ESP, Gas lift, PCP
            data['pump_efficiency'] = np.where(data['artificial_lift_type'] > 0, np.random.beta(8, 2, n_samples), 0)
            data['injection_rate_mcfd'] = np.where(data['artificial_lift_type'] == 3, np.random.uniform(100, 1000, n_samples), 0)
            
            # Reservoir properties
            data['porosity'] = np.random.beta(3, 7, n_samples) * 0.35
            data['permeability_md'] = np.random.lognormal(3, 1.5, n_samples)
            data['oil_saturation'] = np.random.beta(4, 2, n_samples) * 0.8
            data['reservoir_thickness_ft'] = np.random.gamma(2, 20, n_samples)
            data['drainage_area_acres'] = np.random.lognormal(4, 0.5, n_samples)
            
            # PVT properties
            data['oil_api_gravity'] = np.random.normal(35, 5, n_samples)
            data['gas_specific_gravity'] = np.random.normal(0.7, 0.1, n_samples)
            data['oil_viscosity_cp'] = 10 ** (3.5 - 0.025 * data['oil_api_gravity'])
            data['formation_volume_factor'] = 1 + np.random.uniform(0.1, 0.5, n_samples)
            
            # Economic and operational
            data['oil_price_usd'] = np.random.normal(70, 15, n_samples)
            data['operating_cost_usd_bbl'] = np.random.normal(15, 5, n_samples)
            data['workover_count'] = np.random.poisson(data['well_age_days'] / 500, n_samples)
            data['last_workover_days_ago'] = np.random.exponential(180, n_samples)
            
            # Calculate future production (target) - 30 days ahead
            # Using modified Arps decline equation
            time_delta = 30  # days
            
            # Exponential decline
            exp_decline = data['current_oil_rate_bopd'] * np.exp(-data['decline_rate_annual'] / 365 * time_delta)
            
            # Hyperbolic decline
            hyp_decline = data['current_oil_rate_bopd'] / ((1 + data['b_factor'] * data['decline_rate_annual'] / 365 * time_delta) ** (1 / data['b_factor']))
            
            # Harmonic decline (b=1)
            harm_decline = data['current_oil_rate_bopd'] / (1 + data['decline_rate_annual'] / 365 * time_delta)
            
            # Select based on decline type
            future_production = np.where(
                data['decline_type'] == 1, exp_decline,
                np.where(data['decline_type'] == 2, hyp_decline, harm_decline)
            )
            
            # Add effects of operations
            # Workover boost
            workover_effect = np.where(
                data['last_workover_days_ago'] < 30,
                1.2,
                1.0
            )
            
            # Artificial lift effect
            lift_effect = np.where(
                data['artificial_lift_type'] > 0,
                1 + 0.2 * data['pump_efficiency'],
                1.0
            )
            
            # Pressure maintenance effect
            pressure_effect = data['flowing_bottomhole_pressure_psi'] / data['reservoir_pressure_psi']
            
            # Final production with noise
            data['target'] = np.maximum(
                future_production * workover_effect * lift_effect * pressure_effect + np.random.normal(0, 50, n_samples),
                0
            )
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the production forecasting dataset"""
        print(f"[ProductionForecastingDataset] Raw shape: {df.shape}")
        print(f"[ProductionForecastingDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find production target column
        target_col = None
        for col in ['oil_production', 'production', 'oil_rate', 'bopd', 'target']:
            if col in df.columns:
                target_col = col
                break
            # Check for columns containing these terms
            for df_col in df.columns:
                if 'production' in df_col.lower() or 'rate' in df_col.lower():
                    if 'future' in df_col.lower() or 'forecast' in df_col.lower() or 'next' in df_col.lower():
                        target_col = df_col
                        break
            if target_col:
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Try to use last production value as target
            prod_cols = [col for col in df.columns if 'prod' in col.lower() or 'rate' in col.lower()]
            if prod_cols:
                # Use the last one as future production
                df['target'] = df[prod_cols[-1]]
                df = df.drop(prod_cols[-1], axis=1)
            else:
                # Generate synthetic production
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    df['target'] = np.abs(df[numeric_cols].mean(axis=1) * 100 + np.random.normal(0, 50, len(df)))
                else:
                    df['target'] = np.random.lognormal(5, 1, len(df))
        
        # Remove non-numeric columns
        text_cols = ['well_name', 'field', 'operator', 'date', 'api_number']
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
        if len(feature_cols) > 40:
            # Prioritize production-relevant features
            priority_features = ['production', 'rate', 'pressure', 'cumulative', 'decline',
                               'reservoir', 'porosity', 'permeability', 'saturation', 'age']
            
            selected_features = []
            for feat in priority_features:
                for col in feature_cols:
                    if feat in col.lower() and col not in selected_features:
                        selected_features.append(col)
            
            # Add remaining features up to limit
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
        
        # Ensure positive production values
        df = df[df['target'] >= 0]
        
        # Remove extreme outliers
        q99 = df['target'].quantile(0.99)
        df = df[df['target'] <= q99 * 2]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[ProductionForecastingDataset] Final shape: {df.shape}")
        print(f"[ProductionForecastingDataset] Target stats: mean={df['target'].mean():.2f} bopd, std={df['target'].std():.2f} bopd")
        print(f"[ProductionForecastingDataset] Production range: [{df['target'].min():.2f}, {df['target'].max():.2f}] bopd")
        
        return df

if __name__ == "__main__":
    dataset = ProductionForecastingDataset()
    df = dataset.get_data()
    print(f"Loaded ProductionForecastingDataset: {df.shape}")
    print(df.head()) 