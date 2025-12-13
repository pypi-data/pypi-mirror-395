import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class HospitalReadmissionsDataset(BaseDatasetLoader):
    """
    Hospital Readmissions Dataset (binary classification)
    Source: Kaggle - Hospital readmissions data
    Target: readmitted (0=not readmitted, 1=readmitted within 30 days)
    
    This dataset contains hospital discharge data for predicting
    30-day readmission risk.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'HospitalReadmissionsDataset',
            'source_id': 'kaggle:hospital-readmissions',
            'category': 'binary_classification',
            'description': 'Hospital readmissions prediction dataset.',
            'source_url': 'https://www.kaggle.com/datasets/dubradave/hospital-readmissions',
        }
    
    def download_dataset(self, info):
        """Download the hospital readmissions dataset from Kaggle"""
        print(f"[HospitalReadmissionsDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            # Ensure Kaggle credentials are available from environment
            # Supports either ~/.kaggle/kaggle.json or env vars set via env.local
            import os as _os
            try:
                from decouple import config as _config  # type: ignore
            except Exception:
                def _config(key, default=None):
                    return _os.getenv(key, default)
            if _config('KAGGLE_USERNAME') and not _os.getenv('KAGGLE_USERNAME'):
                _os.environ['KAGGLE_USERNAME'] = _config('KAGGLE_USERNAME')
            if _config('KAGGLE_KEY') and not _os.getenv('KAGGLE_KEY'):
                _os.environ['KAGGLE_KEY'] = _config('KAGGLE_KEY')
            try:
                kaggle.api.authenticate()
            except Exception:
                # authenticate() will fail if relying solely on env vars but it is generally safe to proceed
                pass
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[HospitalReadmissionsDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'dubradave/hospital-readmissions',
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
                print(f"[HospitalReadmissionsDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file)
                print(f"[HospitalReadmissionsDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            # Strict: no synthetic fallback permitted — fail fast so tests and callers don't get a fake-easy dataset
            raise RuntimeError(
                f"[HospitalReadmissionsDataset] Failed to download dataset from Kaggle: {e}. "
                "Ensure KAGGLE_USERNAME/KAGGLE_KEY are set (env.local) and network is available, or "
                "pre-provision the dataset via admin APIs so it is available in S3."
            )
    
    def process_dataframe(self, df, info):
        """Process the hospital readmissions dataset"""
        print(f"[HospitalReadmissionsDataset] Raw shape: {df.shape}")
        print(f"[HospitalReadmissionsDataset] Columns: {list(df.columns)[:10]}... (showing first 10)")
        
        # Create binary target
        if 'readmitted' in df.columns:
            # Map common encodings to binary: yes/<30 → 1, otherwise 0
            vals = df['readmitted'].astype(str).str.strip().str.lower()
            df['target'] = vals.isin({'<30', 'yes', 'true', '1', 'y'}).astype(int)
            # Drop original label to avoid leakage
            df = df.drop(columns=['readmitted'])
        else:
            # Strictly avoid synthetic target creation when no label exists
            # Ensure callers provision a valid dataset
            raise ValueError("[HospitalReadmissionsDataset] Expected 'readmitted' column not found in source data")
        
        # Select numeric features
        numeric_cols = ['time_in_hospital', 'n_lab_procedures', 'n_procedures', 
                       'n_medications', 'n_outpatient', 'n_inpatient', 'n_emergency']
        
        # Keep available numeric features
        available_numeric = [col for col in numeric_cols if col in df.columns]
        
        # Handle categorical features - convert to numeric codes
        categorical_cols = ['medical_specialty', 'glucose_test', 'A1Ctest', 'change', 'diabetes_med']
        for col in categorical_cols:
            if col in df.columns:
                # Convert to categorical and then to numeric codes
                df[col] = pd.Categorical(df[col]).codes
                available_numeric.append(col)
        
        # Handle diagnosis codes
        diag_cols = ['diag_1', 'diag_2', 'diag_3']
        for col in diag_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Fill missing values with 0
                df[col] = df[col].fillna(0)
                available_numeric.append(col)
        
        # Select features and target
        df = df[available_numeric + ['target']]
        
        # Remove missing values
        df = df.dropna()
        
        # Ensure all numeric and convert int8 to int64
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Convert int8 to int64
            if df[col].dtype == 'int8':
                df[col] = df[col].astype('int64')
        
        df = df.dropna()
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[HospitalReadmissionsDataset] Final shape: {df.shape}")
        print(f"[HospitalReadmissionsDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[HospitalReadmissionsDataset] Readmission rate: {(df['target'] == 1).mean():.2%}")
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Healthcare)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "HospitalReadmitFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)

        plan = []

        # Visits aggregate and mix ratios
        if has_all(["n_outpatient", "n_inpatient", "n_emergency"]):
            def total_visits(d):
                return d["n_outpatient"] + d["n_inpatient"] + d["n_emergency"]
            plan.append({"name": "total_visits", "requires": ["n_outpatient", "n_inpatient", "n_emergency"], "builder": total_visits})
            plan.append({"name": "inpatient_ratio", "requires": ["n_inpatient"], "builder": lambda d: d["n_inpatient"] / (total_visits(d) + eps)})
            plan.append({"name": "emergency_ratio", "requires": ["n_emergency"], "builder": lambda d: d["n_emergency"] / (total_visits(d) + eps)})
            plan.append({"name": "outpatient_ratio", "requires": ["n_outpatient"], "builder": lambda d: d["n_outpatient"] / (total_visits(d) + eps)})

        # Utilization per day proxies
        if has_all(["time_in_hospital", "n_lab_procedures"]):
            plan.append({"name": "labs_per_day", "requires": ["time_in_hospital", "n_lab_procedures"], "builder": lambda d: d["n_lab_procedures"] / (d["time_in_hospital"] + eps)})
        if has_all(["time_in_hospital", "n_medications"]):
            plan.append({"name": "meds_per_day", "requires": ["time_in_hospital", "n_medications"], "builder": lambda d: d["n_medications"] / (d["time_in_hospital"] + eps)})
        if has_all(["time_in_hospital", "n_procedures"]):
            plan.append({"name": "procedures_per_day", "requires": ["time_in_hospital", "n_procedures"], "builder": lambda d: d["n_procedures"] / (d["time_in_hospital"] + eps)})
        if has_all(["time_in_hospital", "n_lab_procedures", "n_procedures", "n_medications"]):
            plan.append({
                "name": "resource_intensity",
                "requires": ["time_in_hospital", "n_lab_procedures", "n_procedures", "n_medications"],
                "builder": lambda d: (d["n_lab_procedures"] + 3 * d["n_procedures"] + 0.5 * d["n_medications"]) / (d["time_in_hospital"] + eps),
            })

        # Diagnosis aggregates
        diag_cols = [c for c in ["diag_1", "diag_2", "diag_3"] if c in df.columns]
        if diag_cols:
            plan.append({"name": "diag_max", "requires": diag_cols, "builder": lambda d: d[diag_cols].max(axis=1)})
            plan.append({"name": "diag_min", "requires": diag_cols, "builder": lambda d: d[diag_cols].min(axis=1)})
            if len(diag_cols) > 1:
                plan.append({"name": "diag_mean", "requires": diag_cols, "builder": lambda d: d[diag_cols].mean(axis=1)})

        # Binary indicators from categorical strings
        if "change" in df.columns:
            plan.append({"name": "change_yes", "requires": ["change"], "builder": lambda d: (d["change"].astype(str) == "yes").astype(int)})
        if "diabetes_med" in df.columns:
            plan.append({"name": "diabetes_med_yes", "requires": ["diabetes_med"], "builder": lambda d: (d["diabetes_med"].astype(str) == "yes").astype(int)})
        if "glucose_test" in df.columns:
            plan.append({"name": "glucose_abnormal", "requires": ["glucose_test"], "builder": lambda d: (d["glucose_test"].astype(str) == "abnormal").astype(int)})
        if "A1Ctest" in df.columns:
            plan.append({"name": "a1c_abnormal", "requires": ["A1Ctest"], "builder": lambda d: (d["A1Ctest"].astype(str) == "abnormal").astype(int)})

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = HospitalReadmissionsDataset()
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
                except Exception:
                    pass
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        df = self.get_data()
        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df
        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = self.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

if __name__ == "__main__":
    dataset = HospitalReadmissionsDataset()
    df = dataset.get_data()
    print(f"Loaded HospitalReadmissionsDataset: {df.shape}")
    print(df.head())

    # Expanded view without re-download
    df_exp = df.copy(deep=True)
    df_exp, added = HospitalReadmissionsDataset.expand_features_on_dataframe(df_exp)
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

            model = CatBoostClassifier(verbose=False, depth=6, learning_rate=0.1, iterations=300, loss_function="Logloss", eval_metric="AUC", random_seed=42)
            model.fit(Xtr, ytr)
            p = model.predict_proba(Xte)[:, 1]
            aucs_base.append(roc_auc_score(yte, p))

            # Expanded + expander
            Xtr2 = X_exp.iloc[train_idx].copy()
            Xte2 = X_exp.iloc[test_idx].copy()
            ytr2 = y.iloc[train_idx]
            yte2 = y.iloc[test_idx]

            expander = AgentFeatureExpander(prefer_dataset="HospitalReadmissionsDataset")
            Xtr2 = expander.fit_transform(Xtr2, ytr2)
            Xte2 = expander.transform(Xte2)

            model2 = CatBoostClassifier(verbose=False, depth=6, learning_rate=0.1, iterations=300, loss_function="Logloss", eval_metric="AUC", random_seed=42)
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
        print(f"[HospitalReadmissionsDataset] CV run skipped due to: {e}")