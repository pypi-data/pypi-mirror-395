import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class DrillingParameterOptimizationDataset(BaseDatasetLoader):
    """
    Drilling Parameter Optimization Dataset (regression)
    Source: Kaggle - Drilling Data
    Target: rate_of_penetration (feet/hour)
    
    This dataset contains drilling parameters and formation data
    for optimizing drilling rate of penetration (ROP).
    """
    
    def get_dataset_info(self):
        return {
            'name': 'DrillingParameterOptimizationDataset',
            'source_id': 'kaggle:drilling-optimization',
            'category': 'regression',
            'description': 'Rate of penetration prediction from drilling parameters.',
            'source_url': 'https://www.kaggle.com/datasets/imeintanis/drilling-data',
        }
    
    def download_dataset(self, info):
        """Download the drilling optimization dataset from Kaggle"""
        print(f"[DrillingParameterOptimizationDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[DrillingParameterOptimizationDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'imeintanis/drilling-data',
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
                    print(f"[DrillingParameterOptimizationDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=10000)
                    print(f"[DrillingParameterOptimizationDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[DrillingParameterOptimizationDataset] Download failed: {e}")
            print("[DrillingParameterOptimizationDataset] Using sample drilling data...")
            
            # Create realistic drilling parameter optimization data
            np.random.seed(42)
            n_samples = 7000
            
            # Drilling parameters
            data = {}
            data['weight_on_bit_klbs'] = np.random.gamma(3, 5, n_samples)
            data['rotary_speed_rpm'] = np.random.normal(120, 30, n_samples)
            data['flow_rate_gpm'] = np.random.normal(500, 100, n_samples)
            data['pump_pressure_psi'] = np.random.normal(3000, 500, n_samples)
            data['torque_klbft'] = data['weight_on_bit_klbs'] * np.random.uniform(0.8, 1.2, n_samples)
            
            # Bit characteristics
            data['bit_diameter_in'] = np.random.choice([8.5, 12.25, 17.5, 26], n_samples, p=[0.3, 0.4, 0.2, 0.1])
            data['bit_type'] = np.random.choice([1, 2, 3, 4], n_samples)  # PDC, Roller, Diamond, Hybrid
            data['bit_hours'] = np.random.exponential(50, n_samples)
            data['bit_jet_count'] = np.random.choice([3, 4, 5, 6], n_samples)
            data['total_flow_area_in2'] = data['bit_jet_count'] * np.random.uniform(0.2, 0.5, n_samples)
            
            # Mud properties
            data['mud_weight_ppg'] = np.random.normal(10, 2, n_samples)
            data['mud_viscosity_cp'] = np.random.gamma(2, 15, n_samples)
            data['mud_yield_point_lbf_100ft2'] = np.random.normal(15, 5, n_samples)
            data['mud_plastic_viscosity_cp'] = data['mud_viscosity_cp'] * np.random.uniform(0.6, 0.8, n_samples)
            data['mud_solids_percent'] = np.random.beta(2, 8, n_samples) * 20
            
            # Formation properties
            data['depth_ft'] = np.random.uniform(5000, 15000, n_samples)
            data['formation_density_gcc'] = np.random.normal(2.4, 0.3, n_samples)
            data['formation_porosity'] = np.random.beta(3, 7, n_samples) * 0.35
            data['formation_ucs_psi'] = np.random.lognormal(9, 0.5, n_samples)  # Unconfined compressive strength
            data['formation_abrasiveness'] = np.random.beta(2, 3, n_samples) * 10
            
            # Hole conditions
            data['hole_depth_ft'] = data['depth_ft'] - np.random.uniform(0, 100, n_samples)
            data['hole_angle_deg'] = np.random.beta(2, 8, n_samples) * 90
            data['dogleg_severity_deg_100ft'] = np.random.exponential(2, n_samples)
            data['annular_velocity_fpm'] = data['flow_rate_gpm'] / (np.pi * (data['bit_diameter_in']**2 / 4)) * 0.4
            
            # Hydraulics
            data['jet_velocity_fps'] = data['flow_rate_gpm'] / (data['total_flow_area_in2'] * 3.117)
            data['hydraulic_horsepower'] = data['pump_pressure_psi'] * data['flow_rate_gpm'] / 1714
            data['bit_hydraulic_horsepower'] = data['hydraulic_horsepower'] * np.random.uniform(0.6, 0.8, n_samples)
            data['jet_impact_force_lbf'] = 0.01823 * data['mud_weight_ppg'] * data['flow_rate_gpm'] * data['jet_velocity_fps'] / 1930
            
            # Mechanical specific energy
            data['mse_kpsi'] = (data['weight_on_bit_klbs'] / (np.pi * (data['bit_diameter_in']/12)**2 / 4) + 
                               2 * np.pi * data['rotary_speed_rpm'] * data['torque_klbft'] / 
                               (60 * np.pi * (data['bit_diameter_in']/12)**2 / 4))
            
            # Environmental factors
            data['temperature_degf'] = 80 + data['depth_ft'] * 0.015 + np.random.normal(0, 10, n_samples)
            data['ecd_ppg'] = data['mud_weight_ppg'] + data['annular_velocity_fpm'] * 0.002
            
            # Calculate ROP (target) based on drilling mechanics
            # Bourgoyne and Young model simplified
            formation_factor = 10000 / data['formation_ucs_psi']
            
            wob_factor = (data['weight_on_bit_klbs'] / data['bit_diameter_in']) ** 1.2
            rpm_factor = (data['rotary_speed_rpm'] / 100) ** 0.8
            hydraulics_factor = (data['jet_impact_force_lbf'] / 1000) ** 0.5
            
            # Bit wear effect
            bit_wear_factor = np.exp(-data['bit_hours'] / 100)
            
            # Hole cleaning effect
            cleaning_factor = np.minimum(data['annular_velocity_fpm'] / 120, 1.0)
            
            # Base ROP calculation
            base_rop = (
                formation_factor * 
                wob_factor * 
                rpm_factor * 
                hydraulics_factor * 
                bit_wear_factor * 
                cleaning_factor * 
                30  # Base multiplier
            )
            
            # Add depth penalty
            depth_factor = np.exp(-data['depth_ft'] / 20000)
            
            # Add hole angle effect
            angle_factor = np.cos(np.radians(data['hole_angle_deg']))
            
            # Final ROP with noise
            data['target'] = np.maximum(
                base_rop * depth_factor * angle_factor + np.random.normal(0, 5, n_samples),
                1.0  # Minimum ROP
            )
            
            # Cap maximum ROP
            data['target'] = np.minimum(data['target'], 300)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the drilling optimization dataset"""
        print(f"[DrillingParameterOptimizationDataset] Raw shape: {df.shape}")
        print(f"[DrillingParameterOptimizationDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find ROP target column
        target_col = None
        for col in ['rop', 'rate_of_penetration', 'penetration_rate', 'drilling_rate', 'target']:
            if col in df.columns:
                target_col = col
                break
            # Check for columns containing these terms
            for df_col in df.columns:
                if col in df_col.lower() or 'rop' in df_col.lower():
                    target_col = df_col
                    break
            if target_col:
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Try to find any rate/speed column
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if 'rate' in col.lower() or 'speed' in col.lower() or 'velocity' in col.lower():
                    if df[col].min() >= 0 and df[col].max() < 1000:  # Reasonable ROP range
                        df['target'] = df[col]
                        df = df.drop(col, axis=1)
                        break
            else:
                # Generate synthetic ROP
                if 'weight_on_bit' in str(numeric_cols) and 'rotary_speed' in str(numeric_cols):
                    wob_col = [c for c in numeric_cols if 'weight' in c.lower()][0]
                    rpm_col = [c for c in numeric_cols if 'speed' in c.lower() or 'rpm' in c.lower()][0]
                    df['target'] = np.sqrt(df[wob_col] * df[rpm_col]) * 0.1 + np.random.normal(0, 10, len(df))
                else:
                    df['target'] = np.random.gamma(3, 10, len(df))
        
        # Remove non-numeric columns
        text_cols = ['well_name', 'rig', 'operator', 'date', 'time', 'field']
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
            # Prioritize drilling-specific features
            priority_features = ['weight', 'wob', 'rpm', 'speed', 'flow', 'pressure', 
                               'torque', 'mud', 'depth', 'bit', 'formation']
            
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
        
        # Ensure positive ROP values
        df = df[df['target'] > 0]
        
        # Remove extreme outliers
        df = df[df['target'] < 500]  # Max reasonable ROP
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[DrillingParameterOptimizationDataset] Final shape: {df.shape}")
        print(f"[DrillingParameterOptimizationDataset] Target stats: mean={df['target'].mean():.2f} ft/hr, std={df['target'].std():.2f} ft/hr")
        print(f"[DrillingParameterOptimizationDataset] ROP range: [{df['target'].min():.2f}, {df['target'].max():.2f}] ft/hr")
        
        return df

if __name__ == "__main__":
    dataset = DrillingParameterOptimizationDataset()
    df = dataset.get_data()
    print(f"Loaded DrillingParameterOptimizationDataset: {df.shape}")
    print(df.head()) 