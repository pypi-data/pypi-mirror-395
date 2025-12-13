import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class PredictiveMaintenanceDataset(BaseDatasetLoader):
    """
    Predictive Maintenance Dataset (binary classification)
    Source: Kaggle - Machine Predictive Maintenance Classification
    Target: failure (0=normal, 1=failure)
    
    This dataset contains sensor data from industrial equipment
    for predicting machine failures before they occur.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'PredictiveMaintenanceDataset',
            'source_id': 'kaggle:predictive-maintenance',
            'category': 'binary_classification',
            'description': 'Machine failure prediction from sensor and operational data.',
            'source_url': 'https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification',
        }
    
    def download_dataset(self, info):
        """Download the predictive maintenance dataset from Kaggle"""
        print(f"[PredictiveMaintenanceDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[PredictiveMaintenanceDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'shivamb/machine-predictive-maintenance-classification',
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
                    print(f"[PredictiveMaintenanceDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file)
                    print(f"[PredictiveMaintenanceDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[PredictiveMaintenanceDataset] Download failed: {e}")
            print("[PredictiveMaintenanceDataset] Using sample predictive maintenance data...")
            
            # Create realistic predictive maintenance data
            np.random.seed(42)
            n_samples = 10000
            
            # Machine characteristics
            data = {}
            data['machine_id'] = np.random.randint(1, 100, n_samples)
            data['machine_age_days'] = np.random.gamma(3, 200, n_samples)
            data['machine_type'] = np.random.choice([1, 2, 3, 4], n_samples)  # Different machine types
            
            # Operating conditions
            data['rotation_speed_rpm'] = np.random.normal(1500, 200, n_samples)
            data['torque_nm'] = np.random.normal(40, 10, n_samples)
            data['tool_wear_min'] = np.random.exponential(100, n_samples)
            
            # Temperature sensors
            data['air_temp_k'] = np.random.normal(298, 2, n_samples)
            data['process_temp_k'] = data['air_temp_k'] + np.random.normal(10, 2, n_samples)
            data['bearing_temp_c'] = np.random.normal(60, 15, n_samples)
            data['motor_temp_c'] = np.random.normal(70, 20, n_samples)
            
            # Vibration sensors
            data['vibration_x_mm_s'] = np.random.gamma(2, 0.5, n_samples)
            data['vibration_y_mm_s'] = np.random.gamma(2, 0.5, n_samples)
            data['vibration_z_mm_s'] = np.random.gamma(2, 0.5, n_samples)
            data['vibration_total'] = np.sqrt(data['vibration_x_mm_s']**2 + 
                                            data['vibration_y_mm_s']**2 + 
                                            data['vibration_z_mm_s']**2)
            
            # Acoustic sensors
            data['sound_level_db'] = np.random.normal(85, 10, n_samples)
            data['ultrasonic_freq_khz'] = np.random.normal(40, 5, n_samples)
            
            # Electrical measurements
            data['motor_current_a'] = np.random.normal(15, 3, n_samples)
            data['motor_voltage_v'] = np.random.normal(380, 10, n_samples)
            data['power_factor'] = np.random.beta(8, 2, n_samples)
            data['power_consumption_kw'] = (data['motor_current_a'] * data['motor_voltage_v'] * 
                                           data['power_factor'] * np.sqrt(3) / 1000)
            
            # Pressure and flow
            data['hydraulic_pressure_bar'] = np.random.normal(100, 20, n_samples)
            data['coolant_flow_l_min'] = np.random.normal(10, 2, n_samples)
            data['oil_pressure_bar'] = np.random.normal(4, 0.5, n_samples)
            
            # Quality metrics
            data['product_quality_score'] = np.random.beta(5, 1, n_samples) * 100
            data['defect_rate_ppm'] = np.random.exponential(50, n_samples)
            
            # Maintenance history
            data['days_since_maintenance'] = np.random.exponential(30, n_samples)
            data['num_past_failures'] = np.random.poisson(0.5, n_samples)
            
            # Environmental conditions
            data['ambient_humidity_percent'] = np.random.beta(3, 2, n_samples) * 100
            data['dust_level_mg_m3'] = np.random.exponential(0.5, n_samples)
            
            # Calculate failure probability based on multiple factors
            failure_prob = np.zeros(n_samples)
            
            # Age and wear factors
            failure_prob += (data['machine_age_days'] > 1000) * 0.1
            failure_prob += (data['tool_wear_min'] > 200) * 0.15
            
            # Temperature factors
            failure_prob += (data['bearing_temp_c'] > 80) * 0.2
            failure_prob += (data['motor_temp_c'] > 100) * 0.2
            failure_prob += (np.abs(data['process_temp_k'] - data['air_temp_k']) > 15) * 0.1
            
            # Vibration factors
            failure_prob += (data['vibration_total'] > 5) * 0.25
            failure_prob += (data['vibration_total'] > 8) * 0.25
            
            # Electrical factors
            failure_prob += (np.abs(data['motor_current_a'] - 15) > 6) * 0.15
            failure_prob += (data['power_factor'] < 0.7) * 0.1
            
            # Operational factors
            failure_prob += (np.abs(data['rotation_speed_rpm'] - 1500) > 400) * 0.15
            failure_prob += (data['torque_nm'] > 60) * 0.1
            
            # Maintenance factors
            failure_prob += (data['days_since_maintenance'] > 90) * 0.2
            failure_prob += (data['num_past_failures'] > 2) * 0.15
            
            # Quality indicators
            failure_prob += (data['product_quality_score'] < 70) * 0.1
            failure_prob += (data['defect_rate_ppm'] > 100) * 0.1
            
            # Add randomness
            failure_prob += np.random.normal(0, 0.05, n_samples)
            
            # Convert to binary
            data['target'] = (failure_prob > 0.3).astype(int)
            
            # Add some specific failure modes
            # Overheating failures
            overheat_mask = (data['motor_temp_c'] > 110) | (data['bearing_temp_c'] > 100)
            data['target'][overheat_mask] = 1
            
            # Vibration failures
            vibration_mask = data['vibration_total'] > 10
            data['target'][vibration_mask] = 1
            
            df = pd.DataFrame(data)
            
            # Remove machine_id as it's not a feature
            df = df.drop('machine_id', axis=1)
            
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the predictive maintenance dataset"""
        print(f"[PredictiveMaintenanceDataset] Raw shape: {df.shape}")
        print(f"[PredictiveMaintenanceDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['failure', 'fail', 'target', 'machine failure', 'failure_type']:
            if col in df.columns or col.lower() in [c.lower() for c in df.columns]:
                for c in df.columns:
                    if col.lower() == c.lower():
                        target_col = c
                        break
                if target_col:
                    break
        
        if target_col and target_col != 'target':
            # Convert to binary
            if df[target_col].dtype == 'object':
                # Map text values to binary
                df['target'] = df[target_col].apply(lambda x: 0 if str(x).lower() in ['no', 'no failure', 'normal', '0'] else 1)
            else:
                df['target'] = (df[target_col] > 0).astype(int)
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Look for any failure indicator columns
            failure_cols = [col for col in df.columns if 'fail' in col.lower()]
            if failure_cols:
                # Combine multiple failure types
                df['target'] = (df[failure_cols].sum(axis=1) > 0).astype(int)
                df = df.drop(failure_cols, axis=1)
            else:
                # Create target from anomaly detection
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    # Use statistical outliers as failures
                    z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())
                    df['target'] = (z_scores > 3).any(axis=1).astype(int)
                else:
                    raise ValueError("No suitable target column found")
        
        # Remove non-numeric columns
        text_cols = ['uid', 'product_id', 'type', 'machine_id', 'timestamp', 'date']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Handle categorical columns
        for col in df.columns:
            if df[col].dtype == 'object' and col != 'target':
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].isna().all():
                    df = df.drop(col, axis=1)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                if df[col].dtype in [np.int64, np.float64, np.int32, np.float32]:
                    if df[col].notna().sum() > len(df) * 0.5:
                        feature_cols.append(col)
        
        # Limit features if too many
        if len(feature_cols) > 50:
            # Prioritize maintenance-specific features
            priority_features = ['temp', 'vibration', 'pressure', 'speed', 'torque', 
                               'current', 'voltage', 'wear', 'age', 'sound']
            
            selected_features = []
            for feat in priority_features:
                for col in feature_cols:
                    if feat in col.lower() and col not in selected_features:
                        selected_features.append(col)
            
            # Add remaining features up to limit
            for col in feature_cols:
                if col not in selected_features and len(selected_features) < 50:
                    selected_features.append(col)
            
            feature_cols = selected_features[:50]
        
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
            
            if target_counts[minority_class] < target_counts[majority_class] * 0.05:
                # Undersample majority class
                n_minority = target_counts[minority_class]
                n_majority = min(n_minority * 10, target_counts[majority_class])
                
                df_minority = df[df['target'] == minority_class]
                df_majority = df[df['target'] == majority_class].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[PredictiveMaintenanceDataset] Final shape: {df.shape}")
        print(f"[PredictiveMaintenanceDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[PredictiveMaintenanceDataset] Failure rate: {(df['target'] == 1).mean():.2%}")
        
        # Attach lightweight attrs to help downstream expansion
        try:
            df.attrs["dataset_source"] = "PredictiveMaintenanceDataset"
            df.attrs["raw_feature_names"] = [c for c in df.columns if c != 'target']
            df.attrs["feature_expander"] = ("PredictiveMaintenanceDataset", "expand_features_on_dataframe")
        except Exception:
            pass
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Predictive Maintenance)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "PredictiveMaintenanceFeatureAgent", "version": "v1"}

    def _find_cols(self, df: pd.DataFrame, keywords):
        kw = [k.lower() for k in keywords]
        return [c for c in df.columns if any(k in c.lower() for k in kw)]

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        plan = []

        # Temperatures
        temp_cols = self._find_cols(df, ["temp", "temperature"])  # e.g., air/process/bearing/motor
        air_like = [c for c in temp_cols if "air" in c.lower()]
        proc_like = [c for c in temp_cols if "process" in c.lower()]
        if air_like and proc_like:
            a, p = air_like[0], proc_like[0]
            plan.append({"name": "temp_delta_proc_air", "requires": [a, p], "builder": lambda d, A=a, P=p: d[P] - d[A]})

        # Vibration magnitude
        vib_cols = self._find_cols(df, ["vibration", "vib"])
        if vib_cols:
            def vib_total(d):
                vals = d[vib_cols]
                return np.sqrt((vals**2).sum(axis=1))
            plan.append({"name": "vibration_total_mag", "requires": vib_cols, "builder": vib_total})

        # RPM × torque product
        rpm_cols = self._find_cols(df, ["rpm", "rotation_speed", "rotational speed"]) 
        torque_cols = self._find_cols(df, ["torque"]) 
        if rpm_cols and torque_cols:
            r, t = rpm_cols[0], torque_cols[0]
            plan.append({"name": "rpm_x_torque", "requires": [r, t], "builder": lambda d, R=r, T=t: d[R] * d[T]})

        # Tool wear log
        wear_cols = self._find_cols(df, ["wear"]) 
        if wear_cols:
            w = wear_cols[0]
            plan.append({"name": "tool_wear_log1p", "requires": [w], "builder": lambda d, W=w: np.log1p(d[W].clip(lower=0))})

        # Pressures and flows
        press_cols = self._find_cols(df, ["pressure"]) 
        flow_cols = self._find_cols(df, ["flow"]) 
        if len(press_cols) >= 2:
            plan.append({"name": "pressure_diff_any", "requires": press_cols[:2], "builder": lambda d, A=press_cols[0], B=press_cols[1]: d[A] - d[B]})
        if press_cols and flow_cols:
            plan.append({"name": "flow_per_pressure", "requires": [press_cols[0], flow_cols[0]], "builder": lambda d, P=press_cols[0], F=flow_cols[0]: d[F] / (d[P] + eps)})

        # Electrical: specific power
        power_cols = self._find_cols(df, ["power_consumption", "power "]) 
        if power_cols and rpm_cols and torque_cols:
            pc = power_cols[0]
            r, t = rpm_cols[0], torque_cols[0]
            plan.append({"name": "specific_power", "requires": [pc, r, t], "builder": lambda d, P=pc, R=r, T=t: d[P] / (np.abs(d[R]*d[T]) + eps)})

        # Maintenance age ratio
        age_cols = self._find_cols(df, ["age"]) 
        dsm_cols = self._find_cols(df, ["days_since_maintenance"]) 
        if age_cols and dsm_cols:
            plan.append({"name": "maintenance_age_ratio", "requires": [age_cols[0], dsm_cols[0]], "builder": lambda d, A=age_cols[0], D=dsm_cols[0]: d[D] / (d[A] + eps)})

        # Quality flags
        defect_cols = self._find_cols(df, ["defect"]) 
        if defect_cols:
            dc = defect_cols[0]
            plan.append({"name": "defect_high_flag", "requires": [dc], "builder": lambda d, C=dc: (d[C] > d[C].quantile(0.95)).astype(int)})

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = PredictiveMaintenanceDataset()
        agent = self_like.get_feature_agent(provider="GPT5")
        plan = self_like._propose_agent_feature_plan(df, agent)
        added = []
        for item in plan:
            name = item["name"]; requires = item["requires"]; builder = item["builder"]
            if name in df.columns:
                continue
            if all(col in df.columns for col in requires):
                try:
                    df[name] = builder(df); added.append(name)
                except Exception:
                    pass
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        df = self.get_data()
        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df
        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = PredictiveMaintenanceDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

