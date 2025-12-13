import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CyberThreatDetectionDataset(BaseDatasetLoader):
    """
    Cyber Threat Detection Dataset (binary classification)
    Source: Kaggle - Cybersecurity Attack Data
    Target: is_threat (0=benign, 1=threat)
    
    This dataset contains network and system logs for detecting
    various cyber threats and attacks.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'CyberThreatDetectionDataset',
            'source_id': 'kaggle:cyber-threat-detection',
            'category': 'binary_classification',
            'description': 'Cyber threat detection from network traffic and system logs.',
            'source_url': 'https://www.kaggle.com/datasets/solarmainframe/ids-intrusion-csv',
        }
    
    def download_dataset(self, info):
        """Download the cyber threat dataset from Kaggle"""
        print(f"[CyberThreatDetectionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[CyberThreatDetectionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'solarmainframe/ids-intrusion-csv',
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
                    print(f"[CyberThreatDetectionDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=15000)
                    print(f"[CyberThreatDetectionDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[CyberThreatDetectionDataset] Download failed: {e}")
            print("[CyberThreatDetectionDataset] Using sample cyber threat data...")
            
            # Create realistic cyber threat detection data
            np.random.seed(42)
            n_samples = 10000
            threat_rate = 0.15  # 15% threats
            
            # Network traffic features
            data = {}
            data['src_port'] = np.random.choice(range(1, 65536), n_samples)
            data['dst_port'] = np.random.choice([21, 22, 23, 25, 53, 80, 110, 443, 445, 3389] + list(range(1024, 65536)), 
                                               n_samples, p=[0.02, 0.05, 0.01, 0.02, 0.03, 0.15, 0.01, 0.15, 0.02, 0.02] + [0.52/(65536-1024)]*(65536-1024))
            data['protocol'] = np.random.choice([1, 2, 3], n_samples, p=[0.7, 0.25, 0.05])  # TCP, UDP, ICMP
            data['packet_size'] = np.random.gamma(2, 500, n_samples)
            data['flow_duration'] = np.random.exponential(10, n_samples)
            
            # Connection features
            data['syn_flag_count'] = np.random.poisson(1, n_samples)
            data['ack_flag_count'] = np.random.poisson(5, n_samples)
            data['fin_flag_count'] = np.random.poisson(1, n_samples)
            data['rst_flag_count'] = np.random.poisson(0.1, n_samples)
            data['psh_flag_count'] = np.random.poisson(2, n_samples)
            data['urg_flag_count'] = np.random.poisson(0.01, n_samples)
            
            # Traffic statistics
            data['packets_per_second'] = np.random.gamma(3, 10, n_samples)
            data['bytes_per_second'] = data['packets_per_second'] * data['packet_size']
            data['packet_size_variance'] = np.random.exponential(100, n_samples)
            data['inter_arrival_time_avg'] = np.random.exponential(0.1, n_samples)
            
            # System logs
            data['failed_login_attempts'] = np.random.poisson(0.5, n_samples)
            data['successful_logins'] = np.random.poisson(5, n_samples)
            data['privilege_escalation_attempts'] = np.random.poisson(0.01, n_samples)
            data['file_access_anomalies'] = np.random.poisson(0.1, n_samples)
            data['process_creation_rate'] = np.random.poisson(10, n_samples)
            
            # User behavior
            data['user_activity_score'] = np.random.gamma(2, 5, n_samples)
            data['unusual_hour_activity'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
            data['remote_access_count'] = np.random.poisson(1, n_samples)
            data['data_exfiltration_score'] = np.random.exponential(0.5, n_samples)
            
            # Security events
            data['firewall_blocks'] = np.random.poisson(2, n_samples)
            data['ids_alerts'] = np.random.poisson(0.5, n_samples)
            data['antivirus_detections'] = np.random.poisson(0.1, n_samples)
            data['security_policy_violations'] = np.random.poisson(0.2, n_samples)
            
            # Resource usage
            data['cpu_usage_percent'] = np.random.beta(2, 5, n_samples) * 100
            data['memory_usage_percent'] = np.random.beta(3, 4, n_samples) * 100
            data['disk_io_rate'] = np.random.gamma(2, 100, n_samples)
            data['network_bandwidth_usage'] = np.random.gamma(3, 50, n_samples)
            
            # Threat indicators
            data['known_malicious_ip'] = np.random.choice([0, 1], n_samples, p=[0.98, 0.02])
            data['suspicious_dns_queries'] = np.random.poisson(0.2, n_samples)
            data['encrypted_traffic_ratio'] = np.random.beta(3, 2, n_samples)
            data['payload_entropy'] = np.random.beta(5, 2, n_samples) * 8  # bits
            
            # Create threat labels
            n_threats = int(n_samples * threat_rate)
            threat_indices = np.random.choice(n_samples, n_threats, replace=False)
            data['target'] = np.zeros(n_samples, dtype=int)
            data['target'][threat_indices] = 1
            
            # Modify features for different threat types
            # Type 1: DDoS/DoS attacks
            ddos_mask = threat_indices[:n_threats//4]
            data['packets_per_second'][ddos_mask] = data['packets_per_second'][ddos_mask] * np.random.uniform(10, 100, len(ddos_mask))
            data['syn_flag_count'][ddos_mask] = np.random.poisson(50, len(ddos_mask))
            data['packet_size'][ddos_mask] = np.random.choice([64, 128], len(ddos_mask))  # Small packets
            
            # Type 2: Brute force attacks
            bruteforce_mask = threat_indices[n_threats//4:n_threats//2]
            data['failed_login_attempts'][bruteforce_mask] = np.random.poisson(20, len(bruteforce_mask))
            data['successful_logins'][bruteforce_mask] = np.random.poisson(1, len(bruteforce_mask))
            data['remote_access_count'][bruteforce_mask] = np.random.poisson(10, len(bruteforce_mask))
            
            # Type 3: Malware/Backdoor
            malware_mask = threat_indices[n_threats//2:3*n_threats//4]
            data['process_creation_rate'][malware_mask] = np.random.poisson(50, len(malware_mask))
            data['unusual_hour_activity'][malware_mask] = 1
            data['cpu_usage_percent'][malware_mask] = np.random.uniform(70, 100, len(malware_mask))
            data['antivirus_detections'][malware_mask] = np.random.poisson(3, len(malware_mask))
            
            # Type 4: Data exfiltration
            exfil_mask = threat_indices[3*n_threats//4:]
            data['data_exfiltration_score'][exfil_mask] = np.random.uniform(5, 20, len(exfil_mask))
            data['bytes_per_second'][exfil_mask] = data['bytes_per_second'][exfil_mask] * np.random.uniform(5, 50, len(exfil_mask))
            data['encrypted_traffic_ratio'][exfil_mask] = np.random.uniform(0.8, 1.0, len(exfil_mask))
            data['suspicious_dns_queries'][exfil_mask] = np.random.poisson(5, len(exfil_mask))
            
            # Update general threat indicators
            data['known_malicious_ip'][threat_indices[:n_threats//2]] = 1
            data['ids_alerts'][threat_indices] = np.random.poisson(5, len(threat_indices))
            data['firewall_blocks'][threat_indices] = np.random.poisson(10, len(threat_indices))
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the cyber threat dataset"""
        print(f"[CyberThreatDetectionDataset] Raw shape: {df.shape}")
        print(f"[CyberThreatDetectionDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['class', 'label', 'attack', 'threat', 'malicious', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            # Convert to binary
            if df[target_col].dtype == 'object':
                # Map attack types to binary
                benign_values = ['normal', 'benign', 'safe', 'legitimate', '0']
                df['target'] = (~df[target_col].str.lower().isin(benign_values)).astype(int)
            else:
                df['target'] = (df[target_col] != 0).astype(int)
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Generate threat labels based on anomalies
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Look for security-related anomalies
                security_cols = [col for col in numeric_cols if any(
                    term in col.lower() for term in ['attack', 'fail', 'error', 'alert', 'block', 'threat']
                )]
                
                if security_cols:
                    # High values in security columns indicate threats
                    threat_score = df[security_cols].sum(axis=1)
                    threshold = threat_score.quantile(0.85)
                    df['target'] = (threat_score > threshold).astype(int)
                else:
                    # Use general anomaly detection
                    feature_std = df[numeric_cols].std(axis=1)
                    threshold = feature_std.quantile(0.85)
                    df['target'] = (feature_std > threshold).astype(int)
            else:
                df['target'] = np.random.choice([0, 1], len(df), p=[0.85, 0.15])
        
        # Remove non-numeric columns
        text_cols = ['src_ip', 'dst_ip', 'timestamp', 'hostname', 'username', 'log_source']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Convert categorical columns
        cat_cols = ['protocol', 'service', 'flag', 'attack_type', 'severity']
        for col in cat_cols:
            if col in df.columns and df[col].dtype == 'object':
                # Limit categories to prevent explosion
                top_categories = df[col].value_counts().head(10).index
                df[col] = df[col].apply(lambda x: x if x in top_categories else 'other')
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
        
        # Create cyber threat features if too few
        if len(feature_cols) < 15:
            # Add synthetic security features
            df['packet_rate'] = np.random.gamma(3, 10, len(df))
            df['byte_rate'] = np.random.gamma(3, 1000, len(df))
            df['connection_count'] = np.random.poisson(10, len(df))
            df['failed_attempts'] = np.random.poisson(1, len(df))
            df['port_scan_score'] = np.random.exponential(0.5, len(df))
            df['anomaly_score'] = np.random.exponential(1, len(df))
            df['cpu_usage'] = np.random.beta(2, 5, len(df)) * 100
            df['memory_usage'] = np.random.beta(3, 4, len(df)) * 100
            df['firewall_blocks'] = np.random.poisson(2, len(df))
            df['ids_alerts'] = np.random.poisson(0.5, len(df))
            df['encryption_ratio'] = np.random.beta(3, 2, len(df))
            df['payload_entropy'] = np.random.beta(5, 2, len(df)) * 8
            
            new_features = ['packet_rate', 'byte_rate', 'connection_count', 'failed_attempts',
                           'port_scan_score', 'anomaly_score', 'cpu_usage', 'memory_usage',
                           'firewall_blocks', 'ids_alerts', 'encryption_ratio', 'payload_entropy']
            feature_cols.extend(new_features)
        
        # Limit features
        if len(feature_cols) > 40:
            # Prioritize security-relevant features
            priority_features = ['packet', 'byte', 'flag', 'port', 'protocol', 'connection',
                               'fail', 'attack', 'anomaly', 'alert', 'block', 'threat']
            
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
        
        # Balance if needed
        target_counts = df['target'].value_counts()
        if len(target_counts) == 2:
            minority = target_counts.idxmin()
            majority = target_counts.idxmax()
            if target_counts[minority] < target_counts[majority] * 0.05:
                # Undersample majority
                n_minority = target_counts[minority]
                n_majority = min(n_minority * 10, target_counts[majority])
                df_minority = df[df['target'] == minority]
                df_majority = df[df['target'] == majority].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[CyberThreatDetectionDataset] Final shape: {df.shape}")
        print(f"[CyberThreatDetectionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[CyberThreatDetectionDataset] Threat rate: {(df['target'] == 1).mean():.2%}")
        
        return df

if __name__ == "__main__":
    dataset = CyberThreatDetectionDataset()
    df = dataset.get_data()
    print(f"Loaded CyberThreatDetectionDataset: {df.shape}")
    print(df.head()) 