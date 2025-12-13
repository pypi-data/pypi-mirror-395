import io
import zipfile
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class BankMarketingDataset(BaseDatasetLoader):
    """
    UCI Bank Marketing dataset.
    Binary classification: subscribed to deposit (1) vs not (0)
    45,211 instances, 16 features (mixed types)
    Source: UCI repository (bank.zip)
    """

    def get_dataset_info(self):
        return {
            "name": "BankMarketingDataset",
            "source_id": "uci:bank_marketing_zip",
            "category": "binary_classification",
            "description": "UCI Bank Marketing dataset (bank.zip).",
        }

    def download_dataset(self, info):
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip"
        session = requests.Session()
        session.trust_env = False
        r = session.get(url, timeout=60)
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code} while downloading {url}")
        zf = zipfile.ZipFile(io.BytesIO(r.content))
        # Prefer the full dataset with separators ; and header in bank-full.csv
        with zf.open("bank-full.csv") as f:
            df = pd.read_csv(f, sep=";")
        return df

    def process_dataframe(self, df: pd.DataFrame, info):
        # Map target 'y' to binary
        label_col = "y"
        if label_col not in df.columns:
            raise ValueError("bank dataset missing 'y' column")
        df["target"] = df[label_col].astype(str).str.lower().map({"yes": 1, "no": 0}).astype(int)
        df = df.drop(columns=[label_col])
        # Ensure target last
        cols = [c for c in df.columns if c != "target"] + ["target"]
        df = df[cols]
        return df

