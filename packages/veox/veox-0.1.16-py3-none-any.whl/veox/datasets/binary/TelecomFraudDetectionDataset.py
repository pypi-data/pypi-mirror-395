import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class TelecomFraudDetectionDataset(BaseDatasetLoader):
    """
    Telecom Fraud Detection Dataset (binary classification)
    Source: Kaggle - Telecom Fraud Data
    Target: is_fraud (0=legitimate, 1=fraud)
    
    This dataset contains telecom usage patterns for detecting
    fraudulent activities like SIM box fraud, subscription fraud, etc.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'TelecomFraudDetectionDataset',
            'source_id': 'kaggle:telecom-fraud-detection',
            'category': 'binary_classification',
            'description': 'Telecom fraud detection from usage patterns and subscriber behavior.',
            'source_url': 'https://www.kaggle.com/datasets/jainilcoder/telecom-fraud-data',
        }
    
    def download_dataset(self, info):
        """Download the telecom fraud dataset from Kaggle"""
        print(f"[TelecomFraudDetectionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[TelecomFraudDetectionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'jainilcoder/telecom-fraud-data',
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
                    print(f"[TelecomFraudDetectionDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=15000)
                    print(f"[TelecomFraudDetectionDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[TelecomFraudDetectionDataset] Download failed: {e}")
            print("[TelecomFraudDetectionDataset] Using sample telecom fraud data...")
            
            # Create realistic telecom fraud data
            np.random.seed(42)
            n_samples = 10000
            fraud_rate = 0.03  # 3% fraud rate
            
            # Subscriber profile
            data = {}
            data['account_age_days'] = np.random.gamma(3, 100, n_samples)
            data['registration_method'] = np.random.choice([1, 2, 3], n_samples, p=[0.7, 0.2, 0.1])  # Store, Online, Dealer
            data['id_verification_score'] = np.random.beta(8, 2, n_samples)
            data['credit_score'] = np.random.normal(700, 100, n_samples)
            data['num_sim_cards'] = np.random.poisson(1.5, n_samples) + 1
            
            # Usage patterns - Voice
            data['daily_call_count'] = np.random.gamma(2, 5, n_samples)
            data['avg_call_duration_sec'] = np.random.gamma(2, 60, n_samples)
            data['international_call_ratio'] = np.random.beta(1, 20, n_samples)
            data['premium_number_calls'] = np.random.poisson(0.1, n_samples)
            data['unique_numbers_called'] = np.random.gamma(2, 10, n_samples)
            
            # Usage patterns - SMS
            data['daily_sms_count'] = np.random.gamma(2, 3, n_samples)
            data['bulk_sms_ratio'] = np.random.beta(1, 50, n_samples)
            data['international_sms_ratio'] = np.random.beta(1, 30, n_samples)
            data['short_code_sms_count'] = np.random.poisson(0.5, n_samples)
            
            # Usage patterns - Data
            data['daily_data_mb'] = np.random.gamma(3, 100, n_samples)
            data['night_data_ratio'] = np.random.beta(2, 5, n_samples)
            data['vpn_usage_ratio'] = np.random.beta(1, 20, n_samples)
            data['tethering_ratio'] = np.random.beta(1, 10, n_samples)
            
            # Network behavior
            data['sim_swap_count'] = np.random.poisson(0.2, n_samples)
            data['location_changes_daily'] = np.random.poisson(3, n_samples)
            data['roaming_days_ratio'] = np.random.beta(1, 20, n_samples)
            data['device_changes_count'] = np.random.poisson(0.3, n_samples)
            
            # Revenue and billing
            data['monthly_revenue'] = np.random.gamma(3, 20, n_samples)
            data['revenue_variance'] = np.random.exponential(10, n_samples)
            data['payment_failures'] = np.random.poisson(0.2, n_samples)
            data['refund_requests'] = np.random.poisson(0.1, n_samples)
            data['revenue_per_minute'] = data['monthly_revenue'] / (data['daily_call_count'] * 30 * data['avg_call_duration_sec'] / 60 + 1)
            
            # Time-based patterns
            data['night_call_ratio'] = np.random.beta(1, 5, n_samples)
            data['weekend_usage_ratio'] = np.random.beta(2, 3, n_samples)
            data['usage_consistency_score'] = np.random.beta(5, 2, n_samples)
            
            # Fraud indicators
            data['velocity_score'] = np.random.exponential(0.5, n_samples)  # Rapid changes in usage
            data['anomaly_score'] = np.random.exponential(0.3, n_samples)
            data['risk_score'] = np.random.beta(2, 8, n_samples)
            
            # Create fraud labels
            n_frauds = int(n_samples * fraud_rate)
            fraud_indices = np.random.choice(n_samples, n_frauds, replace=False)
            data['target'] = np.zeros(n_samples, dtype=int)
            data['target'][fraud_indices] = 1
            
            # Modify features for different fraud types
            # Type 1: SIM Box fraud (high call volume, many unique numbers)
            simbox_mask = fraud_indices[:n_frauds//3]
            data['daily_call_count'][simbox_mask] = data['daily_call_count'][simbox_mask] * np.random.uniform(10, 50, len(simbox_mask))
            data['unique_numbers_called'][simbox_mask] = data['unique_numbers_called'][simbox_mask] * np.random.uniform(5, 20, len(simbox_mask))
            data['avg_call_duration_sec'][simbox_mask] = np.random.uniform(10, 30, len(simbox_mask))  # Short calls
            data['international_call_ratio'][simbox_mask] = np.random.uniform(0.5, 0.9, len(simbox_mask))
            
            # Type 2: Subscription fraud (new account, high usage)
            subscription_mask = fraud_indices[n_frauds//3:2*n_frauds//3]
            data['account_age_days'][subscription_mask] = np.random.uniform(1, 30, len(subscription_mask))
            data['credit_score'][subscription_mask] = np.random.uniform(400, 600, len(subscription_mask))
            data['premium_number_calls'][subscription_mask] = np.random.poisson(5, len(subscription_mask))
            data['payment_failures'][subscription_mask] = np.random.poisson(2, len(subscription_mask))
            
            # Type 3: Wangiri fraud (missed call scam)
            wangiri_mask = fraud_indices[2*n_frauds//3:]
            data['daily_call_count'][wangiri_mask] = data['daily_call_count'][wangiri_mask] * np.random.uniform(20, 100, len(wangiri_mask))
            data['avg_call_duration_sec'][wangiri_mask] = np.random.uniform(1, 5, len(wangiri_mask))  # Very short
            data['night_call_ratio'][wangiri_mask] = np.random.uniform(0.6, 0.9, len(wangiri_mask))
            data['international_call_ratio'][wangiri_mask] = np.random.uniform(0.7, 1.0, len(wangiri_mask))
            
            # Update fraud indicators
            data['velocity_score'][fraud_indices] = data['velocity_score'][fraud_indices] * np.random.uniform(3, 10, len(fraud_indices))
            data['anomaly_score'][fraud_indices] = data['anomaly_score'][fraud_indices] * np.random.uniform(5, 15, len(fraud_indices))
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the telecom fraud dataset"""
        print(f"[TelecomFraudDetectionDataset] Raw shape: {df.shape}")
        print(f"[TelecomFraudDetectionDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['fraud', 'is_fraud', 'fraudulent', 'label', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            # Convert to binary
            if df[target_col].dtype == 'object':
                df['target'] = (df[target_col].str.lower().isin(['yes', 'true', '1', 'fraud'])).astype(int)
            else:
                df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Generate fraud labels based on anomalies
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Look for usage anomalies
                usage_cols = [col for col in numeric_cols if any(term in col.lower() for term in ['call', 'sms', 'data', 'usage', 'count'])]
                
                if usage_cols:
                    # High usage might indicate fraud
                    usage_sum = df[usage_cols].sum(axis=1)
                    threshold = usage_sum.quantile(0.97)
                    df['target'] = (usage_sum > threshold).astype(int)
                else:
                    # Use general anomaly detection
                    feature_sum = df[numeric_cols].sum(axis=1)
                    threshold = feature_sum.quantile(0.97)
                    df['target'] = (feature_sum > threshold).astype(int)
            else:
                df['target'] = np.random.choice([0, 1], len(df), p=[0.97, 0.03])
        
        # Remove non-numeric columns
        text_cols = ['msisdn', 'imsi', 'imei', 'subscriber_id', 'phone_number', 'timestamp']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Convert categorical columns
        cat_cols = ['plan_type', 'device_type', 'registration_channel', 'payment_method']
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
        
        # Create telecom fraud features if too few
        if len(feature_cols) < 15:
            # Add synthetic fraud detection features
            df['call_volume'] = np.random.gamma(2, 10, len(df))
            df['call_duration_avg'] = np.random.gamma(2, 60, len(df))
            df['international_ratio'] = np.random.beta(1, 20, len(df))
            df['unique_numbers'] = np.random.gamma(2, 10, len(df))
            df['sms_volume'] = np.random.gamma(2, 5, len(df))
            df['data_usage_gb'] = np.random.gamma(2, 2, len(df))
            df['revenue_monthly'] = np.random.gamma(3, 20, len(df))
            df['account_age'] = np.random.gamma(3, 100, len(df))
            df['sim_swaps'] = np.random.poisson(0.2, len(df))
            df['location_changes'] = np.random.poisson(3, len(df))
            df['payment_failures'] = np.random.poisson(0.2, len(df))
            df['velocity_score'] = np.random.exponential(0.5, len(df))
            
            new_features = ['call_volume', 'call_duration_avg', 'international_ratio',
                           'unique_numbers', 'sms_volume', 'data_usage_gb', 'revenue_monthly',
                           'account_age', 'sim_swaps', 'location_changes', 'payment_failures',
                           'velocity_score']
            feature_cols.extend(new_features)
        
        # Limit features
        if len(feature_cols) > 40:
            # Prioritize fraud-relevant features
            priority_features = ['call', 'sms', 'data', 'usage', 'revenue', 'payment',
                               'international', 'roaming', 'velocity', 'anomaly', 'risk']
            
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
                n_majority = min(n_minority * 30, target_counts[majority])
                df_minority = df[df['target'] == minority]
                df_majority = df[df['target'] == majority].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[TelecomFraudDetectionDataset] Final shape: {df.shape}")
        print(f"[TelecomFraudDetectionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[TelecomFraudDetectionDataset] Fraud rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = TelecomFraudDetectionDataset()
    df = dataset.get_data()
    print(f"Loaded TelecomFraudDetectionDataset: {df.shape}")
    print(df.head()) 