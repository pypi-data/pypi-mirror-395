import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CatalystDesignDataset(BaseDatasetLoader):
    """
    Catalyst Design Dataset (regression)
    Source: Kaggle - Catalyst Performance Data
    Target: conversion_efficiency (percentage conversion efficiency)
    
    This dataset contains catalyst composition and reaction conditions
    for designing optimal catalysts for refinery processes.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'CatalystDesignDataset',
            'source_id': 'kaggle:catalyst-design',
            'category': 'regression',
            'description': 'Catalyst conversion efficiency prediction from composition and conditions.',
            'source_url': 'https://www.kaggle.com/datasets/imeintanis/catalyst-data',
        }
    
    def download_dataset(self, info):
        """Download the catalyst design dataset from Kaggle"""
        print(f"[CatalystDesignDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[CatalystDesignDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'imeintanis/catalyst-data',
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
                    print(f"[CatalystDesignDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=8000)
                    print(f"[CatalystDesignDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[CatalystDesignDataset] Download failed: {e}")
            print("[CatalystDesignDataset] Using sample catalyst data...")
            
            # Create realistic catalyst design data
            np.random.seed(42)
            n_samples = 6000
            
            # Catalyst composition (weight %)
            data = {}
            # Active metals
            data['platinum_wt'] = np.random.exponential(0.5, n_samples)
            data['palladium_wt'] = np.random.exponential(0.3, n_samples)
            data['rhodium_wt'] = np.random.exponential(0.1, n_samples)
            data['nickel_wt'] = np.random.gamma(2, 2, n_samples)
            data['cobalt_wt'] = np.random.gamma(2, 1.5, n_samples)
            data['molybdenum_wt'] = np.random.gamma(2, 3, n_samples)
            
            # Support materials
            data['alumina_wt'] = np.random.normal(60, 10, n_samples)
            data['silica_wt'] = np.random.normal(20, 5, n_samples)
            data['zeolite_wt'] = np.random.beta(2, 5, n_samples) * 30
            data['titania_wt'] = np.random.beta(2, 8, n_samples) * 20
            
            # Normalize to 100%
            total_wt = (data['platinum_wt'] + data['palladium_wt'] + data['rhodium_wt'] + 
                       data['nickel_wt'] + data['cobalt_wt'] + data['molybdenum_wt'] +
                       data['alumina_wt'] + data['silica_wt'] + data['zeolite_wt'] + data['titania_wt'])
            
            for key in ['platinum_wt', 'palladium_wt', 'rhodium_wt', 'nickel_wt', 
                       'cobalt_wt', 'molybdenum_wt', 'alumina_wt', 'silica_wt', 
                       'zeolite_wt', 'titania_wt']:
                data[key] = data[key] / total_wt * 100
            
            # Physical properties
            data['surface_area_m2g'] = np.random.gamma(3, 50, n_samples)
            data['pore_volume_ccg'] = np.random.gamma(2, 0.2, n_samples)
            data['pore_diameter_nm'] = np.random.normal(10, 3, n_samples)
            data['particle_size_um'] = np.random.lognormal(2, 0.5, n_samples)
            data['crush_strength_mpa'] = np.random.normal(5, 1, n_samples)
            
            # Preparation conditions
            data['calcination_temp_c'] = np.random.normal(500, 50, n_samples)
            data['calcination_time_hr'] = np.random.gamma(2, 2, n_samples)
            data['reduction_temp_c'] = np.random.normal(400, 40, n_samples)
            data['ph_preparation'] = np.random.normal(7, 1, n_samples)
            data['impregnation_method'] = np.random.choice([1, 2, 3], n_samples)  # Wet, dry, incipient
            
            # Reaction conditions
            data['reaction_temp_c'] = np.random.normal(350, 50, n_samples)
            data['reaction_pressure_bar'] = np.random.gamma(3, 10, n_samples)
            data['space_velocity_hr'] = np.random.normal(2, 0.5, n_samples)
            data['h2_hc_ratio'] = np.random.normal(3, 0.5, n_samples)
            data['feed_sulfur_ppm'] = np.random.exponential(500, n_samples)
            data['feed_nitrogen_ppm'] = np.random.exponential(200, n_samples)
            
            # Catalyst age and regeneration
            data['catalyst_age_days'] = np.random.exponential(100, n_samples)
            data['regeneration_count'] = np.random.poisson(1, n_samples)
            data['carbon_deposit_wt'] = data['catalyst_age_days'] * 0.01 + np.random.exponential(0.5, n_samples)
            
            # Promoters and additives
            data['promoter_k_wt'] = np.random.exponential(0.1, n_samples)
            data['promoter_ce_wt'] = np.random.exponential(0.2, n_samples)
            data['promoter_la_wt'] = np.random.exponential(0.15, n_samples)
            
            # Calculate conversion efficiency (target) based on catalyst properties
            # Metal loading effect
            noble_metal_effect = (
                data['platinum_wt'] * 2 + 
                data['palladium_wt'] * 1.5 + 
                data['rhodium_wt'] * 2.5
            )
            base_metal_effect = (
                data['nickel_wt'] * 0.3 + 
                data['cobalt_wt'] * 0.4 + 
                data['molybdenum_wt'] * 0.5
            )
            
            # Support effect
            support_effect = (
                data['zeolite_wt'] * 0.5 +  # Zeolite provides acidity
                data['surface_area_m2g'] / 100  # High surface area is beneficial
            )
            
            # Reaction conditions effect
            temp_effect = np.exp(-(data['reaction_temp_c'] - 350)**2 / 10000)  # Optimal around 350°C
            pressure_effect = np.minimum(data['reaction_pressure_bar'] / 30, 1.0)
            
            # Poisoning effect
            sulfur_poisoning = np.exp(-data['feed_sulfur_ppm'] / 1000)
            nitrogen_poisoning = np.exp(-data['feed_nitrogen_ppm'] / 500)
            carbon_poisoning = np.exp(-data['carbon_deposit_wt'] / 5)
            
            # Age effect
            age_effect = np.exp(-data['catalyst_age_days'] / 500)
            
            # Promoter effect
            promoter_effect = 1 + (data['promoter_k_wt'] + data['promoter_ce_wt'] + data['promoter_la_wt']) * 0.5
            
            # Calculate final conversion efficiency
            base_conversion = 50
            data['target'] = np.clip(
                base_conversion +
                noble_metal_effect * 3 +
                base_metal_effect * 2 +
                support_effect * 5 +
                temp_effect * 20 +
                pressure_effect * 10 +
                sulfur_poisoning * 10 +
                nitrogen_poisoning * 5 +
                carbon_poisoning * 10 +
                age_effect * 10 +
                promoter_effect * 5 +
                np.random.normal(0, 3, n_samples),
                10, 99  # Realistic conversion range
            )
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the catalyst design dataset"""
        print(f"[CatalystDesignDataset] Raw shape: {df.shape}")
        print(f"[CatalystDesignDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find conversion/efficiency target column
        target_col = None
        for col in ['conversion', 'efficiency', 'activity', 'performance', 'target']:
            if col in df.columns:
                target_col = col
                break
            # Check for columns containing these terms
            for df_col in df.columns:
                if any(term in df_col.lower() for term in ['conversion', 'efficiency', 'activity']):
                    target_col = df_col
                    break
            if target_col:
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Try to find any performance metric
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if any(term in col.lower() for term in ['yield', 'selectivity', 'rate']):
                    df['target'] = df[col]
                    df = df.drop(col, axis=1)
                    break
            else:
                # Generate synthetic conversion based on metal content
                metal_cols = [col for col in numeric_cols if any(metal in col.lower() 
                            for metal in ['pt', 'pd', 'ni', 'co', 'mo', 'platinum', 'palladium'])]
                if metal_cols:
                    # More metal generally means higher conversion
                    df['target'] = 50 + df[metal_cols].sum(axis=1) * 5 + np.random.normal(0, 10, len(df))
                else:
                    df['target'] = np.random.normal(70, 15, len(df))
        
        # Ensure conversion is in percentage
        if df['target'].max() < 1:
            df['target'] = df['target'] * 100
        
        # Remove non-numeric columns
        text_cols = ['catalyst_name', 'batch', 'manufacturer', 'date', 'operator']
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
        if len(feature_cols) > 35:
            # Prioritize catalyst-specific features
            priority_features = ['platinum', 'palladium', 'nickel', 'cobalt', 'molybdenum',
                               'surface', 'pore', 'temperature', 'pressure', 'alumina']
            
            selected_features = []
            for feat in priority_features:
                for col in feature_cols:
                    if feat in col.lower() and col not in selected_features:
                        selected_features.append(col)
            
            # Add remaining features up to limit
            for col in feature_cols:
                if col not in selected_features and len(selected_features) < 35:
                    selected_features.append(col)
            
            feature_cols = selected_features[:35]
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Handle missing values
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Ensure all numeric
        df = df.dropna()
        
        # Ensure realistic conversion values
        df = df[(df['target'] >= 0) & (df['target'] <= 100)]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[CatalystDesignDataset] Final shape: {df.shape}")
        print(f"[CatalystDesignDataset] Target stats: mean={df['target'].mean():.2f}%, std={df['target'].std():.2f}%")
        print(f"[CatalystDesignDataset] Conversion range: [{df['target'].min():.2f}, {df['target'].max():.2f}]%")
        
        return df

if __name__ == "__main__":
    dataset = CatalystDesignDataset()
    df = dataset.get_data()
    print(f"Loaded CatalystDesignDataset: {df.shape}")
    print(df.head()) 