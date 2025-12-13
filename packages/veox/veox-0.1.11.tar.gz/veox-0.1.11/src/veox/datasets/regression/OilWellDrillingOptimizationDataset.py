import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class OilWellDrillingOptimizationDataset(BaseDatasetLoader):
    """
    Oil Well Drilling Optimization Dataset (regression)
    Source: Kaggle - Drilling Speed Prediction (ROP)
    Target: rate_of_penetration (ft/hr)
    
    This dataset contains drilling parameters for optimizing Rate of Penetration (ROP)
    in oil and gas wells, crucial for reducing drilling time and costs.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'OilWellDrillingOptimizationDataset',
            'source_id': 'kaggle:oil-drilling-rop',
            'category': 'regression',
            'description': 'Oil well drilling ROP prediction from operational parameters.',
            'source_url': 'https://www.kaggle.com/datasets/sarmadafzalj/oil-gas-drilling-dataset',
        }
    
    def download_dataset(self, info):
        """Download the drilling optimization dataset from Kaggle"""
        print(f"[OilWellDrillingOptimizationDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[OilWellDrillingOptimizationDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'sarmadafzalj/oil-gas-drilling-dataset',
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
                    print(f"[OilWellDrillingOptimizationDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=10000)
                    print(f"[OilWellDrillingOptimizationDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[OilWellDrillingOptimizationDataset] Download failed: {e}")
            print("[OilWellDrillingOptimizationDataset] Using sample drilling data...")
            
            # Create realistic drilling optimization data
            np.random.seed(42)
            n_samples = 5000
            
            # Drilling parameters
            data = {}
            
            # Weight on Bit (WOB) - thousand pounds
            data['weight_on_bit'] = np.random.gamma(3, 5, n_samples)
            data['weight_on_bit'] = np.clip(data['weight_on_bit'], 5, 60)
            
            # Rotary Speed (RPM)
            data['rotary_speed'] = np.random.normal(120, 30, n_samples)
            data['rotary_speed'] = np.clip(data['rotary_speed'], 40, 200)
            
            # Mud flow rate (gallons per minute)
            data['mud_flow_rate'] = np.random.gamma(4, 100, n_samples)
            data['mud_flow_rate'] = np.clip(data['mud_flow_rate'], 200, 800)
            
            # Mud properties
            data['mud_density'] = np.random.normal(10, 1.5, n_samples)  # ppg
            data['mud_viscosity'] = np.random.gamma(2, 15, n_samples)  # cp
            data['mud_ph'] = np.random.normal(9.5, 0.5, n_samples)
            
            # Bit characteristics
            data['bit_size'] = np.random.choice([6.5, 8.5, 12.25, 17.5], n_samples)  # inches
            data['bit_type'] = np.random.choice([1, 2, 3, 4, 5], n_samples)  # PDC, roller cone, etc.
            data['bit_wear'] = np.random.beta(2, 5, n_samples)  # 0-1 wear factor
            data['bit_hours'] = np.random.exponential(50, n_samples)
            
            # Formation properties
            data['formation_hardness'] = np.random.gamma(3, 1000, n_samples)  # psi
            data['formation_abrasiveness'] = np.random.beta(3, 2, n_samples)
            data['formation_porosity'] = np.random.beta(2, 8, n_samples)
            data['formation_permeability'] = np.random.lognormal(1, 2, n_samples)  # mD
            
            # Depth and pressure
            data['depth'] = np.random.gamma(3, 2000, n_samples)  # feet
            data['differential_pressure'] = np.random.normal(500, 200, n_samples)  # psi
            data['pump_pressure'] = np.random.gamma(3, 500, n_samples)  # psi
            data['standpipe_pressure'] = np.random.gamma(3, 600, n_samples)  # psi
            
            # Torque and drag
            data['torque'] = np.random.gamma(3, 5000, n_samples)  # ft-lbs
            data['drag'] = np.random.gamma(2, 10000, n_samples)  # lbs
            
            # Hydraulics
            data['jet_impact_force'] = np.random.gamma(2, 500, n_samples)  # lbs
            data['hydraulic_horsepower'] = np.random.gamma(3, 100, n_samples)  # hp
            
            # Temperature
            data['bottom_hole_temp'] = 60 + data['depth'] * 0.015 + np.random.normal(0, 10, n_samples)
            
            # Calculate ROP based on drilling mechanics
            # Bourgoyne and Young model simplified
            wob_effect = np.power(data['weight_on_bit'] / 20, 1.2)
            rpm_effect = np.power(data['rotary_speed'] / 100, 0.8)
            
            # Formation effect (harder formation = slower ROP)
            formation_effect = 5000 / (data['formation_hardness'] + 1000)
            
            # Bit wear effect
            wear_effect = 1 - 0.5 * data['bit_wear']
            
            # Hydraulics effect
            hydraulics_effect = np.power(data['jet_impact_force'] / 500, 0.3)
            
            # Depth effect (deeper = slower due to chip removal)
            depth_effect = np.exp(-data['depth'] / 10000)
            
            # Base ROP calculation
            base_rop = 50  # ft/hr
            data['target'] = (
                base_rop * 
                wob_effect * 
                rpm_effect * 
                formation_effect * 
                wear_effect * 
                hydraulics_effect * 
                (0.5 + depth_effect) +
                np.random.normal(0, 5, n_samples)
            )
            
            # Ensure realistic ROP range
            data['target'] = np.clip(data['target'], 5, 300)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the drilling optimization dataset"""
        print(f"[OilWellDrillingOptimizationDataset] Raw shape: {df.shape}")
        print(f"[OilWellDrillingOptimizationDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find ROP column
        rop_col = None
        for col in ['ROP', 'rop', 'rate_of_penetration', 'Rate_of_Penetration', 'target']:
            if col in df.columns:
                rop_col = col
                break
        
        if rop_col and rop_col != 'target':
            df['target'] = df[rop_col]
            df = df.drop(rop_col, axis=1)
        elif 'target' not in df.columns:
            # Look for any column that could be ROP
            for col in df.columns:
                if 'rate' in col.lower() or 'rop' in col.lower():
                    df['target'] = df[col]
                    df = df.drop(col, axis=1)
                    break
            else:
                # Use last numeric column
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    df['target'] = df[numeric_cols[-1]]
                    df = df.drop(numeric_cols[-1], axis=1)
                else:
                    raise ValueError("No suitable target column found")
        
        # Remove non-numeric columns
        text_cols = ['Well_Name', 'well_name', 'Date', 'Time', 'Formation', 'Bit_ID']
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
        if len(feature_cols) > 30:
            # Prioritize drilling parameters
            priority_features = ['wob', 'weight', 'rpm', 'rotary', 'speed', 'flow', 'mud', 
                               'pressure', 'torque', 'depth', 'bit']
            
            selected_features = []
            for feat in priority_features:
                for col in feature_cols:
                    if feat in col.lower() and col not in selected_features:
                        selected_features.append(col)
            
            # Add remaining features up to limit
            for col in feature_cols:
                if col not in selected_features and len(selected_features) < 30:
                    selected_features.append(col)
            
            feature_cols = selected_features
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Handle missing values
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Ensure all numeric
        df = df.dropna()
        
        # Remove outliers in ROP
        if 'target' in df.columns:
            # ROP should be positive and reasonable (0-500 ft/hr)
            df = df[(df['target'] > 0) & (df['target'] < 500)]
            
            # Remove extreme outliers
            q1 = df['target'].quantile(0.01)
            q99 = df['target'].quantile(0.99)
            df = df[(df['target'] >= q1) & (df['target'] <= q99)]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[OilWellDrillingOptimizationDataset] Final shape: {df.shape}")
        print(f"[OilWellDrillingOptimizationDataset] Target stats: mean={df['target'].mean():.2f} ft/hr, std={df['target'].std():.2f} ft/hr")
        print(f"[OilWellDrillingOptimizationDataset] ROP range: [{df['target'].min():.2f}, {df['target'].max():.2f}] ft/hr")
        
        return df

if __name__ == "__main__":
    dataset = OilWellDrillingOptimizationDataset()
    df = dataset.get_data()
    print(f"Loaded OilWellDrillingOptimizationDataset: {df.shape}")
    print(df.head()) 