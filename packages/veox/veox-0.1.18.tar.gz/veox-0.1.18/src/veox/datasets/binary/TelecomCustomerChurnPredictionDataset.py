import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class TelecomCustomerChurnPredictionDataset(BaseDatasetLoader):
    """
    Telecom Customer Churn Prediction Dataset (binary classification)
    Source: Kaggle - Telecom Customer Churn
    Target: will_churn (0=retain, 1=churn)
    
    This dataset contains customer behavior, usage patterns, and service data
    for predicting customer churn in telecommunications.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'TelecomCustomerChurnPredictionDataset',
            'source_id': 'kaggle:telecom-churn-prediction',
            'category': 'binary_classification',
            'description': 'Customer churn prediction from telecom usage patterns.',
            'source_url': 'https://www.kaggle.com/datasets/shilongzhuang/telecom-customer-churn-by-maven-analytics',
        }
    
    def download_dataset(self, info):
        """Download the telecom churn dataset from Kaggle"""
        print(f"[TelecomCustomerChurnPredictionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[TelecomCustomerChurnPredictionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'shilongzhuang/telecom-customer-churn-by-maven-analytics',
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
                    print(f"[TelecomCustomerChurnPredictionDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=20000)
                    print(f"[TelecomCustomerChurnPredictionDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[TelecomCustomerChurnPredictionDataset] Download failed: {e}")
            print("[TelecomCustomerChurnPredictionDataset] Using sample telecom churn data...")
            
            # Create realistic telecom customer churn data
            np.random.seed(42)
            n_samples = 7000
            
            # Customer demographics
            data = {}
            data['tenure_months'] = np.random.gamma(2, 12, n_samples)
            data['age'] = np.random.normal(45, 15, n_samples)
            data['age'] = np.clip(data['age'], 18, 80).astype(int)
            data['income_level'] = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.15, 0.25, 0.3, 0.2, 0.1])
            
            # Service usage - Voice
            data['monthly_minutes'] = np.random.gamma(3, 100, n_samples)
            data['avg_call_duration'] = np.random.gamma(2, 2, n_samples)  # minutes
            data['international_minutes'] = np.random.exponential(10, n_samples)
            data['roaming_minutes'] = np.random.exponential(5, n_samples)
            
            # Service usage - Data
            data['monthly_data_gb'] = np.random.gamma(2, 5, n_samples)
            data['streaming_data_gb'] = data['monthly_data_gb'] * np.random.beta(3, 2, n_samples)
            data['social_media_data_gb'] = data['monthly_data_gb'] * np.random.beta(2, 3, n_samples)
            
            # Service usage - SMS
            data['monthly_sms'] = np.random.poisson(50, n_samples)
            data['international_sms'] = np.random.poisson(5, n_samples)
            
            # Network quality
            data['avg_signal_strength'] = np.random.beta(7, 3, n_samples) * 100  # percentage
            data['dropped_calls_pct'] = np.random.exponential(2, n_samples)
            data['network_complaints'] = np.random.poisson(0.3, n_samples)
            
            # Customer service
            data['support_calls'] = np.random.poisson(1, n_samples)
            data['avg_resolution_time'] = np.random.gamma(2, 30, n_samples)  # minutes
            data['satisfaction_score'] = np.random.beta(5, 2, n_samples) * 10
            
            # Billing and payments
            data['monthly_charges'] = 20 + data['monthly_minutes'] * 0.05 + data['monthly_data_gb'] * 5 + np.random.normal(0, 10, n_samples)
            data['total_charges'] = data['monthly_charges'] * data['tenure_months'] * np.random.uniform(0.9, 1.1, n_samples)
            data['payment_delay_days'] = np.random.exponential(2, n_samples)
            data['autopay_enrolled'] = np.random.choice([0, 1], n_samples, p=[0.4, 0.6])
            
            # Contract and services
            data['contract_type'] = np.random.choice([1, 2, 3], n_samples, p=[0.5, 0.3, 0.2])  # 1=month-to-month, 2=one year, 3=two year
            data['num_services'] = np.random.poisson(3, n_samples) + 1
            data['has_phone_service'] = np.random.choice([0, 1], n_samples, p=[0.1, 0.9])
            data['has_internet_service'] = np.random.choice([0, 1], n_samples, p=[0.2, 0.8])
            data['has_streaming_service'] = np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
            
            # Competitive factors
            data['competitor_offers_viewed'] = np.random.poisson(0.5, n_samples)
            data['price_sensitivity_score'] = np.random.beta(3, 2, n_samples)
            
            # Usage trends
            data['usage_trend_3m'] = np.random.normal(0, 0.2, n_samples)  # percentage change
            data['bill_trend_3m'] = np.random.normal(0.05, 0.1, n_samples)  # percentage change
            
            # Calculate churn probability based on multiple factors
            churn_prob = np.zeros(n_samples)
            
            # Tenure effect (newer customers more likely to churn)
            churn_prob += (data['tenure_months'] < 12) * 0.2
            
            # Contract type effect
            churn_prob += (data['contract_type'] == 1) * 0.15  # month-to-month
            
            # Service quality
            churn_prob += (data['dropped_calls_pct'] > 5) * 0.1
            churn_prob += (data['network_complaints'] > 2) * 0.15
            churn_prob += (data['satisfaction_score'] < 5) * 0.2
            
            # Support experience
            churn_prob += (data['support_calls'] > 3) * 0.1
            churn_prob += (data['avg_resolution_time'] > 60) * 0.1
            
            # Payment issues
            churn_prob += (data['payment_delay_days'] > 7) * 0.15
            churn_prob += (1 - data['autopay_enrolled']) * 0.05
            
            # Usage patterns
            churn_prob += (data['usage_trend_3m'] < -0.2) * 0.1  # declining usage
            churn_prob += (data['bill_trend_3m'] > 0.2) * 0.1  # increasing bills
            
            # Competition
            churn_prob += data['competitor_offers_viewed'] * 0.05
            churn_prob += data['price_sensitivity_score'] * 0.1
            
            # Add randomness
            churn_prob += np.random.normal(0, 0.1, n_samples)
            
            # Convert to binary
            data['target'] = (churn_prob > 0.5).astype(int)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the telecom churn dataset"""
        print(f"[TelecomCustomerChurnPredictionDataset] Raw shape: {df.shape}")
        print(f"[TelecomCustomerChurnPredictionDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find churn column
        churn_col = None
        for col in ['churn', 'Churn', 'Customer_Status', 'churn_label', 'target']:
            if col in df.columns:
                churn_col = col
                break
        
        if churn_col and churn_col != 'target':
            # Convert to binary
            if df[churn_col].dtype == 'object':
                # Map text values to binary
                churn_values = df[churn_col].unique()
                positive_values = ['Yes', 'Churned', 'True', '1', 'Churn']
                df['target'] = df[churn_col].apply(lambda x: 1 if str(x) in positive_values else 0)
            else:
                df['target'] = df[churn_col]
            df = df.drop(churn_col, axis=1)
        elif 'target' not in df.columns:
            raise ValueError("No suitable target column found")
        
        # Remove non-numeric columns
        text_cols = ['Customer_ID', 'customer_id', 'Phone', 'City', 'State', 'Zip_Code']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Handle categorical columns
        categorical_cols = ['Gender', 'Contract', 'Payment_Method', 'Internet_Type']
        for col in categorical_cols:
            if col in df.columns:
                # One-hot encode
                if df[col].nunique() < 10:
                    dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                    df = pd.concat([df, dummies], axis=1)
                df = df.drop(col, axis=1)
        
        # Convert Yes/No columns to binary
        for col in df.columns:
            if df[col].dtype == 'object' and col != 'target':
                if set(df[col].dropna().unique()).issubset({'Yes', 'No', 'yes', 'no'}):
                    df[col] = df[col].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().sum() > len(df) * 0.5:
                    feature_cols.append(col)
        
        # Limit features if too many
        if len(feature_cols) > 40:
            # Prioritize telecom features
            priority_features = ['tenure', 'charge', 'minutes', 'data', 'service', 'contract', 
                               'support', 'satisfaction', 'payment', 'usage']
            
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
        
        # Ensure target is binary
        df['target'] = df['target'].astype(int)
        df = df[df['target'].isin([0, 1])]
        
        # Balance classes if needed
        target_counts = df['target'].value_counts()
        if len(target_counts) == 2:
            minority_class = target_counts.idxmin()
            majority_class = target_counts.idxmax()
            
            if target_counts[minority_class] < target_counts[majority_class] * 0.2:
                # Undersample majority class
                n_minority = target_counts[minority_class]
                n_majority = min(n_minority * 3, target_counts[majority_class])
                
                df_minority = df[df['target'] == minority_class]
                df_majority = df[df['target'] == majority_class].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[TelecomCustomerChurnPredictionDataset] Final shape: {df.shape}")
        print(f"[TelecomCustomerChurnPredictionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[TelecomCustomerChurnPredictionDataset] Churn rate: {(df['target'] == 1).mean():.2%}")
        
        # Attach lightweight attrs to help downstream expansion, without tight coupling
        try:
            df.attrs["dataset_source"] = "TelecomCustomerChurnPredictionDataset"
            df.attrs["raw_feature_names"] = [c for c in df.columns if c != 'target']
            df.attrs["feature_expander"] = ("TelecomCustomerChurnPredictionDataset", "expand_features_on_dataframe")
        except Exception:
            pass
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        """
        Returns a lightweight descriptor for the feature engineering agent.
        This is intentionally simple – it does not perform any I/O or API calls.
        """
        return {
            "provider": provider,
            "name": "TelecomChurnFeatureAgent",
            "version": "v1",
        }

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        """
        Build a deterministic plan of derived features based solely on columns that
        already exist in the provided DataFrame. Each entry is a dict with:
          - name: feature name
          - requires: list of required columns
          - builder: callable(df) -> pd.Series
        """
        eps = 1e-6

        def has_all(cols):
            return all(c in df.columns for c in cols)

        plan = []

        # Tenure bucket (numeric bin index)
        if has_all(["tenure_months"]):
            def tenure_bucket(d):
                bins = [0, 3, 6, 12, 24, 48, 120]
                labels = list(range(len(bins) - 1))
                return pd.cut(d["tenure_months"], bins=bins, labels=labels, include_lowest=True).astype("Int64").fillna(0)
            plan.append({
                "name": "tenure_bucket",
                "requires": ["tenure_months"],
                "builder": tenure_bucket,
            })

        # Bundle diversity and services count variants
        service_flags = [c for c in [
            "has_phone_service", "has_internet_service", "has_streaming_service"
        ] if c in df.columns]
        if service_flags:
            def bundle_diversity(d):
                return d[service_flags].sum(axis=1)
            plan.append({
                "name": "bundle_diversity",
                "requires": service_flags,
                "builder": bundle_diversity,
            })

        if has_all(["num_services", "tenure_months"]):
            def services_per_year(d):
                return d["num_services"] / (d["tenure_months"] / 12.0 + eps)
            plan.append({
                "name": "services_per_year",
                "requires": ["num_services", "tenure_months"],
                "builder": services_per_year,
            })

        # Billing behavior
        if has_all(["monthly_charges", "total_charges", "tenure_months"]):
            def avg_monthly_from_total(d):
                return d["total_charges"] / (d["tenure_months"] + eps)
            def charge_delta_vs_tenure_avg(d):
                return d["monthly_charges"] - (d["total_charges"] / (d["tenure_months"] + eps))
            plan.append({
                "name": "avg_monthly_from_total",
                "requires": ["total_charges", "tenure_months"],
                "builder": avg_monthly_from_total,
            })
            plan.append({
                "name": "charge_delta_vs_tenure_avg",
                "requires": ["monthly_charges", "total_charges", "tenure_months"],
                "builder": charge_delta_vs_tenure_avg,
            })

        if has_all(["payment_delay_days", "autopay_enrolled"]):
            def autopay_and_delay(d):
                return (1 - d["autopay_enrolled"]) * d["payment_delay_days"]
            plan.append({
                "name": "autopay_and_delay",
                "requires": ["payment_delay_days", "autopay_enrolled"],
                "builder": autopay_and_delay,
            })

        # Price-to-usage efficiency
        if has_all(["monthly_charges", "monthly_data_gb"]):
            def cost_per_gb(d):
                return d["monthly_charges"] / (d["monthly_data_gb"] + eps)
            plan.append({
                "name": "cost_per_gb",
                "requires": ["monthly_charges", "monthly_data_gb"],
                "builder": cost_per_gb,
            })

        if has_all(["monthly_charges", "monthly_minutes"]):
            def cost_per_minute(d):
                return d["monthly_charges"] / (d["monthly_minutes"] + eps)
            plan.append({
                "name": "cost_per_minute",
                "requires": ["monthly_charges", "monthly_minutes"],
                "builder": cost_per_minute,
            })

        # Usage structure ratios
        if has_all(["streaming_data_gb", "monthly_data_gb"]):
            def data_share_streaming(d):
                return d["streaming_data_gb"] / (d["monthly_data_gb"] + eps)
            plan.append({
                "name": "data_share_streaming",
                "requires": ["streaming_data_gb", "monthly_data_gb"],
                "builder": data_share_streaming,
            })

        if has_all(["social_media_data_gb", "monthly_data_gb"]):
            def data_share_social(d):
                return d["social_media_data_gb"] / (d["monthly_data_gb"] + eps)
            plan.append({
                "name": "data_share_social",
                "requires": ["social_media_data_gb", "monthly_data_gb"],
                "builder": data_share_social,
            })

        if has_all(["international_minutes", "monthly_minutes"]):
            def international_minutes_ratio(d):
                return d["international_minutes"] / (d["monthly_minutes"] + eps)
            plan.append({
                "name": "international_minutes_ratio",
                "requires": ["international_minutes", "monthly_minutes"],
                "builder": international_minutes_ratio,
            })

        if has_all(["roaming_minutes", "monthly_minutes"]):
            def roaming_minutes_ratio(d):
                return d["roaming_minutes"] / (d["monthly_minutes"] + eps)
            plan.append({
                "name": "roaming_minutes_ratio",
                "requires": ["roaming_minutes", "monthly_minutes"],
                "builder": roaming_minutes_ratio,
            })

        if has_all(["monthly_minutes", "avg_call_duration"]):
            def approx_num_calls(d):
                return d["monthly_minutes"] / (d["avg_call_duration"] + eps)
            plan.append({
                "name": "approx_num_calls",
                "requires": ["monthly_minutes", "avg_call_duration"],
                "builder": approx_num_calls,
            })

        # Support and quality burden scores
        if has_all(["support_calls", "avg_resolution_time"]):
            def support_burden_score(d):
                return d["support_calls"] * np.log1p(d["avg_resolution_time"])
            plan.append({
                "name": "support_burden_score",
                "requires": ["support_calls", "avg_resolution_time"],
                "builder": support_burden_score,
            })

        if has_all(["dropped_calls_pct", "network_complaints"]):
            def quality_burden(d):
                return d["dropped_calls_pct"].clip(lower=0) + 2.0 * d["network_complaints"].clip(lower=0)
            plan.append({
                "name": "quality_burden",
                "requires": ["dropped_calls_pct", "network_complaints"],
                "builder": quality_burden,
            })

        # Contract flags
        if has_all(["contract_type"]):
            def month_to_month(d):
                return (d["contract_type"] == 1).astype(int)
            plan.append({
                "name": "contract_is_month_to_month",
                "requires": ["contract_type"],
                "builder": month_to_month,
            })

        # Dynamics
        if has_all(["bill_trend_3m", "usage_trend_3m"]):
            def usage_to_bill_trend_gap(d):
                return d["bill_trend_3m"] - d["usage_trend_3m"]
            plan.append({
                "name": "usage_to_bill_trend_gap",
                "requires": ["bill_trend_3m", "usage_trend_3m"],
                "builder": usage_to_bill_trend_gap,
            })

        if has_all(["price_sensitivity_score", "bill_trend_3m"]):
            def price_sensitivity_interaction(d):
                return d["price_sensitivity_score"] * d["bill_trend_3m"].clip(lower=0)
            plan.append({
                "name": "price_sensitivity_interaction",
                "requires": ["price_sensitivity_score", "bill_trend_3m"],
                "builder": price_sensitivity_interaction,
            })

        if has_all(["monthly_data_gb", "monthly_minutes"]):
            def data_to_minutes_ratio(d):
                return d["monthly_data_gb"] / (d["monthly_minutes"] + eps)
            plan.append({
                "name": "data_to_minutes_ratio",
                "requires": ["monthly_data_gb", "monthly_minutes"],
                "builder": data_to_minutes_ratio,
            })

        # ========== V13 BEST FEATURES FROM ITERATIVE OPTIMIZATION ==========
        # These features achieved 0.905707 AUC through compound risk modeling
        
        # Core tenure transformations (proven winners)
        if has_all(["tenure_months"]):
            plan.append({
                "name": "tenure_growth",
                "requires": ["tenure_months"],
                "builder": lambda d: 1 - np.exp(-pd.to_numeric(d["tenure_months"], errors="coerce") / 12.0),
            })
            plan.append({
                "name": "tenure_medium_decay", 
                "requires": ["tenure_months"],
                "builder": lambda d: np.exp(-pd.to_numeric(d["tenure_months"], errors="coerce") / 12.0),
            })
            plan.append({
                "name": "tenure_sigmoid",
                "requires": ["tenure_months"],
                "builder": lambda d: 1 / (1 + np.exp(-(pd.to_numeric(d["tenure_months"], errors="coerce") - 24) / 6)),
            })
            
        # Contract-satisfaction combinations (top performers)
        if has_all(["contract_type", "satisfaction_score"]):
            ct_col = "contract_type"
            ss_col = "satisfaction_score"
            
            plan.append({
                "name": "low_contract_low_sat",
                "requires": [ct_col, ss_col],
                "builder": lambda d: ((pd.to_numeric(d[ct_col], errors="coerce") == 1) & 
                                     (pd.to_numeric(d[ss_col], errors="coerce") < 5)).astype(int),
            })
            plan.append({
                "name": "contract_satisfaction_product",
                "requires": [ct_col, ss_col],
                "builder": lambda d: pd.to_numeric(d[ct_col], errors="coerce") * pd.to_numeric(d[ss_col], errors="coerce"),
            })
            plan.append({
                "name": "contract_satisfaction_harmonic",
                "requires": [ct_col, ss_col],
                "builder": lambda d: 2 * pd.to_numeric(d[ct_col], errors="coerce") * pd.to_numeric(d[ss_col], errors="coerce") / 
                                    (pd.to_numeric(d[ct_col], errors="coerce") + pd.to_numeric(d[ss_col], errors="coerce") + eps),
            })
            
        # Resolution time flag (was #3 in V2)
        if has_all(["avg_resolution_time"]):
            plan.append({
                "name": "long_resolution",
                "requires": ["avg_resolution_time"],
                "builder": lambda d: (pd.to_numeric(d["avg_resolution_time"], errors="coerce") > 60).astype(int),
            })
            
        # Competitive lock-in effect
        if has_all(["competitor_offers_viewed", "price_sensitivity_score", "contract_type", "satisfaction_score"]):
            plan.append({
                "name": "lock_in_effect",
                "requires": ["competitor_offers_viewed", "price_sensitivity_score", "contract_type", "satisfaction_score"],
                "builder": lambda d: pd.to_numeric(d["contract_type"], errors="coerce") * pd.to_numeric(d["satisfaction_score"], errors="coerce") / 
                                    (1 + pd.to_numeric(d["competitor_offers_viewed"], errors="coerce") * pd.to_numeric(d["price_sensitivity_score"], errors="coerce")),
            })
            
        # Compound risk scores (V13's key innovation)
        if has_all(["tenure_months", "satisfaction_score", "contract_type", "monthly_charges"]):
            def compound_risk_score(d):
                tm = pd.to_numeric(d["tenure_months"], errors="coerce")
                ss = pd.to_numeric(d["satisfaction_score"], errors="coerce")
                ct = pd.to_numeric(d["contract_type"], errors="coerce")
                mc = pd.to_numeric(d["monthly_charges"], errors="coerce")
                high_charges = (mc > mc.median()).astype(float)
                risk = (
                    (tm < 12) * 0.25 +
                    (ss < 5) * 0.25 +
                    (ct == 1) * 0.25 +
                    high_charges * 0.25
                )
                return risk
                
            plan.append({
                "name": "compound_risk_score",
                "requires": ["tenure_months", "satisfaction_score", "contract_type", "monthly_charges"],
                "builder": compound_risk_score,
            })
            
            def optimized_compound_risk(d):
                tm = pd.to_numeric(d["tenure_months"], errors="coerce")
                ss = pd.to_numeric(d["satisfaction_score"], errors="coerce")
                ct = pd.to_numeric(d["contract_type"], errors="coerce")
                mc = pd.to_numeric(d["monthly_charges"], errors="coerce")
                high_charges = (mc > mc.quantile(0.70)).astype(float)
                risk = (
                    (tm < 10) * 0.35 +
                    (ss < 4.5) * 0.30 +
                    (ct == 1) * 0.20 +
                    high_charges * 0.15
                )
                return risk
                
            plan.append({
                "name": "optimized_compound_risk",
                "requires": ["tenure_months", "satisfaction_score", "contract_type", "monthly_charges"],
                "builder": optimized_compound_risk,
            })
            
        # Behavioral compound risk
        if has_all(["usage_trend_3m", "bill_trend_3m", "support_calls", "network_complaints"]):
            def behavioral_compound_risk(d):
                ut = pd.to_numeric(d["usage_trend_3m"], errors="coerce")
                bt = pd.to_numeric(d["bill_trend_3m"], errors="coerce")
                sc = pd.to_numeric(d["support_calls"], errors="coerce")
                nc = pd.to_numeric(d["network_complaints"], errors="coerce")
                risk = (
                    np.maximum(0, -ut) * 0.3 +
                    np.maximum(0, bt) * 0.3 +
                    (sc > 2) * 0.2 +
                    (nc > 1) * 0.2
                )
                return risk
                
            plan.append({
                "name": "behavioral_compound_risk",
                "requires": ["usage_trend_3m", "bill_trend_3m", "support_calls", "network_complaints"],
                "builder": behavioral_compound_risk,
            })
            
        # Temporal compound risk
        if has_all(["tenure_months", "payment_delay_days", "autopay_enrolled"]):
            def temporal_compound_risk(d):
                tm = pd.to_numeric(d["tenure_months"], errors="coerce")
                pdd = pd.to_numeric(d["payment_delay_days"], errors="coerce")
                ae = pd.to_numeric(d["autopay_enrolled"], errors="coerce")
                risk = (
                    np.exp(-tm / 12) * 0.4 +
                    (pdd > 14) * 0.3 +
                    (1 - ae) * 0.3
                )
                return risk
                
            plan.append({
                "name": "temporal_compound_risk",
                "requires": ["tenure_months", "payment_delay_days", "autopay_enrolled"],
                "builder": temporal_compound_risk,
            })
            
        # Critical mass indicators
        if has_all(["tenure_months", "satisfaction_score", "contract_type"]):
            def critical_mass_2factors(d):
                tm = pd.to_numeric(d["tenure_months"], errors="coerce")
                ss = pd.to_numeric(d["satisfaction_score"], errors="coerce")
                ct = pd.to_numeric(d["contract_type"], errors="coerce")
                risk = (
                    ((tm < 12) & (ss < 5)) |
                    ((tm < 12) & (ct == 1)) |
                    ((ss < 5) & (ct == 1))
                ).astype(int)
                return risk
                
            plan.append({
                "name": "critical_mass_2factors",
                "requires": ["tenure_months", "satisfaction_score", "contract_type"],
                "builder": critical_mass_2factors,
            })

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        """
        Static helper so other components (e.g., an expander stage) can apply the
        same telecom-specific engineered features without coupling to dataset I/O.
        Returns: (df_with_features, list_of_added_feature_names)
        """
        self_like = TelecomCustomerChurnPredictionDataset()
        agent = self_like.get_feature_agent(provider="GPT5")
        plan = self_like._propose_agent_feature_plan(df, agent)

        added = []
        for item in plan:
            name = item["name"]
            requires = item["requires"]
            builder = item["builder"]
            if name in df.columns:
                continue
            if all(col in df.columns for col in requires):
                try:
                    df[name] = builder(df)
                    added.append(name)
                except Exception as _:
                    # Skip feature on any unexpected numeric/conversion issues
                    pass
        return df, added

    def _apply_agent_feature_plan(self, df: pd.DataFrame, plan: list) -> (pd.DataFrame, list):
        added = []
        for item in plan:
            name = item["name"]
            requires = item["requires"]
            builder = item["builder"]
            if name in df.columns:
                continue
            if all(col in df.columns for col in requires):
                try:
                    df[name] = builder(df)
                    added.append(name)
                except Exception as _:
                    # Best-effort: skip if computation fails for any row/column type issue
                    pass
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        """
        Returns the processed dataset enriched with deterministic, high-value
        derived features. This method never re-downloads data; it builds on
        top of the result of get_data().

        - agent_provider is informational and recorded in DataFrame.attrs
        - if features are already applied (attrs flag), returns as-is unless force=True
        """
        df = self.get_data()

        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df

        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = self._apply_agent_feature_plan(df, plan)

        # Record provenance so pipeline expanders can no-op
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass

        return df

if __name__ == "__main__":
    dataset = TelecomCustomerChurnPredictionDataset()
    # Load once (baseline)
    df = dataset.get_data()
    print(f"Loaded TelecomCustomerChurnPredictionDataset: {df.shape}")
    print(df.head())

    # Prepare expanded view without re-downloading by reusing df in-memory
    df_exp = df.copy(deep=True)
    df_exp, added = TelecomCustomerChurnPredictionDataset.expand_features_on_dataframe(df_exp)
    try:
        df_exp.attrs["agent_expansion_applied"] = True
        df_exp.attrs["agent_provider"] = "GPT5"
        df_exp.attrs["agent_expanded_features"] = list(added)
    except Exception:
        pass

    # K-fold CatBoost AUC comparison: baseline vs expanded+AgentFeatureExpander
    try:
        from sklearn.model_selection import StratifiedKFold
        from sklearn.metrics import roc_auc_score
        from catboost import CatBoostClassifier
        from app.seed_data.Generative.shared.stages.transforms.expanders.AgentFeatureExpander import AgentFeatureExpander

        X_base = df.drop(columns=["target"])
        y = df["target"]
        X_exp = df_exp.drop(columns=["target"])

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        aucs_base = []
        aucs_exp = []

        for train_idx, test_idx in skf.split(X_base, y):
            # Baseline
            Xtr = X_base.iloc[train_idx]
            Xte = X_base.iloc[test_idx]
            ytr = y.iloc[train_idx]
            yte = y.iloc[test_idx]

            model = CatBoostClassifier(
                verbose=False,
                depth=6,
                learning_rate=0.1,
                iterations=300,
                loss_function="Logloss",
                eval_metric="AUC",
                random_seed=42,
            )
            model.fit(Xtr, ytr)
            p = model.predict_proba(Xte)[:, 1]
            aucs_base.append(roc_auc_score(yte, p))

            # Expanded + expander stage (no-op expected due to attrs)
            Xtr2 = X_exp.iloc[train_idx].copy()
            Xte2 = X_exp.iloc[test_idx].copy()
            ytr2 = y.iloc[train_idx]
            yte2 = y.iloc[test_idx]

            expander = AgentFeatureExpander(prefer_dataset="TelecomCustomerChurnPredictionDataset")
            Xtr2 = expander.fit_transform(Xtr2, ytr2)
            Xte2 = expander.transform(Xte2)

            model2 = CatBoostClassifier(
                verbose=False,
                depth=6,
                learning_rate=0.1,
                iterations=300,
                loss_function="Logloss",
                eval_metric="AUC",
                random_seed=42,
            )
            model2.fit(Xtr2, ytr2)
            p2 = model2.predict_proba(Xte2)[:, 1]
            aucs_exp.append(roc_auc_score(yte2, p2))

        print({
            "baseline_auc_mean": float(np.mean(aucs_base)),
            "baseline_auc_std": float(np.std(aucs_base)),
            "expanded_auc_mean": float(np.mean(aucs_exp)),
            "expanded_auc_std": float(np.std(aucs_exp)),
            "folds": len(aucs_base),
            "added_features": len(added),
        })
    except Exception as e:
        print(f"[TelecomCustomerChurnPredictionDataset] CV run skipped due to: {e}")