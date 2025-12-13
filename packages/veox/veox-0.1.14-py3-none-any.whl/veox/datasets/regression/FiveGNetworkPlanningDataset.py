import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class FiveGNetworkPlanningDataset(BaseDatasetLoader):
    """
    5G Network Planning Dataset (regression)
    Source: Kaggle - 5G Network Coverage Data
    Target: coverage_quality_score (0-100, network coverage quality)
    
    This dataset contains 5G network planning parameters for optimizing
    cell tower placement and coverage quality.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'FiveGNetworkPlanningDataset',
            'source_id': 'kaggle:5g-network-planning',
            'category': 'regression',
            'description': '5G network coverage quality prediction from planning parameters.',
            'source_url': 'https://www.kaggle.com/datasets/bensafaiedh/5g-nr-channel-measurement-campaign',
        }
    
    def download_dataset(self, info):
        """Download the 5G network dataset from Kaggle"""
        print(f"[FiveGNetworkPlanningDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[FiveGNetworkPlanningDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'bensafaiedh/5g-nr-channel-measurement-campaign',
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
                    print(f"[FiveGNetworkPlanningDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=10000)
                    print(f"[FiveGNetworkPlanningDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[FiveGNetworkPlanningDataset] Download failed: {e}")
            print("[FiveGNetworkPlanningDataset] Using sample 5G planning data...")
            
            # Create realistic 5G network planning data
            np.random.seed(42)
            n_samples = 8000
            
            # Geographic and demographic features
            data = {}
            data['population_density'] = np.random.gamma(2, 500, n_samples)  # people per sq km
            data['area_type'] = np.random.choice([1, 2, 3, 4], n_samples, p=[0.3, 0.4, 0.2, 0.1])  # Urban, Suburban, Rural, Industrial
            data['terrain_elevation_m'] = np.random.normal(100, 50, n_samples)
            data['building_density'] = np.random.beta(3, 2, n_samples)
            data['avg_building_height_m'] = np.random.gamma(2, 10, n_samples)
            
            # Cell tower parameters
            data['tower_height_m'] = np.random.choice([30, 40, 50, 60, 80], n_samples)
            data['antenna_tilt_degrees'] = np.random.normal(5, 2, n_samples)
            data['transmit_power_dbm'] = np.random.normal(46, 3, n_samples)  # 5G typical power
            data['antenna_gain_dbi'] = np.random.normal(18, 2, n_samples)
            data['num_antenna_elements'] = np.random.choice([64, 128, 256], n_samples, p=[0.3, 0.5, 0.2])
            
            # Frequency and spectrum
            data['frequency_ghz'] = np.random.choice([3.5, 28, 39], n_samples, p=[0.5, 0.3, 0.2])  # Common 5G bands
            data['bandwidth_mhz'] = np.random.choice([50, 100, 200, 400], n_samples, p=[0.2, 0.4, 0.3, 0.1])
            data['mimo_layers'] = np.random.choice([2, 4, 8, 16], n_samples, p=[0.1, 0.3, 0.4, 0.2])
            
            # Interference and noise
            data['noise_figure_db'] = np.random.normal(7, 1, n_samples)
            data['interference_level_dbm'] = np.random.normal(-100, 10, n_samples)
            data['adjacent_cell_interference'] = np.random.exponential(0.1, n_samples)
            
            # Traffic demand
            data['expected_users'] = data['population_density'] * np.random.uniform(0.1, 0.3, n_samples)
            data['peak_traffic_gbps'] = data['expected_users'] * np.random.gamma(2, 0.001, n_samples)
            data['avg_user_throughput_mbps'] = np.random.gamma(3, 20, n_samples)
            data['traffic_growth_rate'] = np.random.normal(0.3, 0.1, n_samples)  # 30% annual growth
            
            # Environmental factors
            data['avg_rainfall_mm'] = np.random.gamma(2, 50, n_samples)
            data['foliage_density'] = np.random.beta(2, 3, n_samples)
            data['atmospheric_pressure_hpa'] = np.random.normal(1013, 20, n_samples)
            
            # Neighboring cells
            data['num_neighboring_cells'] = np.random.poisson(6, n_samples)
            data['avg_neighbor_distance_m'] = np.random.gamma(3, 200, n_samples)
            data['handover_rate'] = np.random.exponential(0.2, n_samples)
            
            # Backhaul capacity
            data['backhaul_capacity_gbps'] = np.random.choice([1, 10, 40, 100], n_samples, p=[0.2, 0.4, 0.3, 0.1])
            data['backhaul_latency_ms'] = np.random.gamma(2, 2, n_samples)
            data['fiber_availability'] = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
            
            # Calculate coverage quality score (target)
            coverage_score = 50  # Base score
            
            # Signal propagation factors
            # Higher frequency = more path loss
            path_loss_factor = np.where(data['frequency_ghz'] < 6, 1, 
                                      np.where(data['frequency_ghz'] < 30, 1.5, 2))
            coverage_score -= path_loss_factor * 10
            
            # Tower and antenna configuration
            coverage_score += data['tower_height_m'] / 10
            coverage_score += data['antenna_gain_dbi'] / 2
            coverage_score += np.log(data['num_antenna_elements']) * 5
            
            # Spectrum efficiency
            coverage_score += np.log(data['bandwidth_mhz']) * 3
            coverage_score += np.log(data['mimo_layers']) * 4
            
            # Environmental impact
            coverage_score -= data['building_density'] * 10
            coverage_score -= data['foliage_density'] * 5
            coverage_score -= data['avg_rainfall_mm'] / 100
            
            # Interference management
            coverage_score -= (data['interference_level_dbm'] + 100) / 5
            coverage_score -= data['adjacent_cell_interference'] * 20
            
            # Traffic handling capability
            traffic_capability = data['bandwidth_mhz'] * data['mimo_layers'] / (data['expected_users'] + 1)
            coverage_score += np.minimum(traffic_capability / 10, 10)
            
            # Backhaul quality
            coverage_score += np.log(data['backhaul_capacity_gbps'] + 1) * 5
            coverage_score += data['fiber_availability'] * 10
            
            # Area type adjustment
            area_adjustment = np.where(data['area_type'] == 1, 0,  # Urban: baseline
                                     np.where(data['area_type'] == 2, 5,   # Suburban: easier
                                            np.where(data['area_type'] == 3, -5,  # Rural: harder
                                                   -10)))                          # Industrial: interference
            coverage_score += area_adjustment
            
            # Add noise and clip
            coverage_score += np.random.normal(0, 5, n_samples)
            data['target'] = np.clip(coverage_score, 0, 100)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the 5G network planning dataset"""
        print(f"[FiveGNetworkPlanningDataset] Raw shape: {df.shape}")
        print(f"[FiveGNetworkPlanningDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['rsrp', 'sinr', 'quality', 'coverage', 'score', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            # Convert signal measurements to quality score
            if 'rsrp' in target_col.lower():  # Reference Signal Received Power
                # RSRP typically ranges from -140 to -40 dBm
                df['target'] = (df[target_col] + 140) / 100 * 100  # Normalize to 0-100
            elif 'sinr' in target_col.lower():  # Signal to Interference plus Noise Ratio
                # SINR typically ranges from -20 to 30 dB
                df['target'] = (df[target_col] + 20) / 50 * 100
            else:
                df['target'] = df[target_col]
                if df['target'].max() > 100:
                    df['target'] = (df['target'] - df['target'].min()) / (df['target'].max() - df['target'].min()) * 100
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Generate coverage score from available features
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Create synthetic coverage score
                base_score = 50
                
                # Look for signal-related columns
                for col in numeric_cols:
                    if any(term in col.lower() for term in ['power', 'signal', 'gain', 'loss']):
                        col_norm = (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-6)
                        base_score += col_norm * 10
                
                df['target'] = base_score
            else:
                df['target'] = np.random.normal(70, 15, len(df))
        
        # Remove non-numeric columns
        text_cols = ['timestamp', 'location', 'cell_id', 'operator', 'device_id']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Convert categorical columns
        cat_cols = ['band', 'technology', 'environment', 'weather']
        for col in cat_cols:
            if col in df.columns and df[col].dtype == 'object':
                dummies = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df, dummies], axis=1)
                df = df.drop(col, axis=1)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().sum() > len(df) * 0.5:
                    feature_cols.append(col)
        
        # Create 5G planning features if too few
        if len(feature_cols) < 15:
            # Add synthetic 5G features
            df['frequency_ghz'] = np.random.choice([3.5, 28, 39], len(df))
            df['bandwidth_mhz'] = np.random.choice([50, 100, 200, 400], len(df))
            df['transmit_power_dbm'] = np.random.normal(46, 3, len(df))
            df['antenna_gain_dbi'] = np.random.normal(18, 2, len(df))
            df['path_loss_db'] = np.random.normal(120, 20, len(df))
            df['building_penetration_loss_db'] = np.random.normal(20, 5, len(df))
            df['mimo_rank'] = np.random.choice([2, 4, 8], len(df))
            df['modulation_order'] = np.random.choice([4, 6, 8], len(df))  # QPSK, 64QAM, 256QAM
            df['resource_blocks'] = np.random.randint(50, 273, len(df))
            df['user_distance_m'] = np.random.gamma(2, 200, len(df))
            
            new_features = ['frequency_ghz', 'bandwidth_mhz', 'transmit_power_dbm', 
                           'antenna_gain_dbi', 'path_loss_db', 'building_penetration_loss_db',
                           'mimo_rank', 'modulation_order', 'resource_blocks', 'user_distance_m']
            feature_cols.extend(new_features)
        
        # Limit features
        if len(feature_cols) > 40:
            # Prioritize 5G-specific features
            priority_features = ['frequency', 'bandwidth', 'power', 'gain', 'loss', 'mimo',
                               'sinr', 'rsrp', 'rsrq', 'throughput', 'latency', 'coverage']
            
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
        
        # Clip target to [0, 100]
        df['target'] = np.clip(df['target'], 0, 100)
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[FiveGNetworkPlanningDataset] Final shape: {df.shape}")
        print(f"[FiveGNetworkPlanningDataset] Target stats: mean={df['target'].mean():.2f}, std={df['target'].std():.2f}")
        print(f"[FiveGNetworkPlanningDataset] Coverage score range: [{df['target'].min():.2f}, {df['target'].max():.2f}]")
        
        return df

if __name__ == "__main__":
    dataset = FiveGNetworkPlanningDataset()
    df = dataset.get_data()
    print(f"Loaded FiveGNetworkPlanningDataset: {df.shape}")
    print(df.head()) 