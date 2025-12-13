import os
import pandas as pd
import numpy as np
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CreditCardDefaultDataset(BaseDatasetLoader):
    """UCI Credit Card Default dataset (binary classification).

    This dataset contains information on default payments from credit card 
    clients in Taiwan. The goal is to predict whether a client will default 
    on their credit card payment next month based on their payment history, 
    demographic factors, and other features.

    30,000 instances with 23 features + binary target.
    
    Real-world banking/finance industry dataset for default prediction.
    
    Source: UCI Default of Credit Card Clients dataset
    Link: https://raw.githubusercontent.com/thomasXwang/UCI-Credit-card-defaults/master/UCI_Credit_Card.csv
    """

    def get_dataset_info(self):
        return {
            "name": "CreditCardDefaultDataset",
            "source_id": "uci:credit_card_default_taiwan",
            "source_url": "https://raw.githubusercontent.com/thomasXwang/UCI-Credit-card-defaults/master/UCI_Credit_Card.csv",
            "category": "binary_classification",
            "description": "UCI Credit Card Default dataset - predict default payment for Taiwan credit card clients.",
            "target_column": "default.payment.next.month",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = info["source_url"]
        print(f"[{dataset_name}] Downloading from {url}")
        try:
            r = requests.get(url, timeout=60)
            print(f"[{dataset_name}] HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            # Expect ~2.8MB for this dataset
            if len(r.content) < 100000:
                preview = r.content[:500].decode("utf-8", errors="replace")
                print(f"[{dataset_name}] Warning: file might be small. Preview:\n{preview}")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The target column might be named differently
        target_candidates = ["default.payment.next.month", "default payment next month", "Y", "target"]
        target_col = None
        
        for candidate in target_candidates:
            if candidate in df.columns:
                target_col = candidate
                break
                
        if target_col is None:
            # If no standard name found, assume last column is target
            target_col = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {target_col}")

        # Map target column to binary target: 0=no default, 1=default
        df["target"] = pd.to_numeric(df[target_col], errors="coerce").fillna(0).astype(int)
        df.drop(columns=[target_col], inplace=True)

        # Drop ID column if exists
        if "ID" in df.columns:
            df.drop(columns=["ID"], inplace=True)

        # Convert all remaining columns to numeric where possible
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows with any NA values
        before = len(df)
        df.dropna(inplace=True)
        dropped = before - len(df)
        print(f"[{dataset_name}] Dropped {dropped} rows with NA values")

        # Deduplicate
        before = len(df)
        df.drop_duplicates(inplace=True)
        dups = before - len(df)
        if dups:
            print(f"[{dataset_name}] Removed {dups} duplicate rows")

        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Credit Default)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "CreditDefaultFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        plan = []
        
        def has_all(cols):
            return all(c in df.columns for c in cols)

        # Common column sets in credit default dataset
        limit_col = 'LIMIT_BAL' if 'LIMIT_BAL' in df.columns else 'limit_bal' if 'limit_bal' in df.columns else None
        bill_cols = [c for c in df.columns if c.lower().startswith('bill_amt')]
        pay_amt_cols = [c for c in df.columns if c.lower().startswith('pay_amt')]
        pay_stat_cols = [c for c in df.columns if c.lower().startswith('pay_') and not c.lower().startswith('pay_amt')]

        # Per-month ratios and utilization
        for c in bill_cols:
            if limit_col:
                plan.append({"name": f"{c}_util", "requires": [c, limit_col], "builder": lambda d, col=c: (d[col].clip(lower=0) / (d[limit_col] + eps))})
        for c in pay_amt_cols:
            month_suffix = ''.join(filter(str.isdigit, c))
            bill_match = next((b for b in bill_cols if b.endswith(month_suffix)), None)
            if bill_match:
                plan.append({"name": f"pay_ratio_{month_suffix}", "requires": [c, bill_match], "builder": lambda d, a=c, b=bill_match: (d[a].clip(lower=0) / (d[b].abs() + eps))})

        # Aggregates across months
        if bill_cols:
            plan.append({"name": "bill_amt_mean", "requires": bill_cols, "builder": lambda d: d[bill_cols].mean(axis=1)})
            plan.append({"name": "bill_amt_std", "requires": bill_cols, "builder": lambda d: d[bill_cols].std(axis=1)})
            plan.append({"name": "bill_amt_sum", "requires": bill_cols, "builder": lambda d: d[bill_cols].sum(axis=1)})
            plan.append({"name": "bill_amt_min", "requires": bill_cols, "builder": lambda d: d[bill_cols].min(axis=1)})
            plan.append({"name": "bill_amt_max", "requires": bill_cols, "builder": lambda d: d[bill_cols].max(axis=1)})
            
        if pay_amt_cols:
            plan.append({"name": "pay_amt_mean", "requires": pay_amt_cols, "builder": lambda d: d[pay_amt_cols].mean(axis=1)})
            plan.append({"name": "pay_amt_std", "requires": pay_amt_cols, "builder": lambda d: d[pay_amt_cols].std(axis=1)})
            plan.append({"name": "pay_amt_sum", "requires": pay_amt_cols, "builder": lambda d: d[pay_amt_cols].sum(axis=1)})
            plan.append({"name": "pay_amt_min", "requires": pay_amt_cols, "builder": lambda d: d[pay_amt_cols].min(axis=1)})
            plan.append({"name": "pay_amt_max", "requires": pay_amt_cols, "builder": lambda d: d[pay_amt_cols].max(axis=1)})

        # Delinquency indicators (status > 0 means delay months)
        if pay_stat_cols:
            plan.append({"name": "num_delinquent", "requires": pay_stat_cols, "builder": lambda d: (d[pay_stat_cols] > 0).sum(axis=1)})
            plan.append({"name": "max_delinquency", "requires": pay_stat_cols, "builder": lambda d: d[pay_stat_cols].max(axis=1)})
            plan.append({"name": "sum_delinquency", "requires": pay_stat_cols, "builder": lambda d: d[pay_stat_cols].clip(lower=0).sum(axis=1)})
            plan.append({"name": "avg_delinquency", "requires": pay_stat_cols, "builder": lambda d: d[pay_stat_cols].clip(lower=0).mean(axis=1)})
            
            # Recency-weighted delinquency (recent months matter more)
            def rw_delinquency(d):
                weights = [0.35, 0.25, 0.2, 0.1, 0.07, 0.03]
                result = 0
                for i, col in enumerate(pay_stat_cols[:6]):
                    if col in d.columns and i < len(weights):
                        result += d[col].clip(lower=0) * weights[i]
                return result
            plan.append({"name": "rw_delinquency", "requires": pay_stat_cols[:6], "builder": rw_delinquency})
            
            # consecutive delinq streak approximation
            def delinq_streak(d):
                arr = (d[pay_stat_cols].values > 0).astype(int)
                # count longest run of 1s row-wise
                streaks = []
                for row in arr:
                    best = cur = 0
                    for v in row:
                        if v:
                            cur += 1; best = max(best, cur)
                        else:
                            cur = 0
                    streaks.append(best)
                return pd.Series(streaks, index=d.index)
            plan.append({"name": "delinq_longest_streak", "requires": pay_stat_cols, "builder": delinq_streak})

        # Age features
        if 'AGE' in df.columns or 'age' in df.columns:
            age_c = 'AGE' if 'AGE' in df.columns else 'age'
            plan.append({"name": "age_bin", "requires": [age_c], "builder": lambda d, a=age_c: pd.qcut(d[a], q=10, duplicates='drop').cat.codes})
            plan.append({"name": "age_squared", "requires": [age_c], "builder": lambda d, a=age_c: d[a] ** 2})
            plan.append({"name": "log_age", "requires": [age_c], "builder": lambda d, a=age_c: np.log1p(d[a])})
            plan.append({"name": "age_young", "requires": [age_c], "builder": lambda d, a=age_c: (d[a] < 30).astype(int)})
            plan.append({"name": "age_senior", "requires": [age_c], "builder": lambda d, a=age_c: (d[a] >= 60).astype(int)})

        # Payment behavior patterns
        if has_all(["bill_amt_sum", "pay_amt_sum"]):
            plan.append({
                "name": "payment_gap",
                "requires": ["bill_amt_sum", "pay_amt_sum"],
                "builder": lambda d: (d["bill_amt_sum"] - d["pay_amt_sum"]) / (d["bill_amt_sum"].abs() + eps)
            })
            plan.append({
                "name": "payment_coverage",
                "requires": ["pay_amt_sum", "bill_amt_sum"],
                "builder": lambda d: d["pay_amt_sum"] / (d["bill_amt_sum"].abs() + eps)
            })
            
        # Utilization patterns
        if limit_col and has_all(["bill_amt_mean"]):
            plan.append({
                "name": "avg_utilization",
                "requires": ["bill_amt_mean", limit_col],
                "builder": lambda d: d["bill_amt_mean"] / (d[limit_col] + eps)
            })
            plan.append({
                "name": "avg_util_squared",
                "requires": ["bill_amt_mean", limit_col],
                "builder": lambda d: (d["bill_amt_mean"] / (d[limit_col] + eps)) ** 2
            })
            
        if limit_col and has_all(["bill_amt_max"]):
            plan.append({
                "name": "max_utilization",
                "requires": ["bill_amt_max", limit_col],
                "builder": lambda d: d["bill_amt_max"] / (d[limit_col] + eps)
            })
            
        # Risk scores based on delinquency patterns
        if has_all(["num_delinquent", "max_delinquency"]):
            plan.append({
                "name": "delinq_intensity",
                "requires": ["num_delinquent", "max_delinquency"],
                "builder": lambda d: d["num_delinquent"] * d["max_delinquency"]
            })
            plan.append({
                "name": "delinq_severity",
                "requires": ["num_delinquent", "max_delinquency"],
                "builder": lambda d: (d["num_delinquent"] * 0.3 + d["max_delinquency"] * 0.7)
            })
            
        # Advanced risk indicators
        if has_all(["rw_delinquency", "avg_utilization"]):
            plan.append({
                "name": "risk_score_v1",
                "requires": ["rw_delinquency", "avg_utilization"],
                "builder": lambda d: d["rw_delinquency"] * d["avg_utilization"]
            })
            
        if has_all(["delinq_intensity", "payment_gap"]):
            plan.append({
                "name": "risk_score_v2",
                "requires": ["delinq_intensity", "payment_gap"],
                "builder": lambda d: d["delinq_intensity"] * (1 + d["payment_gap"].clip(lower=0))
            })
            
        # Age interaction features
        if has_all(["age_bin", "rw_delinquency"]):
            plan.append({
                "name": "age_x_delinq",
                "requires": ["age_bin", "rw_delinquency"],
                "builder": lambda d: d["age_bin"] * d["rw_delinquency"]
            })
            
        if has_all(["age_young", "avg_utilization"]):
            plan.append({
                "name": "young_high_util",
                "requires": ["age_young", "avg_utilization"],
                "builder": lambda d: d["age_young"] * d["avg_utilization"]
            })
            
        # Education features if available
        if 'EDUCATION' in df.columns or 'education' in df.columns:
            edu_c = 'EDUCATION' if 'EDUCATION' in df.columns else 'education'
            plan.append({"name": "edu_high", "requires": [edu_c], "builder": lambda d, e=edu_c: (d[e] >= 3).astype(int)})
            plan.append({"name": "edu_low", "requires": [edu_c], "builder": lambda d, e=edu_c: (d[e] <= 2).astype(int)})
            
            if has_all(["edu_high", "rw_delinquency"]):
                plan.append({
                    "name": "edu_x_delinq",
                    "requires": ["edu_high", "rw_delinquency"],
                    "builder": lambda d: d["edu_high"] * d["rw_delinquency"]
                })
                
        # Marriage features if available
        if 'MARRIAGE' in df.columns or 'marriage' in df.columns:
            mar_c = 'MARRIAGE' if 'MARRIAGE' in df.columns else 'marriage'
            plan.append({"name": "married", "requires": [mar_c], "builder": lambda d, m=mar_c: (d[m] == 1).astype(int)})
            plan.append({"name": "single", "requires": [mar_c], "builder": lambda d, m=mar_c: (d[m] == 2).astype(int)})
            
        # Sex features if available
        if 'SEX' in df.columns or 'sex' in df.columns:
            sex_c = 'SEX' if 'SEX' in df.columns else 'sex'
            plan.append({"name": "is_male", "requires": [sex_c], "builder": lambda d, s=sex_c: (d[s] == 1).astype(int)})
            plan.append({"name": "is_female", "requires": [sex_c], "builder": lambda d, s=sex_c: (d[s] == 2).astype(int)})
            
        # Polynomial and nonlinear features
        if has_all(["rw_delinquency"]):
            plan.append({
                "name": "rw_delinq_squared",
                "requires": ["rw_delinquency"],
                "builder": lambda d: d["rw_delinquency"] ** 2
            })
            plan.append({
                "name": "rw_delinq_sqrt",
                "requires": ["rw_delinquency"],
                "builder": lambda d: np.sqrt(d["rw_delinquency"].clip(lower=0))
            })
            plan.append({
                "name": "log1p_rw_delinq",
                "requires": ["rw_delinquency"],
                "builder": lambda d: np.log1p(d["rw_delinquency"].clip(lower=0))
            })
            
        if has_all(["avg_utilization"]):
            plan.append({
                "name": "util_cubed",
                "requires": ["avg_utilization"],
                "builder": lambda d: d["avg_utilization"] ** 3
            })
            plan.append({
                "name": "sqrt_util",
                "requires": ["avg_utilization"],
                "builder": lambda d: np.sqrt(d["avg_utilization"].clip(lower=0))
            })
            
        # Composite risk features
        if has_all(["rw_delinq_squared", "avg_util_squared"]):
            plan.append({
                "name": "squared_risk",
                "requires": ["rw_delinq_squared", "avg_util_squared"],
                "builder": lambda d: d["rw_delinq_squared"] * d["avg_util_squared"]
            })
            
        if has_all(["log1p_rw_delinq", "sqrt_util"]):
            plan.append({
                "name": "log_sqrt_risk",
                "requires": ["log1p_rw_delinq", "sqrt_util"],
                "builder": lambda d: d["log1p_rw_delinq"] * d["sqrt_util"]
            })
            
        # Payment consistency features
        if pay_amt_cols and has_all(["pay_amt_std", "pay_amt_mean"]):
            plan.append({
                "name": "payment_cv",
                "requires": ["pay_amt_std", "pay_amt_mean"],
                "builder": lambda d: d["pay_amt_std"] / (d["pay_amt_mean"].abs() + eps)
            })
            
        # Bill volatility features
        if bill_cols and has_all(["bill_amt_std", "bill_amt_mean"]):
            plan.append({
                "name": "bill_cv",
                "requires": ["bill_amt_std", "bill_amt_mean"],
                "builder": lambda d: d["bill_amt_std"] / (d["bill_amt_mean"].abs() + eps)
            })
            
        # Master risk score combining multiple factors
        if has_all(["rw_delinquency", "avg_utilization", "payment_gap"]):
            plan.append({
                "name": "master_risk",
                "requires": ["rw_delinquency", "avg_utilization", "payment_gap"],
                "builder": lambda d: (
                    0.4 * (d["rw_delinquency"] / (d["rw_delinquency"].max() + eps)) +
                    0.3 * (d["avg_utilization"] / (d["avg_utilization"].max() + eps)) +
                    0.3 * (d["payment_gap"].clip(lower=0) / (d["payment_gap"].clip(lower=0).max() + eps))
                )
            })
            
        if has_all(["master_risk"]):
            plan.append({
                "name": "master_risk_squared",
                "requires": ["master_risk"],
                "builder": lambda d: d["master_risk"] ** 2
            })
            plan.append({
                "name": "master_risk_cubed",
                "requires": ["master_risk"],
                "builder": lambda d: d["master_risk"] ** 3
            })
            plan.append({
                "name": "sigmoid_risk",
                "requires": ["master_risk"],
                "builder": lambda d: 1.0 / (1.0 + np.exp(-5 * (d["master_risk"] - 0.5)))
            })

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = CreditCardDefaultDataset()
        agent = self_like.get_feature_agent(provider="GPT5")
        
        # Execute plan in multiple passes to handle dependencies
        added = []
        max_passes = 3  # Allow up to 3 passes for dependent features
        
        for pass_num in range(max_passes):
            plan = self_like._propose_agent_feature_plan(df, agent)
            pass_added = []
            
            for item in plan:
                name = item["name"]
                requires = item["requires"]
                builder = item["builder"]
                
                if name in df.columns:
                    continue
                    
                if all(col in df.columns for col in requires):
                    try:
                        df[name] = builder(df)
                        pass_added.append(name)
                        if name not in added:
                            added.append(name)
                    except Exception as e:
                        # Silently skip failures
                        pass
            
            # If no new features were added in this pass, stop
            if not pass_added:
                break
                
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        df = self.get_data()
        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df
        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = CreditCardDefaultDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

if __name__ == "__main__":
    ds = CreditCardDefaultDataset()
    frame = ds.get_data()
    print(frame.head())

    # Expanded
    df_exp = frame.copy(deep=True)
    df_exp, added = CreditCardDefaultDataset.expand_features_on_dataframe(df_exp)
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
            expander = AgentFeatureExpander(prefer_dataset="CreditCardDefaultDataset")
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
        print(f"[CreditCardDefaultDataset] CV run skipped due to: {e}")