if __name__ == "__main__":
    dataset = PredictiveMaintenanceDataset()
    df = dataset.get_data()
    print(f"Loaded PredictiveMaintenanceDataset: {df.shape}")
    print(df.head())

    # Expanded
    df_exp = df.copy(deep=True)
    df_exp, added = PredictiveMaintenanceDataset.expand_features_on_dataframe(df_exp)
    try:
        df_exp.attrs["agent_expansion_applied"] = True
        df_exp.attrs["agent_provider"] = "GPT5"
        df_exp.attrs["agent_expanded_features"] = list(added)
    except Exception:
        pass

    # 5-fold CatBoost AUC comparison
    try:
        from sklearn.model_selection import StratifiedKFold
        from sklearn.metrics import roc_auc_score
        from catboost import CatBoostClassifier
        from app.seed_data.Generative.shared.stages.transforms.expanders.AgentFeatureExpander import AgentFeatureExpander

        X_base = df.drop(columns=["target"]); y = df["target"]
        X_exp = df_exp.drop(columns=["target"])
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        aucs_base = []; aucs_exp = []
        for tr, te in skf.split(X_base, y):
            Xtr, Xte, ytr, yte = X_base.iloc[tr], X_base.iloc[te], y.iloc[tr], y.iloc[te]
            m = CatBoostClassifier(verbose=False, depth=6, learning_rate=0.1, iterations=300, loss_function="Logloss", eval_metric="AUC", random_seed=42)
            m.fit(Xtr, ytr); p = m.predict_proba(Xte)[:, 1]; aucs_base.append(roc_auc_score(yte, p))

            Xtr2, Xte2 = X_exp.iloc[tr].copy(), X_exp.iloc[te].copy()
            expander = AgentFeatureExpander(prefer_dataset="PredictiveMaintenanceDataset")
            Xtr2 = expander.fit_transform(Xtr2, ytr); Xte2 = expander.transform(Xte2)
            m2 = CatBoostClassifier(verbose=False, depth=6, learning_rate=0.1, iterations=300, loss_function="Logloss", eval_metric="AUC", random_seed=42)
            m2.fit(Xtr2, ytr); p2 = m2.predict_proba(Xte2)[:, 1]; aucs_exp.append(roc_auc_score(yte, p2))

        import numpy as _np
        print({
            "baseline_auc_mean": float(_np.mean(aucs_base)),
            "baseline_auc_std": float(_np.std(aucs_base)),
            "expanded_auc_mean": float(_np.mean(aucs_exp)),
            "expanded_auc_std": float(_np.std(aucs_exp)),
            "folds": len(aucs_base),
            "added_features": len(added),
        })
    except Exception as e:
        print(f"[PredictiveMaintenanceDataset] CV run skipped due to: {e}")