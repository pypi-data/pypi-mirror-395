import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class FraudTransactionDetectionDataset(BaseDatasetLoader):
    """
    Fraud Transaction Detection Dataset (binary classification)
    Source: Kaggle - Credit Card Fraud Detection
    Target: is_fraud (0=legitimate, 1=fraud)
    
    This dataset contains transaction data for detecting fraudulent transactions.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'FraudTransactionDetectionDataset',
            'source_id': 'kaggle:fraud-transaction-detection',
            'category': 'binary_classification',
            'description': 'Fraud detection from transaction patterns and features.',
            'source_url': 'https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud',
        }
    
    def download_dataset(self, info):
        """Download the fraud detection dataset from Kaggle"""
        print(f"[FraudTransactionDetectionDataset] Downloading from Kaggle...")
        
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
                print(f"[FraudTransactionDetectionDataset] Downloading to {temp_dir}")
                kaggle.api.dataset_download_files(
                    'mlg-ulb/creditcardfraud',
                    path=temp_dir,
                    unzip=True
                )
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                data_file = csv_files[0]
                print(f"[FraudTransactionDetectionDataset] Reading: {os.path.basename(data_file)}")
                df = pd.read_csv(data_file)
                # Map target and balance modestly for tractable CV
                if 'Class' in df.columns:
                    df = df.rename(columns={'Class': 'target'})
                # Subsample majority to 10:1 ratio to ease CV runtime
                fraud_df = df[df['target'] == 1]
                normal_df = df[df['target'] == 0].sample(n=min(len(fraud_df) * 10, len(df[df['target']==0])), random_state=42)
                df = pd.concat([fraud_df, normal_df])
                csv_data = df.to_csv(index=False)
                print(f"[FraudTransactionDetectionDataset] Loaded {df.shape[0]} rows")
                return csv_data.encode('utf-8')
        except Exception as e:
            # Strict: fail so tests do not silently use synthetic data
            raise RuntimeError(
                f"[FraudTransactionDetectionDataset] Failed to download from Kaggle: {e}. "
                "Ensure KAGGLE_USERNAME/KAGGLE_KEY are set and network is available, or pre-provision in S3."
            )
    
    def process_dataframe(self, df, info):
        """Process the fraud detection dataset"""
        print(f"[FraudTransactionDetectionDataset] Raw shape: {df.shape}")
        print(f"[FraudTransactionDetectionDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find fraud target column
        target_col = None
        for col in ['class', 'fraud', 'is_fraud', 'label', 'target']:
            if col in df.columns or col.upper() in df.columns:
                target_col = col if col in df.columns else col.upper()
                break
        
        if target_col and target_col != 'target':
            df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            raise ValueError("[FraudTransactionDetectionDataset] No target column present in source data")
        
        # Remove non-numeric columns except Time (convert it)
        if 'Time' in df.columns:
            df['time_hours'] = df['Time'] / 3600.0  # Convert seconds to hours
            df = df.drop('Time', axis=1)
        
        text_cols = ['id', 'transaction_id', 'customer_id', 'merchant_id', 'card_number']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().sum() > len(df) * 0.5:
                    feature_cols.append(col)
        
        # Limit features
        if len(feature_cols) > 50:
            # For PCA features, keep all V columns
            v_cols = [col for col in feature_cols if col.startswith('V')]
            other_cols = [col for col in feature_cols if not col.startswith('V')]
            
            if len(v_cols) > 0:
                # Keep all V columns and some others
                feature_cols = v_cols + other_cols[:50-len(v_cols)]
            else:
                # Prioritize transaction features
                priority_features = ['amount', 'time', 'distance', 'velocity', 'risk', 'score']
                
                selected_features = []
                for feat in priority_features:
                    for col in feature_cols:
                        if feat in col.lower() and col not in selected_features:
                            selected_features.append(col)
                
                # Add remaining
                for col in feature_cols:
                    if col not in selected_features and len(selected_features) < 50:
                        selected_features.append(col)
                
                feature_cols = selected_features[:50]
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Do not add engineered features here; keep baseline minimal.

        # Handle missing values
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Ensure all numeric
        df = df.dropna()
        
        # Ensure binary target
        df['target'] = df['target'].astype(int)
        df = df[df['target'].isin([0, 1])]
        
        # Check class balance
        target_counts = df['target'].value_counts()
        if len(target_counts) == 2:
            fraud_rate = target_counts[1] / len(df)
            if fraud_rate < 0.001 or fraud_rate > 0.5:
                # Rebalance to ~2% fraud rate
                n_fraud = target_counts[1]
                n_normal = min(n_fraud * 50, target_counts[0])
                df_fraud = df[df['target'] == 1]
                df_normal = df[df['target'] == 0].sample(n=n_normal, random_state=42)
                df = pd.concat([df_fraud, df_normal])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[FraudTransactionDetectionDataset] Final shape: {df.shape}")
        print(f"[FraudTransactionDetectionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[FraudTransactionDetectionDataset] Fraud rate: {(df['target'] == 1).mean():.2%}")
        
        # Attach lightweight attrs to help downstream expansion
        try:
            df.attrs["dataset_source"] = "FraudTransactionDetectionDataset"
            df.attrs["raw_feature_names"] = [c for c in df.columns if c != 'target']
            df.attrs["feature_expander"] = ("FraudTransactionDetectionDataset", "expand_features_on_dataframe")
        except Exception:
            pass
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Fraud)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "FraudFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []
        # Amount transforms and ratios vs robust PCA magnitude
        if 'Amount' in df.columns:
            plan.append({"name": "amount_log1p", "requires": ["Amount"], "builder": lambda d: np.log1p(d["Amount"].clip(lower=0))})
        # PCA magnitude/outlier scores
        v_cols = [c for c in df.columns if c.startswith('V')]
        if v_cols:
            plan.append({"name": "pca_abs_sum", "requires": v_cols, "builder": lambda d: d[v_cols].abs().sum(axis=1)})
            use = v_cols[:10] if len(v_cols) >= 10 else v_cols
            plan.append({"name": "pca_topk_l2", "requires": use, "builder": lambda d: np.sqrt((d[use]**2).sum(axis=1))})
            # Robust variants using trimmed sums to reduce noise
            plan.append({"name": "pca_abs_sum_trim80", "requires": v_cols, "builder": lambda d: d[v_cols].abs().apply(lambda r: r.sort_values().iloc[int(0.2*len(r)) : int(0.8*len(r))].sum(), axis=1)})
            # Top-3 absolute components and their indices as signals
            def top3_abs(d):
                vals = d[v_cols].abs()
                part = np.partition(vals.values, -3, axis=1)[:, -3:]
                return pd.Series(part.sum(axis=1), index=d.index)
            plan.append({"name": "pca_top3_abs_sum", "requires": v_cols, "builder": top3_abs})
        # Time-of-day cyclic features from time_hours if available
        if has_all(["time_hours"]) and ("time_sin" not in df.columns or "time_cos" not in df.columns):
            plan.append({"name": "time_sin", "requires": ["time_hours"], "builder": lambda d: np.sin(2*np.pi*(d["time_hours"]%24)/24.0)})
            plan.append({"name": "time_cos", "requires": ["time_hours"], "builder": lambda d: np.cos(2*np.pi*(d["time_hours"]%24)/24.0)})
            # Night/weekend flags (if day-of-week present otherwise derive from hours mod 24)
            plan.append({"name": "is_night", "requires": ["time_hours"], "builder": lambda d: ((d["time_hours"]%24 < 6) | (d["time_hours"]%24 > 22)).astype(int)})
        
        # Amount normalization by PCA magnitude
        if 'Amount' in df.columns and ("pca_abs_sum" in df.columns or v_cols):
            def amount_over_pca(d):
                base = d["pca_abs_sum"] if "pca_abs_sum" in d.columns else d[v_cols].abs().sum(axis=1)
                return np.log1p(d["Amount"].clip(lower=0)) / (np.log1p(base) + eps)
            plan.append({"name": "amount_over_pca_sum", "requires": ["Amount"], "builder": amount_over_pca})
        # Interaction: amount with PCA magnitude
        if has_all(["Amount"]) and ("pca_abs_sum" in df.columns or v_cols):
            def amount_pca(d):
                pca_sum = d["pca_abs_sum"] if "pca_abs_sum" in d.columns else d[v_cols].abs().sum(axis=1)
                return np.log1p(d["Amount"].clip(lower=0)) * np.log1p(pca_sum)
            plan.append({"name": "amount_pca_interaction", "requires": ["Amount"], "builder": amount_pca})
        
        # Pairwise interactions among a few high-signal PCA components
        if v_cols:
            use2 = v_cols[:5]
            for i in range(len(use2)):
                for j in range(i+1, len(use2)):
                    c1, c2 = use2[i], use2[j]
                    name = f"{c1}_x_{c2}"
                    plan.append({"name": name, "requires": [c1, c2], "builder": lambda d, a=c1, b=c2: d[a]*d[b]})
        
        # Quantile flags for extreme PCA magnitude and amount
        if v_cols:
            plan.append({"name": "pca_abs_sum_q99", "requires": v_cols, "builder": lambda d: (d[v_cols].abs().sum(axis=1) > d[v_cols].abs().sum(axis=1).quantile(0.99)).astype(int)})
        if 'Amount' in df.columns:
            plan.append({"name": "amount_q99", "requires": ["Amount"], "builder": lambda d: (d["Amount"] > d["Amount"].quantile(0.99)).astype(int)})
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = FraudTransactionDetectionDataset()
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
        df, added = FraudTransactionDetectionDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

if __name__ == "__main__":
    dataset = FraudTransactionDetectionDataset()
    df = dataset.get_data()
    print(f"Loaded FraudTransactionDetectionDataset: {df.shape}")
    print(df.head())

    # Expanded view without re-download
    df_exp = df.copy(deep=True)
    df_exp, added = FraudTransactionDetectionDataset.expand_features_on_dataframe(df_exp)
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
            expander = AgentFeatureExpander(prefer_dataset="FraudTransactionDetectionDataset")
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
        print(f"[FraudTransactionDetectionDataset] CV run skipped due to: {e}")