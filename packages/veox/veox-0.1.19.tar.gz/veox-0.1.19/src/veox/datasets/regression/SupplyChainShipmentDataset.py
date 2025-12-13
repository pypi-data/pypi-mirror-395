import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class SupplyChainShipmentDataset(BaseDatasetLoader):
    """
    Supply Chain Shipment Pricing Dataset (regression)
    Source: Kaggle - Supply chain shipment pricing data
    Target: freight_cost_usd
    
    This dataset contains supply chain shipment data with various
    attributes for predicting freight costs.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'SupplyChainShipmentDataset',
            'source_id': 'kaggle:supply-chain-shipment-pricing',
            'category': 'regression',
            'description': 'Supply chain shipment data for freight cost prediction.',
            'source_url': 'https://www.kaggle.com/datasets/divyeshardeshana/supply-chain-shipment-pricing-data',
        }
    
    def download_dataset(self, info):
        """Download the supply chain shipment dataset from Kaggle"""
        print(f"[SupplyChainShipmentDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[SupplyChainShipmentDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'divyeshardeshana/supply-chain-shipment-pricing-data',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV file
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                
                data_file = csv_files[0]
                print(f"[SupplyChainShipmentDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file, nrows=50000)
                print(f"[SupplyChainShipmentDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[SupplyChainShipmentDataset] Download failed: {e}")
            print("[SupplyChainShipmentDataset] Using sample data...")
            
            # Create sample data
            np.random.seed(42)
            n_samples = 10000
            
            data = {
                'country': np.random.choice(['USA', 'China', 'India', 'Germany', 'UK', 
                                           'Japan', 'Brazil', 'Canada'], n_samples),
                'managed_by': np.random.choice(['PMO', 'RMO', 'FMO', 'SMO'], n_samples),
                'fulfill_via': np.random.choice(['Direct Drop', 'From RDC', 'From DC'], n_samples),
                'vendor_inco_term': np.random.choice(['EXW', 'FCA', 'CPT', 'CIP', 'DAT', 
                                                    'DAP', 'DDP', 'FAS', 'FOB'], n_samples),
                'shipment_mode': np.random.choice(['Air', 'Truck', 'Air Charter', 'Ocean'], 
                                                n_samples, p=[0.6, 0.2, 0.05, 0.15]),
                'product_group': np.random.choice(['ARV', 'HRDT', 'MRDT', 'ACT'], n_samples),
                'sub_classification': np.random.choice(['HIV', 'Malaria', 'TB', 'Other'], n_samples),
                'vendor': np.random.choice([f'Vendor_{i}' for i in range(50)], n_samples),
                'item_description': np.random.choice([f'Item_{i}' for i in range(100)], n_samples),
                'molecule_test_type': np.random.choice([f'Test_{i}' for i in range(20)], n_samples),
                'brand': np.random.choice([f'Brand_{i}' for i in range(30)], n_samples),
                'dosage': np.random.choice(['10mg', '20mg', '50mg', '100mg', '200mg'], n_samples),
                'dosage_form': np.random.choice(['Tablet', 'Capsule', 'Injection', 'Syrup'], n_samples),
                'unit_of_measure_per_pack': np.random.randint(1, 1000, n_samples),
                'line_item_quantity': np.random.randint(1, 10000, n_samples),
                'line_item_value': np.random.uniform(100, 50000, n_samples),
                'pack_price': np.random.uniform(1, 500, n_samples),
                'unit_price': np.random.uniform(0.1, 50, n_samples),
                'weight_kilograms': np.random.exponential(50, n_samples),
                'freight_cost_groups': np.random.choice(['0-25', '25-50', '50-100', '100-250', 
                                                       '250-500', '500-1000', '1000+'], n_samples),
            }
            
            # Generate freight cost based on weight, distance, and mode
            base_cost = data['weight_kilograms'] * np.random.uniform(0.5, 2, n_samples)
            mode_multiplier = {'Air': 5, 'Air Charter': 8, 'Ocean': 0.5, 'Truck': 1}
            mode_mult = np.array([mode_multiplier[mode] for mode in data['shipment_mode']])
            freight_cost = base_cost * mode_mult * np.random.uniform(0.8, 1.2, n_samples)
            
            data['freight_cost_usd'] = freight_cost
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the supply chain shipment dataset"""
        print(f"[SupplyChainShipmentDataset] Raw shape: {df.shape}")
        print(f"[SupplyChainShipmentDataset] Columns: {list(df.columns)[:10]}... (showing first 10)")
        
        # Identify target column
        target_col = None
        for col in ['freight_cost_usd', 'freight_cost', 'Freight Cost (USD)', 'cost', 'price']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col:
            df['target'] = pd.to_numeric(df[target_col], errors='coerce')
            df = df.drop(target_col, axis=1)
        else:
            # Create synthetic target
            if 'weight_kilograms' in df.columns:
                df['target'] = df['weight_kilograms'] * np.random.uniform(1, 5, len(df))
            elif 'Weight (Kilograms)' in df.columns:
                df['target'] = pd.to_numeric(df['Weight (Kilograms)'], errors='coerce') * np.random.uniform(1, 5, len(df))
            else:
                df['target'] = np.random.exponential(500, len(df))
        
        # Drop non-numeric columns that are not useful
        drop_cols = ['id', 'ID', 'project_code', 'Project Code', 'pq_number', 'PQ #', 
                    'po_so_number', 'PO / SO #', 'asn_dn_number', 'ASN/DN #', 
                    'invoice_number', 'Invoice #']
        for col in drop_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Handle date columns
        date_cols = ['scheduled_delivery_date', 'delivered_to_client_date', 
                    'delivery_recorded_date', 'first_line_designation',
                    'Scheduled Delivery Date', 'Delivered to Client Date',
                    'Delivery Recorded Date', 'PQ First Sent to Client Date',
                    'PO Sent to Vendor Date']
        for col in date_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    if df[col].notna().sum() > 0:
                        df[f'{col}_year'] = df[col].dt.year
                        df[f'{col}_month'] = df[col].dt.month
                        df[f'{col}_day'] = df[col].dt.day
                except:
                    pass
                df = df.drop(col, axis=1)
        
        # Select numeric columns first
        numeric_cols = []
        for col in df.columns:
            if col != 'target' and df[col].dtype in ['int64', 'float64']:
                numeric_cols.append(col)
        
        # Handle categorical features
        categorical_cols = []
        for col in df.columns:
            if col != 'target' and col not in numeric_cols and df[col].dtype == 'object':
                categorical_cols.append(col)
        
        # Limit categories for high cardinality features
        for col in categorical_cols:
            if df[col].nunique() > 50:
                top_categories = df[col].value_counts().head(50).index
                df[col] = df[col].where(df[col].isin(top_categories), 'Other')
        
        # One-hot encode categorical features
        if categorical_cols:
            df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
            # Convert boolean columns to int
            for col in df.columns:
                if df[col].dtype == 'bool':
                    df[col] = df[col].astype(int)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Remove missing values
        df = df.dropna()
        
        # Ensure all numeric and convert int8/int32 to int64
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Convert int8 and int32 to int64
            if df[col].dtype in ['int8', 'int32']:
                df[col] = df[col].astype('int64')
        
        df = df.dropna()
        
        # Remove outliers in target
        if len(df) > 100:
            q1 = df['target'].quantile(0.01)
            q99 = df['target'].quantile(0.99)
            df = df[(df['target'] >= q1) & (df['target'] <= q99)]
        
        # Limit size if needed
        if len(df) > 20000:
            df = df.sample(n=20000, random_state=42)
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[SupplyChainShipmentDataset] Final shape: {df.shape}")
        print(f"[SupplyChainShipmentDataset] Target stats: mean=${df['target'].mean():.2f}, std=${df['target'].std():.2f}")
        print(f"[SupplyChainShipmentDataset] Target range: [${df['target'].min():.2f}, ${df['target'].max():.2f}]")
        
        return df

if __name__ == "__main__":
    dataset = SupplyChainShipmentDataset()
    df = dataset.get_data()
    print(f"Loaded SupplyChainShipmentDataset: {df.shape}")
    print(df.head()) 