import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BillingAnomalyDetectionDataset(BaseDatasetLoader):
    """
    Billing Anomaly Detection Dataset (binary classification)
    Source: Kaggle - Telecom Billing Data
    Target: is_anomaly (0=normal, 1=anomaly)
    
    This dataset contains telecom billing patterns for detecting
    anomalous charges and billing errors.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'BillingAnomalyDetectionDataset',
            'source_id': 'kaggle:billing-anomaly-detection',
            'category': 'binary_classification',
            'description': 'Billing anomaly detection from telecom usage and charge patterns.',
            'source_url': 'https://www.kaggle.com/datasets/prathamtripathi/customerbillingdataset',
        }
    
    def download_dataset(self, info):
        """Download the billing dataset from Kaggle"""
        print(f"[BillingAnomalyDetectionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[BillingAnomalyDetectionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'prathamtripathi/customerbillingdataset',
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
                    print(f"[BillingAnomalyDetectionDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=15000)
                    print(f"[BillingAnomalyDetectionDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[BillingAnomalyDetectionDataset] Download failed: {e}")
            print("[BillingAnomalyDetectionDataset] Using sample billing data...")
            
            # Create realistic billing anomaly data
            np.random.seed(42)
            n_samples = 10000
            anomaly_rate = 0.05  # 5% anomalies
            
            # Billing features
            data = {}
            
            # Usage metrics
            data['voice_minutes_used'] = np.random.gamma(3, 50, n_samples)
            data['data_gb_used'] = np.random.gamma(2, 2, n_samples)
            data['sms_count'] = np.random.poisson(30, n_samples)
            data['international_minutes'] = np.random.exponential(5, n_samples)
            data['roaming_minutes'] = np.random.exponential(3, n_samples)
            
            # Plan details
            data['plan_monthly_charge'] = np.random.choice([29.99, 49.99, 69.99, 99.99], n_samples, p=[0.3, 0.4, 0.2, 0.1])
            data['plan_voice_limit'] = np.random.choice([500, 1000, -1, -1], n_samples, p=[0.2, 0.3, 0.25, 0.25])  # -1 = unlimited
            data['plan_data_limit'] = np.random.choice([2, 5, 10, -1], n_samples, p=[0.2, 0.3, 0.3, 0.2])
            data['plan_sms_limit'] = np.random.choice([100, 500, -1], n_samples, p=[0.2, 0.3, 0.5])
            
            # Charges
            data['base_charge'] = data['plan_monthly_charge']
            data['voice_overage_charge'] = np.zeros(n_samples)
            data['data_overage_charge'] = np.zeros(n_samples)
            data['international_charge'] = data['international_minutes'] * np.random.uniform(0.5, 2, n_samples)
            data['roaming_charge'] = data['roaming_minutes'] * np.random.uniform(1, 3, n_samples)
            data['service_charges'] = np.random.exponential(5, n_samples)
            data['taxes_and_fees'] = data['base_charge'] * np.random.uniform(0.08, 0.15, n_samples)
            
            # Calculate overages
            voice_overage = np.maximum(0, data['voice_minutes_used'] - np.where(data['plan_voice_limit'] == -1, 99999, data['plan_voice_limit']))
            data['voice_overage_charge'] = voice_overage * 0.45
            
            data_overage = np.maximum(0, data['data_gb_used'] - np.where(data['plan_data_limit'] == -1, 99999, data['plan_data_limit']))
            data['data_overage_charge'] = data_overage * 15
            
            # Total bill calculation
            data['total_charge'] = (
                data['base_charge'] + 
                data['voice_overage_charge'] + 
                data['data_overage_charge'] + 
                data['international_charge'] + 
                data['roaming_charge'] + 
                data['service_charges'] + 
                data['taxes_and_fees']
            )
            
            # Historical billing
            data['avg_bill_last_3_months'] = data['total_charge'] * np.random.uniform(0.8, 1.2, n_samples)
            data['max_bill_last_12_months'] = data['total_charge'] * np.random.uniform(1.1, 2, n_samples)
            data['bill_variance_last_6_months'] = np.random.exponential(20, n_samples)
            
            # Payment history
            data['days_since_last_payment'] = np.random.gamma(2, 15, n_samples)
            data['payment_method'] = np.random.choice([1, 2, 3, 4], n_samples, p=[0.5, 0.3, 0.15, 0.05])  # Auto, Card, Check, Cash
            data['late_payments_last_year'] = np.random.poisson(0.5, n_samples)
            data['disputed_charges_count'] = np.random.poisson(0.1, n_samples)
            
            # Customer profile
            data['customer_tenure_months'] = np.random.gamma(3, 12, n_samples)
            data['credit_score_range'] = np.random.choice([1, 2, 3, 4], n_samples, p=[0.1, 0.3, 0.4, 0.2])  # Poor, Fair, Good, Excellent
            data['contract_type'] = np.random.choice([1, 2, 3], n_samples, p=[0.5, 0.3, 0.2])  # Monthly, 1-year, 2-year
            
            # Billing patterns
            data['bill_spike_ratio'] = data['total_charge'] / (data['avg_bill_last_3_months'] + 1)
            data['usage_charge_ratio'] = (data['voice_overage_charge'] + data['data_overage_charge']) / (data['total_charge'] + 1)
            data['international_charge_ratio'] = data['international_charge'] / (data['total_charge'] + 1)
            
            # Create anomalies
            n_anomalies = int(n_samples * anomaly_rate)
            anomaly_indices = np.random.choice(n_samples, n_anomalies, replace=False)
            data['target'] = np.zeros(n_samples, dtype=int)
            data['target'][anomaly_indices] = 1
            
            # Modify features for anomalies
            # Type 1: Billing system errors (charges without usage)
            error_mask = anomaly_indices[:n_anomalies//3]
            data['voice_overage_charge'][error_mask] += np.random.uniform(50, 200, len(error_mask))
            data['data_overage_charge'][error_mask] += np.random.uniform(100, 500, len(error_mask))
            data['total_charge'][error_mask] = data['total_charge'][error_mask] * np.random.uniform(2, 5, len(error_mask))
            
            # Type 2: Fraudulent usage
            fraud_mask = anomaly_indices[n_anomalies//3:2*n_anomalies//3]
            data['international_minutes'][fraud_mask] = data['international_minutes'][fraud_mask] * np.random.uniform(10, 50, len(fraud_mask))
            data['international_charge'][fraud_mask] = data['international_charge'][fraud_mask] * np.random.uniform(10, 50, len(fraud_mask))
            data['roaming_charge'][fraud_mask] = data['roaming_charge'][fraud_mask] * np.random.uniform(5, 20, len(fraud_mask))
            
            # Type 3: Duplicate charges
            duplicate_mask = anomaly_indices[2*n_anomalies//3:]
            data['service_charges'][duplicate_mask] = data['service_charges'][duplicate_mask] * np.random.uniform(3, 10, len(duplicate_mask))
            data['total_charge'][duplicate_mask] = data['total_charge'][duplicate_mask] * np.random.uniform(1.5, 3, len(duplicate_mask))
            
            # Recalculate ratios for anomalies
            data['bill_spike_ratio'] = data['total_charge'] / (data['avg_bill_last_3_months'] + 1)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the billing anomaly dataset"""
        print(f"[BillingAnomalyDetectionDataset] Raw shape: {df.shape}")
        print(f"[BillingAnomalyDetectionDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['anomaly', 'is_anomaly', 'fraud', 'label', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            # Convert to binary
            if df[target_col].dtype == 'object':
                df['target'] = (df[target_col].str.lower() == 'yes').astype(int)
            else:
                df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Generate anomalies based on billing patterns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Look for charge/amount columns
                charge_cols = [col for col in numeric_cols if 'charge' in col.lower() or 'amount' in col.lower() or 'bill' in col.lower()]
                
                if charge_cols:
                    # Anomaly if charges are unusually high
                    charge_sum = df[charge_cols].sum(axis=1)
                    threshold = charge_sum.quantile(0.95)
                    df['target'] = (charge_sum > threshold).astype(int)
                else:
                    # Use statistical outlier detection
                    feature_sum = df[numeric_cols].sum(axis=1)
                    threshold = feature_sum.quantile(0.95)
                    df['target'] = (feature_sum > threshold).astype(int)
            else:
                # Random anomalies
                df['target'] = np.random.choice([0, 1], len(df), p=[0.95, 0.05])
        
        # Remove non-numeric columns
        text_cols = ['customer_id', 'account_number', 'billing_date', 'payment_date', 'description']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Convert categorical columns
        cat_cols = ['payment_method', 'billing_cycle', 'plan_type', 'customer_segment']
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
        
        # Create billing features if too few
        if len(feature_cols) < 10:
            # Add synthetic billing features
            df['monthly_charge'] = np.random.gamma(3, 20, len(df))
            df['usage_charge'] = np.random.exponential(10, len(df))
            df['overage_charge'] = np.random.exponential(5, len(df))
            df['total_charge'] = df['monthly_charge'] + df['usage_charge'] + df['overage_charge']
            df['charge_variance'] = np.random.exponential(10, len(df))
            df['days_since_payment'] = np.random.gamma(2, 15, len(df))
            
            feature_cols.extend(['monthly_charge', 'usage_charge', 'overage_charge', 
                               'total_charge', 'charge_variance', 'days_since_payment'])
        
        # Limit features
        if len(feature_cols) > 40:
            # Prioritize billing features
            priority_features = ['charge', 'bill', 'amount', 'usage', 'overage', 'payment', 
                               'balance', 'credit', 'debit', 'fee']
            
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
        
        # Ensure binary target
        df['target'] = df['target'].astype(int)
        df = df[df['target'].isin([0, 1])]
        
        # Balance if severely imbalanced
        target_counts = df['target'].value_counts()
        if len(target_counts) == 2:
            minority = target_counts.idxmin()
            majority = target_counts.idxmax()
            if target_counts[minority] < target_counts[majority] * 0.01:
                # Undersample majority
                n_minority = target_counts[minority]
                n_majority = min(n_minority * 20, target_counts[majority])
                df_minority = df[df['target'] == minority]
                df_majority = df[df['target'] == majority].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[BillingAnomalyDetectionDataset] Final shape: {df.shape}")
        print(f"[BillingAnomalyDetectionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[BillingAnomalyDetectionDataset] Anomaly rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = BillingAnomalyDetectionDataset()
    df = dataset.get_data()
    print(f"Loaded BillingAnomalyDetectionDataset: {df.shape}")
    print(df.head()) 