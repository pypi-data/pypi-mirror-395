import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class LoanDefaultPredictionDataset(BaseDatasetLoader):
    """
    Loan Default Prediction Dataset (binary classification)
    Source: Kaggle - Lending Club Loan Data
    Target: loan_status (0=paid, 1=default)
    
    This dataset contains loan application data and borrower information
    for predicting loan defaults.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'LoanDefaultPredictionDataset',
            'source_id': 'kaggle:loan-default-prediction',
            'category': 'binary_classification',
            'description': 'Loan default prediction from borrower and loan characteristics.',
            'source_url': 'https://www.kaggle.com/datasets/wordsforthewise/lending-club',
        }
    
    def download_dataset(self, info):
        """Download the loan default dataset from Kaggle"""
        print(f"[LoanDefaultPredictionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[LoanDefaultPredictionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'wordsforthewise/lending-club',
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
                    # Use accepted loans file
                    data_file = None
                    for f in csv_files:
                        if 'accepted' in f.lower():
                            data_file = f
                            break
                    if not data_file:
                        data_file = csv_files[0]
                    
                    print(f"[LoanDefaultPredictionDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=10000)
                    print(f"[LoanDefaultPredictionDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[LoanDefaultPredictionDataset] Download failed: {e}")
            print("[LoanDefaultPredictionDataset] Using sample loan data...")
            
            # Create realistic loan default data
            np.random.seed(42)
            n_samples = 8000
            
            # Borrower characteristics
            data = {}
            data['annual_income'] = np.random.lognormal(11, 0.5, n_samples)
            data['employment_length'] = np.random.gamma(2, 2, n_samples)
            data['home_ownership'] = np.random.choice([1, 2, 3, 4], n_samples, p=[0.1, 0.4, 0.4, 0.1])  # RENT, MORTGAGE, OWN, OTHER
            data['verification_status'] = np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.4, 0.3])  # Not, Source, Verified
            
            # Credit history
            data['fico_score'] = np.random.normal(700, 50, n_samples)
            data['credit_history_length'] = np.random.gamma(3, 3, n_samples)
            data['delinquencies_last_2yrs'] = np.random.poisson(0.5, n_samples)
            data['inquiries_last_6mths'] = np.random.poisson(1, n_samples)
            data['open_accounts'] = np.random.poisson(10, n_samples)
            data['public_records'] = np.random.poisson(0.1, n_samples)
            data['revolving_balance'] = np.random.lognormal(9, 1, n_samples)
            data['revolving_utilization'] = np.random.beta(2, 3, n_samples)
            data['total_accounts'] = data['open_accounts'] + np.random.poisson(5, n_samples)
            
            # Loan characteristics
            data['loan_amount'] = np.random.lognormal(9.5, 0.7, n_samples)
            data['interest_rate'] = 5 + 20 * (1 - (data['fico_score'] - 600) / 200) + np.random.normal(0, 2, n_samples)
            data['term_months'] = np.random.choice([36, 60], n_samples, p=[0.7, 0.3])
            data['installment'] = data['loan_amount'] * (data['interest_rate'] / 100 / 12) / (1 - (1 + data['interest_rate'] / 100 / 12) ** (-data['term_months']))
            data['purpose'] = np.random.choice([1, 2, 3, 4, 5, 6], n_samples, p=[0.2, 0.3, 0.2, 0.1, 0.1, 0.1])  # credit_card, debt_consolidation, home_improvement, etc.
            
            # Debt-to-income ratio
            data['dti'] = (data['installment'] * 12 + data['revolving_balance'] * 0.03 * 12) / data['annual_income'] * 100
            
            # Calculate default probability
            default_prob = np.zeros(n_samples)
            
            # Credit score impact
            default_prob += np.where(data['fico_score'] < 650, 0.3, 
                           np.where(data['fico_score'] < 700, 0.15, 0.05))
            
            # DTI impact
            default_prob += np.where(data['dti'] > 40, 0.2,
                           np.where(data['dti'] > 30, 0.1, 0.02))
            
            # Delinquency history
            default_prob += data['delinquencies_last_2yrs'] * 0.1
            default_prob += data['public_records'] * 0.2
            
            # Income vs loan amount
            default_prob += np.where(data['loan_amount'] > data['annual_income'] * 0.5, 0.15, 0)
            
            # Interest rate (high risk borrowers)
            default_prob += np.where(data['interest_rate'] > 15, 0.1, 0)
            
            # Add randomness
            default_prob += np.random.normal(0, 0.05, n_samples)
            
            # Convert to binary
            data['target'] = (default_prob > 0.3).astype(int)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the loan default dataset"""
        print(f"[LoanDefaultPredictionDataset] Raw shape: {df.shape}")
        print(f"[LoanDefaultPredictionDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find loan status column
        target_col = None
        for col in ['loan_status', 'default', 'status', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            # Map loan status to binary
            if df[target_col].dtype == 'object':
                default_values = ['default', 'charged off', 'late', 'in grace period']
                df['target'] = df[target_col].str.lower().apply(
                    lambda x: 1 if any(val in str(x) for val in default_values) else 0
                )
            else:
                df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Generate based on available features
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Use high-risk indicators
                risk_score = 0
                if 'int_rate' in df.columns:
                    risk_score += (df['int_rate'] > 15).astype(int)
                if 'dti' in df.columns:
                    risk_score += (df['dti'] > 30).astype(int)
                if 'annual_inc' in df.columns and 'loan_amnt' in df.columns:
                    risk_score += (df['loan_amnt'] > df['annual_inc'] * 0.5).astype(int)
                
                df['target'] = (risk_score >= 2).astype(int)
            else:
                df['target'] = np.random.choice([0, 1], len(df), p=[0.85, 0.15])
        
        # Remove non-numeric columns
        text_cols = ['id', 'member_id', 'emp_title', 'issue_d', 'url', 'desc', 'title', 'zip_code', 'addr_state']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Convert categorical columns
        cat_cols = ['term', 'grade', 'sub_grade', 'home_ownership', 'verification_status', 'purpose', 'initial_list_status']
        for col in cat_cols:
            if col in df.columns:
                if df[col].dtype == 'object':
                    # Create dummy variables
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
        
        # Limit features
        if len(feature_cols) > 50:
            # Prioritize important features
            priority_features = ['loan_amnt', 'int_rate', 'installment', 'annual_inc', 'dti',
                               'fico', 'delinq', 'inq', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util']
            
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
            if target_counts[minority] < target_counts[majority] * 0.1:
                n_minority = target_counts[minority]
                n_majority = min(n_minority * 5, target_counts[majority])
                df_minority = df[df['target'] == minority]
                df_majority = df[df['target'] == majority].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[LoanDefaultPredictionDataset] Final shape: {df.shape}")
        print(f"[LoanDefaultPredictionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[LoanDefaultPredictionDataset] Default rate: {(df['target'] == 1).mean():.2%}")
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Loan Default)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "LoanDefaultFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        plan = []

        # Column aliases across LC variants
        loan_amt = 'loan_amount' if 'loan_amount' in df.columns else 'loan_amnt' if 'loan_amnt' in df.columns else None
        ann_inc = 'annual_income' if 'annual_income' in df.columns else 'annual_inc' if 'annual_inc' in df.columns else None
        int_rate = 'interest_rate' if 'interest_rate' in df.columns else 'int_rate' if 'int_rate' in df.columns else None
        installment = 'installment' if 'installment' in df.columns else None
        dti = 'dti' if 'dti' in df.columns else None
        revol_bal = 'revolving_balance' if 'revolving_balance' in df.columns else 'revol_bal' if 'revol_bal' in df.columns else None
        revol_util = 'revolving_utilization' if 'revolving_utilization' in df.columns else 'revol_util' if 'revol_util' in df.columns else None
        open_acc = 'open_accounts' if 'open_accounts' in df.columns else 'open_acc' if 'open_acc' in df.columns else None
        total_acc = 'total_accounts' if 'total_accounts' in df.columns else 'total_acc' if 'total_acc' in df.columns else None
        inq6 = 'inquiries_last_6mths' if 'inquiries_last_6mths' in df.columns else 'inq_last_6mths' if 'inq_last_6mths' in df.columns else None
        delinq2 = 'delinquencies_last_2yrs' if 'delinquencies_last_2yrs' in df.columns else 'delinq_2yrs' if 'delinq_2yrs' in df.columns else None
        fico = 'fico_score' if 'fico_score' in df.columns else None
        fico_low = 'fico_range_low' if 'fico_range_low' in df.columns else None
        fico_high = 'fico_range_high' if 'fico_range_high' in df.columns else None

        # FICO mean from range
        if fico_low and fico_high and 'fico_mean' not in df.columns:
            plan.append({"name": "fico_mean", "requires": [fico_low, fico_high], "builder": lambda d, L=fico_low, H=fico_high: (d[L]+d[H])/2.0})

        # Core affordability and risk ratios
        if loan_amt and ann_inc:
            plan.append({"name": "loan_to_income", "requires": [loan_amt, ann_inc], "builder": lambda d, A=loan_amt, I=ann_inc: d[A]/(d[I]+eps)})
        if installment and ann_inc:
            plan.append({"name": "installment_to_income", "requires": [installment, ann_inc], "builder": lambda d, P=installment, I=ann_inc: (12.0*d[P])/(d[I]+eps)})
        if revol_bal and ann_inc:
            plan.append({"name": "revol_bal_to_income", "requires": [revol_bal, ann_inc], "builder": lambda d, R=revol_bal, I=ann_inc: d[R]/(d[I]+eps)})
        if revol_util:
            plan.append({"name": "revol_util_log1p", "requires": [revol_util], "builder": lambda d, U=revol_util: np.log1p(d[U].clip(lower=0))})

        # Composition and history
        if open_acc and total_acc:
            plan.append({"name": "open_to_total_acc", "requires": [open_acc, total_acc], "builder": lambda d, O=open_acc, T=total_acc: d[O]/(d[T]+eps)})

        # Risk stacking interactions
        if dti and int_rate:
            plan.append({"name": "dti_x_int_rate", "requires": [dti, int_rate], "builder": lambda d, D=dti, R=int_rate: d[D]*d[R]})
        if inq6 and revol_util:
            plan.append({"name": "inq_x_revol_util", "requires": [inq6, revol_util], "builder": lambda d, Q=inq6, U=revol_util: d[Q]*d[U]})
        if delinq2 and revol_bal:
            plan.append({"name": "delinq_x_revol_bal", "requires": [delinq2, revol_bal], "builder": lambda d, DL=delinq2, RB=revol_bal: d[DL]*np.log1p(d[RB].clip(lower=0))})

        # DTI bins
        if dti:
            plan.append({"name": "dti_bin", "requires": [dti], "builder": lambda d, D=dti: pd.qcut(d[D], q=10, duplicates='drop').cat.codes})

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = LoanDefaultPredictionDataset()
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
        df, added = LoanDefaultPredictionDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

if __name__ == "__main__":
    dataset = LoanDefaultPredictionDataset()
    df = dataset.get_data()
    print(f"Loaded LoanDefaultPredictionDataset: {df.shape}")
    print(df.head())

    # Expanded view without re-download
    df_exp = df.copy(deep=True)
    df_exp, added = LoanDefaultPredictionDataset.expand_features_on_dataframe(df_exp)
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

            Xtr2, Xte2 = X_exp.iloc[tr].copy()
            expander = AgentFeatureExpander(prefer_dataset="LoanDefaultPredictionDataset")
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
        print(f"[LoanDefaultPredictionDataset] CV run skipped due to: {e}")