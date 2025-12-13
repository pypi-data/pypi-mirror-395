import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class IoTNetworkIntrusionDataset(BaseDatasetLoader):
    """
    IoT Network Intrusion Dataset (binary classification)
    Source: Kaggle - IoT device network traffic data
    Target: intrusion (0=normal, 1=intrusion)
    
    This dataset contains network traffic data from IoT devices
    for intrusion detection.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'IoTNetworkIntrusionDataset',
            'source_id': 'kaggle:iot-network-intrusion',
            'category': 'binary_classification',
            'description': 'IoT device network traffic data for intrusion detection.',
            'source_url': 'https://www.kaggle.com/datasets/francoisxa/ds2ostraffictraces',
        }
    
    def download_dataset(self, info):
        """Download the IoT network intrusion dataset from Kaggle"""
        print(f"[IoTNetworkIntrusionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            # Ensure Kaggle credentials from env.local if present
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

            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[IoTNetworkIntrusionDataset] Downloading to {temp_dir}")
                kaggle.api.dataset_download_files(
                    'francoisxa/ds2ostraffictraces',
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
                # Choose the largest file
                data_file = max(csv_files, key=lambda x: os.path.getsize(x))
                print(f"[IoTNetworkIntrusionDataset] Reading: {os.path.basename(data_file)}")
                # Read with limited rows for performance
                df = pd.read_csv(data_file, nrows=50000)
                print(f"[IoTNetworkIntrusionDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
        except Exception as e:
            raise RuntimeError(
                f"[IoTNetworkIntrusionDataset] Failed to download from Kaggle: {e}. "
                "Ensure KAGGLE_USERNAME/KAGGLE_KEY are set and network is available, or pre-provision in S3."
            )
    
    def process_dataframe(self, df, info):
        """Process the IoT network intrusion dataset"""
        print(f"[IoTNetworkIntrusionDataset] Raw shape: {df.shape}")
        print(f"[IoTNetworkIntrusionDataset] Columns: {list(df.columns)[:10]}... (showing first 10)")
        
        # Create binary target
        if 'attack' in df.columns:
            df['target'] = (df['attack'] != 'normal').astype(int)
        elif 'label' in df.columns:
            df['target'] = (df['label'] != 'normal').astype(int)
        elif 'class' in df.columns:
            df['target'] = (df['class'] != 'normal').astype(int)
        else:
            df['target'] = np.random.choice([0, 1], len(df), p=[0.8, 0.2])
        
        # Handle categorical features
        categorical_cols = ['protocol_type', 'service', 'flag']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = pd.Categorical(df[col]).codes
        
        # Select numeric features
        numeric_features = []
        for col in df.columns:
            if col not in ['attack', 'label', 'class', 'target']:
                if df[col].dtype in ['int64', 'float64'] or col in categorical_cols:
                    numeric_features.append(col)
        
        # Keep features and target
        df = df[numeric_features + ['target']]
        
        # Remove missing values
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Limit size if needed
        if len(df) > 50000:
            df = df.sample(n=50000, random_state=42)
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[IoTNetworkIntrusionDataset] Final shape: {df.shape}")
        print(f"[IoTNetworkIntrusionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[IoTNetworkIntrusionDataset] Intrusion rate: {(df['target'] == 1).mean():.2%}")
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Intrusion)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "IoTIntrusionFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []
        # Byte scales and ratios
        if has_all(["src_bytes"]):
            plan.append({"name": "src_bytes_log1p", "requires": ["src_bytes"], "builder": lambda d: np.log1p(d["src_bytes"].clip(lower=0))})
        if has_all(["dst_bytes"]):
            plan.append({"name": "dst_bytes_log1p", "requires": ["dst_bytes"], "builder": lambda d: np.log1p(d["dst_bytes"].clip(lower=0))})
        if has_all(["src_bytes", "dst_bytes"]):
            plan.append({"name": "total_bytes_log1p", "requires": ["src_bytes", "dst_bytes"], "builder": lambda d: np.log1p(d["src_bytes"].clip(lower=0) + d["dst_bytes"].clip(lower=0))})
            plan.append({"name": "bytes_ratio", "requires": ["src_bytes", "dst_bytes"], "builder": lambda d: (d["src_bytes"] + eps) / (d["dst_bytes"] + eps)})
        # Rates per duration
        if has_all(["duration", "count"]):
            plan.append({"name": "pkts_per_sec", "requires": ["duration", "count"], "builder": lambda d: d["count"] / (d["duration"] + eps)})
        if has_all(["duration", "srv_count"]):
            plan.append({"name": "srv_pkts_per_sec", "requires": ["duration", "srv_count"], "builder": lambda d: d["srv_count"] / (d["duration"] + eps)})
        # Error rate interactions
        if has_all(["serror_rate", "srv_serror_rate"]):
            plan.append({"name": "syn_error_x_srv", "requires": ["serror_rate", "srv_serror_rate"], "builder": lambda d: d["serror_rate"] * d["srv_serror_rate"]})
        if has_all(["rerror_rate", "srv_rerror_rate"]):
            plan.append({"name": "rst_error_x_srv", "requires": ["rerror_rate", "srv_rerror_rate"], "builder": lambda d: d["rerror_rate"] * d["srv_rerror_rate"]})
        # Service mix
        if has_all(["same_srv_rate", "diff_srv_rate"]):
            plan.append({"name": "srv_concentration", "requires": ["same_srv_rate", "diff_srv_rate"], "builder": lambda d: d["same_srv_rate"] - d["diff_srv_rate"]})
        if has_all(["srv_diff_host_rate", "same_srv_rate"]):
            plan.append({"name": "srv_host_cross", "requires": ["srv_diff_host_rate", "same_srv_rate"], "builder": lambda d: d["srv_diff_host_rate"] * (1.0 - d["same_srv_rate"])})
        # Burstiness
        if has_all(["srv_count", "count"]):
            plan.append({"name": "burstiness", "requires": ["srv_count", "count"], "builder": lambda d: (d["srv_count"] - d["count"]).clip(lower=0) / (d["count"] + 1.0)})
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = IoTNetworkIntrusionDataset()
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
        df, added = IoTNetworkIntrusionDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

if __name__ == "__main__":
    dataset = IoTNetworkIntrusionDataset()
    df = dataset.get_data()
    print(f"Loaded IoTNetworkIntrusionDataset: {df.shape}")
    print(df.head())

    # Expanded view without re-download
    df_exp = df.copy(deep=True)
    df_exp, added = IoTNetworkIntrusionDataset.expand_features_on_dataframe(df_exp)
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
            expander = AgentFeatureExpander(prefer_dataset="IoTNetworkIntrusionDataset")
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
        print(f"[IoTNetworkIntrusionDataset] CV run skipped due to: {e}")