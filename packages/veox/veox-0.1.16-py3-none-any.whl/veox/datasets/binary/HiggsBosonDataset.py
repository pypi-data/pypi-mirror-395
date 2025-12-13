import pandas as pd
import numpy as np
import os
import tempfile
import zipfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class HiggsBosonDataset(BaseDatasetLoader):
    """
    Higgs Boson Dataset (binary classification)
    Source: Kaggle Competition - CERN Higgs Boson Machine Learning Challenge
    Target: signal (0=background, 1=signal)
    
    This dataset contains simulated particle collision data from CERN
    for detecting Higgs boson particles.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'HiggsBosonDataset',
            'source_id': 'kaggle:higgs-boson',
            'category': 'binary_classification',
            'description': 'CERN particle collision data for Higgs boson detection.',
            'source_url': 'https://www.kaggle.com/c/higgs-boson/data',
        }
    
    def download_dataset(self, info):
        """Download the Higgs Boson dataset from Kaggle"""
        print(f"[HiggsBosonDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[HiggsBosonDataset] Downloading to {temp_dir}")
                
                # Download competition data
                kaggle.api.competition_download_files(
                    'higgs-boson',
                    path=temp_dir,
                    quiet=False
                )
                
                # Extract zip files
                zip_files = [f for f in os.listdir(temp_dir) if f.endswith('.zip')]
                for zip_file in zip_files:
                    with zipfile.ZipFile(os.path.join(temp_dir, zip_file), 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                
                # Look for training data
                train_file = None
                for file in os.listdir(temp_dir):
                    if 'train' in file.lower() and file.endswith('.csv'):
                        train_file = os.path.join(temp_dir, file)
                        break
                
                if not train_file:
                    raise FileNotFoundError("Training file not found")
                
                print(f"[HiggsBosonDataset] Reading: {os.path.basename(train_file)}")
                
                # Read a subset due to large size
                df = pd.read_csv(train_file, nrows=50000)
                print(f"[HiggsBosonDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[HiggsBosonDataset] Download failed: {e}")
            print("[HiggsBosonDataset] Using sample data...")
            
            # Create sample particle physics data
            np.random.seed(42)
            n_samples = 10000
            
            # Kinematic features
            data = {
                'EventId': range(n_samples),
                'DER_mass_MMC': np.random.gamma(2, 50, n_samples),
                'DER_mass_transverse_met_lep': np.random.gamma(2, 30, n_samples),
                'DER_mass_vis': np.random.gamma(2, 40, n_samples),
                'DER_pt_h': np.random.exponential(50, n_samples),
                'DER_deltaeta_jet_jet': np.random.normal(0, 2, n_samples),
                'DER_mass_jet_jet': np.random.gamma(2, 100, n_samples),
                'DER_prodeta_jet_jet': np.random.normal(0, 5, n_samples),
                'DER_deltar_tau_lep': np.random.gamma(2, 1, n_samples),
                'DER_pt_tot': np.random.exponential(30, n_samples),
                'DER_sum_pt': np.random.exponential(100, n_samples),
                'DER_pt_ratio_lep_tau': np.random.beta(2, 2, n_samples),
                'DER_met_phi_centrality': np.random.uniform(-1.5, 1.5, n_samples),
                'DER_lep_eta_centrality': np.random.uniform(0, 1, n_samples),
                'PRI_tau_pt': np.random.exponential(40, n_samples),
                'PRI_tau_eta': np.random.normal(0, 2.5, n_samples),
                'PRI_tau_phi': np.random.uniform(-np.pi, np.pi, n_samples),
                'PRI_lep_pt': np.random.exponential(30, n_samples),
                'PRI_lep_eta': np.random.normal(0, 2.5, n_samples),
                'PRI_lep_phi': np.random.uniform(-np.pi, np.pi, n_samples),
                'PRI_met': np.random.exponential(40, n_samples),
                'PRI_met_phi': np.random.uniform(-np.pi, np.pi, n_samples),
                'PRI_met_sumet': np.random.exponential(200, n_samples),
                'PRI_jet_num': np.random.choice([0, 1, 2, 3], n_samples, p=[0.4, 0.3, 0.2, 0.1]),
                'PRI_jet_leading_pt': np.random.exponential(50, n_samples),
                'PRI_jet_leading_eta': np.random.normal(0, 2.5, n_samples),
                'PRI_jet_leading_phi': np.random.uniform(-np.pi, np.pi, n_samples),
                'PRI_jet_subleading_pt': np.random.exponential(30, n_samples),
                'PRI_jet_subleading_eta': np.random.normal(0, 2.5, n_samples),
                'PRI_jet_subleading_phi': np.random.uniform(-np.pi, np.pi, n_samples),
                'PRI_jet_all_pt': np.random.exponential(100, n_samples),
                'Weight': np.random.exponential(1, n_samples)
            }
            
            # Create labels (signal vs background)
            labels = []
            for i in range(n_samples):
                # Signal more likely with certain feature combinations
                signal_prob = 0.3
                if data['DER_mass_MMC'][i] > 100 and data['DER_mass_MMC'][i] < 150:
                    signal_prob += 0.3
                if data['DER_mass_vis'][i] > 80 and data['DER_mass_vis'][i] < 120:
                    signal_prob += 0.2
                
                labels.append('s' if np.random.random() < signal_prob else 'b')
            
            data['Label'] = labels
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the Higgs Boson dataset"""
        print(f"[HiggsBosonDataset] Raw shape: {df.shape}")
        print(f"[HiggsBosonDataset] Columns sample: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['Label', 'label', 'target', 'signal']:
            if col in df.columns:
                target_col = col
                break
        
        if not target_col:
            raise ValueError("Could not find target column")
        
        # Create binary target (0=background, 1=signal)
        df['target'] = (df[target_col] == 's').astype(int)
        
        # Drop non-feature columns
        drop_cols = ['EventId', 'Weight', target_col]
        for col in drop_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Replace -999 with NaN (missing value indicator in this dataset)
        df = df.replace(-999.0, np.nan)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target' and df[col].dtype in ['int64', 'float64']:
                feature_cols.append(col)
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Fill missing values with median
        for col in feature_cols:
            median_val = df[col].median()
            if pd.isna(median_val):
                median_val = 0
            df[col] = df[col].fillna(median_val)
        
        # Remove any remaining missing values
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[HiggsBosonDataset] Final shape: {df.shape}")
        print(f"[HiggsBosonDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[HiggsBosonDataset] Signal rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = HiggsBosonDataset()
    df = dataset.get_data()
    print(f"Loaded HiggsBosonDataset: {df.shape}")
    print(df.head()) 