import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BankMarketingDataset(BaseDatasetLoader):
    """UCI Bank Marketing (Direct Marketing Campaign) dataset – binary classification.

    Dataset summary
    ----------------
    • 41,188 contacts with structured socio-economic information collected from a Portuguese banking institution.
    • Goal: predict whether the client subscribed to a term deposit (`y` = "yes"/"no").
    • 20 input features (numeric + categorical) + binary target.

    References
    ----------
    Original UCI page: https://archive.ics.uci.edu/ml/datasets/Bank+Marketing
    Direct CSV link used here (semicolon-delimited, includes header):
    https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional/bank-additional-full.csv
    """

    # ------------------------------------------------------------------
    # Required hooks
    # ------------------------------------------------------------------
    def get_dataset_info(self):
        """Return metadata used by the loader framework"""
        return {
            "name": "BankMarketingDataset",
            "source_id": "uci:bank_marketing_additional_full",
            "source_url": "uci_repo",  # Special marker for UCI repo
            "category": "binary_classification",
            "description": (
                "Bank marketing dataset (41 188 contacts) – predict subscription to term deposit "
                "based on socio-economic features."),
            "target_column": "y",
        }

    def download_dataset(self, info):
        """Download the CSV file using ucimlrepo or fallback URLs"""
        dataset_name = info["name"]
        
        # Try ucimlrepo first
        try:
            print(f"[{dataset_name}] Attempting to fetch from UCI repository using ucimlrepo...")
            try:
                from ucimlrepo import fetch_ucirepo
                bank_marketing = fetch_ucirepo(id=222)  # Bank Marketing dataset
                X = bank_marketing.data.features
                y = bank_marketing.data.targets
                df = pd.concat([X, y], axis=1)
                import io
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';')  # Use semicolon separator
                print(f"[{dataset_name}] Successfully downloaded from UCI via ucimlrepo")
                return csv_buffer.getvalue().encode('utf-8')
            except ImportError:
                print(f"[{dataset_name}] ucimlrepo not available, trying direct URLs...")
        except Exception as e:
            print(f"[{dataset_name}] UCI repository failed: {e}")
        
        # Fallback URLs if ucimlrepo fails
        fallback_urls = [
            "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/bank-additional-full.csv",
            "https://raw.githubusercontent.com/madmashup/targeted-marketing-predictive-engine/master/banking.csv"
        ]
        
        for i, test_url in enumerate(fallback_urls):
            try:
                print(f"[{dataset_name}] Trying URL {i+1}: {test_url}")
                r = requests.get(test_url, timeout=60)
                print(f"[{dataset_name}] HTTP {r.status_code}")
                if r.status_code == 200:
                    if len(r.content) < 50000:  # expect > 4 MB
                        preview = r.content[:500].decode("utf-8", errors="replace")
                        print(f"[{dataset_name}] Warning: file unusually small. Preview:\n{preview}")
                    print(f"[{dataset_name}] Successfully downloaded from URL {i+1}")
                    return r.content
            except Exception as e:
                print(f"[{dataset_name}] URL {i+1} failed: {e}")
                continue
        
        raise RuntimeError(f"[{dataset_name}] All download URLs failed")

    def process_dataframe(self, df, info):
        """Clean and transform the raw DataFrame.

        Key steps:
        1. Ensure columns are parsed correctly (semicolon delimiter and header).
        2. Convert the `y` column (yes/no) to integer `target` (1/0).
        3. Perform basic NA handling and shuffle.
        """
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")
        
        # Check for different possible target column names
        possible_targets = ["y", "target", "subscription", "deposit"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        print(f"[{dataset_name}] Target column '{actual_target}' unique values: {df[actual_target].unique()}")

        # Target conversion: "yes" -> 1, "no" -> 0
        target_mapping = {"yes": 1, "no": 0, "y": 1, "n": 0, 1: 1, 0: 0}
        df["target"] = df[actual_target].map(target_mapping)
        
        # Handle any unmapped values
        if df["target"].isna().any():
            unmapped_values = df[df["target"].isna()][actual_target].unique()
            print(f"[{dataset_name}] Warning: Found unmapped values in target column: {unmapped_values}")
            
            # Try additional mappings
            additional_mapping = {}
            for val in unmapped_values:
                if str(val).lower() in ["yes", "y", "true", "1"]:
                    additional_mapping[val] = 1
                elif str(val).lower() in ["no", "n", "false", "0"]:
                    additional_mapping[val] = 0
                else:
                    additional_mapping[val] = 0  # Default to 0
            
            # Apply additional mapping
            for original, mapped in additional_mapping.items():
                df.loc[df[actual_target] == original, "target"] = mapped
            
            # Fill any remaining NAs with 0
            df["target"] = df["target"].fillna(0)

        df["target"] = df["target"].astype(int)
        
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)

        # Handle categorical variables with encoding
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        categorical_cols = [col for col in categorical_cols if col != "target"]
        
        print(f"[{dataset_name}] Encoding categorical columns: {categorical_cols}")
        
        for col in categorical_cols:
            if col in df.columns:
                # Use label encoding for all categorical variables
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))

        # Convert all feature columns to numeric, coercing errors
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values 
        before_dropna = len(df)
        df.dropna(inplace=True)
        if before_dropna > len(df):
            print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")

        # Deduplicate
        before_dedup = len(df)
        df.drop_duplicates(inplace=True)
        if len(df) < before_dedup:
            print(f"[{dataset_name}] Removed {before_dedup - len(df)} duplicate rows.")

        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Bank Marketing)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "BankMarketingFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Duration transforms
        if 'duration' in df.columns:
            plan.append({"name": "duration_log1p", "requires": ["duration"], "builder": lambda d: np.log1p(d["duration"].clip(lower=0))})
            plan.append({"name": "duration_bin", "requires": ["duration"], "builder": lambda d: pd.qcut(d["duration"], q=10, duplicates='drop').cat.codes})

        # Contact/campaign dynamics
        if 'campaign' in df.columns:
            plan.append({"name": "campaign_log1p", "requires": ["campaign"], "builder": lambda d: np.log1p(d["campaign"].clip(lower=0))})
        if has_all(["campaign", "previous"]):
            plan.append({"name": "campaign_per_previous", "requires": ["campaign", "previous"], "builder": lambda d: d["campaign"]/(d["previous"]+1.0)})

        # pdays semantics
        if 'pdays' in df.columns:
            plan.append({"name": "pdays_is_missing_999", "requires": ["pdays"], "builder": lambda d: (d["pdays"] == 999).astype(int)})
            plan.append({"name": "pdays_recent", "requires": ["pdays"], "builder": lambda d: (d["pdays"].replace(999, np.nan) < 5).fillna(0).astype(int)})

        # Contact type flags
        if 'contact' in df.columns:
            plan.append({"name": "contact_is_cellular", "requires": ["contact"], "builder": lambda d: (d["contact"] == d["contact"].max()).astype(int)})

        # Socio-economic: age bands and interactions
        if 'age' in df.columns:
            plan.append({"name": "age_bin", "requires": ["age"], "builder": lambda d: pd.qcut(d["age"], q=10, duplicates='drop').cat.codes})
            plan.append({"name": "age_senior", "requires": ["age"], "builder": lambda d: (d["age"] >= 60).astype(int)})
        if has_all(["age", "campaign"]):
            plan.append({"name": "age_x_campaign", "requires": ["age", "campaign"], "builder": lambda d: d["age"] * d["campaign"]})

        # Macro indicators interactions
        if has_all(["euribor3m", "emp.var.rate"]):
            plan.append({"name": "euribor_x_empvar", "requires": ["euribor3m", "emp.var.rate"], "builder": lambda d: d["euribor3m"] * d["emp.var.rate"]})
        if has_all(["cons.price.idx", "cons.conf.idx"]):
            plan.append({"name": "price_x_conf", "requires": ["cons.price.idx", "cons.conf.idx"], "builder": lambda d: d["cons.price.idx"] * d["cons.conf.idx"]})

        # Seasonality from month/day_of_week if present (encoded numerically in process step)
        if 'month' in df.columns:
            plan.append({"name": "is_summer", "requires": ["month"], "builder": lambda d: d["month"].isin([5,6,7,8]).astype(int)})
        if 'day_of_week' in df.columns:
            plan.append({"name": "is_weekend", "requires": ["day_of_week"], "builder": lambda d: d["day_of_week"].isin([5,6]).astype(int)})

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = BankMarketingDataset()
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
        df, added = BankMarketingDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

    # Quick CV block (CatBoost AUC baseline vs expanded)
    # Note: This runs only under __main__

# For quick manual testing
if __name__ == "__main__":
    ds = BankMarketingDataset()
    frame = ds.get_data()
    print(frame.head())

    # Expanded
    df_exp = frame.copy(deep=True)
    df_exp, added = BankMarketingDataset.expand_features_on_dataframe(df_exp)
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

        X_base = frame.drop(columns=["target"]); y = frame["target"]
        X_exp = df_exp.drop(columns=["target"])
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        aucs_base = []; aucs_exp = []
        for tr, te in skf.split(X_base, y):
            Xtr, Xte, ytr, yte = X_base.iloc[tr], X_base.iloc[te], y.iloc[tr], y.iloc[te]
            m = CatBoostClassifier(verbose=False, depth=6, learning_rate=0.1, iterations=300, loss_function="Logloss", eval_metric="AUC", random_seed=42)
            m.fit(Xtr, ytr); p = m.predict_proba(Xte)[:, 1]; aucs_base.append(roc_auc_score(yte, p))

            Xtr2, Xte2 = X_exp.iloc[tr].copy(), X_exp.iloc[te].copy()
            expander = AgentFeatureExpander(prefer_dataset="BankMarketingDataset")
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
        print(f"[BankMarketingDataset] CV run skipped due to: {e}")