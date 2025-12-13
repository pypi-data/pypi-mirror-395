import io
import os
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import requests

try:
    from app.datasets.BaseDatasetLoader import BaseDatasetLoader
except Exception:  # pragma: no cover
    class BaseDatasetLoader:  # type: ignore
        def get_dataset_info(self):  # pragma: no cover
            raise NotImplementedError

        def download_dataset(self, info):  # pragma: no cover
            raise NotImplementedError

        def process_dataframe(self, df, info):  # pragma: no cover
            return df

        def get_data(self, refresh: bool = False):  # pragma: no cover
            info = self.get_dataset_info()
            df = self.download_dataset(info)
            return self.process_dataframe(df, info)


class SECOMDatasetLoader(BaseDatasetLoader):
    """Loader for the SECOM semiconductor dataset compatible with DOUG."""

    CACHE_ENV = "SEED_DATA_CACHE"

    def __init__(self, cache_root: Optional[str] = None):
        self._cache_root = Path(cache_root) if cache_root else None
        self._cached_df: Optional[pd.DataFrame] = None

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------
    def _cache_dir(self) -> Path:
        base = self._cache_root
        if base is None:
            env_path = os.environ.get(self.CACHE_ENV)
            base = Path(env_path) if env_path else Path(__file__).resolve().parent / "_cache"
        cache_dir = Path(base)
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def _cache_path(self) -> Path:
        return self._cache_dir() / "SECOMDataset.pkl"

    # ------------------------------------------------------------------
    # BaseDatasetLoader interface
    # ------------------------------------------------------------------
    def get_dataset_info(self):
        return {
            "name": "SECOMDataset",
            "source_id": "uci:secom_179",
            "source_url": "uci_repo",
            "category": "binary_classification",
            "description": "SECOM semiconductor: 1567x591 sensors, many NaNs, imbalanced pass/fail.",
            "target_column": "target",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        try:
            print(f"[{dataset_name}] Attempting to fetch from UCI repository using ucimlrepo...")
            from ucimlrepo import fetch_ucirepo
            secom = fetch_ucirepo(id=179)
            X = secom.data.features
            y = secom.data.targets
            if isinstance(y, pd.DataFrame):
                y = y.iloc[:, 0]
            # DIAGNOSTIC: Log original labels before mapping
            y_unique_original = y.unique()
            print(f"[{dataset_name}] [DIAGNOSTIC] Original UCI labels: {y_unique_original}, distribution: {y.value_counts().to_dict()}", flush=True)
            y_binary = (y == 1).astype(int)  # 1 = fail (positive), -1 = pass (negative)
            # DIAGNOSTIC: Log mapped labels after conversion
            y_unique_mapped = np.unique(y_binary)
            y_distribution_mapped = dict(zip(*np.unique(y_binary, return_counts=True)))
            print(f"[{dataset_name}] [DIAGNOSTIC] Mapped binary labels: {y_unique_mapped}, distribution: {y_distribution_mapped}", flush=True)
            print(f"[{dataset_name}] [DIAGNOSTIC] Label mapping: UCI -1 (pass) -> 0 (negative), UCI 1 (fail) -> 1 (positive)", flush=True)
            df = pd.concat([X, pd.Series(y_binary, name="target")], axis=1)
            print(f"[{dataset_name}] Successfully downloaded from UCI via ucimlrepo")
            print(f"[{dataset_name}] Shape: {df.shape}, Target distribution: {df['target'].value_counts().to_dict()}")
            print(f"[{dataset_name}] Missing values: {df.isnull().sum().sum()}")
            return df
        except ImportError:
            print(f"[{dataset_name}] ucimlrepo not available, trying direct download...")
        except Exception as exc:
            print(f"[{dataset_name}] UCI repository failed: {exc}")

        try:
            data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom.data"
            labels_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom_labels.data"
            print(f"[{dataset_name}] Downloading data...")
            data_response = requests.get(data_url, timeout=60)
            labels_response = requests.get(labels_url, timeout=30)
            if data_response.status_code != 200 or labels_response.status_code != 200:
                raise RuntimeError(
                    f"Failed to download: data {data_response.status_code}, labels {labels_response.status_code}"
                )
            X = pd.read_csv(io.StringIO(data_response.text), sep=" ", header=None)
            labels_df = pd.read_csv(io.StringIO(labels_response.text), sep=" ", header=None)
            y = labels_df.iloc[:, 0]
            # DIAGNOSTIC: Log original labels before mapping
            y_unique_original = y.unique()
            print(f"[{dataset_name}] [DIAGNOSTIC] Original UCI labels (direct download): {y_unique_original}, distribution: {y.value_counts().to_dict()}", flush=True)
            y_binary = (y == 1).astype(int)  # 1 = fail (positive), -1 = pass (negative)
            # DIAGNOSTIC: Log mapped labels after conversion
            y_unique_mapped = np.unique(y_binary)
            y_distribution_mapped = dict(zip(*np.unique(y_binary, return_counts=True)))
            print(f"[{dataset_name}] [DIAGNOSTIC] Mapped binary labels (direct download): {y_unique_mapped}, distribution: {y_distribution_mapped}", flush=True)
            print(f"[{dataset_name}] [DIAGNOSTIC] Label mapping: UCI -1 (pass) -> 0 (negative), UCI 1 (fail) -> 1 (positive)", flush=True)
            X.columns = [f"feature_{i}" for i in range(X.shape[1])]
            X = X.replace("NaN", np.nan)
            for col in X.columns:
                X[col] = pd.to_numeric(X[col], errors="coerce")
            df = pd.concat([X, pd.Series(y_binary, name="target", index=X.index)], axis=1)
            print(f"[{dataset_name}] Successfully downloaded and parsed")
            print(f"[{dataset_name}] Shape: {df.shape}, Target distribution: {df['target'].value_counts().to_dict()}")
            print(f"[{dataset_name}] Missing values: {df.isnull().sum().sum()}")
            return df
        except Exception as exc:
            print(f"[{dataset_name}] Direct download failed: {exc}")
            np.random.seed(42)
            n_samples = 1567
            n_features = 591
            X = pd.DataFrame(
                np.random.randn(n_samples, n_features),
                columns=[f"feature_{i}" for i in range(n_features)],
            )
            mask = np.random.random((n_samples, n_features)) < 0.4
            X[mask] = np.nan
            y = pd.Series(np.random.binomial(1, 0.06, n_samples), name="target")
            df = pd.concat([X, y], axis=1)
            print(f"[{dataset_name}] Using synthetic fallback data")
            return df

    def process_dataframe(self, df: pd.DataFrame, info):
        if "target" in df.columns:
            df["target"] = df["target"].astype(int)
            cols = [c for c in df.columns if c != "target"] + ["target"]
            df = df[cols]
        return df

    def get_data(self, refresh: bool = False) -> pd.DataFrame:
        info = self.get_dataset_info()
        cache_path = self._cache_path()
        bypass_env = os.environ.get("SEED_DATA_CACHE_BYPASS", "0") == "1"
        if self._cached_df is not None and not refresh and not bypass_env:
            return self._cached_df
        use_cache = cache_path.exists() and not refresh and not bypass_env
        if use_cache:
            try:
                df = pd.read_pickle(cache_path)
                if isinstance(df, pd.DataFrame) and "target" in df.columns:
                    self._cached_df = df
                    return df
            except Exception as exc:
                print(f"[{info['name']}] Failed to read cache ({exc}); re-fetching")
        df = self.download_dataset(info)
        if not isinstance(df, pd.DataFrame):
            raise TypeError("download_dataset must return a pandas DataFrame")
        df = self.process_dataframe(df, info)
        try:
            df.to_pickle(cache_path)
        except Exception as exc:
            print(f"[{info['name']}] Warning: failed to write cache ({exc})")
        self._cached_df = df
        return df

    # ---------------- Feature helpers ----------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "SECOMFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        plan = []
        plan.append({
            "name": "n_missing",
            "requires": [c for c in df.columns if c != "target"],
            "builder": lambda d: d.isna().sum(axis=1),
        })
        if "feature_59" in df.columns:
            plan.append({
                "name": "f59_sqrt",
                "requires": ["feature_59"],
                "builder": lambda d: np.sqrt(np.abs(pd.to_numeric(d["feature_59"], errors="coerce").astype(float))),
            })
        if set(["feature_59", "feature_28"]).issubset(df.columns):
            plan.append({
                "name": "feature_59_div_feature_28",
                "requires": ["feature_59", "feature_28"],
                "builder": lambda d: pd.to_numeric(d["feature_59"], errors="coerce").astype(float) /
                (pd.to_numeric(d["feature_28"], errors="coerce").astype(float) + eps),
            })
        if set(["feature_129", "feature_28"]).issubset(df.columns):
            plan.append({
                "name": "feature_129_div_feature_28",
                "requires": ["feature_129", "feature_28"],
                "builder": lambda d: pd.to_numeric(d["feature_129"], errors="coerce").astype(float) /
                (pd.to_numeric(d["feature_28"], errors="coerce").astype(float) + eps),
            })
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        added = []
        loader = SECOMDatasetLoader()
        agent = loader.get_feature_agent(provider="GPT5")
        plan = loader._propose_agent_feature_plan(df, agent)
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
        _ = self._propose_agent_feature_plan(df, agent)
        df, added = self.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df


SECOMDataset = SECOMDatasetLoader


if __name__ == "__main__":
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_auc_score
    from sklearn.impute import SimpleImputer
    from sklearn.ensemble import ExtraTreesClassifier

    ds = SECOMDatasetLoader()
    df = ds.get_data()
    X_base = df.drop(columns=["target"]) if "target" in df.columns else df
    y = df["target"] if "target" in df.columns else None

    df_exp = df.copy(deep=True)
    df_exp, added_names = SECOMDatasetLoader.expand_features_on_dataframe(df_exp)
    X_exp = df_exp.drop(columns=["target"]) if "target" in df_exp.columns else df_exp

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    aucs_base = []
    aucs_exp = []

    print("\nBaseline (no expander) 5-fold AUCs:")
    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X_base, y), 1):
        Xtr = X_base.iloc[train_idx]
        Xte = X_base.iloc[test_idx]
        ytr = y.iloc[train_idx]
        yte = y.iloc[test_idx]
        imp = SimpleImputer(strategy='median')
        imp.fit(Xtr)
        Xtr_imp = pd.DataFrame(imp.transform(Xtr), columns=Xtr.columns, index=Xtr.index)
        Xte_imp = pd.DataFrame(imp.transform(Xte), columns=Xte.columns, index=Xte.index)
        model = ExtraTreesClassifier(n_estimators=1500, max_depth=10, min_samples_leaf=3, max_features='sqrt', class_weight='balanced', random_state=42, n_jobs=-1)
        model.fit(Xtr_imp, ytr)
        p = model.predict_proba(Xte_imp)[:, 1]
        auc = roc_auc_score(yte, p)
        aucs_base.append(auc)
        print(f"Fold {fold_idx}: AUC={auc:.6f}")

    print("\nAgent-expanded 5-fold AUCs:")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X_exp, y), 1):
        Xtr2 = X_exp.iloc[train_idx].copy()
        Xte2 = X_exp.iloc[test_idx].copy()
        ytr2 = y.iloc[train_idx]
        yte2 = y.iloc[test_idx]
        imp2 = SimpleImputer(strategy='median')
        imp2.fit(Xtr2)
        Xtr2_imp = pd.DataFrame(imp2.transform(Xtr2), columns=Xtr2.columns, index=Xtr2.index)
        Xte2_imp = pd.DataFrame(imp2.transform(Xte2), columns=Xte2.columns, index=Xte2.index)
        model2 = ExtraTreesClassifier(n_estimators=1500, max_depth=10, min_samples_leaf=3, max_features='sqrt', class_weight='balanced', random_state=42, n_jobs=-1)
        model2.fit(Xtr2_imp, ytr2)
        p2 = model2.predict_proba(Xte2_imp)[:, 1]
        auc2 = roc_auc_score(yte2, p2)
        aucs_exp.append(auc2)
        print(f"Fold {fold_idx}: AUC={auc2:.6f}")

